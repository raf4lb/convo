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
from src.web.controllers.interfaces import IMessageHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


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
        errors = []

        # Check for required top-level structure
        if not isinstance(body, dict):
            errors.append("Request body must be a JSON object")
            return errors

        if "entry" not in body or not isinstance(body["entry"], list):
            errors.append("Missing or invalid 'entry' field")
            return errors

        if not body["entry"]:
            errors.append("Empty 'entry' array")
            return errors

        try:
            entry = body["entry"][0]
            if "changes" not in entry or not isinstance(entry["changes"], list):
                errors.append("Missing or invalid 'changes' field")
                return errors

            if not entry["changes"]:
                errors.append("Empty 'changes' array")
                return errors

            change = entry["changes"][0]
            if "value" not in change or not isinstance(change["value"], dict):
                errors.append("Missing or invalid 'value' field")
                return errors

            value = change["value"]

            # Validate required fields in value
            if "contacts" not in value or not isinstance(value["contacts"], list):
                errors.append("Missing or invalid 'contacts' field")
            elif not value["contacts"]:
                errors.append("Empty 'contacts' array")
            else:
                contact = value["contacts"][0]
                if "wa_id" not in contact:
                    errors.append("Missing 'wa_id' in contact")
                if "profile" not in contact or "name" not in contact.get("profile", {}):
                    errors.append("Missing 'profile.name' in contact")

            if "messages" not in value or not isinstance(value["messages"], list):
                errors.append("Missing or invalid 'messages' field")
            elif not value["messages"]:
                errors.append("Empty 'messages' array")
            else:
                message = value["messages"][0]
                if "id" not in message:
                    errors.append("Missing 'id' in message")
                if "timestamp" not in message:
                    errors.append("Missing 'timestamp' in message")
                if "text" not in message or "body" not in message.get("text", {}):
                    errors.append("Missing 'text.body' in message")

            if "metadata" not in value or not isinstance(value["metadata"], dict):
                errors.append("Missing or invalid 'metadata' field")
            elif "display_phone_number" not in value["metadata"]:
                errors.append("Missing 'display_phone_number' in metadata")

        except (KeyError, IndexError, TypeError) as e:
            errors.append(f"Invalid webhook payload structure: {str(e)}")

        return errors

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
            "sent_by_user_id": message.sent_by_user_id,
            "text": message.text,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat()
            if message.updated_at
            else None,
        }
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )
