from dataclasses import dataclass


@dataclass
class Device:
    @dataclass
    class Location:
        latitude: float
        longitude: float
        altitude_meters: float
        accuracy_meters: float
    id: str
    name: str
    brand: str
    model: str
    os: str
    location: Location
