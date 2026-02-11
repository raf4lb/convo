import os

import psycopg2
import pytest

from src.infrastructure.database.init_postgres_db import init_postgres_database


class TestConnectionWrapper:
    """
    Wrapper around psycopg2 connection that prevents commits during tests.

    This ensures that all database operations within a test are rolled back
    after the test completes, even if the code under test calls conn.commit().
    """

    def __init__(self, conn):
        self._conn = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Don't close the connection, let the fixture handle it
        return False

    def cursor(self):
        return self._conn.cursor()

    def commit(self):
        # No-op: prevent commits during tests to enable rollback
        pass

    def rollback(self):
        # Delegate to actual connection
        self._conn.rollback()

    def close(self):
        # No-op: let the fixture close the connection
        pass

    def __getattr__(self, name):
        # Delegate other attributes to the wrapped connection
        return getattr(self._conn, name)


@pytest.fixture(scope="session")
def test_database_url():
    """
    Provide test database URL from environment.

    The test database is separate from the development database to ensure
    isolation. Schema is initialized once per test session.

    Returns:
        str: PostgreSQL connection URL for test database

    Raises:
        pytest.skip: If TEST_DATABASE_URL environment variable is not set
    """
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL not set")

    # Initialize schema once per session
    init_postgres_database(url)

    return url


@pytest.fixture
def db_connection(test_database_url):
    """
    Provide database connection with automatic rollback after test.

    Each test gets a fresh connection with autocommit disabled, running in
    a transaction. After the test completes, all changes are rolled back,
    ensuring test isolation without manual cleanup.

    Args:
        test_database_url: Test database URL from session fixture

    Yields:
        psycopg2.connection: Database connection in transaction mode

    Cleanup:
        Rolls back transaction and closes connection
    """
    conn = psycopg2.connect(test_database_url)
    conn.autocommit = False  # Enable transaction mode

    yield conn

    conn.rollback()  # Rollback any changes made during test
    conn.close()


@pytest.fixture
def db_cursor(db_connection):
    """
    Provide database cursor for direct SQL queries in tests.

    Useful for verification queries that need to check data directly
    without going through DAOs or repositories.

    Args:
        db_connection: Database connection from fixture

    Yields:
        psycopg2.cursor: Database cursor

    Cleanup:
        Closes cursor after test
    """
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
