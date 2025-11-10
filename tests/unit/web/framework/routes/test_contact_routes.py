from src.web.controllers.http_types import StatusCodes
from src.web.framework.routes.contact_routes import contact_route_blueprint


def test_create_company_contact(
    app,
    client,
    company,
    contact_repository,
):
    # Arrange
    app.config["contact_repository"] = contact_repository
    app.register_blueprint(contact_route_blueprint, url_prefix="/contacts")
    phone_number = "5588999999999"
    contact_name = "Test Contact"
    data = {
        "company_id": company.id,
        "name": contact_name,
        "phone_number": phone_number,
    }

    # Act
    response = client.post("/contacts/", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    fetched_contact = contact_repository.get_company_contact_by_phone_number(
        phone_number=phone_number,
        company_id=company.id,
    )
    assert fetched_contact.name == contact_name


def test_get_contact(
    app,
    client,
    contact,
    contact_repository,
):
    # Arrange
    app.config["contact_repository"] = contact_repository
    app.register_blueprint(contact_route_blueprint, url_prefix="/contacts")

    # Act
    response = client.get(f"/contacts/{contact.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json.get("name") == contact.name
