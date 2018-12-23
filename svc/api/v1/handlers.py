import imghdr
import logging
import os
from uuid import uuid4

from aiohttp import web

from svc.api import json_response
from svc.api.services.base import BaseDBService
from svc.api.v1.models import ImageQuery
from svc.api.v1.processors import ImageProcessor

logger = logging.getLogger(__name__)


async def upload_image(request):
    reader = await request.multipart()

    field = await reader.next()
    if not field or field.name != 'img':
        raise web.HTTPBadRequest(reason='Please provide image file.')
    file_name = field.filename
    file_name = file_name.replace(' ', '_')

    size = 0
    file_path = os.path.join(request.config_dict['img_dir'], file_name)
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    if not imghdr.what(file_path):
        raise web.HTTPBadRequest(reason='Failed to save image.')

    uid = str(uuid4())
    try:
        await BaseDBService(request.config_dict['db']).add_image(uid, file_path, file_name)
    except Exception:
        raise web.HTTPBadRequest(reason='Failed to save image.')
    logger.info('Saved image info DB, uuid: %s', uid)
    return json_response({'id': uid})


async def download_image(request):
    image_data = await BaseDBService(
        request.config_dict['db']).get_image(request.match_info['image_id'])
    if not image_data:
        raise web.HTTPNotFound(reason='There is no image with requested image ID.')
    logger.info('Found image in DB, data: %s', image_data)
    query_params = ImageQuery().load(request.query)
    logger.info('Requested query params: %s', query_params)
    file_path, file_name = image_data
    zoom_value = query_params.pop('zoom')
    zoom_image_path = os.path.join(
        request.config_dict['thumbnail_dir'], f'{zoom_value}_{file_name}')
    if os.path.exists(zoom_image_path):
        image = ImageProcessor(zoom_image_path, zoom_value, **query_params)
        logger.info('Found image in cache')
    else:
        image = ImageProcessor(file_path, zoom_value, **query_params)
        image.zoom()
        image.save(zoom_image_path)
        logger.info('Saved zoomed image in cache')
    try:
        temp_image = image.crop()
        temp_file_path = request.config_dict['tmp_dir'].joinpath(f'{uuid4().hex}_{file_name}')
        temp_image.save(temp_file_path)
        logger.info('Created zoomed and cropped temp image')
    except Exception:
        raise web.HTTPBadRequest(reason='Failed to process image.')
    return web.FileResponse(temp_file_path)
