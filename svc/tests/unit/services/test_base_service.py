from svc.api.services.base import BaseDBService


class TestBaseDBService(object):

    async def test_ping(self, db_path):
        result = await BaseDBService(db_path).ping()
        assert result == [(1,)]

    async def test_prepare(self, db_path):
        result = await BaseDBService(db_path).prepare()
        assert not result
