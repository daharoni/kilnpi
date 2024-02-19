from asyncio import Lock
from datetime import datetime
from ..models.sensor_model import TemperatureData

last_temperature = TemperatureData(temperature=0.0, flags={}, timestamp=datetime.now(), timeSinceFiringStart=0)
# Lock to ensure thread-safe access to last_temperature
temperature_lock = Lock()

firingStartTime = datetime.now()
isFiring = False

async def write_temperature(tempData: TemperatureData):
    global last_temperature
    global temperature_lock
    
    async with temperature_lock:
        last_temperature = tempData

async def read_temperature():
    global last_temperature
    global temperature_lock
    
    async with temperature_lock:
        return last_temperature
