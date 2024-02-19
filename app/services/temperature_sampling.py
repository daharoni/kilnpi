from typing import Dict
import os
import asyncio
from fastapi import WebSocket
import json
from datetime import datetime
from app.services.websocket_manager import broadcast
from app.utils.global_state import write_temperature, firingStartTime
from app.hardware.max31855 import MAX31855
from app.hardware.spi_devices import spi_device_class


# Initialize MAX31855 sensor (adjust bus and device numbers as necessary)
max31855_sensor = MAX31855(spi_device_class, bus=0, device=0)

async def poll_temperature_sensor() -> None:
    """
    An asynchronous function that continuously reads the temperature from a MAX31855 sensor
    and broadcasts the temperature data to connected clients.
    """
    new_temp = 100
    while True:
        max_ic_temp, faults = max31855_sensor.read_temperature()
        print(f"Current Temperature: {max_ic_temp}°C")
        faults = "some_flag"
        timestamp = datetime.now()
        time_since_firing_start = timestamp - firingStartTime
        last_temperature = {
            "temperature": new_temp,
            "faults": faults,
            "timestamp": timestamp.isoformat(),
            "timeSinceFiringStart": time_since_firing_start.total_seconds() / (60 * 60)
        }
        await write_temperature(last_temperature)
        await broadcast(json.dumps(last_temperature))
        await asyncio.sleep(3)