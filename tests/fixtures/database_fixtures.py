import pytest

from src.infrastructure.database.init_db import init_db


@pytest.fixture
def sqlite3_database(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    return db_path
