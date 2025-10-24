import pytest

from src.application.exceptions import CompanyNotFoundError
from src.application.use_cases.company.company_use_cases import (
    CreateCompanyUseCase,
    UpdateCompanyUseCase,
)


def test_create_company_use_case(company, company_repository):
    # Arrange
    create_use_case = CreateCompanyUseCase(repository=company_repository)
    # Act
    create_use_case.execute(company)
    # Assert
    assert company.id in {c.id for c in company_repository.get_companies()}


def test_update_company_use_case_existing_company(company, company_repository):
    # Arrange
    company_repository.create_company(company)
    update_use_case = UpdateCompanyUseCase(repository=company_repository)

    # Act
    new_name = "New Name"
    company.name = new_name
    update_use_case.execute(company)

    # Assert
    company = company_repository.get_company_by_id(company.id)
    assert company.name == new_name


def test_update_company_use_case_non_existing_company(company, company_repository):
    # Arrange
    use_case = UpdateCompanyUseCase(repository=company_repository)
    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        use_case.execute(company)
