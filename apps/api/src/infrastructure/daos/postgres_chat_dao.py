import psycopg2


class PostgresChatDAO:
    def __init__(self, database_url: str):
        # Convert SQLAlchemy format to psycopg2 format if needed
        if database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
        self.database_url = database_url

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def insert(self, chat_data: dict) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO chats (id, company_id, contact_id, status, attached_user_id)
                    VALUES (%(id)s, %(company_id)s, %(contact_id)s, %(status)s, %(attached_user_id)s)
                    RETURNING id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    """,
                    chat_data,
                )
                result = cursor.fetchone()
            conn.commit()
            return result

    def update(self, chat_data: dict) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE chats
                    SET
                        company_id = %(company_id)s,
                        contact_id = %(contact_id)s,
                        status = %(status)s,
                        attached_user_id = %(attached_user_id)s,
                        updated_at = %(updated_at)s
                    WHERE id = %(id)s
                    RETURNING id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    """,
                    chat_data,
                )
                result = cursor.fetchone()
            conn.commit()
            return result

    def get_by_id(self, chat_id: str) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    FROM chats
                    WHERE id = %s
                    """,
                    (chat_id,),
                )
                return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    FROM chats
                    ORDER BY created_at DESC
                    """,
                )
                return cursor.fetchall()

    def get_by_company_id(self, company_id: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    FROM chats
                    WHERE company_id = %s
                    ORDER BY created_at DESC
                    """,
                    (company_id,),
                )

                return cursor.fetchall()

    def get_company_chat_by_contact_id(
        self, company_id: str, contact_id: str
    ) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, company_id, contact_id, status, attached_user_id, created_at, updated_at
                    FROM chats
                    WHERE company_id = %s AND contact_id = %s
                    ORDER BY created_at DESC
                    """,
                    (company_id, contact_id),
                )

                return cursor.fetchone()

    def delete(self, chat_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM chats WHERE id = %s", (chat_id,))
            conn.commit()
