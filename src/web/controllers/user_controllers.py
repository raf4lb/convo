from src.application.use_cases.user.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)
from src.domain.errors import UserNotFoundError
from src.domain.repositories.user_repository import IUserRepository
from src.web.controllers.http_types import HttpRequest, HttpResponse, StatusCodes


class UserController:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository


class CreateUserHTTPController(UserController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateUserUseCase(repository=self._repository)
        user = use_case.execute(
            name=request.body["name"],
            email=request.body["email"],
            type=request.body["type"],
            company_id=request.body["company_id"],
        )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "company_id": user.company_id,
            },
        )


class GetUserHTTPController(UserController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetUserUseCase(repository=self._repository)
        try:
            user = use_case.execute(user_id=request.path_params["id"])
        except UserNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "user not found"},
            )
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "company_id": user.company_id,
            },
        )


class UpdateUserHTTPController(UserController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = UpdateUserUseCase(repository=self._repository)
        try:
            user = use_case.execute(
                user_id=request.path_params["id"],
                name=request.body["name"],
                email=request.body["email"],
                type=request.body["type"],
                company_id=request.body["company_id"],
            )
        except UserNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "user not found"},
            )
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "company_id": user.company_id,
            },
        )


class DeleteUserHTTPController(UserController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = DeleteUserUseCase(repository=self._repository)
        try:
            use_case.execute(user_id=request.path_params["id"])
        except UserNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "user not found"},
            )
        return HttpResponse(status_code=StatusCodes.NO_CONTENT.value)
