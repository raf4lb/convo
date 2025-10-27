from src.infrastructure.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)


def test_create_company(company):
    # Arrange
    repository = InMemoryCompanyRepository()

    # Act
    repository.save(company)

    # Assert
    assert repository.get_company_by_id(company.id) is not None


def test_update_company(company):
    # Arrange
    repository = InMemoryCompanyRepository()
    repository.save(company)

    # Act
    new_name = "New Name"
    company.name = new_name
    repository.save(company)

    # Assert
    company = repository.get_company_by_id(company.id)
    assert company.name == new_name
