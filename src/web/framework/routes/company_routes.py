from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.company_controllers import (
    CreateCompanyHttpController,
    DeleteCompanyHttpController,
    GetCompanyHttpController,
    ListCompanyHttpController,
    UpdateCompanyHttpController,
)
from src.web.framework.adapter import request_adapter

company_routes = APIRouter(prefix="/companies")


@company_routes.get("/")
async def list_companies(request: Request) -> JSONResponse:
    repository = request.app.state.company_repository
    controller = ListCompanyHttpController(company_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@company_routes.post("/")
async def create_company(request: Request) -> JSONResponse:
    repository = request.app.state.company_repository
    controller = CreateCompanyHttpController(company_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@company_routes.get("/{id}")
async def get_company(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.company_repository
    controller = GetCompanyHttpController(company_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@company_routes.put("/{id}")
async def update_company(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.company_repository
    controller = UpdateCompanyHttpController(company_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@company_routes.delete("/{id}")
async def delete_company(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.company_repository
    controller = DeleteCompanyHttpController(company_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
