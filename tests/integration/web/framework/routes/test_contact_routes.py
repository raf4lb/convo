from src.web.http_types import StatusCodes


def test_create_company_contact(
    client,
    company,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository
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
    client,
    contact,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository

    # Act
    response = client.get(f"/contacts/{contact.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json().get("name") == contact.name


def test_user_not_found(
    client,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository

    # Act
    response = client.get("/contacts/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value
