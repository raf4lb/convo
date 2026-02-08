from datetime import UTC, datetime, timedelta

import jwt

from src.infrastructure.settings import AppSettings


class JWTService:
    """Service for creating and verifying JWT tokens."""

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def create_access_token(self, user_id: str) -> str:
        """Create a JWT access token."""
        expires_delta = timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": user_id,
            "exp": expire,
            "type": "access",
        }

        return jwt.encode(
            payload,
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def create_refresh_token(self, user_id: str) -> str:
        """Create a JWT refresh token."""
        expires_delta = timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)
        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": user_id,
            "exp": expire,
            "type": "refresh",
        }

        return jwt.encode(
            payload,
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def verify_token(self, token: str, token_type: str = "access") -> dict:
        """
        Verify and decode a JWT token.

        Args:
            token: The JWT token to verify
            token_type: Expected token type ("access" or "refresh")

        Returns:
            The decoded payload

        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
            ValueError: If token type doesn't match expected type
        """
        payload = jwt.decode(
            token,
            self.settings.JWT_SECRET,
            algorithms=[self.settings.JWT_ALGORITHM],
        )

        if payload.get("type") != token_type:
            raise ValueError(f"Invalid token type. Expected {token_type}")

        return payload
