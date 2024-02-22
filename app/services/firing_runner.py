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
from app.routers.app_state import get_state
from app.routers.app_state import current_state




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
    global firing_profile

    # Based on time kiln has been running, find the temperature point from the selected firing profile
    profile = current_state.firingProfile
    setpoint = None
    if profile:
        soak_temp = 700
        soak_length = 0.25
        count = 0
        time1 = 0
        temp1 = 0
        for point in profile['temperature_profile']:
            if (point['time'] > time_since_start):
                # Find which linear curve we are currently on
                # y = mx+b
                time2 = point['time']
                temp2 = point['temperature']
                m = (temp2 - temp1) / (time2 - time1)
                b = temp2 - m * time2
                setpoint = m * time_since_start + b
                
                break
            time1 = point['time']
            temp1 = point['temperature']
        return setpoint
    else:
        return None

async def run_kiln() -> None:
    global logger
    global kiln_temp
    
    kiln_params = load_kiln_parameters()
    pid_controller = PIDController(kiln_params)

    while True:
        if current_state.isFiring:
            if (kiln_temp.timeSinceFiringStart):
                setpoint = get_profile_setpoint(kiln_temp.timeSinceFiringStart)
                if setpoint:
                    value = kiln_temp.temperature
                    pid_duty = pid_controller.compute(setpoint= setpoint,measured_value= value, current_time= kiln_temp.timestamp)
        await asyncio.sleep(kiln_params.pid_parameters.period)