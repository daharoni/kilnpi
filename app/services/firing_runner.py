from app.utils.pid_controller import PIDController
import json
import logging
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.kiln_model import KilnParameters
from app.utils.global_state import temperature_broadcaster
from app.models.sensor_model import TemperatureData, DutyCycleData
from datetime import datetime
from app.routers.app_state import current_state, get_kiln_parameters
from app.hardware.pwm_relay import PWMRelay, gpio_class
from app.services.websocket_manager import broadcast
from app.models.sensor_model import DutyCyclePoint
from app.database.database import last_measurement




logger = logging.getLogger("logger")
kiln_temp_smoothed = None
kiln_temp_history = []



async def kiln_temperature_listener(temp_data: TemperatureData):
    global kiln_temp
    global kiln_temp_history
    
    kiln_temp = temp_data
    kiln_temp_history.append(temp_data.temperature)
    kiln_temp_history = kiln_temp_history[-4:]

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
    global kiln_temp_history
    
    last_timestamp = datetime.now()
    
    kiln_params = get_kiln_parameters()
    pid_controller = PIDController(kiln_params)
    
    pin = 12
    frequency = kiln_params.pwm_settings.period / kiln_params.pwm_settings.period
    pwm_relay = PWMRelay(gpio_class, pin, frequency)
    
    duty_cycle_data = DutyCycleData()

    while True:
        if current_state.isFiring:
            if not pwm_relay.isRunning:
                pwm_relay.start(0)
            if (kiln_temp.timeSinceFiringStart):
                setpoint = get_profile_setpoint(kiln_temp.timeSinceFiringStart)
                if setpoint:
                    kiln_temp_smoothed = sum(kiln_temp_history) / len(kiln_temp_history)
                    if (kiln_temp_smoothed is not None):
                        duty_cycle_data.duty_cycle = pid_controller.compute(setpoint= setpoint,measured_value= kiln_temp_smoothed, current_time= kiln_temp.timestamp)
                        
                        duty_cycle_data.timestamp = datetime.now()
                        duty_cycle_data.timeSinceFiringStart = duty_cycle_data.timestamp - current_state.startFiringTime
                        duty_cycle_data.timeSinceFiringStart = duty_cycle_data.timeSinceFiringStart.total_seconds() / (60 * 60)
                        
                        last_measurement.duty_cycle = duty_cycle_data.duty_cycle
                        last_measurement.setpoint_value = setpoint
                        last_measurement.kiln_temperaure = kiln_temp_smoothed
                        last_measurement.time_since_start = duty_cycle_data.timeSinceFiringStart
                        
                        if (duty_cycle_data.duty_cycle is not None):
                            pwm_relay.change_duty_cycle(duty_cycle_data.duty_cycle * 100)
                    else:
                        print(f"Fault with temperature sensor -> {kiln_temp.faults}")
        else:
            if pwm_relay.isRunning:
                pwm_relay.stop()
                
        timestamp = datetime.now()
        time_since_last_display_update = timestamp - last_timestamp
        
        if (time_since_last_display_update.total_seconds() >= kiln_params.display_parameters.temperature_display_period):
            if (current_state.isFiring):
                newPoint = DutyCyclePoint(time=duty_cycle_data.timeSinceFiringStart, duty_cycle=duty_cycle_data.duty_cycle)
                current_state.dutyCycleData.append(newPoint)
            await broadcast(duty_cycle_data.model_dump_json()) # Sends new temperature measurement to vue js 
            last_timestamp = timestamp
            
        await asyncio.sleep(kiln_params.pid_parameters.period)
        