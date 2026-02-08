#!/usr/bin/env python3
import os
from pathlib import Path

from src.infrastructure.database.postgres_setup import create_connection


def seed_postgres_database(database_url: str) -> None:
    """
    Seed PostgreSQL database with test data from SQL seed file.

    Args:
        database_url: PostgreSQL connection URL

    Raises:
        FileNotFoundError: If seed file doesn't exist
        Exception: If database seeding fails
    """
    seed_file = Path(__file__).parent / "seed_postgres_db.sql"

    if not seed_file.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_file}")

    with open(seed_file) as f:
        seed_sql = f.read()

    # Convert SQLAlchemy format to psycopg2 format if needed
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    try:
        conn = create_connection(database_url)
        cursor = conn.cursor()

        cursor.execute(seed_sql)
        conn.commit()

        cursor.close()
        conn.close()

        print("PostgreSQL database seeded successfully")
        print("- 2 companies inserted")
        print("- 5 users inserted")
        print("- 6 contacts inserted")
        print("- 5 chats inserted")
        print("- 24 messages inserted")

    except Exception as e:
        raise Exception(f"Error seeding PostgreSQL database: {e}")


if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    seed_postgres_database(database_url)
