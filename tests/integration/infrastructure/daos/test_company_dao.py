import sqlite3

from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.company_dao import SQLiteCompanyDAO


def insert_company(
    sqlite3_database: str,
    company_id: str,
    company_name: str,
    company_email: str = "test@company.com",
    company_phone: str = "123456789",
    is_active: bool = True,
    attendant_sees_all_conversations: bool = True,
    whatsapp_api_key: str | None = None,
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO companies (
                id, name, email, phone, is_active,
                attendant_sees_all_conversations, whatsapp_api_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_id,
                company_name,
                company_email,
                company_phone,
                1 if is_active else 0,
                1 if attendant_sees_all_conversations else 0,
                whatsapp_api_key,
            ),
        )
        conn.commit()


def test_company_dao_insert(sqlite3_database):
    # Arrange
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)
    company_id = generate_uuid4()
    company_name = "Company Name"
    company_data = {
        "id": company_id,
        "name": company_name,
        "email": "test@company.com",
        "phone": "123456789",
        "is_active": True,
        "attendant_sees_all_conversations": True,
        "whatsapp_api_key": "some-key",
        "updated_at": None,
    }

    # Act
    company_dao.insert(company_data=company_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT id, name, email, phone FROM companies WHERE id = ?",
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == company_id
        assert data[1] == company_name
        assert data[2] == company_data["email"]
        assert data[3] == company_data["phone"]


def test_company_dao_update(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Name",
        company_email="old@email.com",
        company_phone="000000000",
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)
    new_company_name = "New Company Name"
    new_company_email = "new@email.com"
    new_company_phone = "123456789"

    company_data = {
        "id": company_id,
        "name": new_company_name,
        "email": new_company_email,
        "phone": new_company_phone,
        "is_active": False,
        "attendant_sees_all_conversations": False,
        "whatsapp_api_key": "new-api-key",
        "updated_at": get_now(),
    }

    # Act
    company_dao.update(company_data=company_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            """
            SELECT name, email, phone, is_active, attendant_sees_all_conversations, whatsapp_api_key
            FROM companies
            WHERE id = ?
            """,
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == new_company_name
        assert data[1] == new_company_email
        assert data[2] == new_company_phone
        assert bool(data[3]) is False
        assert bool(data[4]) is False
        assert data[5] == "new-api-key"


def test_company_dao_get_by_id(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    company_name = "Get By Id Test"
    company_email = "get@email.com"
    company_phone = "987654321"
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name=company_name,
        company_email=company_email,
        company_phone=company_phone,
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)

    # Act
    row = company_dao.get_by_id(company_id=company_id)

    # Assert
    assert row is not None
    assert row[0] == company_id
    assert row[1] == company_name
    assert row[4] == company_email
    assert row[5] == company_phone


def test_company_dao_get_all(sqlite3_database):
    # Arrange
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)
    company_id_1 = generate_uuid4()
    company_id_2 = generate_uuid4()

    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id_1,
        company_name="C1",
        company_email="c1@e.com",
        company_phone="1",
    )
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id_2,
        company_name="C2",
        company_email="c2@e.com",
        company_phone="2",
    )

    # Act
    companies = company_dao.get_all()

    # Assert
    assert len(companies) >= 2
    ids = [c[0] for c in companies]
    assert company_id_1 in ids
    assert company_id_2 in ids


def test_company_dao_delete(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Name",
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)

    # Act
    company_dao.delete(company_id=company_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT COUNT(name) FROM companies WHERE id = ?",
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == 0
