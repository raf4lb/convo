from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.helpers.helpers import generate_uuid4


def test_validate_user_valid_user():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id=None,
    )

    # Act
    errors = user.validate()

    # Assert
    assert not errors


def test_validate_user_invalid_id():
    # Arrange
    user = User(
        id="invalid_id",
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id=None,
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid id"


def test_validate_user_invalid_company_id():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id="invalid_id",
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid company id"


def test_validate_user_invalid_name():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name=1,
        email="email@test.com",
        company_id=generate_uuid4(),
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid name"


def test_validate_user_invalid_email():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email=12,
        company_id=generate_uuid4(),
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid email"


def test_validate_user_invalid_type():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type="invalid_type",
        name="Test User",
        email="email@test.com",
        company_id=generate_uuid4(),
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid user type"


def test_validate_user_invalid_created_at():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id=generate_uuid4(),
        created_at=10,
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid created at"


def test_validate_user_invalid_updated_at():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id=generate_uuid4(),
        updated_at=10,
    )

    # Act
    errors = user.validate()

    # Assert
    assert errors[0] == "invalid updated at"


def test_validate_user_invalid_is_active():
    # Arrange
    user = User(
        id=generate_uuid4(),
        type=UserTypes.ADMINISTRATOR,
        name="Test User",
        email="email@test.com",
        company_id=generate_uuid4(),
        is_active="not a bool",
    )

    # Act
    errors = user.validate()

    # Assert
    assert "invalid is_active" in errors
