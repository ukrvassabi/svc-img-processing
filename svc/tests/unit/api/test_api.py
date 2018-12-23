import pytest
from aiohttp import web

from svc.api import json_response


def test_json_response():
    result = json_response({'test': 'test'})
    assert result.status == web.HTTPOk.status_code


def test_json_response_value_error():
    with pytest.raises(ValueError):
        json_response({'test': 'test'}, body=b'OK', text='OK')
