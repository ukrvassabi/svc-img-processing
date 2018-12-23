try:
    import ujson as json
except ImportError:  # pragma: no cover
    import json

from aiohttp import web
from aiohttp.helpers import sentinel
from aiohttp.web_response import Response


class ImageRequest(web.Request):
    """
    Override web.Request
    """

    async def json(self, *, loads=json.loads):
        """
        Return body as json. Custom implementation for using ujson
        """
        body = await self.text()
        return loads(body)


class ImageApplication(web.Application):
    """
    Override web.Application
    """

    def _make_request(self, *args, **kwargs):
        return ImageRequest(*args, self._loop, client_max_size=self._client_max_size)


def json_response(
        data=sentinel, *, text=None, body=None, status=200, reason=None, headers=None,
        content_type='application/json', dumps=json.dumps):
    if data is not sentinel:
        if text or body:
            raise ValueError('only one of data, text, or body should be specified')
        else:
            text = dumps(data)
    return Response(
        text=text, body=body, status=status, reason=reason, headers=headers,
        content_type=content_type)
