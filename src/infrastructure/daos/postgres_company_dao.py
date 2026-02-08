import psycopg2


class PostgresCompanyDAO:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def _connect(self):
        return psycopg2.connect(self.database_url)

    def insert(self, company_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO companies (id, name, email, phone, is_active,
                                           attendant_sees_all_conversations, whatsapp_api_key)
                    VALUES (%(id)s, %(name)s, %(email)s, %(phone)s, %(is_active)s,
                            %(attendant_sees_all_conversations)s, %(whatsapp_api_key)s)
                    """,
                    company_data,
                )
            conn.commit()

    def update(self, company_data: dict) -> None:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE companies
                    SET name                             = %(name)s,
                        email                            = %(email)s,
                        phone                            = %(phone)s,
                        is_active                        = %(is_active)s,
                        attendant_sees_all_conversations = %(attendant_sees_all_conversations)s,
                        whatsapp_api_key                 = %(whatsapp_api_key)s,
                        updated_at                       = %(updated_at)s
                    WHERE id = %(id)s
                    """,
                    company_data,
                )
            conn.commit()

    def get_by_id(self, company_id: str) -> tuple:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
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
                    WHERE id = %s
                    """,
                    (company_id,),
                )
                return cursor.fetchone()

    def get_all(self) -> list[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
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
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM companies WHERE id = %s", (company_id,))
            conn.commit()
