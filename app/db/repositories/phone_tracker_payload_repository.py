from app.db.models import PhoneTrackerPayload
from app.db.repositories.interaction_repository import is_concurrent_call
from app.db.repositories.neo4j_repository import connect_to_neo4j_return_single
from app.db.services.phone_tracker_payload import query_for_create_devices_and_connection, \
    convert_phone_tracker_payload_to_params


def insert_phone_tracker_payload(phone_tracker_payload: PhoneTrackerPayload):
    from_device_id = phone_tracker_payload.from_device.id
    to_device_id = phone_tracker_payload.to_device.id
    timestamp = phone_tracker_payload.interaction.timestamp
    if  (from_device_id == to_device_id or
            is_concurrent_call(from_device_id, to_device_id, timestamp)):
        return None
    return connect_to_neo4j_return_single(
        query=query_for_create_devices_and_connection,
        params=convert_phone_tracker_payload_to_params(phone_tracker_payload)
    ).map(lambda res: [
        {"from device": dict(res["d1"])},
        {"to device": dict(res["r"])},
        {"interaction": dict(res["d2"])}
    ]).value_or(None)