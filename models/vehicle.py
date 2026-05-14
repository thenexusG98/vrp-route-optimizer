from pydantic import BaseModel

from .location import Location


class Vehicle(BaseModel):
    id: str
    start_location: Location
    capacity_weight: float   # kg
    capacity_volume: float   # m3
    cost_per_km: float
