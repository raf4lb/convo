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
from src.domain.repositories.company_repository import ICompanyRepository
from src.domain.repositories.user_repository import IUserRepository
from src.web.controllers.interfaces import IUserHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


class CreateUserHttpController(IUserHttpController):
    def __init__(
        self, user_repository: IUserRepository, company_repository: ICompanyRepository
    ):
        super().__init__(user_repository=user_repository)
        self._company_repository = company_repository

    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateUserUseCase(
            user_repository=self._repository,
            company_repository=self._company_repository,
        )
        try:
            user = use_case.execute(
                name=request.body["name"],
                email=request.body["email"],
                type=UserTypes(request.body["type"]),
                company_id=request.body["company_id"],
            )
        except InvalidUserError as e:
            return HttpResponse(
                status_code=StatusCodes.BAD_REQUEST.value,
                body={
                    "errors": e.errors,
                },
            )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "company_id": user.company_id,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            },
        )


class GetUserHttpController(IUserHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetUserUseCase(user_repository=self._repository)
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
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            },
        )


class UpdateUserHttpController(IUserHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = UpdateUserUseCase(user_repository=self._repository)
        try:
            user = use_case.execute(
                user_id=request.path_params["id"],
                name=request.body["name"],
                email=request.body["email"],
                type=UserTypes(request.body["type"]),
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
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            },
        )


class DeleteUserHttpController(IUserHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = DeleteUserUseCase(user_repository=self._repository)
        try:
            use_case.execute(user_id=request.path_params["id"])
        except UserNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "user not found"},
            )
        return HttpResponse(status_code=StatusCodes.NO_CONTENT.value)


class ListUserHttpController(IUserHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = ListUserUseCase(user_repository=self._repository)
        users = use_case.execute()
        data = {
            "results": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "company_id": user.company_id,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                    if user.updated_at
                    else None,
                }
                for user in users
            ]
        }

        return HttpResponse(status_code=StatusCodes.OK.value, body=data)
