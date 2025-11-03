import pytest

from src.application.use_cases.company_use_cases import (
    CreateCompanyUseCase,
    DeleteCompanyUseCase,
    GetCompanyUseCase,
    ListCompanyUseCase,
    UpdateCompanyUseCase,
)
from src.domain.errors import CompanyNotFoundError


def test_list_company_use_case(company, company_repository):
    # Arrange
    company_repository.save(company)

    # Act
    use_case = ListCompanyUseCase(company_repository=company_repository)
    companies = use_case.execute()

    # Assert
    assert companies == [company]


def test_create_company_use_case(company_repository):
    # Arrange
    name = "Test Company"
    use_case = CreateCompanyUseCase(company_repository=company_repository)

    # Act
    company = use_case.execute(name)

    # Assert
    assert company_repository.get_by_id(company.id) is not None


def test_get_company_use_case(company, company_repository):
    # Arrange
    company_repository.save(company)

    # Act
    use_case = GetCompanyUseCase(company_repository=company_repository)
    fetched_company = use_case.execute(company_id=company.id)

    # Assert
    assert fetched_company.id == company.id


def test_update_company_use_case_existing_company(company, company_repository):
    # Arrange
    company_repository.save(company)
    use_case = UpdateCompanyUseCase(company_repository=company_repository)

    # Act
    new_name = "New Name"
    company = use_case.execute(company.id, new_name)

    # Assert
    assert company.name == new_name


def test_update_company_use_case_non_existing_company(company_repository):
    # Arrange
    use_case = UpdateCompanyUseCase(company_repository=company_repository)

    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        use_case.execute("company.id", "New Name")


def test_delete_company_use_case(company, company_repository):
    # Arrange
    company_repository.save(company)
    use_case = DeleteCompanyUseCase(company_repository=company_repository)

    # Act
    use_case.execute(company.id)

    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        company_repository.get_by_id(company.id)
