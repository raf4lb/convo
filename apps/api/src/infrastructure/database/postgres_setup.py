from contextlib import contextmanager

import psycopg2


def create_connection(database_url: str):
    """
    Create and return a PostgreSQL database connection.

    Args:
        database_url: PostgreSQL connection URL in format:
                     postgresql://user:password@host:port/database

    Returns:
        psycopg2 connection object
    """
    return psycopg2.connect(database_url)


@contextmanager
def get_connection(database_url: str):
    """
    Context manager for PostgreSQL database connections.
    Automatically handles connection cleanup.

    Args:
        database_url: PostgreSQL connection URL

    Yields:
        psycopg2 connection object
    """
    conn = None
    try:
        conn = create_connection(database_url)
        yield conn
    finally:
        if conn:
            conn.close()
