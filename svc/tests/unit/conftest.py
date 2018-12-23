import pathlib
import shutil
import tempfile

import pytest


@pytest.fixture(scope='module')
def db_path():
    db_path = pathlib.Path(tempfile.mkdtemp()).joinpath('test.sqlite3')
    yield db_path
    shutil.rmtree(db_path, ignore_errors=True)
