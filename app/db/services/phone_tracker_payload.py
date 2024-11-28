from typing import Optional, Dict

from app.db.models.phone_tracker_payload import PhoneTrackerPayload
from app.db.services.device_service import convert_device_to_model
from app.db.services.interaction_service import convert_interaction_to_model


def json_to_model(payload: dict) -> Optional[PhoneTrackerPayload]:
    try:
        devices = list(map(convert_device_to_model, payload['devices']))
        interaction = convert_interaction_to_model(payload['interaction'])

        if interaction is None:
            print("Invalid interaction data.")
            return None
        from_device = devices[0] if devices[0].id == payload['interaction']['from_device'] else devices[1]
        to_device = devices[0] if devices[0].id == payload['interaction']['to_device'] else devices[1]
        return PhoneTrackerPayload(from_device=from_device,
                                   to_device=to_device,
                                   interaction=interaction)
    except KeyError as e:
        print(f"Missing required field in payload: {e}")
        return None


query_for_create_devices_and_connection  = """
    MERGE (d1:Device {id: $id1})
    ON CREATE SET d1.brand = $brand1,
        d1.model = $model1,
        d1.name = $name1,
        d1.os = $os1,
        d1.latitude = $latitude1,
        d1.longitude = $longitude1,
        d1.altitude_meters = $altitude_meters1,
        d1.accuracy_meters = $accuracy_meters1

    MERGE (d2:Device {id: $id2})
    ON CREATE SET d2.brand = $brand2,
        d2.model = $model2,
        d1.name = $name1,
        d2.os = $os2,
        d2.latitude = $latitude2,
        d2.longitude = $longitude2,
        d2.altitude_meters = $altitude_meters2,
        d2.accuracy_meters = $accuracy_meters2

    MERGE (d1)-[r:INTERACTED_WITH { timestamp: $timestamp }]->(d2)
    ON CREATE SET r.method = $method,
        r.bluetooth_version = $bluetooth_version,
        r.signal_strength_dbm = $signal_strength_dbm,
        r.distance_meters = $distance_meters,
        r.duration_seconds = $duration_seconds,
        r.timestamp = $timestamp
    RETURN d1, r, d2
"""

def convert_phone_tracker_payload_to_params(phone_tracker_payload: PhoneTrackerPayload) -> Dict:
    from_device = phone_tracker_payload.from_device
    to_device = phone_tracker_payload.to_device
    interaction = phone_tracker_payload.interaction
    return {
        "id1": from_device.id,
        "name1": from_device.name,
        "brand1": from_device.brand,
        "model1": from_device.model,
        "os1": from_device.os,
        "latitude1": from_device.location.latitude,
        "longitude1": from_device.location.longitude,
        "altitude_meters1": from_device.location.altitude_meters,
        "accuracy_meters1": from_device.location.accuracy_meters,

        "id2": to_device.id,
        "name2": to_device.name,
        "brand2": to_device.brand,
        "model2": to_device.model,
        "os2": to_device.os,
        "latitude2": to_device.location.latitude,
        "longitude2": to_device.location.longitude,
        "altitude_meters2": to_device.location.altitude_meters,
        "accuracy_meters2": to_device.location.accuracy_meters,

        "method": interaction.method,
        "bluetooth_version": interaction.bluetooth_version,
        "signal_strength_dbm": interaction.signal_strength_dbm,
        "distance_meters": interaction.distance_meters,
        "duration_seconds": interaction.duration_seconds,
        "timestamp": interaction.timestamp
    }
