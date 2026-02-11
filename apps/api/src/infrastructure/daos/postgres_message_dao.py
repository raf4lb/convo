import psycopg2


class PostgresMessageDAO:
    def __init__(self, database_url: str):
        # Convert SQLAlchemy format to psycopg2 format if needed
        if database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
        self.database_url = database_url

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def insert(self, message_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO messages (id, external_id, external_timestamp, chat_id, text, sent_by_user_id, read)
                    VALUES (%(id)s, %(external_id)s, %(external_timestamp)s, %(chat_id)s, %(text)s, %(sent_by_user_id)s, %(read)s)
                    """,
                    message_data,
                )
            conn.commit()

    def update(self, message_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE messages
                    SET
                        external_id = %(external_id)s,
                        external_timestamp = %(external_timestamp)s,
                        chat_id = %(chat_id)s,
                        text = %(text)s,
                        sent_by_user_id = %(sent_by_user_id)s,
                        read = %(read)s,
                        updated_at = %(updated_at)s
                    WHERE id = %(id)s
                    """,
                    message_data,
                )
            conn.commit()

    def get_by_id(self, message_id: str) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, external_id, external_timestamp, chat_id, text, sent_by_user_id, read, created_at, updated_at
                    FROM messages
                    WHERE id = %s
                    """,
                    (message_id,),
                )
                return cursor.fetchone()

    def get_by_chat_id(self, chat_id: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, external_id, external_timestamp, chat_id, text, sent_by_user_id, read, created_at, updated_at
                    FROM messages
                    WHERE chat_id = %s
                    ORDER BY external_timestamp ASC
                    """,
                    (chat_id,),
                )
                return cursor.fetchall()

    def get_by_external_id(self, external_id: str) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, external_id, external_timestamp, chat_id, text, sent_by_user_id, read, created_at, updated_at
                    FROM messages
                    WHERE external_id = %s
                    """,
                    (external_id,),
                )
                return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, external_id, external_timestamp, chat_id, text, sent_by_user_id, read, created_at, updated_at
                    FROM messages
                    ORDER BY created_at DESC
                    """
                )
                return cursor.fetchall()

    def delete(self, message_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
            conn.commit()

    def mark_chat_messages_as_read(self, chat_id: str) -> int:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE messages
                    SET read = TRUE, updated_at = CURRENT_TIMESTAMP
                    WHERE chat_id = %s AND read = FALSE
                    """,
                    (chat_id,),
                )
                updated_count = cursor.rowcount
            conn.commit()
        return updated_count
