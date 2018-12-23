import asyncio
import logging
import os
import pathlib
import shutil
import tempfile

import uvloop
from aiohttp import web
from aiohttp_swagger import setup_swagger

from svc.api import ImageApplication
from svc.api.services.base import BaseDBService
from svc.api.v1 import subapp as app_v1

logger = logging.getLogger(__file__)


def abs_path(rel_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, rel_path)


async def on_startup(app):
    await BaseDBService(app['db']).prepare()


async def on_shutdown(app):
    shutil.rmtree(app['tmp_dir'], ignore_errors=True)


async def create_app():
    """
    Initialize the application server
    """
    base_path = '/api/v1'
    # Init application
    app = ImageApplication()

    storage_path = os.path.join(os.path.dirname(__file__), 'storage')
    img_path = os.path.join(storage_path, 'img')
    thumbnail_path = os.path.join(storage_path, 'thumbnail')
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
        # create img dirs inside
        os.makedirs(img_path)
        os.makedirs(thumbnail_path)

    app['img_dir'] = img_path
    app['thumbnail_dir'] = thumbnail_path
    app['db'] = os.path.join(storage_path, 'image_db.sqlite3')
    app['tmp_dir'] = pathlib.Path(tempfile.mkdtemp())

    # include swagger file under /api/doc endpoint
    setup_swagger(
        app, swagger_url=f'{base_path}/doc', swagger_from_file=abs_path('specs/svc_img_v1.yml'))

    # Configure v1 routes
    subapp_v1 = await app_v1.init_subapp()
    app.add_subapp(base_path, subapp_v1)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    logger.info('Application started')
    return app

if __name__ == '__main__':  # pragma: no cover
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    web.run_app(app, host='127.0.0.1', port=8881)
