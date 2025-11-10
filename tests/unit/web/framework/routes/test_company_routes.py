import pytest

from src.domain.errors import CompanyNotFoundError
from src.web.controllers.http_types import StatusCodes
from src.web.framework.routes.company_routes import company_route_blueprint


def test_list_companies(
    app,
    client,
    company_factory,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")
    companies = [company_factory() for _ in range(3)]

    # Act
    response = client.get("/companies/")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert len(response.json.get("companies")) == len(companies)


def test_create_company(
    app,
    client,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")
    company_name = "Test Company"
    data = {"name": company_name}

    # Act
    response = client.post("/companies/", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    created_company = response.json
    fetched_company = company_repository.get_by_id(
        company_id=created_company.get("id"),
    )
    assert fetched_company.name == company_name


def test_get_company(
    app,
    client,
    company,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")

    # Act
    response = client.get(f"/companies/{company.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json.get("name") == company.name


def test_update_company(
    app,
    client,
    company,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")
    new_company_name = "New Company Name"
    data = {"name": new_company_name}

    # Act
    response = client.put(f"/companies/{company.id}", json=data)

    # Assert
    assert response.status_code == StatusCodes.OK.value
    fetched_company = company_repository.get_by_id(
        company_id=company.id,
    )
    assert fetched_company.name == new_company_name


def test_delete_company(
    app,
    client,
    company,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")

    # Act
    response = client.delete(f"/companies/{company.id}")

    # Assert
    assert response.status_code == StatusCodes.NO_CONTENT.value
    with pytest.raises(CompanyNotFoundError):
        company_repository.get_by_id(
            company_id=company.id,
        )


def test_company_not_found(
    app,
    client,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")

    # Act
    response = client.get("/companies/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_delete_non_existing_company(
    app,
    client,
    company_repository,
):
    # Arrange
    app.config["company_repository"] = company_repository
    app.register_blueprint(company_route_blueprint, url_prefix="/companies")

    # Act
    response = client.delete("/companies/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value
    assert response.json.get("detail") == "company not found"
