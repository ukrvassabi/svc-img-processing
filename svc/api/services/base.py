import aiosqlite


CREATE_TABLES_SQL = '''
    CREATE TABLE IF NOT EXISTS images(
        uuid VARCHAR(255) PRIMARY KEY,
        path VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL
    )
'''
INSERT_IMAGE_SQL = '''
    INSERT INTO images(uuid, path, name) VALUES(?, ?, ?)
'''
SELECT_IMAGE_SQL = '''
    SELECT path, name from images where uuid=?
'''


class BaseDBService(object):

    def __init__(self, db_path):
        self.db = db_path

    def get_conn(self):
        return aiosqlite.connect(self.db)

    async def ping(self):
        async with self.get_conn() as conn:
            cursor = await conn.execute('SELECT 1')
            result = await cursor.fetchall()
        return result

    async def prepare(self):
        async with self.get_conn() as conn:
            await conn.execute(CREATE_TABLES_SQL)

    async def add_image(self, uuid, path, file_name):
        async with self.get_conn() as conn:
            await conn.execute(INSERT_IMAGE_SQL, (uuid, path, file_name))
            await conn.commit()

    async def get_image(self, uuid):
        async with self.get_conn() as conn:
            cursor = await conn.execute(SELECT_IMAGE_SQL, (uuid, ))
            result = await cursor.fetchone()
        return result
