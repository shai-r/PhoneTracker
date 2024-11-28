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
        brand=device_data['brand'],
        model=device_data['model'],
        os=device_data['os'],
        location=location
    )
