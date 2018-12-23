from svc.api import ImageApplication
from svc.api.v1 import handlers
from svc.api.v1.middlewares import error_handling


async def init_subapp():
    app = ImageApplication(middlewares=[error_handling])
    app.router.add_route('POST', '/upload', handlers.upload_image)
    app.router.add_route('GET', '/download/{image_id}', handlers.download_image)
    return app
