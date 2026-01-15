import sqlite3
from sqlite3 import Connection


class SQLiteContactDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> Connection:
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def insert(self, contact_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO contacts (id, name, phone_number, email, company_id,
                                      is_blocked, last_contact_at)
                VALUES (:id, :name, :phone_number, :email, :company_id,
                        :is_blocked, :last_contact_at)
                """,
                contact_data,
            )
            conn.commit()

    def update(self, contact_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE contacts
                SET name            = :name,
                    phone_number    = :phone_number,
                    email           = :email,
                    company_id      = :company_id,
                    is_blocked      = :is_blocked,
                    last_contact_at = :last_contact_at,
                    updated_at      = :updated_at
                WHERE id = :id
                """,
                contact_data,
            )
            conn.commit()

    def get_by_id(self, contact_id: str) -> tuple:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id,
                       name,
                       phone_number,
                       email,
                       company_id,
                       is_blocked,
                       last_contact_at,
                       created_at,
                       updated_at
                FROM contacts
                WHERE id = ?
                """,
                (contact_id,),
            )
            return cursor.fetchone()

    def get_by_phone_number(self, phone_number: str) -> tuple:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT
                    id, name, phone_number, email, company_id,
                    is_blocked, last_contact_at, created_at, updated_at
                FROM contacts
                WHERE phone_number = ?
                """,
                (phone_number,),
            )
            return cursor.fetchone()

    def get_company_contact_by_phone_number(
        self, company_id: str, phone_number: str
    ) -> tuple:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT
                    id, name, phone_number, email, company_id,
                    is_blocked, last_contact_at, created_at, updated_at
                FROM contacts
                WHERE company_id = ? AND phone_number = ?
                """,
                (company_id, phone_number),
            )
            return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id,
                     name,
                     phone_number,
                     email,
                     company_id,
                     is_blocked,
                     last_contact_at,
                     created_at,
                     updated_at
                FROM contacts
                ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()

    def delete(self, contact_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
