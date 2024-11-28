from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Interaction:
    from_device: str
    to_device: str
    method: str
    timestamp: datetime
    bluetooth_version: Optional[str] = None
    signal_strength_dbm: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[int] = None