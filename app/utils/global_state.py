import asyncio
from asyncio import Lock
from datetime import datetime
from ..models.sensor_model import TemperatureData

last_temperature = TemperatureData(temperature=0.0, flags={}, timestamp=datetime.now(), timeSinceFiringStart=0)

class TemperatureBroadcaster:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    async def broadcast(self, temperature):
        for listener in self.listeners:
            await listener(temperature)

temperature_broadcaster = TemperatureBroadcaster()

async def broadcast_new_temp(tempData: TemperatureData):
    global last_temperature
    global temperature_broadcaster
    
    last_temperature = tempData
    await temperature_broadcaster.broadcast(tempData)
    
def get_temperature():
    global last_temperature
    return last_temperature
