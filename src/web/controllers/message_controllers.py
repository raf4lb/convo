from datetime import UTC, datetime
from typing import Any

from src.application.exceptions import ReceiverContactDoesNotExistError
from src.application.use_cases.message_use_cases import (
    GetMessageUseCase,
    ReceiveMessageUseCase,
)
from src.domain.errors import MessageNotFoundError
from src.domain.repositories.chat_repository import IChatRepository
from src.domain.repositories.contact_repository import IContactRepository
from src.domain.repositories.message_repository import IMessageRepository
from src.web.controllers.http_types import HttpRequest, HttpResponse, StatusCodes
from src.web.controllers.interfaces import IMessageHttpController


class ReceiveMessageHttpController(IMessageHttpController):
    def __init__(
        self,
        message_repository: IMessageRepository,
        contact_repository: IContactRepository,
        chat_repository: IChatRepository,
    ):
        super().__init__(message_repository=message_repository)
        self._contact_repository = contact_repository
        self._chat_repository = chat_repository

    def _extract_data_from_body(self, body: dict) -> dict[str, Any]:
        payload = body["entry"][0]["changes"][0]["value"]
        return {
            "sender_phone_number": payload["contacts"][0]["wa_id"],
            "sender_name": payload["contacts"][0]["profile"]["name"],
            "message_external_id": payload["messages"][0]["id"],
            "message_timestamp": datetime.fromtimestamp(
                timestamp=float(payload["messages"][0]["timestamp"]),
                tz=UTC,
            ),
            "receiver_phone_number": payload["metadata"]["display_phone_number"],
            "text": payload["messages"][0]["text"]["body"],
        }

    def _validate_body(self, body: dict) -> list[str]:
        return []

    def handle(self, request: HttpRequest) -> HttpResponse:
        if errors := self._validate_body(request.body):
            return HttpResponse(
                status_code=StatusCodes.BAD_REQUEST.value,
                body={"detail": errors},
            )

        extracted_data = self._extract_data_from_body(request.body)

        use_case = ReceiveMessageUseCase(
            message_repository=self._message_repository,
            contact_repository=self._contact_repository,
            chat_repository=self._chat_repository,
        )
        try:
            message = use_case.execute(
                sender_phone_number=extracted_data["sender_phone_number"],
                sender_name=extracted_data["sender_name"],
                message_external_id=extracted_data["message_external_id"],
                message_timestamp=extracted_data["message_timestamp"],
                receiver_phone_number=extracted_data["receiver_phone_number"],
                text=extracted_data["text"],
            )
        except ReceiverContactDoesNotExistError:
            return HttpResponse(
                status_code=StatusCodes.BAD_REQUEST.value,
                body={"detail": "receiver contact does not exist"},
            )

        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={"message_id": message.id},
        )


class GetMessageHttpController(IMessageHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetMessageUseCase(message_repository=self._message_repository)
        try:
            message = use_case.execute(request.path_params["id"])
        except MessageNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "message not found"},
            )

        body = {
            "id": message.id,
            "external_id": message.external_id,
            "external_timestamp": message.external_timestamp.isoformat(),
            "chat_id": message.chat_id,
            "is_received": message.is_received,
            "text": message.text,
            "received_by": message.received_by,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat()
            if message.updated_at
            else None,
        }
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )
