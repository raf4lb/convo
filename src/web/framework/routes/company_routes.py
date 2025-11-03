from flask import Blueprint, current_app, jsonify, request

from src.web.controllers.company_controllers import (
    CreateCompanyHttpController,
    DeleteCompanyHttpController,
    GetCompanyHttpController,
    ListCompanyHttpController,
    UpdateCompanyHttpController,
)
from src.web.framework.adapter import flask_adapter

company_route_blueprint = Blueprint("company_routes", __name__)


@company_route_blueprint.route("/", methods=["GET"])
def list_companies():
    repository = current_app.config["company_repository"]
    controller = ListCompanyHttpController(company_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@company_route_blueprint.route("/", methods=["POST"])
def create_company():
    repository = current_app.config["company_repository"]
    controller = CreateCompanyHttpController(company_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@company_route_blueprint.route("/<id>", methods=["GET"])
def get_company(id):
    repository = current_app.config["company_repository"]
    controller = GetCompanyHttpController(company_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@company_route_blueprint.route("/<id>", methods=["PUT"])
def update_company(id):
    repository = current_app.config["company_repository"]
    controller = UpdateCompanyHttpController(company_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code


@company_route_blueprint.route("/<id>", methods=["DELETE"])
def delete_company(id):
    repository = current_app.config["company_repository"]
    controller = DeleteCompanyHttpController(company_repository=repository)
    response = controller.handle(request=flask_adapter(request))
    return jsonify(response.body), response.status_code
