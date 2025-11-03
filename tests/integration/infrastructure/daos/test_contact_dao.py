import sqlite3

from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.contact_dao import SQLiteContactDAO

DEFAULT_NUMBER = "5588123456789"


def insert_contact(
    sqlite3_database: str,
    contact_id: str,
    contact_name: str,
    phone_number: str = DEFAULT_NUMBER,
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO contacts (id, name, phone_number)
            VALUES (?, ?, ?)
            """,
            (contact_id, contact_name, phone_number),
        )
        conn.commit()


def test_contact_dao_insert(sqlite3_database):
    # Arrange
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)
    contact_id = generate_uuid4()
    contact_name = "Contact Name"
    contact_data = {
        "id": contact_id,
        "name": contact_name,
        "phone_number": DEFAULT_NUMBER,
        "company_id": None,
    }

    # Act
    contact_dao.insert(contact_data=contact_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT id, name FROM contacts WHERE id = ?",
            (contact_id,),
        )
        data = cursor.fetchone()
        assert data[0] == contact_id
        assert data[1] == contact_name


def test_contact_dao_update(sqlite3_database):
    # Arrange
    contact_id = generate_uuid4()
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name="Contact Name",
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)
    new_contact_name = "New Contact Name"
    contact_data = {
        "id": contact_id,
        "name": new_contact_name,
        "phone_number": DEFAULT_NUMBER,
        "company_id": None,
        "updated_at": get_now(),
    }

    # Act
    contact_dao.update(contact_data=contact_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name, updated_at FROM contacts WHERE id = ?",
            (contact_id,),
        )
        data = cursor.fetchone()
        assert data[0] == new_contact_name
        assert data[1] is not None


def test_contact_dao_get_by_id(sqlite3_database):
    # Arrange
    contact_id = generate_uuid4()
    contact_name = "Company Name"
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name=contact_name,
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    contact_dao.get_by_id(contact_id=contact_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name FROM contacts WHERE id = ?",
            (contact_id,),
        )
        data = cursor.fetchone()
        assert data[0] == contact_name


def test_contact_dao_get_all(sqlite3_database):
    # Arrange
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=generate_uuid4(),
        contact_name="Contact 1",
    )
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=generate_uuid4(),
        contact_name="Contact 2",
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    contacts = contact_dao.get_all()

    # Assert
    assert len(contacts) == 2


def test_contact_dao_delete(sqlite3_database):
    # Arrange
    contact_id = generate_uuid4()
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name="Contact Name",
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    contact_dao.delete(contact_id=contact_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT COUNT(name) FROM contacts WHERE id = ?",
            (contact_id,),
        )
        data = cursor.fetchone()
        assert data[0] == 0
