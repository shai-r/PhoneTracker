from typing import Optional

from app.db.models import Device


def convert_location_to_model(location_data: Optional[dict]) -> Optional[Device.Location]:
    try:
        if location_data:
            return Device.Location(
                latitude=location_data['latitude'],
                longitude=location_data['longitude'],
                altitude_meters=location_data['altitude_meters'],
                accuracy_meters=location_data['accuracy_meters']
            )
        return None
    except KeyError as e:
        print(f"Missing location field: {e}")
        return None


def convert_device_to_model(device_data: dict) -> Device:
    location_data = device_data.get('location', None)
    location = convert_location_to_model(location_data)

    return Device(
        id=device_data['id'],
        name=device_data['name'],
        brand=device_data['brand'],
        model=device_data['model'],
        os=device_data['os'],
        location=location
    )

query_for_bluetooth_device_connections = """
    MATCH (start:Device)
    MATCH (end:Device)
    WHERE start <> end
    MATCH path = shortestPath((start)-[:INTERACTED_WITH*]->(end))
    WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
    WITH path, length(path) as pathLength
    ORDER BY pathLength DESC
    LIMIT 1
    RETURN path, pathLength
"""

query_for_devices_with_strong_connections = """
    MATCH (d1:Device)-[c:INTERACTED_WITH]->(d2:Device)
    WHERE c.signal_strength_dbm > -60
    MATCH path = shortestPath((d1)-[:INTERACTED_WITH*]->(d2))
    RETURN path
"""

query_count_connected_devices= """
    MATCH (d1:Device {id: $device_id})-[c:INTERACTED_WITH]->(d2:Device)
    RETURN COUNT(d2) AS connected_devices_count
"""

def params_for_one_id(device_id: str):
    return {"device_id": device_id}

query_check_direct_connection = """
   MATCH (d1:Device {id: $device_id_1})
    MATCH (d2:Device {id: $device_id_2})
    OPTIONAL MATCH (d1)-[c1:INTERACTED_WITH]->(d2)
    OPTIONAL MATCH (d2)-[c2:INTERACTED_WITH]->(d1)
    RETURN COUNT(c1) > 0 AS is_connected_1, COUNT(c2) > 0 AS is_connected_2
"""


def params_for_two_ids(device_id_1: str, device_id_2: str):
    return {
        "device_id_1": device_id_1,
        "device_id_2": device_id_2
    }

query_for_most_recent_interaction = """
    MATCH (start_device:Device {id: $device_id})-[interaction:INTERACTED_WITH]->(end_device:Device)
    WITH start_device, interaction, end_device
    ORDER BY interaction.timestamp DESC
    LIMIT 1
    RETURN start_device, interaction, end_device
"""

