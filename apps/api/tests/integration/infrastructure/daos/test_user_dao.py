import sqlite3

from src.domain.enums import UserTypes
from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.user_dao import SQLiteUserDAO

DEFAULT_EMAIL = "email@test.com"


def insert_user(
    sqlite3_database: str,
    user_id: str,
    user_name: str,
    email: str = DEFAULT_EMAIL,
    is_active: bool = True,
    password_hash: str = "test_hash",
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                user_name,
                email,
                UserTypes.STAFF.value,
                password_hash,
                is_active,
            ),
        )
        conn.commit()


def test_user_dao_insert(sqlite3_database):
    # Arrange
    user_id = generate_uuid4()
    user_name = "Contact Name"
    user_data = {
        "id": user_id,
        "name": user_name,
        "email": DEFAULT_EMAIL,
        "type": UserTypes.STAFF.value,
        "password_hash": "test_hash",
        "company_id": None,
        "is_active": True,
    }
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    user_dao.insert(user_data=user_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT id, name FROM users WHERE id = ?",
            (user_id,),
        )
        data = cursor.fetchone()
        assert data[0] == user_id
        assert data[1] == user_name


def test_user_dao_update(sqlite3_database):
    # Arrange
    user_id = generate_uuid4()
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=user_id,
        user_name="User Name",
    )
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    new_user_name = "New User Name"
    user_data = {
        "id": user_id,
        "name": new_user_name,
        "email": DEFAULT_EMAIL,
        "type": UserTypes.STAFF.value,
        "password_hash": "test_hash",
        "company_id": None,
        "is_active": True,
        "updated_at": get_now(),
    }
    user_dao.update(user_data=user_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        data = cursor.fetchone()
        assert data[0] == new_user_name
        assert data[1] is not None


def test_user_dao_get_by_id(sqlite3_database):
    # Arrange
    user_id = generate_uuid4()
    user_name = "User Name"
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=user_id,
        user_name=user_name,
    )
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    user_dao.get_by_id(user_id=user_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name FROM users WHERE id = ?",
            (user_id,),
        )
        data = cursor.fetchone()
        assert data[0] == user_name


def test_user_dao_get_all(sqlite3_database):
    # Arrange
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=generate_uuid4(),
        user_name="User Name 1",
        email=DEFAULT_EMAIL,
    )
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=generate_uuid4(),
        user_name="User Name 2",
        email=DEFAULT_EMAIL + ".br",
    )
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    users = user_dao.get_all()

    # Assert
    assert len(users) == 2


def test_user_dao_delete(sqlite3_database):
    # Arrange
    user_id = generate_uuid4()
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=user_id,
        user_name="User Name 1",
    )
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    user_dao.delete(user_id=user_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT COUNT(name) FROM users WHERE id = ?",
            (user_id,),
        )
        data = cursor.fetchone()
        assert data[0] == 0


def test_user_dao_update_is_active(sqlite3_database):
    # Arrange
    user_id = generate_uuid4()
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=user_id,
        user_name="User Name",
        is_active=True,
    )
    user_dao = SQLiteUserDAO(db_path=sqlite3_database)

    # Act
    user_data = {
        "id": user_id,
        "name": "User Name",
        "email": DEFAULT_EMAIL,
        "type": UserTypes.STAFF.value,
        "password_hash": "test_hash",
        "company_id": None,
        "is_active": False,
        "updated_at": get_now(),
    }
    user_dao.update(user_data=user_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT is_active FROM users WHERE id = ?",
            (user_id,),
        )
        data = cursor.fetchone()
        assert data[0] == 0
