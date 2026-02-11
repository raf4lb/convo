from src.application.use_cases.chat_use_cases import (
    AssignAttendantToChatUseCase,
    GetChatsByAttendantUseCase,
    GetChatUseCase,
    GetPendingChatsUseCase,
    GetResolvedChatsUseCase,
    GetUnassignedChatsUseCase,
    ListChatsByCompanyUseCase,
    SearchChatsUseCase,
)
from src.application.use_cases.message_use_cases import (
    GetChatMessagesUseCase,
    MarkChatAsReadUseCase,
    SendMessageUseCase,
)
from src.domain.errors import ChatNotFoundError
from src.web.controllers.interfaces import IChatHttpController, IMessageHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes

# class CreateCompanyHttpController(ICompanyHttpController):
#     def handle(self, request: HttpRequest) -> HttpResponse:
#         use_case = CreateCompanyUseCase(company_repository=self._repository)
#         company = use_case.execute(
#             name=request.body["name"],
#         )
#         return HttpResponse(
#             status_code=StatusCodes.CREATED.value,
#             body={
#                 "id": company.id,
#                 "name": company.name,
#                 "created_at": company.created_at.isoformat(),
#                 "updated_at": company.updated_at.isoformat(),
#             },
#         )
#
#
# class GetCompanyHttpController(ICompanyHttpController):
#     def handle(self, request: HttpRequest) -> HttpResponse:
#         use_case = GetCompanyUseCase(company_repository=self._repository)
#         try:
#             company = use_case.execute(company_id=request.path_params["id"])
#         except CompanyNotFoundError:
#             return HttpResponse(
#                 status_code=StatusCodes.NOT_FOUND.value,
#                 body={"detail": "company not found"},
#             )
#         return HttpResponse(
#             status_code=StatusCodes.OK.value,
#             body={
#                 "id": company.id,
#                 "name": company.name,
#             },
#         )
#
#
# class UpdateCompanyHttpController(ICompanyHttpController):
#     def handle(self, request: HttpRequest) -> HttpResponse:
#         use_case = UpdateCompanyUseCase(company_repository=self._repository)
#         company = use_case.execute(
#             company_id=request.path_params["id"],
#             name=request.body["name"],
#         )
#         return HttpResponse(
#             status_code=StatusCodes.OK.value,
#             body={
#                 "id": company.id,
#                 "name": company.name,
#             },
#         )
#
#
# class DeleteCompanyHttpController(ICompanyHttpController):
#     def handle(self, request: HttpRequest) -> HttpResponse:
#         use_case = DeleteCompanyUseCase(company_repository=self._repository)
#         try:
#             use_case.execute(company_id=request.path_params["id"])
#         except CompanyNotFoundError:
#             return HttpResponse(
#                 status_code=StatusCodes.NOT_FOUND.value,
#                 body={"detail": "company not found"},
#             )
#         return HttpResponse(status_code=StatusCodes.NO_CONTENT.value)


class GetChatHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetChatUseCase(chat_repository=self._chat_repository)
        chat_id = request.path_params["chat_id"]

        try:
            chat = use_case.execute(chat_id=chat_id)
        except ChatNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "chat not found"},
            )

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": chat.id,
                "company_id": chat.company_id,
                "contact_id": chat.contact_id,
                "status": chat.status.value,
                "attached_user_id": chat.attached_user_id,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat() if chat.updated_at else None,
            },
        )


class ListChatsByCompanyHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = ListChatsByCompanyUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(company_id=request.query_params["company_id"])
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class MarkChatAsReadHttpController(IMessageHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = MarkChatAsReadUseCase(message_repository=self._message_repository)
        chat_id = request.path_params["chat_id"]
        updated_count = use_case.execute(chat_id=chat_id)

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={"updated_count": updated_count},
        )


class GetUnassignedChatsHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetUnassignedChatsUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(company_id=request.query_params["company_id"])
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class GetPendingChatsHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetPendingChatsUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(company_id=request.query_params["company_id"])
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class GetResolvedChatsHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetResolvedChatsUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(company_id=request.query_params["company_id"])
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class GetChatsByAttendantHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetChatsByAttendantUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(
            company_id=request.query_params["company_id"],
            attendant_id=request.query_params["attendant_id"],
        )
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class SearchChatsHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = SearchChatsUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(
            company_id=request.query_params["company_id"],
            query=request.query_params["query"],
            user_id=request.query_params.get("user_id"),
        )
        body = {
            "results": [
                {
                    "id": chat.id,
                    "company_id": chat.company_id,
                    "contact_id": chat.contact_id,
                    "status": chat.status.value,
                    "attached_user_id": chat.attached_user_id,
                    "created_at": chat.created_at.isoformat(),
                    "updated_at": chat.updated_at.isoformat()
                    if chat.updated_at
                    else None,
                }
                for chat in chats
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class AssignAttendantToChatHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = AssignAttendantToChatUseCase(chat_repository=self._chat_repository)
        chat_id = request.path_params["chat_id"]
        attendant_id = request.body.get("attendant_id")

        try:
            chat = use_case.execute(chat_id=chat_id, attendant_id=attendant_id)
        except ChatNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "chat not found"},
            )

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": chat.id,
                "company_id": chat.company_id,
                "contact_id": chat.contact_id,
                "status": chat.status.value,
                "attached_user_id": chat.attached_user_id,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat() if chat.updated_at else None,
            },
        )


class GetChatMessagesHttpController(IMessageHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetChatMessagesUseCase(message_repository=self._message_repository)
        chat_id = request.path_params["chat_id"]
        messages = use_case.execute(chat_id=chat_id)

        body = {
            "results": [
                {
                    "id": message.id,
                    "external_id": message.external_id,
                    "external_timestamp": message.external_timestamp.isoformat(),
                    "chat_id": message.chat_id,
                    "text": message.text,
                    "sent_by_user_id": message.sent_by_user_id,
                    "read": message.read,
                    "created_at": message.created_at.isoformat(),
                    "updated_at": message.updated_at.isoformat()
                    if message.updated_at
                    else None,
                }
                for message in messages
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )


class SendMessageHttpController(IMessageHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = SendMessageUseCase(message_repository=self._message_repository)
        chat_id = request.path_params["chat_id"]
        text = request.body["text"]
        sent_by_user_id = request.body["sent_by_user_id"]

        message = use_case.execute(
            chat_id=chat_id,
            text=text,
            sent_by_user_id=sent_by_user_id,
        )

        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": message.id,
                "external_id": message.external_id,
                "external_timestamp": message.external_timestamp.isoformat(),
                "chat_id": message.chat_id,
                "text": message.text,
                "sent_by_user_id": message.sent_by_user_id,
                "read": message.read,
                "created_at": message.created_at.isoformat(),
                "updated_at": message.updated_at.isoformat()
                if message.updated_at
                else None,
            },
        )
