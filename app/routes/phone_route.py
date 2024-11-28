from flask import Blueprint, request, jsonify

from app.db.services.device_service import query_for_devices_with_strong_connections, \
   query_count_connected_devices, \
   params_for_one_id, query_check_direct_connection, params_for_two_ids, \
   query_for_bluetooth_device_connections, query_for_most_recent_interaction
from app.db.repositories.neo4j_repository import connect_to_neo4j_return_data
from app.db.repositories.phone_tracker_payload_repository import insert_phone_tracker_payload
from app.db.services.phone_tracker_payload import json_to_model

phone_blueprint = Blueprint("phone", __name__)

@phone_blueprint.route("/phone_tracker", methods=['POST'])
def get_interaction():
   insert_phone_tracker_payload(json_to_model(request.json))
   return jsonify({ "message": "received interaction" }), 200

@phone_blueprint.route("/bluetooth_connections", methods=['GET'])
def get_bluetooth_connections():
   return jsonify(connect_to_neo4j_return_data(query_for_bluetooth_device_connections)), 200

@phone_blueprint.route("/strong_connections", methods=['GET'])
def get_devices_with_strong_connections():
   return jsonify(connect_to_neo4j_return_data(query_for_devices_with_strong_connections)), 200

@phone_blueprint.route("/devices_connected/<device_id>", methods=['GET'])
def how_many_devices_connected_to_specific_device(device_id: str):
   return jsonify(connect_to_neo4j_return_data(
      query_count_connected_devices,
      params_for_one_id(device_id)
   )), 200

@phone_blueprint.route("/direct_connection/<device_id_1>/<device_id_2>", methods=['GET'])
def is_direct_connection(device_id_1: str, device_id_2: str):
   result = connect_to_neo4j_return_data(
      query_check_direct_connection,
      params_for_two_ids(device_id_1, device_id_2)
   )
   if not result:
      return jsonify({"is_directly_connected": False}), 200
   is_connected = any(value.get("is_connected_1") is True or value.get("is_connected_2") is True for value in result)
   return jsonify({
      "is_directly_connected": is_connected
   }), 200

@phone_blueprint.route('/most_recent_interaction/<device_id>', methods=['GET'])
def get_most_recent_interaction(device_id):
    result = connect_to_neo4j_return_data(
       query_for_most_recent_interaction,
       params_for_one_id(device_id)
    )

    if not result:
        return jsonify({"message": "No interaction found for this device"}), 404
    return jsonify(result), 200

