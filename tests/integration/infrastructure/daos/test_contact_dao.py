import sqlite3
from datetime import datetime

from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.contact_dao import SQLiteContactDAO
from tests.integration.infrastructure.daos.test_company_dao import insert_company

DEFAULT_NUMBER = "5588123456789"


def insert_contact(
    sqlite3_database: str,
    contact_id: str,
    contact_name: str,
    contact_email: str = "test@contact.com",
    phone_number: str = DEFAULT_NUMBER,
    company_id: str | None = None,
    is_blocked: bool = False,
    last_contact_at: datetime | None = None,
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO contacts (
                id, name, phone_number, email, company_id,
                is_blocked, last_contact_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                contact_id,
                contact_name,
                phone_number,
                contact_email,
                company_id,
                1 if is_blocked else 0,
                last_contact_at,
            ),
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
        "phone_number": "5588123456789",
        "email": "test@contact.com",
        "company_id": None,
        "is_blocked": False,
        "last_contact_at": None,
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
        contact_email="test@contact.com",
        company_id="contact@test.com",
        phone_number="5511999999999",
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)
    new_contact_name = "New Contact Name"
    new_contact_email = "newcontact@test.com"
    contact_data = {
        "id": contact_id,
        "name": new_contact_name,
        "phone_number": DEFAULT_NUMBER,
        "email": new_contact_email,
        "company_id": None,
        "is_blocked": False,
        "last_contact_at": get_now(),
        "updated_at": get_now(),
    }

    # Act
    contact_dao.update(contact_data=contact_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name, email, updated_at FROM contacts WHERE id = ?",
            (contact_id,),
        )
        data = cursor.fetchone()
        assert data[0] == new_contact_name
        assert data[1] == new_contact_email
        assert data[2] is not None


def test_contact_dao_get_by_id(sqlite3_database):
    # Arrange
    contact_id = generate_uuid4()
    contact_name = "Company Name"
    contact_phone = "5588123456789"
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name=contact_name,
        phone_number=contact_phone,
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    row = contact_dao.get_by_id(contact_id=contact_id)

    # Assert
    assert row is not None
    assert row[0] == contact_id
    assert row[1] == contact_name
    assert row[2] == contact_phone


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
    rows = contact_dao.get_all()

    # Assert
    assert len(rows) == 2


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


def test_contact_dao_get_by_phone_number(sqlite3_database):
    # Arrange
    contact_id = generate_uuid4()
    contact_name = "Phone Search Test"
    phone_number = "5511911112222"
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name=contact_name,
        phone_number=phone_number,
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    row = contact_dao.get_by_phone_number(phone_number=phone_number)

    # Assert
    assert row is not None
    assert row[0] == contact_id
    assert row[2] == phone_number


def test_contact_dao_get_company_contact_by_phone_number(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Search Test",
    )

    contact_id = generate_uuid4()
    contact_name = "Company Contact"
    phone_number = "5511933334444"

    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name=contact_name,
        phone_number=phone_number,
        company_id=company_id,
    )
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)

    # Act
    row = contact_dao.get_company_contact_by_phone_number(
        company_id=company_id,
        phone_number=phone_number,
    )

    # Assert
    assert row is not None
    assert row[0] == contact_id
    assert row[4] == company_id
    assert row[2] == phone_number


def test_contact_dao_get_company_contact_by_phone_number_not_found(sqlite3_database):
    # Arrange
    contact_dao = SQLiteContactDAO(db_path=sqlite3_database)
    company_id = generate_uuid4()
    phone_number = "00000000000"

    # Act
    row = contact_dao.get_company_contact_by_phone_number(
        company_id=company_id,
        phone_number=phone_number,
    )

    # Assert
    assert row is None
