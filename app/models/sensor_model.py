from pydantic import BaseModel

class TemperatureData(BaseModel):
    temperature: float
    timestamp: str
