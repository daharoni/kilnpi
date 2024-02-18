from asyncio import Lock
from datetime import datetime
from ..models.sensor_model import TemperatureData

# Global state for the last logged temperature
last_temperature = TemperatureData(temperature=0.0, flags=0, timestamp=datetime.now())
# Lock to ensure thread-safe access to last_temperature
temperature_lock = Lock()

firingStartTime = datetime.now()
isFiring = False

