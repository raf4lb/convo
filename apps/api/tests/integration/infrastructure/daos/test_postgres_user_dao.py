import uuid

import pytest


@pytest.mark.integration
@pytest.mark.dao
class TestPostgresUserDAO:
    """
    Integration tests for PostgresUserDAO.

    Tests verify that the DAO correctly interacts with PostgreSQL database.
    Each test runs in an isolated transaction that is rolled back after
    completion, ensuring no data pollution between tests.
    """

    def test_get_by_company_id(self, user_dao, db_cursor):
        """Test retrieving users by company ID."""
        # Arrange - Create test companies
        company1_id = str(uuid.uuid4())
        company2_id = str(uuid.uuid4())

        for company_id in [company1_id, company2_id]:
            db_cursor.execute(
                """
                INSERT INTO companies (id, name, email, phone, is_active,
                                       attendant_sees_all_conversations, whatsapp_api_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    company_id,
                    f"Company {company_id[:8]}",
                    f"{company_id[:8]}@test.com",
                    "+1234567890",
                    True,
                    False,
                    "api_key",
                ),
            )

        # Insert users for company1
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user1_id,
                "User 1",
                "user1@test.com",
                "administrator",
                "hash1",
                company1_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user2_id,
                "User 2",
                "user2@test.com",
                "manager",
                "hash2",
                company1_id,
                True,
            ),
        )

        # Insert user for company2
        user3_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user3_id,
                "User 3",
                "user3@test.com",
                "attendant",
                "hash3",
                company2_id,
                True,
            ),
        )

        # Act
        results = user_dao.get_by_company_id(company1_id)

        # Assert
        assert len(results) == 2
        user_ids = [result[0] for result in results]
        assert user1_id in user_ids
        assert user2_id in user_ids
        assert user3_id not in user_ids

    def test_get_by_company_and_role(self, user_dao, db_cursor):
        """Test retrieving users by company ID and role."""
        # Arrange - Create test company
        company_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO companies (id, name, email, phone, is_active,
                                   attendant_sees_all_conversations, whatsapp_api_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                "Test Company",
                "test@company.com",
                "+1234567890",
                True,
                False,
                "api_key",
            ),
        )

        # Insert users with different roles
        admin_id = str(uuid.uuid4())
        manager_id = str(uuid.uuid4())
        attendant_id = str(uuid.uuid4())

        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                admin_id,
                "Admin User",
                "admin@test.com",
                "administrator",
                "hash1",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                manager_id,
                "Manager User",
                "manager@test.com",
                "manager",
                "hash2",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                attendant_id,
                "Attendant User",
                "attendant@test.com",
                "attendant",
                "hash3",
                company_id,
                True,
            ),
        )

        # Act
        admin_results = user_dao.get_by_company_and_role(company_id, "administrator")
        manager_results = user_dao.get_by_company_and_role(company_id, "manager")
        attendant_results = user_dao.get_by_company_and_role(company_id, "attendant")

        # Assert
        assert len(admin_results) == 1
        assert admin_results[0][0] == admin_id
        assert admin_results[0][1] == "Admin User"

        assert len(manager_results) == 1
        assert manager_results[0][0] == manager_id
        assert manager_results[0][1] == "Manager User"

        assert len(attendant_results) == 1
        assert attendant_results[0][0] == attendant_id
        assert attendant_results[0][1] == "Attendant User"

    def test_search_users_by_name(self, user_dao, db_cursor):
        """Test searching users by name."""
        # Arrange - Create test company
        company_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO companies (id, name, email, phone, is_active,
                                   attendant_sees_all_conversations, whatsapp_api_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                "Test Company",
                "test@company.com",
                "+1234567890",
                True,
                False,
                "api_key",
            ),
        )

        # Insert users with different names
        john_id = str(uuid.uuid4())
        jane_id = str(uuid.uuid4())
        bob_id = str(uuid.uuid4())

        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                john_id,
                "John Doe",
                "john@test.com",
                "administrator",
                "hash1",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                jane_id,
                "Jane Smith",
                "jane@test.com",
                "manager",
                "hash2",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                bob_id,
                "Bob Johnson",
                "bob@test.com",
                "attendant",
                "hash3",
                company_id,
                True,
            ),
        )

        # Act - Search for "john" (should match "John Doe" and "Bob Johnson")
        results = user_dao.search_users(company_id, "john")

        # Assert
        assert len(results) == 2
        user_names = [result[1] for result in results]
        assert "John Doe" in user_names
        assert "Bob Johnson" in user_names
        assert "Jane Smith" not in user_names

    def test_search_users_by_email(self, user_dao, db_cursor):
        """Test searching users by email."""
        # Arrange - Create test company
        company_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO companies (id, name, email, phone, is_active,
                                   attendant_sees_all_conversations, whatsapp_api_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                "Test Company",
                "test@company.com",
                "+1234567890",
                True,
                False,
                "api_key",
            ),
        )

        # Insert users with different emails
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user1_id,
                "User 1",
                "alice@example.com",
                "administrator",
                "hash1",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (user2_id, "User 2", "bob@test.com", "manager", "hash2", company_id, True),
        )

        # Act - Search for "example" (should match alice@example.com)
        results = user_dao.search_users(company_id, "example")

        # Assert
        assert len(results) == 1
        assert results[0][0] == user1_id
        assert results[0][2] == "alice@example.com"

    def test_search_with_role_filter(self, user_dao, db_cursor):
        """Test searching users with role filter."""
        # Arrange - Create test company
        company_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO companies (id, name, email, phone, is_active,
                                   attendant_sees_all_conversations, whatsapp_api_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                "Test Company",
                "test@company.com",
                "+1234567890",
                True,
                False,
                "api_key",
            ),
        )

        # Insert users - two Johns, one admin and one manager
        john_admin_id = str(uuid.uuid4())
        john_manager_id = str(uuid.uuid4())

        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                john_admin_id,
                "John Admin",
                "john.admin@test.com",
                "administrator",
                "hash1",
                company_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                john_manager_id,
                "John Manager",
                "john.manager@test.com",
                "manager",
                "hash2",
                company_id,
                True,
            ),
        )

        # Act - Search for "john" with role filter for "administrator"
        results = user_dao.search_users(company_id, "john", role="administrator")

        # Assert
        assert len(results) == 1
        assert results[0][0] == john_admin_id
        assert results[0][1] == "John Admin"
        assert results[0][3] == "administrator"

    def test_multi_tenancy_isolation(self, user_dao, db_cursor):
        """Test that users from other companies are not returned."""
        # Arrange - Create two companies
        company1_id = str(uuid.uuid4())
        company2_id = str(uuid.uuid4())

        for company_id in [company1_id, company2_id]:
            db_cursor.execute(
                """
                INSERT INTO companies (id, name, email, phone, is_active,
                                       attendant_sees_all_conversations, whatsapp_api_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    company_id,
                    f"Company {company_id[:8]}",
                    f"{company_id[:8]}@test.com",
                    "+1234567890",
                    True,
                    False,
                    "api_key",
                ),
            )

        # Insert users for both companies
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user1_id,
                "Company 1 User",
                "user1@test.com",
                "administrator",
                "hash1",
                company1_id,
                True,
            ),
        )
        db_cursor.execute(
            """
            INSERT INTO users (id, name, email, type, password_hash, company_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user2_id,
                "Company 2 User",
                "user2@test.com",
                "administrator",
                "hash2",
                company2_id,
                True,
            ),
        )

        # Act - Get users for company1
        results = user_dao.get_by_company_id(company1_id)

        # Assert - Only company1 users are returned
        assert len(results) == 1
        assert results[0][0] == user1_id
        assert results[0][4] == company1_id  # company_id field

        # Act - Search across company1
        search_results = user_dao.search_users(company1_id, "user")

        # Assert - Only company1 users are in search results
        assert len(search_results) == 1
        assert search_results[0][0] == user1_id
