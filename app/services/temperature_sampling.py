# app/services/temperature_sampling.py
import os
import asyncio
from fastapi import WebSocket
import json
from datetime import datetime
from app.services.websocket_manager import broadcast
from app.utils.global_state import last_temperature, temperature_lock, firingStartTime
from app.hardware.max31855 import MAX31855
from app.hardware.spi_devices import spi_device_class


# Initialize MAX31855 sensor (adjust bus and device numbers as necessary)
max31855_sensor = MAX31855(spi_device_class, bus=0, device=0)

async def poll_temperature_sensor():
    new_temp = 100
    while True:
        new_temp += 5
        max_ic_temp, faults = max31855_sensor.read_temperature()
        print(f"Current Temperature: {max_ic_temp}°C")
        faults = "some_flag"
        timestamp = datetime.now()
        timeSinceFiringStart = timestamp - firingStartTime
        async with temperature_lock:
            last_temperature = {"temperature": new_temp, "faults": faults, "timestamp": timestamp.isoformat(), "timeSinceFiringStart": timeSinceFiringStart.total_seconds()/(60 * 60)}
            await broadcast(json.dumps(last_temperature))
            # print(new_temp)
        await asyncio.sleep(3)