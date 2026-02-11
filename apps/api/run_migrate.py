#!/usr/bin/env python3
"""
Script to run database migrations.
Executes all SQL files in the migrations directory.
Compatível com Windows, macOS e Linux.
"""

import os

from src.infrastructure.database.run_migrations import run_migrations


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Erro: DATABASE_URL environment variable is required")
        print("Configure DATABASE_URL no arquivo .env")
        exit(1)

    # Convert SQLAlchemy format to psycopg2 format if needed
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    run_migrations(database_url)


if __name__ == "__main__":
    main()
