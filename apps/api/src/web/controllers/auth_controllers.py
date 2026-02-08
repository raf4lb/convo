from src.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,
    SetPasswordUseCase,
)
from src.domain.entities.user import User
from src.domain.errors import UserNotFoundError
from src.web.http_types import HttpRequest, HttpResponse


class LoginHttpController:
    """Handle login requests."""

    def __init__(self, login_use_case: LoginUseCase) -> None:
        self.login_use_case = login_use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            body = request.body
            email = body.get("email")
            password = body.get("password")

            if not email or not password:
                return HttpResponse(
                    status_code=400, body={"error": "Email and password are required"}
                )

            result = self.login_use_case.execute(email=email, password=password)

            return HttpResponse(
                status_code=200,
                body={
                    "user": {
                        "id": result.user.id,
                        "name": result.user.name,
                        "email": result.user.email,
                        "type": result.user.type.value,
                        "company_id": result.user.company_id,
                        "is_active": result.user.is_active,
                    },
                    "access_token": result.access_token,
                    "refresh_token": result.refresh_token,
                },
            )
        except (UserNotFoundError, ValueError) as e:
            return HttpResponse(status_code=401, body={"error": str(e)})
        except Exception:
            return HttpResponse(
                status_code=500, body={"error": "Internal server error"}
            )


class RefreshTokenHttpController:
    """Handle token refresh requests."""

    def __init__(self, refresh_token_use_case: RefreshTokenUseCase) -> None:
        self.refresh_token_use_case = refresh_token_use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            refresh_token = request.cookies.get("refresh_token")

            if not refresh_token:
                return HttpResponse(
                    status_code=401, body={"error": "No refresh token provided"}
                )

            access_token = self.refresh_token_use_case.execute(
                refresh_token=refresh_token
            )

            return HttpResponse(
                status_code=200,
                body={"access_token": access_token},
            )
        except Exception:
            return HttpResponse(
                status_code=401, body={"error": "Invalid or expired token"}
            )


class LogoutHttpController:
    """Handle logout requests."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            status_code=200,
            body={"message": "Logged out successfully"},
        )


class GetCurrentUserHttpController:
    """Handle get current user requests."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        user: User = request.context.get("current_user")

        if not user:
            return HttpResponse(status_code=401, body={"error": "Not authenticated"})

        return HttpResponse(
            status_code=200,
            body={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "type": user.type.value,
                "company_id": user.company_id,
                "is_active": user.is_active,
            },
        )


class SetPasswordHttpController:
    """Handle set password requests."""

    def __init__(self, set_password_use_case: SetPasswordUseCase) -> None:
        self.set_password_use_case = set_password_use_case

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            user: User = request.context.get("current_user")

            if not user:
                return HttpResponse(
                    status_code=401, body={"error": "Not authenticated"}
                )

            body = request.body
            password = body.get("password")

            if not password:
                return HttpResponse(
                    status_code=400, body={"error": "Password is required"}
                )

            updated_user = self.set_password_use_case.execute(
                user_id=user.id, password=password
            )

            return HttpResponse(
                status_code=200,
                body={
                    "message": "Password set successfully",
                    "user": {
                        "id": updated_user.id,
                        "name": updated_user.name,
                        "email": updated_user.email,
                    },
                },
            )
        except UserNotFoundError:
            return HttpResponse(status_code=404, body={"error": "User not found"})
        except ValueError as e:
            return HttpResponse(status_code=400, body={"error": str(e)})
        except Exception:
            return HttpResponse(
                status_code=500, body={"error": "Internal server error"}
            )
