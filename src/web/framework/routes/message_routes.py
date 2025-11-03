from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.message_controllers import (
    GetMessageHttpController,
    ReceiveMessageHttpController,
)
from src.web.framework.adapter import flask_adapter

message_route_blueprint = Blueprint("message_routes", __name__)


@message_route_blueprint.route("/receive", methods=["POST"])
def receive_message():
    message_repository = current_app.config["message_repository"]
    contact_repository = current_app.config["contact_repository"]
    chat_repository = current_app.config["chat_repository"]
    controller = ReceiveMessageHttpController(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@message_route_blueprint.route("/<id>", methods=["GET"])
def get_message(id):
    repository = current_app.config["message_repository"]
    controller = GetMessageHttpController(message_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
