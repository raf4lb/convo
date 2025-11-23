from flask import Blueprint

readiness_route_blueprint = Blueprint("readiness_routes", __name__)


@readiness_route_blueprint.route("/", methods=["GET"])
def ready():
    return {"status": "ok"}, 200