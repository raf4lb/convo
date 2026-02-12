from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from src.web.controllers.message_controllers import ReceiveMessageHttpController
from src.web.controllers.webhook_controllers import (
    VerifyWebhookHttpController,
)
from src.web.framework.adapter import request_adapter

webhook_routes = APIRouter(prefix="/webhook")


@webhook_routes.get("/")
async def verify(request: Request):
    controller = VerifyWebhookHttpController(
        verify_token=request.app.state.settings.WEBHOOK_VERIFY_TOKEN
    )
    response = controller.handle(request=await request_adapter(request))
    return PlainTextResponse(content=response.body, status_code=response.status_code)


@webhook_routes.post("/")
async def receive_messages(request: Request):
    message_repository = request.app.state.message_repository
    contact_repository = request.app.state.contact_repository
    chat_repository = request.app.state.chat_repository
    connection_manager = request.app.state.connection_manager

    controller = ReceiveMessageHttpController(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )
    response = controller.handle(request=await request_adapter(request))
    # TODO: fix dual write problem
    # Broadcast message to WebSocket clients if successfully created
    if response.status_code == 201 and "message_id" in response.body:
        message_id = response.body["message_id"]
        # Fetch the created message to get full details
        message = message_repository.get_by_id(message_id)
        if message:
            # Format message for WebSocket broadcast
            broadcast_data = {
                "conversationId": message.chat_id,
                "id": message.id,
                "text": message.text,
                "timestamp": message.external_timestamp.isoformat(),
                "sender": "customer" if message.is_from_contact() else "user",
            }
            await connection_manager.broadcast_message(broadcast_data)

    return JSONResponse(content=response.body, status_code=response.status_code)
