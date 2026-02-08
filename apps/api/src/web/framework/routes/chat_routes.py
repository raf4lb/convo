from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.chat_controllers import ListChatsByCompanyHttpController
from src.web.framework.adapter import request_adapter

chat_routes = APIRouter(prefix="/chats")


@chat_routes.get("/")
async def list_company_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = ListChatsByCompanyHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
