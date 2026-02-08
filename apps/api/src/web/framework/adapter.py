from json import JSONDecodeError

from fastapi import Request

from src.web.http_types import HttpRequest


async def request_adapter(request: Request) -> HttpRequest:
    body = None
    try:
        body = await request.json()
    except JSONDecodeError:
        pass

    context = {}
    if hasattr(request.state, "current_user"):
        context["current_user"] = request.state.current_user

    return HttpRequest(
        url=str(request.url),
        headers=dict(request.headers),
        query_params=dict(request.query_params),
        path_params=request.path_params,
        body=body,
        cookies=dict(request.cookies),
        context=context,
    )
