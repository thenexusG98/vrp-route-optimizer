from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    id: str
    lat: float
    lon: float
    address: Optional[str] = None
