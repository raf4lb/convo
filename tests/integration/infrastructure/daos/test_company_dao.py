import sqlite3

from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.company_dao import SQLiteCompanyDAO


def insert_company(
    sqlite3_database: str,
    company_id: str,
    company_name: str,
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO companies (id, name)
            VALUES (?, ?)
            """,
            (company_id, company_name),
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
    }

    # Act
    company_dao.insert(company_data=company_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT id, name FROM companies WHERE id = ?",
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == company_id
        assert data[1] == company_name


def test_company_dao_update(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Name",
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)
    new_company_name = " New Company Name"
    company_data = {
        "id": company_id,
        "name": new_company_name,
        "updated_at": get_now(),
    }

    # Act
    company_dao.update(company_data=company_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name FROM companies WHERE id = ?",
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == new_company_name


def test_company_dao_get_by_id(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    company_name = "Company Name"
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name=company_name,
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)

    # Act
    company_dao.get_by_id(company_id=company_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT name FROM companies WHERE id = ?",
            (company_id,),
        )
        data = cursor.fetchone()
        assert data[0] == company_name


def test_company_dao_get_all(sqlite3_database):
    # Arrange
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=generate_uuid4(),
        company_name="Company 1",
    )
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=generate_uuid4(),
        company_name="Company 2",
    )
    company_dao = SQLiteCompanyDAO(db_path=sqlite3_database)

    # Act
    companies = company_dao.get_all()

    # Assert
    assert len(companies) == 2


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
