from pydantic import BaseModel
from typing import List


class RouteStop(BaseModel):
    order_id: str
    sequence: int


class VehicleRoute(BaseModel):
    vehicle_id: str
    stops: List[RouteStop]
    total_distance_m: int  # metros


class SolverResult(BaseModel):
    routes: List[VehicleRoute]
