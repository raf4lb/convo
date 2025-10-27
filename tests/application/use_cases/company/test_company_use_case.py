import pytest

from src.application.use_cases.company.company_use_cases import (
    CreateCompanyUseCase,
    UpdateCompanyUseCase,
)
from src.domain.errors import CompanyNotFoundError


def test_create_company_use_case(company_repository):
    # Arrange
    name = "Test Company"
    use_case = CreateCompanyUseCase(repository=company_repository)

    # Act
    company = use_case.execute(name)

    # Assert
    assert company_repository.get_company_by_id(company.id) is not None


def test_update_company_use_case_existing_company(company, company_repository):
    # Arrange
    company_repository.save(company)
    use_case = UpdateCompanyUseCase(repository=company_repository)

    # Act
    new_name = "New Name"
    company = use_case.execute(company.id, new_name)

    # Assert
    assert company.name == new_name


def test_update_company_use_case_non_existing_company(company, company_repository):
    # Arrange
    use_case = UpdateCompanyUseCase(repository=company_repository)

    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        use_case.execute(company.id, "New Name")
