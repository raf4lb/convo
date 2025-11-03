from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.chat_controllers import ListChatsByCompanyHttpController
from src.web.framework.adapter import flask_adapter

chat_route_blueprint = Blueprint("chat_routes", __name__)


@chat_route_blueprint.route("/", methods=["GET"])
def list_company_chats():
    repository = current_app.config["chat_repository"]
    controller = ListChatsByCompanyHttpController(chat_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
