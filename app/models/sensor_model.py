from pydantic import BaseModel
from datetime import datetime

class TemperatureData(BaseModel):
    temperature: float
    flags: int
    timestamp: datetime
