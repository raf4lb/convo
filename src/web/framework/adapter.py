from json import JSONDecodeError

from fastapi import Request

from src.web.controllers.http_types import HttpRequest


async def request_adapter(request: Request) -> HttpRequest:
    body = None
    try:
        body = await request.json()
    except JSONDecodeError:
        pass

    return HttpRequest(
        url=str(request.url),
        headers=dict(request.headers),
        query_params=dict(request.query_params),
        path_params=request.path_params,
        body=body,
    )
