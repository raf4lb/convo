import jwt
from fastapi import Request

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.security.jwt_service import JWTService


async def get_current_user(request: Request) -> User | None:
    """
    Extract and verify JWT from cookies, return current user.

    Returns None if token is missing, invalid, or user not found.
    """
    access_token = request.cookies.get("access_token")

    if not access_token:
        return None

    try:
        jwt_service: JWTService = request.app.state.jwt_service
        user_repository: IUserRepository = request.app.state.user_repository

        payload = jwt_service.verify_token(access_token, token_type="access")
        user_id = payload["sub"]

        user = user_repository.get_by_id(user_id=user_id)

        if not user.is_active:
            return None

        return user

    except (jwt.InvalidTokenError, ValueError, Exception):
        return None


async def auth_middleware(request: Request, call_next):
    """
    Middleware to extract current user from JWT and attach to request state.
    """
    user = await get_current_user(request)

    if user:
        request.state.current_user = user

    response = await call_next(request)
    return response
