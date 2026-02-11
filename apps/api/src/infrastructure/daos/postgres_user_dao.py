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

    def insert(self, user_data: dict) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
                    VALUES (%(id)s, %(name)s, %(email)s, %(type)s, %(password_hash)s, %(company_id)s, %(is_active)s)
                    RETURNING id, name, email, type, company_id, is_active, created_at, updated_at
                """,
                    user_data,
                )
                result = cursor.fetchone()
            conn.commit()
            return result

    def update(self, user_data: dict) -> tuple:
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
                    RETURNING id, name, email, type, company_id, is_active, created_at, updated_at
                """,
                    user_data,
                )
                result = cursor.fetchone()
            conn.commit()
            return result

    def update_password(self, user_id: str, password_hash: str) -> None:
        """Update only the password hash for a user."""
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = %(password_hash)s
                    WHERE id = %(id)s
                """,
                    {"id": user_id, "password_hash": password_hash},
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

    def get_by_email(self, email: str) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, type, password_hash, company_id, is_active, created_at, updated_at
                    FROM users
                    WHERE email = %s
                """,
                    (email,),
                )
                return cursor.fetchone()

    def delete(self, user_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()

    def get_by_company_id(self, company_id: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, type, company_id, is_active, created_at, updated_at
                    FROM users
                    WHERE company_id = %s
                    ORDER BY created_at DESC
                    """,
                    (company_id,),
                )
                return cursor.fetchall()

    def get_by_company_and_role(self, company_id: str, role: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, type, company_id, is_active, created_at, updated_at
                    FROM users
                    WHERE company_id = %s AND type = %s
                    ORDER BY created_at DESC
                    """,
                    (company_id, role),
                )
                return cursor.fetchall()

    def search_users(
        self, company_id: str, query: str, role: str | None = None
    ) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                search_pattern = f"%{query}%"
                base_query = """
                    SELECT id, name, email, type, company_id, is_active, created_at, updated_at
                    FROM users
                    WHERE company_id = %s
                    AND (name ILIKE %s OR email ILIKE %s)
                """

                if role:
                    base_query += " AND type = %s"
                    cursor.execute(
                        base_query + " ORDER BY created_at DESC",
                        (company_id, search_pattern, search_pattern, role),
                    )
                else:
                    cursor.execute(
                        base_query + " ORDER BY created_at DESC",
                        (company_id, search_pattern, search_pattern),
                    )

                return cursor.fetchall()
