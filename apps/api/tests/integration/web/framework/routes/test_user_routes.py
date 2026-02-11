import pytest

from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError
from src.web.http_types import StatusCodes


def test_list_users_endpoint(
    client,
    company,
    user_factory,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    users = [user_factory() for _ in range(3)]

    # Act
    response = client.get(f"/users/?company_id={company.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert len(response.json().get("results")) == len(users)


def test_create_user_endpoint(
    client,
    user_repository,
    company_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    client.app.state.company_repository = company_repository
    name = "Test User"
    email = "email@test.com"
    _type = UserTypes.STAFF.value
    data = {
        "name": name,
        "email": email,
        "type": _type,
        "company_id": None,
    }

    # Act
    response = client.post("/users/", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    created_user = response.json()
    fetched_user = user_repository.get_by_id(
        user_id=created_user.get("id"),
    )
    assert fetched_user.name == name


def test_get_user_endpoint(
    client,
    staff_user,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.get(f"/users/{staff_user.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json().get("name") == staff_user.name


def test_update_user_endpoint(
    client,
    staff_user,
    user_repository,
    company_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    client.app.state.company_repository = company_repository
    new_user_name = "New User Name"
    data = {
        "name": new_user_name,
        "email": staff_user.email,
        "type": staff_user.type.value,
        "company_id": staff_user.company_id,
    }

    # Act
    response = client.put(f"/users/{staff_user.id}", json=data)

    # Assert
    assert response.status_code == StatusCodes.OK.value
    fetched_user = user_repository.get_by_id(
        user_id=staff_user.id,
    )
    assert fetched_user.name == new_user_name


def test_delete_user_endpoint(
    client,
    staff_user,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.delete(f"/users/{staff_user.id}")

    # Assert
    assert response.status_code == StatusCodes.NO_CONTENT.value
    with pytest.raises(UserNotFoundError):
        user_repository.get_by_id(
            user_id=staff_user.id,
        )


def test_user_endpoint_not_found(
    client,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.get("/users/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_update_user_endpoint_non_existing_user(
    client,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    data = {
        "name": "Test User",
        "email": "email@test.com",
        "type": UserTypes.STAFF.value,
        "company_id": "company_id",
    }

    # Act
    response = client.put("/users/invalid_id", json=data)

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_create_user_endpoint_invalid_data(
    client,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    data = {
        "name": 10,
        "email": "email@test.com",
        "type": UserTypes.STAFF.value,
        "company_id": "company_id",
    }

    # Act
    response = client.post("/users/", json=data)

    # Assert
    assert response.status_code == StatusCodes.BAD_REQUEST.value
    assert set(response.json().get("errors")) == {"invalid name", "invalid company id"}


def test_delete_user_endpoint_non_existing_user(
    client,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.delete("/users/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value
    assert response.json().get("detail") == "user not found"


def test_create_user_with_is_active_false(
    client,
    user_repository,
    company_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    client.app.state.company_repository = company_repository
    data = {
        "name": "Inactive User",
        "email": "inactive@test.com",
        "type": UserTypes.STAFF.value,
        "company_id": None,
        "is_active": False,
    }

    # Act
    response = client.post("/users/", json=data)

    # Assert
    assert response.status_code == StatusCodes.CREATED.value
    created_user = response.json()
    assert created_user.get("is_active") is False
    fetched_user = user_repository.get_by_id(user_id=created_user.get("id"))
    assert fetched_user.is_active is False


def test_get_user_includes_is_active(
    client,
    staff_user,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.get(f"/users/{staff_user.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    user_data = response.json()
    assert "is_active" in user_data
    assert user_data.get("is_active") is True


def test_update_user_is_active(
    client,
    staff_user,
    user_repository,
    company_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    client.app.state.company_repository = company_repository
    data = {
        "name": staff_user.name,
        "email": staff_user.email,
        "type": staff_user.type.value,
        "is_active": False,
    }

    # Act
    response = client.put(f"/users/{staff_user.id}", json=data)

    # Assert
    assert response.status_code == StatusCodes.OK.value
    updated_user = response.json()
    assert updated_user.get("is_active") is False
    fetched_user = user_repository.get_by_id(user_id=staff_user.id)
    assert fetched_user.is_active is False


def test_list_users_includes_is_active(
    client,
    company,
    user_factory,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    user_factory(is_active=True)
    user_factory(is_active=False)

    # Act
    response = client.get(f"/users/?company_id={company.id}")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    results = response.json().get("results")
    assert len(results) == 2
    for user in results:
        assert "is_active" in user
