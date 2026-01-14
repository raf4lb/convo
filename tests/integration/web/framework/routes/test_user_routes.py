import pytest

from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError
from src.web.http_types import StatusCodes


def test_list_users(
    client,
    user_factory,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
    users = [user_factory() for _ in range(3)]

    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert len(response.json().get("results")) == len(users)


def test_create_user(
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


def test_get_user(
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


def test_update_user(
    client,
    staff_user,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository
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


def test_delete_user(
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


def test_user_not_found(
    client,
    user_repository,
):
    # Arrange
    client.app.state.user_repository = user_repository

    # Act
    response = client.get("/users/invalid_id")

    # Assert
    assert response.status_code == StatusCodes.NOT_FOUND.value


def test_update_non_existing_user(
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


def test_create_user_invalid_data(
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


def test_delete_non_existing_user(
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
