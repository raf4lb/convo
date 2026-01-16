from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.contact_controllers import (
    CreateCompanyContactHttpController,
    GetCompanyContactsHttpController,
    GetContactHttpController,
)
from src.web.framework.adapter import request_adapter

contact_routes = APIRouter(prefix="/contacts")


@contact_routes.post("/")
async def create_company_contact(request: Request) -> JSONResponse:
    repository = request.app.state.contact_repository
    controller = CreateCompanyContactHttpController(contact_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@contact_routes.get("/{id}")
async def get_contact(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.contact_repository
    controller = GetContactHttpController(contact_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@contact_routes.get("/company/{company_id}")
async def get_company_contacts(request: Request, company_id: str) -> JSONResponse:
    repository = request.app.state.contact_repository
    controller = GetCompanyContactsHttpController(contact_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
