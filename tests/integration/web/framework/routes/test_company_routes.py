import pytest

from src.domain.errors import CompanyNotFoundError
from src.web.http_types import StatusCodes


def test_list_companies(
    client,
    company_factory,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository
    _ = [company_factory() for _ in range(3)]

    # Act
    response = client.get("/companies/")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert len(response.json().get("results")) == len(company_repository.get_all())


def test_create_company(
    client,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository
    company_name = "Test Company"
    company_email = "new@example.com"
    company_phone = "123456789"
    data = {"name": company_name, "email": company_email, "phone": company_phone}

    # Act
    response = client.post("/companies/", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    created_company = response.json()
    created_id = created_company.get("id")
    fetched_company = company_repository.get_by_id(company_id=created_id)

    assert fetched_company.name == company_name
    assert fetched_company.email == company_email
    assert fetched_company.phone == company_phone


def test_get_company(
    client,
    company,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository

    # Act
    response = client.get(f"/companies/{company.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json().get("name") == company.name


def test_update_company(
    client,
    company,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository
    new_company_name = "New Company Company"
    new_company_email = "new@example.com"
    new_company_phone = "123456789"
    data = {
        "name": new_company_name,
        "email": new_company_email,
        "phone": new_company_phone,
    }

    # Act
    response = client.patch(f"/companies/{company.id}", json=data)

    # Assert
    assert response.status_code == StatusCodes.OK.value
    fetched_company = company_repository.get_by_id(
        company_id=company.id,
    )
    assert fetched_company.name == new_company_name
    assert fetched_company.email == new_company_email
    assert fetched_company.phone == new_company_phone


def test_delete_company(
    client,
    company,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository

    # Act
    response = client.delete(f"/companies/{company.id}")

    # Assert
    assert response.status_code == StatusCodes.NO_CONTENT.value
    with pytest.raises(CompanyNotFoundError):
        company_repository.get_by_id(
            company_id=company.id,
        )


def test_company_not_found(
    client,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository

    # Act
    response = client.get("/companies/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_delete_non_existing_company(
    client,
    company_repository,
):
    # Arrange
    client.app.state.company_repository = company_repository

    # Act
    response = client.delete("/companies/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value
    assert response.json().get("detail") == "company not found"
