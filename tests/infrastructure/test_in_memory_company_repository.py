import pytest

from src.application.exceptions import CompanyNotFoundError


def test_create_company(company, company_repository):
    # Act
    company_repository.create_company(company)
    # Assert
    assert company.id in {company.id for company in company_repository.get_companies()}


def test_updating_existing_company(company, company_repository):
    # Arrange
    company_repository.create_company(company)
    # Act
    company.name = "new name"
    company_repository.update_company(company)
    # Assert
    company = company_repository.get_company_by_id(company.id)
    assert company.name == "new name"


def test_updating_non_existing_user(company, company_repository):
    # Act
    company.name = "new name"
    # Assert
    with pytest.raises(CompanyNotFoundError):
        company_repository.update_company(company)
