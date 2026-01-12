from src.infrastructure.settings import settings
from src.web.controllers.interfaces import IHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


class VerifyWebhookHttpController(IHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        verify_token = settings.WEBHOOK_VERIFY_TOKEN

        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("Webhook verificado com sucesso!")
            return HttpResponse(body=challenge, status_code=StatusCodes.OK.value)
        else:
            return HttpResponse(body=challenge, status_code=StatusCodes.FORBIDDEN.value)


class ReceiveMessagesWebhookHttpController(IHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        print("\n===== WEBHOOK RECEBIDO =====")
        print("Headers:")
        print(dict(request.headers))

        print("\nJSON:")
        print(request.body)

        print("============================\n")

        return HttpResponse(
            body={"status": "received"}, status_code=StatusCodes.OK.value
        )
