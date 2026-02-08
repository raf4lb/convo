#!/usr/bin/env python3
"""
Script para inicializar o banco de dados PostgreSQL com o schema.
Cria todas as tabelas necessárias no banco de dados.
Equivalente a executar: python src/infrastructure/database/init_postgres_db.py
Compatível com Windows, macOS e Linux.
"""

import os

from src.infrastructure.database.init_postgres_db import init_postgres_database


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Erro: DATABASE_URL environment variable is required")
        print("Configure DATABASE_URL no arquivo .env")
        exit(1)

    # Convert SQLAlchemy format to psycopg2 format if needed
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    init_postgres_database(database_url)


if __name__ == "__main__":
    main()
