from dataclasses import dataclass
from typing import List

from app.db.models import Device, Interaction


@dataclass
class PhoneTrackerPayload:
    devices: List[Device]
    interaction: Interaction