from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.message_controllers import (
    GetMessageHttpController,
    ReceiveMessageHttpController,
)
from src.web.framework.adapter import request_adapter

message_routes = APIRouter(prefix="/messages")


@message_routes.post("/receive")
async def receive_message(request: Request) -> JSONResponse:
    message_repository = request.app.state.message_repository
    contact_repository = request.app.state.contact_repository
    chat_repository = request.app.state.chat_repository
    controller = ReceiveMessageHttpController(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@message_routes.get("/{id}")
async def get_message(request: Request, id: str) -> JSONResponse:
    repository = request.app.state.message_repository
    controller = GetMessageHttpController(message_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
