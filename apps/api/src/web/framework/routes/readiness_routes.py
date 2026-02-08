from fastapi import APIRouter

readiness_routes = APIRouter(prefix="/ready")


@readiness_routes.get("/")
def ready() -> dict:
    return {"status": "ready"}
