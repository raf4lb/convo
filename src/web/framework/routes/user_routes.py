from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.user_controllers import (
    CreateUserHttpController,
    DeleteUserHttpController,
    GetUserHttpController,
    ListUserHttpController,
    UpdateUserHttpController,
)
from src.web.framework.adapter import flask_adapter

user_route_blueprint = Blueprint("user_routes", __name__)


@user_route_blueprint.route("/", methods=["GET"])
def list_users():
    repository = current_app.config["user_repository"]
    controller = ListUserHttpController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/", methods=["POST"])
def create_user():
    user_repository = current_app.config["user_repository"]
    company_repository = current_app.config["company_repository"]
    controller = CreateUserHttpController(
        user_repository=user_repository,
        company_repository=company_repository,
    )
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["GET"])
def get_user(id):
    repository = current_app.config["user_repository"]
    controller = GetUserHttpController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["PUT"])
def update_user(id):
    repository = current_app.config["user_repository"]
    controller = UpdateUserHttpController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@user_route_blueprint.route("/<id>", methods=["DELETE"])
def delete_user(id):
    repository = current_app.config["user_repository"]
    controller = DeleteUserHttpController(user_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
