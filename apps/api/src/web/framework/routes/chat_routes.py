from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.web.controllers.chat_controllers import (
    AssignAttendantToChatHttpController,
    GetChatHttpController,
    GetChatMessagesHttpController,
    GetChatsByAttendantHttpController,
    GetPendingChatsHttpController,
    GetResolvedChatsHttpController,
    GetUnassignedChatsHttpController,
    ListChatsByCompanyHttpController,
    MarkChatAsReadHttpController,
    SearchChatsHttpController,
    SendMessageHttpController,
)
from src.web.framework.adapter import request_adapter

chat_routes = APIRouter(prefix="/chats")


@chat_routes.get("/")
async def list_company_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = ListChatsByCompanyHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/unassigned")
async def get_unassigned_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = GetUnassignedChatsHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/pending")
async def get_pending_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = GetPendingChatsHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/resolved")
async def get_resolved_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = GetResolvedChatsHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/by-attendant")
async def get_chats_by_attendant(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = GetChatsByAttendantHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/search")
async def search_chats(request: Request) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = SearchChatsHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/{chat_id}")
async def get_chat(request: Request, chat_id: str) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = GetChatHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.patch("/{chat_id}/assign")
async def assign_attendant_to_chat(request: Request, chat_id: str) -> JSONResponse:
    repository = request.app.state.chat_repository
    controller = AssignAttendantToChatHttpController(chat_repository=repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.get("/{chat_id}/messages")
async def get_chat_messages(request: Request, chat_id: str) -> JSONResponse:
    message_repository = request.app.state.message_repository
    controller = GetChatMessagesHttpController(message_repository=message_repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.post("/{chat_id}/messages")
async def send_message(request: Request, chat_id: str) -> JSONResponse:
    message_repository = request.app.state.message_repository
    user_repository = request.app.state.user_repository
    connection_manager = request.app.state.connection_manager
    controller = SendMessageHttpController(message_repository=message_repository)
    response = controller.handle(request=await request_adapter(request))
    # TODO: fix dual-write problem
    # Broadcast message to WebSocket clients if successfully created
    if response.status_code == 201 and "id" in response.body:
        message_id = response.body["id"]
        # Fetch the created message to get full details
        message = message_repository.get_by_id(message_id)
        if message:
            # Send ISO timestamp for client-side formatting
            timestamp_str = message.external_timestamp.isoformat()

            # Build base broadcast data
            broadcast_data = {
                "conversationId": message.chat_id,
                "id": message.id,
                "text": message.text,
                "timestamp": timestamp_str,
                "sender": "customer" if message.is_from_contact() else "attendant",
            }

            # Add attendant name if message is from user
            if message.sent_by_user_id:
                user = user_repository.get_by_id(message.sent_by_user_id)
                if user:
                    broadcast_data["attendantName"] = user.name

            await connection_manager.broadcast_message(broadcast_data)

    return JSONResponse(content=response.body, status_code=response.status_code)


@chat_routes.patch("/{chat_id}/read")
async def mark_chat_as_read(request: Request, chat_id: str) -> JSONResponse:
    message_repository = request.app.state.message_repository
    controller = MarkChatAsReadHttpController(message_repository=message_repository)
    response = controller.handle(request=await request_adapter(request))
    return JSONResponse(content=response.body, status_code=response.status_code)
