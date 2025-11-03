import sqlite3
from sqlite3 import Connection


class SQLiteUserDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> Connection:
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def insert(self, user_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users (id, name, email, type, company_id)
                VALUES (:id, :name, :email, :type, :company_id)
            """,
                user_data,
            )
            conn.commit()

    def update(self, user_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE users
                SET
                    name = :name,
                    email = :email,
                    type = :type,
                    company_id = :company_id,
                    updated_at = :updated_at
                WHERE id = :id
            """,
                user_data,
            )
            conn.commit()

    def get_by_id(self, user_id: str) -> tuple:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, name, email, type, company_id, created_at, updated_at
                FROM users
                WHERE id = ?
            """,
                (user_id,),
            )
            return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT id, name, email, type, company_id, created_at, updated_at
                FROM users
                ORDER BY created_at DESC
            """)
            return cursor.fetchall()

    def delete(self, user_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
