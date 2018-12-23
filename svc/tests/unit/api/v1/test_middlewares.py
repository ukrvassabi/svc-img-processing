from aiohttp import web
from marshmallow import ValidationError

from svc.api import json_response
from svc.api.v1.middlewares import error_handling


async def handler(request):
    return web.Response(body=b'OK')


async def test_error_handling_middleware(aiohttp_client):
    app = web.Application()
    app.middlewares.append(error_handling)
    app.router.add_route('GET', '/', handler)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert txt == 'OK'


async def test_error_handling_middleware_validation_error(aiohttp_client):
    async def handler(request):
        raise ValidationError('Incorrect value.')

    app = web.Application()
    app.middlewares.append(error_handling)
    app.router.add_route('GET', '/', handler)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert 400 == resp.status
    msg = await resp.json()
    assert msg == {'error_msg': ['Incorrect value.']}


async def test_error_handling_middleware_http_error(aiohttp_client):
    async def handler(request):
        raise web.HTTPNotFound(reason='Item not found.')

    app = web.Application()
    app.middlewares.append(error_handling)
    app.router.add_route('GET', '/', handler)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert 404 == resp.status
    msg = await resp.json()
    assert msg == {'error_msg': 'Item not found.'}


async def test_error_handling_middleware_json_response_error(aiohttp_client):
    async def handler(request):
        return json_response({'test': 'test'}, body=b'OK', text='OK')

    app = web.Application()
    app.middlewares.append(error_handling)
    app.router.add_route('GET', '/', handler)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert 500 == resp.status
    msg = await resp.json()
    assert msg == {'error_msg': 'Unexpected error.'}
