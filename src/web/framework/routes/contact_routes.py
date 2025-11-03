from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.contact_controllers import (
    CreateContactHttpController,
    GetContactHttpController,
)
from src.web.framework.adapter import flask_adapter

contact_route_blueprint = Blueprint("contact_routes", __name__)


@contact_route_blueprint.route("/", methods=["POST"])
def create_company_contact():
    repository = current_app.config["contact_repository"]
    controller = CreateContactHttpController(contact_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@contact_route_blueprint.route("/<id>", methods=["GET"])
def get_contact(id):
    repository = current_app.config["contact_repository"]
    controller = GetContactHttpController(contact_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
