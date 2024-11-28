from flask import Blueprint, request, jsonify

from app.db.services.json_to_model_service import json_to_model

phone_blueprint = Blueprint("phone", __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   print(json_to_model(request.json))
   return jsonify({ }), 200
