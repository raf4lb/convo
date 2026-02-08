from dataclasses import dataclass

from src.domain.entities.user import User
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.security.jwt_service import JWTService
from src.infrastructure.security.password_service import (
    hash_password,
    validate_password,
    verify_password,
)


@dataclass
class LoginResult:
    access_token: str
    refresh_token: str
    user: User


class LoginUseCase:
    """Authenticate user with email and password."""

    def __init__(
        self, user_repository: IUserRepository, jwt_service: JWTService
    ) -> None:
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> LoginResult:
        """
        Verify credentials and return tokens.

        Raises:
            UserNotFoundError: If user doesn't exist
            ValueError: If password is incorrect or user has no password
        """
        try:
            user = self.user_repository.get_by_email(email=email)
        except UserNotFoundError:
            raise ValueError("Invalid email or password")

        if not user.has_password():
            raise ValueError("User has no password set. Please use password reset.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        access_token = self.jwt_service.create_access_token(user_id=user.id)
        refresh_token = self.jwt_service.create_refresh_token(user_id=user.id)

        return LoginResult(
            access_token=access_token, refresh_token=refresh_token, user=user
        )


class RefreshTokenUseCase:
    """Generate new access token from refresh token."""

    def __init__(
        self, user_repository: IUserRepository, jwt_service: JWTService
    ) -> None:
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    def execute(self, refresh_token: str) -> str:
        """
        Validate refresh token and return new access token.

        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
            ValueError: If token type is wrong
            UserNotFoundError: If user doesn't exist
        """
        payload = self.jwt_service.verify_token(refresh_token, token_type="refresh")
        user_id = payload["sub"]

        user = self.user_repository.get_by_id(user_id=user_id)

        if not user.is_active:
            raise ValueError("User account is inactive")

        return self.jwt_service.create_access_token(user_id=user.id)


class SetPasswordUseCase:
    """Set or update user password."""

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, user_id: str, password: str) -> User:
        """
        Set user password after validation.

        Raises:
            UserNotFoundError: If user doesn't exist
            ValueError: If password doesn't meet requirements
        """
        user = self.user_repository.get_by_id(user_id=user_id)

        validation_errors = validate_password(password)
        if validation_errors:
            raise ValueError("; ".join(validation_errors))

        password_hash = hash_password(password)

        # Update only the password, not other user fields
        self.user_repository.update_password(
            user_id=user.id, password_hash=password_hash
        )

        # Return the user (password_hash won't be included since get_by_id doesn't return it)
        return self.user_repository.get_by_id(user_id=user.id)
