import logging

from aiohttp import web
from marshmallow import ValidationError

from svc.api import json_response

logger = logging.getLogger(__name__)


@web.middleware
async def error_handling(request, handler):
    try:
        return await handler(request)
    except ValidationError as exc:
        logger.info(f'Validation error in handler: {exc.messages}.')
        return json_response({'error_msg': exc.messages}, status=web.HTTPBadRequest.status_code)
    except web.HTTPError as exc:
        return json_response({'error_msg': exc.reason}, status=exc.status_code)
    except Exception:
        logger.exception('Unexpected error.')
        return json_response(
            {'error_msg': 'Unexpected error.'}, status=web.HTTPInternalServerError.status_code)
