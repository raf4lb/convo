import pytest

from fixtures.database_fixtures import TestConnectionWrapper
from src.infrastructure.daos.postgres_company_dao import PostgresCompanyDAO
from src.infrastructure.daos.postgres_user_dao import PostgresUserDAO


@pytest.fixture
def company_dao(test_database_url, db_connection, monkeypatch):
    """
    Provide PostgresCompanyDAO using test database connection.

    The DAO is monkey-patched to use a wrapped test connection that prevents
    commits. This ensures that all DAO operations participate in the test
    transaction and are rolled back after the test completes, even if the
    DAO explicitly calls commit().

    Args:
        test_database_url: Test database URL from session fixture
        db_connection: Test database connection from fixture
        monkeypatch: Pytest monkeypatch fixture for patching _connect method

    Returns:
        PostgresCompanyDAO: Company DAO instance configured for testing
    """
    dao = PostgresCompanyDAO(test_database_url)

    # Wrap the connection to prevent commits during tests
    wrapped_connection = TestConnectionWrapper(db_connection)

    # Monkey-patch _connect to return wrapped test connection
    # The wrapper prevents commits, ensuring rollback works correctly
    monkeypatch.setattr(dao, "_connect", lambda: wrapped_connection)

    return dao


@pytest.fixture
def user_dao(test_database_url, db_connection, monkeypatch):
    """
    Provide PostgresUserDAO using test database connection.

    The DAO is monkey-patched to use a wrapped test connection that prevents
    commits. This ensures that all DAO operations participate in the test
    transaction and are rolled back after the test completes.

    Args:
        test_database_url: Test database URL from session fixture
        db_connection: Test database connection from fixture
        monkeypatch: Pytest monkeypatch fixture for patching _connect method

    Returns:
        PostgresUserDAO: User DAO instance configured for testing
    """
    dao = PostgresUserDAO(test_database_url)

    # Wrap the connection to prevent commits during tests
    wrapped_connection = TestConnectionWrapper(db_connection)

    # Monkey-patch _connect to return wrapped test connection
    monkeypatch.setattr(dao, "_connect", lambda: wrapped_connection)

    return dao


# Additional DAO fixtures can be added following the same pattern:
#
# @pytest.fixture
# def user_dao(test_database_url, db_connection, monkeypatch):
#     """Provide PostgresUserDAO using test database connection."""
#     dao = PostgresUserDAO(test_database_url)
#     monkeypatch.setattr(dao, "_connect", lambda: db_connection)
#     return dao
#
# @pytest.fixture
# def contact_dao(test_database_url, db_connection, monkeypatch):
#     """Provide PostgresContactDAO using test database connection."""
#     dao = PostgresContactDAO(test_database_url)
#     monkeypatch.setattr(dao, "_connect", lambda: db_connection)
#     return dao
#
# @pytest.fixture
# def chat_dao(test_database_url, db_connection, monkeypatch):
#     """Provide PostgresChatDAO using test database connection."""
#     dao = PostgresChatDAO(test_database_url)
#     monkeypatch.setattr(dao, "_connect", lambda: db_connection)
#     return dao
#
# @pytest.fixture
# def message_dao(test_database_url, db_connection, monkeypatch):
#     """Provide PostgresMessageDAO using test database connection."""
#     dao = PostgresMessageDAO(test_database_url)
#     monkeypatch.setattr(dao, "_connect", lambda: db_connection)
#     return dao
