from pydantic import BaseModel
from datetime import time

from .location import Location


class Order(BaseModel):
    id: str
    location: Location
    weight: float        # kg
    volume: float        # m3
    due_time: time       # Ventana de tiempo límite
    priority: int = 1   # 1: Normal, 2: Alta
