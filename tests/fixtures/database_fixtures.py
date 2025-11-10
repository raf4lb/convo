import pytest

from src.infrastructure.database.init_db import init_db
from src.infrastructure.database.sqlite_setup import setup_sqlite_converters


@pytest.fixture
def sqlite3_database(tmp_path):
    db_path = tmp_path / "test.db"
    setup_sqlite_converters()
    init_db(db_path)
    return db_path
