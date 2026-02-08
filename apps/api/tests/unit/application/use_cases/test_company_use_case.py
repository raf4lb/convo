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
    assert company in companies


def test_create_company_use_case(company_repository):
    # Arrange
    name = "Test Company"
    email = "new@example.com"
    phone = "123456789"
    use_case = CreateCompanyUseCase(company_repository=company_repository)

    # Act
    company = use_case.execute(name=name, email=email, phone=phone)

    # Assert
    persisted_company = company_repository.get_by_id(company.id)
    assert persisted_company is not None
    assert persisted_company.name == name
    assert persisted_company.email == email
    assert persisted_company.phone == phone
    assert persisted_company.is_active is True
    assert persisted_company.attendant_sees_all_conversations is True


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
    new_email = "new@example.com"
    new_phone = "123456789"
    company = use_case.execute(company.id, new_name, new_email, new_phone)

    # Assert
    assert company.name == new_name
    assert company.email == new_email
    assert company.phone == new_phone


def test_update_company_use_case_non_existing_company(company_repository):
    # Arrange
    use_case = UpdateCompanyUseCase(company_repository=company_repository)
    non_existing_id = "non-existent-id"
    company_name = "New Name"
    company_email = "new@example.com"
    company_phone = "123456789"

    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        use_case.execute(
            company_id=non_existing_id,
            name=company_name,
            email=company_email,
            phone=company_phone,
        )


def test_delete_company_use_case(company, company_repository):
    # Arrange
    company_repository.save(company)
    use_case = DeleteCompanyUseCase(company_repository=company_repository)

    # Act
    use_case.execute(company.id)

    # Act/Assert
    with pytest.raises(CompanyNotFoundError):
        company_repository.get_by_id(company.id)
