import psycopg2


class PostgresUserDAO:
    def __init__(self, database_url: str):
        # Convert SQLAlchemy format to psycopg2 format if needed
        if database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
        self.database_url = database_url

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def insert(self, user_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (id, name, email, type, company_id, is_active)
                    VALUES (%(id)s, %(name)s, %(email)s, %(type)s, %(company_id)s, %(is_active)s)
                """,
                    user_data,
                )
            conn.commit()

    def update(self, user_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET
                        name = %(name)s,
                        email = %(email)s,
                        type = %(type)s,
                        company_id = %(company_id)s,
                        is_active = %(is_active)s,
                        updated_at = %(updated_at)s
                    WHERE id = %(id)s
                """,
                    user_data,
                )
            conn.commit()

    def get_by_id(self, user_id: str) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, type, company_id, is_active, created_at, updated_at
                    FROM users
                    WHERE id = %s
                """,
                    (user_id,),
                )
                return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, name, email, type, company_id, is_active, created_at, updated_at
                    FROM users
                    ORDER BY created_at DESC
                """)
                return cursor.fetchall()

    def delete(self, user_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
