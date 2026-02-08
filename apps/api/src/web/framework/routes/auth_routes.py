from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,
    SetPasswordUseCase,
)
from src.web.controllers.auth_controllers import (
    GetCurrentUserHttpController,
    LoginHttpController,
    LogoutHttpController,
    RefreshTokenHttpController,
    SetPasswordHttpController,
)
from src.web.framework.adapter import request_adapter

auth_routes = APIRouter(prefix="/auth")


@auth_routes.post("/login")
async def login(request: Request) -> JSONResponse:
    jwt_service = request.app.state.jwt_service
    user_repository = request.app.state.user_repository

    login_use_case = LoginUseCase(
        user_repository=user_repository, jwt_service=jwt_service
    )
    controller = LoginHttpController(login_use_case=login_use_case)
    response = controller.handle(request=await request_adapter(request))

    json_response = JSONResponse(
        content=response.body, status_code=response.status_code
    )

    if response.status_code == 200:
        settings = request.app.state.settings
        access_token = response.body.get("access_token")
        refresh_token = response.body.get("refresh_token")

        json_response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite="strict",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        json_response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

    return json_response


@auth_routes.post("/refresh")
async def refresh_token(request: Request) -> JSONResponse:
    jwt_service = request.app.state.jwt_service
    user_repository = request.app.state.user_repository

    refresh_token_use_case = RefreshTokenUseCase(
        user_repository=user_repository, jwt_service=jwt_service
    )
    controller = RefreshTokenHttpController(
        refresh_token_use_case=refresh_token_use_case
    )
    response = controller.handle(request=await request_adapter(request))

    json_response = JSONResponse(
        content=response.body, status_code=response.status_code
    )

    if response.status_code == 200:
        settings = request.app.state.settings
        access_token = response.body.get("access_token")

        json_response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite="strict",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    return json_response


@auth_routes.post("/logout")
async def logout(request: Request) -> JSONResponse:
    controller = LogoutHttpController()
    response = controller.handle(request=await request_adapter(request))

    json_response = JSONResponse(
        content=response.body, status_code=response.status_code
    )

    json_response.delete_cookie(key="access_token")
    json_response.delete_cookie(key="refresh_token")

    return json_response


@auth_routes.get("/me")
async def get_current_user(request: Request) -> JSONResponse:
    controller = GetCurrentUserHttpController()
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@auth_routes.post("/set-password")
async def set_password(request: Request) -> JSONResponse:
    user_repository = request.app.state.user_repository

    set_password_use_case = SetPasswordUseCase(user_repository=user_repository)
    controller = SetPasswordHttpController(set_password_use_case=set_password_use_case)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
