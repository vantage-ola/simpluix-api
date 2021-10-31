from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from http_status import HttpStatus
from models import db, InfoCategory, InfoCategorySchema, Info, InfoSchema
from sqlalchemy.exc import SQLAlchemyError


service_blueprint = Blueprint('service', __name__)

info_schema = InfoSchema()
info_category_schema = InfoCategorySchema()

service = Api(service_blueprint)
