from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.user_controllers import (
    CreateUserHTTPController,
    DeleteUserHTTPController,
    GetUserHTTPController,
    UpdateUserHTTPController,
)
from src.web.framework.adapter import flask_adapter

user_route_blueprint = Blueprint("user_routes", __name__)


@user_route_blueprint.route("/", methods=["POST"])
def create_user():
    repository = current_app.config["user_repository"]
    controller = CreateUserHTTPController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["GET"])
def get_user(id):
    repository = current_app.config["user_repository"]
    controller = GetUserHTTPController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["PUT"])
def update_user(id):
    repository = current_app.config["user_repository"]
    controller = UpdateUserHTTPController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["DELETE"])
def delete_user(id):
    repository = current_app.config["user_repository"]
    controller = DeleteUserHTTPController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
