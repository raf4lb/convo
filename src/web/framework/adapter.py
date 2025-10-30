from flask import Request as FlaskRequest

from src.web.controllers.http_types import HttpRequest


def flask_adapter(request: FlaskRequest) -> HttpRequest:
    return HttpRequest(
        url=request.url,
        headers={key: value for key, value in request.headers.items()},
        query_params=request.args,
        path_params=request.view_args,
        body=request.json if request.is_json else {},
    )
