#!/usr/bin/env python3
"""
Setup test database for integration tests.

Creates/resets the test database by connecting to PostgreSQL and
recreating the database. This script is called automatically by
run_tests.py unless the --no-db flag is used.
"""

import os
import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def setup_test_database():
    """
    Create or reset the test database.

    Connects to the default postgres database to create/drop the test database.
    Uses the same credentials as the main database but creates a separate
    test database (convo_test_db).

    Returns:
        bool: True if successful, False otherwise
    """
    # Get database connection parameters from environment
    db_user = os.getenv("DATABASE_USER", "convo_user")
    db_password = os.getenv("DATABASE_PASSWORD", "convo_pass")
    db_host = os.getenv("DATABASE_HOST", "db")
    db_port = os.getenv("DATABASE_PORT", "5432")
    test_db_name = "convo_test_db"

    print("Setting up test database...")

    try:
        # Connect to default postgres database to create/drop test database
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Drop test database if exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
        exists = cursor.fetchone()
        if exists:
            print(f"Dropping existing test database: {test_db_name}")
            # Terminate connections to the test database
            cursor.execute(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{test_db_name}'
                  AND pid <> pg_backend_pid()
                """
            )
            cursor.execute(f"DROP DATABASE {test_db_name}")

        # Create fresh test database
        print(f"Creating test database: {test_db_name}")
        cursor.execute(f"CREATE DATABASE {test_db_name}")

        cursor.close()
        conn.close()

        print("Test database created successfully.")
        print("Schema will be initialized on first test run.")
        return True

    except psycopg2.Error as e:
        print(f"Error setting up test database: {e}")
        print("Continuing with tests. DAO tests may fail.")
        return False
    except Exception as e:
        print(f"Unexpected error setting up test database: {e}")
        print("Continuing with tests. DAO tests may fail.")
        return False


if __name__ == "__main__":
    success = setup_test_database()
    sys.exit(0 if success else 1)
