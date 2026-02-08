import sqlite3
from sqlite3 import Connection


class SQLiteCompanyDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> Connection:
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def insert(self, company_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO companies (id, name, email, phone, is_active,
                                       attendant_sees_all_conversations, whatsapp_api_key)
                VALUES (:id, :name, :email, :phone, :is_active,
                        :attendant_sees_all_conversations, :whatsapp_api_key)
                """,
                company_data,
            )
            conn.commit()

    def update(self, company_data: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE companies
                SET name                             = :name,
                    email                            = :email,
                    phone                            = :phone,
                    is_active                        = :is_active,
                    attendant_sees_all_conversations = :attendant_sees_all_conversations,
                    whatsapp_api_key                 = :whatsapp_api_key,
                    updated_at                       = :updated_at
                WHERE id = :id
                """,
                company_data,
            )
            conn.commit()

    def get_by_id(self, company_id: str) -> tuple:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id,
                       name,
                       created_at,
                       updated_at,
                       email,
                       phone,
                       is_active,
                       attendant_sees_all_conversations,
                       whatsapp_api_key
                FROM companies
                WHERE id = ?
                """,
                (company_id,),
            )
            return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            cursor = conn.execute("""
                                  SELECT id,
                                         name,
                                         created_at,
                                         updated_at,
                                         email,
                                         phone,
                                         is_active,
                                         attendant_sees_all_conversations,
                                         whatsapp_api_key
                                  FROM companies
                                  ORDER BY created_at DESC
                                  """)
            return cursor.fetchall()

    def delete(self, company_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
            conn.commit()
