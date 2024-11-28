from flask import Blueprint, request, jsonify

from app.db.repositories.phone_tracker_payload_repository import insert_phone_tracker_payload
from app.db.services.json_to_model_service import json_to_model

phone_blueprint = Blueprint("phone", __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   print(insert_phone_tracker_payload(json_to_model(request.json)))
   return jsonify({ }), 200
