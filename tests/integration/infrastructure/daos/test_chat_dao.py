import sqlite3

from src.domain.enums import ChatStatuses
from src.helpers.helpers import generate_uuid4, get_now
from src.infrastructure.daos.chat_dao import SQLiteChatDAO
from tests.integration.infrastructure.daos.test_company_dao import insert_company
from tests.integration.infrastructure.daos.test_contact_dao import insert_contact
from tests.integration.infrastructure.daos.test_user_dao import insert_user


def insert_chat(
    sqlite3_database: str,
    chat_id: str,
    contact_id: str,
    company_id: str,
    attached_user_id: str | None = None,
) -> None:
    with sqlite3.connect(database=sqlite3_database) as conn:
        conn.execute(
            """
            INSERT INTO chats (id, company_id, contact_id, status, attached_user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (chat_id, company_id, contact_id, "open", attached_user_id),
        )
        conn.commit()


def test_chat_dao_insert(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Name",
    )
    contact_id = generate_uuid4()
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name="Contact Name",
    )
    chat_id = generate_uuid4()
    chat_data = {
        "id": chat_id,
        "company_id": company_id,
        "contact_id": contact_id,
        "status": ChatStatuses.OPEN.value,
        "attached_user_id": None,
    }
    chat_dao = SQLiteChatDAO(db_path=sqlite3_database)

    # Act
    chat_dao.insert(chat_data=chat_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT id, contact_id FROM chats WHERE id = ?",
            (chat_id,),
        )
        data = cursor.fetchone()
        assert data[0] == chat_id
        assert data[1] == contact_id


def test_chat_dao_update(sqlite3_database):
    # Arrange
    company_id = generate_uuid4()
    insert_company(
        sqlite3_database=sqlite3_database,
        company_id=company_id,
        company_name="Company Name",
    )
    contact_id = generate_uuid4()
    insert_contact(
        sqlite3_database=sqlite3_database,
        contact_id=contact_id,
        contact_name="Contact Name",
    )
    chat_id = generate_uuid4()
    insert_chat(
        sqlite3_database=sqlite3_database,
        chat_id=chat_id,
        contact_id=contact_id,
        company_id=company_id,
    )
    attached_user_id = generate_uuid4()
    insert_user(
        sqlite3_database=sqlite3_database,
        user_id=attached_user_id,
        user_name="User name",
    )
    chat_data = {
        "id": chat_id,
        "contact_id": contact_id,
        "company_id": company_id,
        "status": ChatStatuses.OPEN.value,
        "attached_user_id": attached_user_id,
        "updated_at": get_now(),
    }
    chat_dao = SQLiteChatDAO(db_path=sqlite3_database)

    # Act
    chat_dao.update(chat_data=chat_data)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT attached_user_id, updated_at FROM chats WHERE id = ?",
            (chat_id,),
        )
        data = cursor.fetchone()
        assert data[0] == attached_user_id
        assert data[1] is not None


def test_chat_dao_get_by_id(sqlite3_database):
    # Arrange
    chat_id = generate_uuid4()
    attached_user_id = generate_uuid4()
    insert_chat(
        sqlite3_database=sqlite3_database,
        chat_id=chat_id,
        contact_id=generate_uuid4(),
        company_id=generate_uuid4(),
        attached_user_id=attached_user_id,
    )
    chat_dao = SQLiteChatDAO(db_path=sqlite3_database)

    # Act
    chat_dao.get_by_id(chat_id=chat_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT attached_user_id FROM chats WHERE id = ?",
            (chat_id,),
        )
        data = cursor.fetchone()
        assert data[0] == attached_user_id


def test_chat_dao_get_all(sqlite3_database):
    # Arrange
    insert_chat(
        sqlite3_database=sqlite3_database,
        chat_id=generate_uuid4(),
        contact_id=generate_uuid4(),
        company_id=generate_uuid4(),
    )
    insert_chat(
        sqlite3_database=sqlite3_database,
        chat_id=generate_uuid4(),
        contact_id=generate_uuid4(),
        company_id=generate_uuid4(),
    )
    chat_dao = SQLiteChatDAO(db_path=sqlite3_database)

    # Act
    chats = chat_dao.get_all()

    # Assert
    assert len(chats) == 2


def test_chat_dao_delete(sqlite3_database):
    # Arrange
    chat_id = generate_uuid4()
    insert_chat(
        sqlite3_database=sqlite3_database,
        chat_id=chat_id,
        contact_id=generate_uuid4(),
        company_id=generate_uuid4(),
        attached_user_id=generate_uuid4(),
    )
    chat_dao = SQLiteChatDAO(db_path=sqlite3_database)

    # Act
    chat_dao.delete(chat_id=chat_id)

    # Assert
    with sqlite3.connect(database=sqlite3_database) as conn:
        cursor = conn.execute(
            "SELECT COUNT(attached_user_id) FROM chats WHERE id = ?",
            (chat_id,),
        )
        data = cursor.fetchone()
        assert data[0] == 0
