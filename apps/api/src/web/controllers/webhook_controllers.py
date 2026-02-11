from src.web.controllers.interfaces import IHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


class VerifyWebhookHttpController(IHttpController):
    def __init__(self, verify_token: str):
        self._verify_token = verify_token

    def handle(self, request: HttpRequest) -> HttpResponse:
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if mode == "subscribe" and token == self._verify_token:
            return HttpResponse(body=challenge, status_code=StatusCodes.OK.value)
        else:
            return HttpResponse(body=challenge, status_code=StatusCodes.FORBIDDEN.value)
