from fastapi import APIRouter
from ..models.sensor_model import TemperatureData

router = APIRouter()

@router.get("/temperature/")
async def get_temperature():
    # Logic to get temperature
    return TemperatureData(temperature=25.0, timestamp="2023-04-01T10:00:00Z")
