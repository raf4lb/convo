import sqlite3
from sqlite3 import Connection


class SQLiteChatDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> Connection:
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def insert(self, chat_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO chats (id, company_id, contact_id, status, attached_user_id)
                VALUES (:id, :company_id, :contact_id, :status, :attached_user_id)
                """,
                chat_data,
            )
            conn.commit()

    def update(self, chat_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE chats
                SET
                    company_id = :company_id,
                    contact_id = :contact_id,
                    status = :status,
                    attached_user_id = :attached_user_id,
                    updated_at = :updated_at
                WHERE id = :id
                """,
                chat_data,
            )
            conn.commit()

    def get_by_id(self, chat_id: str) -> tuple | None:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                FROM chats
                WHERE id = ?
                """,
                (chat_id,),
            )
            return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                FROM chats
                ORDER BY created_at DESC
                """,
            )
            return cursor.fetchall()

    def get_by_company_id(self, company_id: str) -> list[tuple]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                FROM chats
                WHERE company_id = ?
                ORDER BY created_at DESC
                """,
                (company_id,),
            )

            return cursor.fetchall()

    def get_company_chat_by_contact_id(
        self, company_id: str, contact_id: str
    ) -> tuple | None:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                FROM chats
                WHERE company_id = ? AND contact_id = ?
                ORDER BY created_at DESC
                """,
                (company_id, contact_id),
            )

            return cursor.fetchone()

    def delete(self, chat_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
            conn.commit()
