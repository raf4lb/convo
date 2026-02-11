from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.chat_controllers import (
    ListChatsByCompanyHttpController,
    MarkChatAsReadHttpController,
)
from src.web.framework.adapter import request_adapter

chat_routes = APIRouter(prefix="/chats")


@chat_routes.get("/")
async def list_company_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = ListChatsByCompanyHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.patch("/{chat_id}/read")
async def mark_chat_as_read(request: Request, chat_id: str) -> JSONResponse:
    message_repository = request.app.state.message_repository
    controller = MarkChatAsReadHttpController(message_repository=message_repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
