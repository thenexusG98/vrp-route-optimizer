from pydantic import BaseModel
from typing import List

from .location import Location
from .order import Order
from .vehicle import Vehicle


class OptimizationRequest(BaseModel):
    orders: List[Order]
    vehicles: List[Vehicle]
    depot: Location   # Punto central de salida/regreso
