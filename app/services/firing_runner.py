from app.utils.pid_controller import PIDController
import json
import logging
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.kiln_model import KilnParameters
from app.utils.global_state import last_temperature
from app.utils.global_state import temperature_broadcaster
from app.models.sensor_model import TemperatureData
from datetime import datetime




logger = logging.getLogger("logger")
kiln_temp = TemperatureData()


def load_kiln_parameters() -> KilnParameters:
    """
    Load firing profiles from a JSON file and return them as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing firing profiles.
    """
    global logger
    
    try:
        with open('data/kiln_parameters.json') as f:
            data = json.load(f)
        
            # Parse the JSON data into a Pydantic model
            kiln_params = KilnParameters.model_validate(data)
            logger.info(f"Read kiln parameters file: {kiln_params}")
            return kiln_params
    except IOError as e:
        logger.error(f"Error opening or reading the kiln parameter file: {e}")
        return None

async def kiln_temperature_listener(temp_data: TemperatureData):
    global kiln_temp
    kiln_temp = temp_data

temperature_broadcaster.add_listener(kiln_temperature_listener)

def get_profile_setpoint(time_since_start):
    # Based on time kiln has been running, find the temperature point from the selected firing profile
    setpoint = 100
    return setpoint

async def run_kiln() -> None:
    global logger
    global kiln_temp
    
    kiln_params = load_kiln_parameters()
    pid_controller = PIDController(kiln_params)

    while True:
        setpoint = get_profile_setpoint(kiln_temp.timeSinceFiringStart)
        pid_duty = pid_controller.compute(setpoint=50,measured_value=kiln_temp.temperature, current_time= kiln_temp.timestamp)
        await asyncio.sleep(kiln_params.pid_parameters.period)