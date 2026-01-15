import pytest

from src.application.exceptions import InvalidUserError
from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUserUseCase,
    UpdateUserUseCase,
)
from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError
from src.helpers.helpers import generate_uuid4


def test_create_user_use_case_with_company(
    company, user_repository, company_repository
):
    # Arrange
    name = "Test User"
    email = "email@test.com"
    type = UserTypes.STAFF
    use_case = CreateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act
    user = use_case.execute(
        name=name,
        email=email,
        type=type,
        company_id=company.id,
    )

    # Assert
    assert user_repository.get_by_id(user.id) is not None


def test_create_user_use_case_without_company(user_repository, company_repository):
    # Arrange
    name = "Test User"
    email = "email@test.com"
    type = UserTypes.STAFF
    use_case = CreateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act
    user = use_case.execute(
        name=name,
        email=email,
        type=type,
    )

    # Assert
    assert user_repository.get_by_id(user.id) is not None


def test_create_user_use_case_invalid_user_data(user_repository, company_repository):
    # Arrange
    name = 10
    email = "email@test.com"
    type = UserTypes.STAFF
    use_case = CreateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act/Assert
    with pytest.raises(InvalidUserError):
        use_case.execute(
            name=name,
            email=email,
            type=type,
            company_id=generate_uuid4(),
        )


def test_create_user_use_case_invalid_company(user_repository, company_repository):
    # Arrange
    name = "Test User"
    email = "email@test.com"
    type = UserTypes.STAFF
    use_case = CreateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act/Assert
    with pytest.raises(InvalidUserError):
        use_case.execute(
            name=name,
            email=email,
            type=type,
            company_id=generate_uuid4(),
        )


def test_get_user_use_case(staff_user, user_repository):
    # Arrange
    use_case = GetUserUseCase(user_repository=user_repository)

    # Act
    fetched_user = use_case.execute(user_id=staff_user.id)

    # Assert
    assert fetched_user.name == staff_user.name


def test_update_user_use_case_existing_user(
    staff_user, user_repository, company_repository
):
    # Arrange
    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act
    new_name = "New Name"
    use_case.execute(
        user_id=staff_user.id,
        name=new_name,
        email=staff_user.email,
        type=staff_user.type,
    )

    # Assert
    user = user_repository.get_by_id(staff_user.id)
    assert user.name == new_name


def test_update_user_use_case_non_existing_user(user_repository, company_repository):
    # Arrange
    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        company_repository=company_repository,
    )

    # Act/Assert
    with pytest.raises(UserNotFoundError):
        use_case.execute(
            user_id="staff_user.id",
            name="New Name",
            email="staff_user.email",
            type=UserTypes.STAFF,
        )


def test_delete_user_use_case(staff_user, user_repository):
    # Arrange
    use_case = DeleteUserUseCase(user_repository=user_repository)

    # Act
    use_case.execute(staff_user.id)

    # Act/Assert
    with pytest.raises(UserNotFoundError):
        user_repository.get_by_id(staff_user.id)


def test_list_user_use_case(user_factory, user_repository):
    # Arrange
    user_factory(name="User 1")
    user_factory(name="User 2")
    use_case = ListUserUseCase(user_repository=user_repository)

    # Act
    users = use_case.execute()

    # Assert
    assert len(users) == 2
