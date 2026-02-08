from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.user_controllers import (
    CreateUserHttpController,
    DeleteUserHttpController,
    GetUserHttpController,
    ListUserHttpController,
    UpdateUserHttpController,
)
from src.web.framework.adapter import request_adapter

user_routes = APIRouter(prefix="/users")


@user_routes.get("/")
async def list_users(request: Request) -> JSONResponse:
    repository = request.app.state.user_repository
    controller = ListUserHttpController(user_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@user_routes.post("/")
async def create_user(request: Request) -> JSONResponse:
    user_repository = request.app.state.user_repository
    company_repository = request.app.state.company_repository
    controller = CreateUserHttpController(
        user_repository=user_repository,
        company_repository=company_repository,
    )
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@user_routes.get("/{id}")
async def get_user(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.user_repository
    controller = GetUserHttpController(user_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@user_routes.put("/{id}")
async def update_user(request: Request, id: str) -> JSONResponse:
    user_repository = request.app.state.user_repository
    company_repository = request.app.state.company_repository
    controller = UpdateUserHttpController(
        user_repository=user_repository,
        company_repository=company_repository,
    )
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@user_routes.delete("/{id}")
async def delete_user(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.user_repository
    controller = DeleteUserHttpController(user_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
