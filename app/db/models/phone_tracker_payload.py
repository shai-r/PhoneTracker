from dataclasses import dataclass

from app.db.models import Device, Interaction


@dataclass
class PhoneTrackerPayload:
    from_device: Device
    to_device: Device
    interaction: Interaction