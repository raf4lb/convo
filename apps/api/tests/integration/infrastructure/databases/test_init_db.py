import os.path

from src.infrastructure.database.init_db import init_db


def test_init_db(tmp_path):
    db_path = tmp_path / "test.db"
    assert not os.path.isfile(db_path)
    init_db(db_path)
    assert os.path.isfile(db_path)
