from src.application.use_cases.chat_use_cases import ListChatsByCompanyUseCase
from src.web.controllers.interfaces import IChatHttpController
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


class ListChatsByCompanyHttpController(IChatHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = ListChatsByCompanyUseCase(chat_repository=self._chat_repository)
        chats = use_case.execute(company_id=request.query_params["company_id"])
        body = {
            "chats": [
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
