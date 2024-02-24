from pydantic import BaseModel
from typing import List

class FiringProfilePoint(BaseModel):
    time: float  # Assuming time is measured in minutes or a similar discrete unit
    temperature: float  # Temperature at the given time

class FiringProfile(BaseModel):
    id: int
    name: str
    max_temperature: float
    temperature_profile: List[FiringProfilePoint]
    
