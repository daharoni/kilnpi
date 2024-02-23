from typing import Dict
import os
import asyncio
from fastapi import WebSocket
import json
from datetime import datetime
from app.services.websocket_manager import broadcast
from app.utils.global_state import broadcast_new_temp, last_temperature
from app.hardware.max31855 import MAX31855
from app.hardware.spi_devices import spi_device_class
from app.models.sensor_model import TemperatureData
from app.models.firing_model import TemperatureProfilePoint
from app.routers.app_state import current_state, get_kiln_parameters
import logging
from database import add_new_temperature_entry




# Initialize MAX31855 sensor (adjust bus and device numbers as necessary)
max31855_sensor = MAX31855(spi_device_class, bus=0, device=0)
logger = logging.getLogger("logger")

async def poll_temperature_sensor() -> None:
    """
    An asynchronous function that continuously reads the temperature from a MAX31855 sensor
    and broadcasts the temperature data to connected clients.
    """
    global logger
    kiln_params = get_kiln_parameters()

    while True:
        max_ic_temp, faults = max31855_sensor.read_temperature()
        timestamp = datetime.now()
        # print(f"Temp -> {max_ic_temp} and fauts -> {faults}")
        if current_state.startFiringTime:
            time_since_firing_start = timestamp - current_state.startFiringTime
            time_since_firing_start = time_since_firing_start.total_seconds() / (60 * 60)
        else:
            time_since_firing_start = None
        last_temperature = TemperatureData(
            temperature = max_ic_temp,
            faults = faults,
            timestamp= timestamp.isoformat(),
            timeSinceFiringStart= time_since_firing_start
        )
        # logger.info(last_temperature)
        await broadcast_new_temp(last_temperature)
        
        if (current_state.isFiring):
            newPoint = TemperatureProfilePoint(time=time_since_firing_start, temperature=max_ic_temp)
            current_state.kilnTemperatureData.append(newPoint) # adds temp to state tracking to allow webpage refresh
            await add_new_temperature_entry(last_temperature)
        
        time_since_last_display_update = timestamp - last_timestamp
        
        if (time_since_last_display_update.total_seconds >= kiln_params.display_parameters.temperature_display_period):
            await broadcast(last_temperature.model_dump_json()) # Sends new temperature measurement to vue js 
            last_timestamp = timestamp
       
        await asyncio.sleep(kiln_params.sensor_parameters.temperature_sampling_period)