import os
from pathlib import Path

from src.infrastructure.database.postgres_setup import create_connection


def init_postgres_database(database_url: str) -> None:
    """
    Initialize PostgreSQL database by creating tables from SQL schema file.

    Args:
        database_url: PostgreSQL connection URL

    Raises:
        FileNotFoundError: If schema file doesn't exist
        Exception: If database initialization fails
    """
    schema_file = Path(__file__).parent / "create_postgres_tables.sql"

    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    with open(schema_file) as f:
        schema_sql = f.read()

    try:
        conn = create_connection(database_url)
        cursor = conn.cursor()

        cursor.execute(schema_sql)
        conn.commit()

        cursor.close()
        conn.close()

        print("PostgreSQL database initialized successfully")

    except Exception as e:
        print(f"Error initializing PostgreSQL database: {e}")
        raise


if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    init_postgres_database(database_url)
