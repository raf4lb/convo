from src.web.http_types import StatusCodes


def test_create_company_contact_endpoint(
    client,
    company,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository
    phone_number = "5588999999999"
    contact_name = "Test Contact"
    contact_email = "test@contact.com"
    data = {
        "company_id": company.id,
        "name": contact_name,
        "phone_number": phone_number,
        "email": contact_email,
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


def test_get_contact_endpoint(
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


def test_get_contact_endpoint_not_found(
    client,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository

    # Act
    response = client.get("/contacts/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_get_company_contacts_endpoint(
    client,
    company,
    contact_factory,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository
    contact_factory(name="Contact 1", company_id=company.id)
    contact_factory(name="Contact 2", company_id=company.id)
    contact_factory(name="Contact 3", company_id=company.id)

    # Act
    response = client.get(f"/contacts/company/{company.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    data = response.json().get("results")
    assert len(data) == 3
    assert any(c["name"] == "Contact 1" for c in data)


def test_get_company_contact_by_phone_endpoint(
    client,
    contact,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository
    url = f"/contacts/company/{contact.company_id}/phone/{contact.phone_number}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["phone_number"] == contact.phone_number
    assert data["company_id"] == contact.company_id
    assert data["id"] == contact.id


def test_get_company_contact_by_phone_endpoint_not_found(client, company):
    # Arrange
    phone_number = "5511999999999"
    url = f"/contacts/company/{company.id}/phone/{phone_number}"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "contact not found"}


def test_search_company_contacts_endpoint(
    client,
    company,
    contact_factory,
    contact_repository,
):
    # Arrange
    client.app.state.contact_repository = contact_repository
    contact_factory(
        name="John Doe",
        phone_number="123456789",
        email="john@example.com",
        company_id=company.id,
    )
    contact_factory(
        name="Jane Smith",
        phone_number="987654321",
        email="jane@example.com",
        company_id=company.id,
    )

    contact_factory(
        name="Alice Brown",
        phone_number="555555555",
        email="alice@other.com",
        company_id=company.id,
    )
    # Different company
    contact_factory(
        name="John Other",
        phone_number="111111111",
        company_id="other_company",
    )
    url = "/contacts/search/"

    # Act - Search by name (case-insensitive)
    query_params = {
        "company_id": company.id,
        "query": "JOHN",
    }
    response_name = client.get(url, params=query_params)

    # # Act - Search by phone
    query_params = {
        "company_id": company.id,
        "query": "9876",
    }
    response_phone = client.get(url, params=query_params)

    # # Act - Search by email
    query_params = {
        "company_id": company.id,
        "query": "EXAMPLE",
    }
    response_email = client.get(url, params=query_params)

    # Assert
    assert response_name.status_code == StatusCodes.OK.value
    results_name = response_name.json().get("results")
    assert len(results_name) == 1
    assert results_name[0].get("name") == "John Doe"

    assert response_phone.status_code == StatusCodes.OK.value
    results_phone = response_phone.json().get("results")
    assert len(results_phone) == 1
    assert results_phone[0].get("name") == "Jane Smith"

    assert response_email.status_code == StatusCodes.OK.value
    results_email = response_email.json().get("results")
    assert len(results_email) == 2
    assert any(c.get("name") == "John Doe" for c in results_email)
    assert any(c.get("name") == "Jane Smith" for c in results_email)
