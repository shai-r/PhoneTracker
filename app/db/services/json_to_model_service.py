from typing import Optional

from app.db.models.phone_tracker import PhoneTrackerPayload
from app.db.services.device_service import convert_device_to_model
from app.db.services.interaction_service import convert_interaction_to_model


def json_to_model(payload: dict) -> Optional[PhoneTrackerPayload]:
    try:
        devices = list(map(convert_device_to_model, payload['devices']))
        interaction = convert_interaction_to_model(payload['interaction'])

        if interaction is None:
            print("Invalid interaction data.")
            return None

        return PhoneTrackerPayload(devices=devices, interaction=interaction)

    except KeyError as e:
        print(f"Missing required field in payload: {e}")
        return None

