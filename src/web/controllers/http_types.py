from enum import Enum


class StatusCodes(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    NOT_FOUND = 404


class HttpRequest:
    def __init__(
        self,
        url: str,
        headers: dict,
        query_params: dict,
        body: dict,
        path_params: dict,
    ):
        self.url = url
        self.headers = headers
        self.query_params = query_params
        self.body = body
        self.path_params = path_params


class HttpResponse:
    def __init__(
        self,
        status_code: int,
        body: dict | None = None,
    ):
        self.status_code = status_code
        self.body = body
