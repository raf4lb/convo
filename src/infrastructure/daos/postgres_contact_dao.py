import psycopg2


class PostgresContactDAO:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def insert(self, contact_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO contacts (
                        id, name, phone_number, email, company_id, is_blocked, tags, notes, last_contact_at
                    ) VALUES (
                        %(id)s, %(name)s, %(phone_number)s, %(email)s, %(company_id)s, %(is_blocked)s, %(tags)s, %(notes)s, %(last_contact_at)s
                    )
                    """,
                    contact_data,
                )
            conn.commit()

    def update(self, contact_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE contacts SET
                        name = %(name)s,
                        phone_number = %(phone_number)s,
                        email = %(email)s,
                        company_id = %(company_id)s,
                        is_blocked = %(is_blocked)s,
                        tags = %(tags)s,
                        notes = %(notes)s,
                        last_contact_at = %(last_contact_at)s,
                        updated_at = %(updated_at)s
                    WHERE id = %(id)s
                    """,
                    contact_data,
                )
            conn.commit()

    def get_by_id(self, contact_id: str) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id,
                           name,
                           phone_number,
                           email,
                           company_id,
                           is_blocked,
                           tags,
                           notes,
                           last_contact_at,
                           created_at,
                           updated_at
                    FROM contacts
                    WHERE id = %s
                    """,
                    (contact_id,),
                )
                return cursor.fetchone()

    def get_by_company_id(self, company_id: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, phone_number, email, company_id, is_blocked, tags, notes, last_contact_at, created_at, updated_at
                    FROM contacts
                    WHERE company_id = %s
                    ORDER BY name ASC
                    """,
                    (company_id,),
                )
                return cursor.fetchall()

    def get_by_phone_number(self, phone_number: str) -> tuple | None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id, name, phone_number, email, company_id,
                        is_blocked, tags, notes, last_contact_at, created_at, updated_at
                    FROM contacts
                    WHERE phone_number = %s
                    """,
                    (phone_number,),
                )
                return cursor.fetchone()

    def get_company_contact_by_phone_number(
        self, company_id: str, phone_number: str
    ) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id, name, phone_number, email, company_id,
                        is_blocked, tags, notes, last_contact_at, created_at, updated_at
                    FROM contacts
                    WHERE company_id = %s AND phone_number = %s
                    """,
                    (company_id, phone_number),
                )
                return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id,
                         name,
                         phone_number,
                         email,
                         company_id,
                         is_blocked,
                         tags,
                         notes,
                         last_contact_at,
                         created_at,
                         updated_at
                    FROM contacts
                    ORDER BY created_at DESC
                    """
                )
                return cursor.fetchall()

    def search_contacts(self, company_id: str, query: str) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                lower_query = f"%{query.lower()}%"
                cursor.execute(
                    """
                    SELECT id, name, phone_number, email, company_id, is_blocked, tags, notes, last_contact_at, created_at, updated_at
                    FROM contacts
                    WHERE company_id = %s AND (LOWER(name) LIKE %s OR phone_number LIKE %s OR LOWER(email) LIKE %s)
                    ORDER BY name ASC
                    """,
                    (company_id, lower_query, f"%{query}%", lower_query),
                )
                return cursor.fetchall()

    def delete(self, contact_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
