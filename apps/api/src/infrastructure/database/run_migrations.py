import os
from pathlib import Path

from src.infrastructure.database.postgres_setup import create_connection


def run_migrations(database_url: str) -> None:
    """
    Run all SQL migration files in the migrations directory.

    Args:
        database_url: PostgreSQL connection URL

    Raises:
        Exception: If migration fails
    """
    migrations_dir = Path(__file__).parent / "migrations"

    if not migrations_dir.exists():
        print("No migrations directory found")
        return

    # Convert SQLAlchemy format to psycopg2 format if needed
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print("No migration files found")
        return

    try:
        conn = create_connection(database_url)
        cursor = conn.cursor()

        for migration_file in migration_files:
            print(f"Running migration: {migration_file.name}")
            with open(migration_file) as f:
                migration_sql = f.read()

            cursor.execute(migration_sql)
            conn.commit()
            print(f"✓ Completed: {migration_file.name}")

        cursor.close()
        conn.close()

        print(f"\n✓ Successfully ran {len(migration_files)} migration(s)")

    except Exception as e:
        print(f"✗ Error running migrations: {e}")
        raise


if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    run_migrations(database_url)
