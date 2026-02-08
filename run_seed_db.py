#!/usr/bin/env python3
"""
Script para popular o banco de dados PostgreSQL com dados de teste.
Executa o script de seed que insere empresas e contatos no banco.
Equivalente a executar: python src/infrastructure/database/seed_postgres_db.py
Compatível com Windows, macOS e Linux.
"""

import os

from src.infrastructure.database.seed_postgres_db import seed_postgres_database


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Erro: DATABASE_URL environment variable is required")
        print("Configure DATABASE_URL no arquivo .env")
        exit(1)

    seed_postgres_database(database_url)


if __name__ == "__main__":
    main()
