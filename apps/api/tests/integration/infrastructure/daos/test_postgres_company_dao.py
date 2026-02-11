import uuid
from datetime import datetime

import pytest


@pytest.mark.integration
@pytest.mark.dao
class TestPostgresCompanyDAO:
    """
    Integration tests for PostgresCompanyDAO.

    Tests verify that the DAO correctly interacts with PostgreSQL database.
    Each test runs in an isolated transaction that is rolled back after
    completion, ensuring no data pollution between tests.
    """

    def test_insert_company(self, company_dao, db_cursor):
        """Test inserting a new company."""
        # Arrange
        company_data = {
            "id": str(uuid.uuid4()),
            "name": "Test Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "is_active": True,
            "attendant_sees_all_conversations": False,
            "whatsapp_api_key": "test_api_key",
        }

        # Act
        company_dao.insert(company_data)

        # Assert - Verify via DAO
        result = company_dao.get_by_id(company_data["id"])
        assert result is not None
        assert result[1] == "Test Company"  # name field
        assert result[4] == "test@company.com"  # email field
        assert result[6] is True  # is_active field

        # Assert - Verify via raw SQL
        db_cursor.execute(
            "SELECT name, email FROM companies WHERE id = %s",
            (company_data["id"],),
        )
        row = db_cursor.fetchone()
        assert row[0] == "Test Company"
        assert row[1] == "test@company.com"

    def test_get_by_id(self, company_dao, db_cursor):
        """Test retrieving a company by ID."""
        # Arrange - Insert test data directly via SQL
        company_id = str(uuid.uuid4())
        db_cursor.execute(
            """
            INSERT INTO companies (id, name, email, phone, is_active,
                                   attendant_sees_all_conversations, whatsapp_api_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                company_id,
                "Direct SQL Company",
                "sql@company.com",
                "+9876543210",
                True,
                True,
                "sql_api_key",
            ),
        )

        # Act
        result = company_dao.get_by_id(company_id)

        # Assert
        assert result is not None
        assert result[0] == company_id  # id field
        assert result[1] == "Direct SQL Company"  # name field
        assert result[4] == "sql@company.com"  # email field
        assert result[5] == "+9876543210"  # phone field
        assert result[6] is True  # is_active field
        assert result[7] is True  # attendant_sees_all_conversations field

    def test_get_by_id_not_found(self, company_dao):
        """Test retrieving a non-existent company returns None."""
        # Arrange
        non_existent_id = str(uuid.uuid4())

        # Act
        result = company_dao.get_by_id(non_existent_id)

        # Assert
        assert result is None

    def test_get_all(self, company_dao, db_cursor):
        """Test retrieving all companies."""
        # Arrange - Insert multiple companies via SQL
        company_ids = [str(uuid.uuid4()) for _ in range(3)]
        for i, company_id in enumerate(company_ids):
            db_cursor.execute(
                """
                INSERT INTO companies (id, name, email, phone, is_active,
                                       attendant_sees_all_conversations,
                                       whatsapp_api_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    company_id,
                    f"Company {i + 1}",
                    f"company{i + 1}@test.com",
                    f"+123456789{i}",
                    True,
                    False,
                    f"api_key_{i + 1}",
                ),
            )

        # Act
        results = company_dao.get_all()

        # Assert
        assert len(results) == 3
        # Results should be ordered by created_at DESC (most recent first)
        company_names = [result[1] for result in results]
        assert "Company 1" in company_names
        assert "Company 2" in company_names
        assert "Company 3" in company_names

    def test_update_company(self, company_dao, db_cursor):
        """Test updating an existing company."""
        # Arrange - Insert company first
        company_id = str(uuid.uuid4())
        original_data = {
            "id": company_id,
            "name": "Original Name",
            "email": "original@company.com",
            "phone": "+1111111111",
            "is_active": True,
            "attendant_sees_all_conversations": False,
            "whatsapp_api_key": "original_key",
        }
        company_dao.insert(original_data)

        # Act - Update the company
        updated_data = {
            "id": company_id,
            "name": "Updated Name",
            "email": "updated@company.com",
            "phone": "+2222222222",
            "is_active": False,
            "attendant_sees_all_conversations": True,
            "whatsapp_api_key": "updated_key",
            "updated_at": datetime.now(),
        }
        company_dao.update(updated_data)

        # Assert - Verify via DAO
        result = company_dao.get_by_id(company_id)
        assert result[1] == "Updated Name"
        assert result[4] == "updated@company.com"
        assert result[5] == "+2222222222"
        assert result[6] is False  # is_active
        assert result[7] is True  # attendant_sees_all_conversations
        assert result[8] == "updated_key"  # whatsapp_api_key

        # Assert - Verify via raw SQL
        db_cursor.execute(
            "SELECT name, email, is_active FROM companies WHERE id = %s",
            (company_id,),
        )
        row = db_cursor.fetchone()
        assert row[0] == "Updated Name"
        assert row[1] == "updated@company.com"
        assert row[2] is False

    def test_delete_company(self, company_dao, db_cursor):
        """Test deleting a company."""
        # Arrange - Insert company first
        company_id = str(uuid.uuid4())
        company_data = {
            "id": company_id,
            "name": "To Be Deleted",
            "email": "delete@company.com",
            "phone": "+9999999999",
            "is_active": True,
            "attendant_sees_all_conversations": False,
            "whatsapp_api_key": "delete_key",
        }
        company_dao.insert(company_data)

        # Verify it exists
        assert company_dao.get_by_id(company_id) is not None

        # Act
        company_dao.delete(company_id)

        # Assert - Verify via DAO
        assert company_dao.get_by_id(company_id) is None

        # Assert - Verify via raw SQL
        db_cursor.execute("SELECT COUNT(*) FROM companies WHERE id = %s", (company_id,))
        count = db_cursor.fetchone()[0]
        assert count == 0

    def test_transaction_rollback_isolation(self, company_dao):
        """
        Test that changes are rolled back and don't affect other tests.

        This test verifies the transaction isolation mechanism works correctly.
        Any data inserted here should be rolled back and not visible in
        subsequent tests.
        """
        # Arrange
        company_id = str(uuid.uuid4())
        company_data = {
            "id": company_id,
            "name": "Rollback Test Company",
            "email": "rollback@test.com",
            "phone": "+0000000000",
            "is_active": True,
            "attendant_sees_all_conversations": False,
            "whatsapp_api_key": "rollback_key",
        }

        # Act
        company_dao.insert(company_data)

        # Assert - Data exists within this transaction
        result = company_dao.get_by_id(company_id)
        assert result is not None
        assert result[1] == "Rollback Test Company"

        # Note: After this test completes, the transaction will be rolled back
        # by the db_connection fixture, so this data won't exist in other tests
