from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class DutyCyclePoint(BaseModel):
    time: float  # Hours 
    dutyCycle: float  # Duty Cycle at the given time
    
class TemperatureData(BaseModel):
    """
    Used to store a temperature measurement with related data
    """
    type: str = 'temperature_data'
    temperature: Optional[float] = None
    faults: Optional[Dict[str, bool]] = None
    timestamp: Optional[datetime] = None
    timeSinceFiringStart: Optional[float] = None

class DutyCycleData(BaseModel):
    """
    Used to store a duty cycle time point with related data
    """
    type: str = 'duty_cycle_data'
    duty_cycle: Optional[float] = None
    timestamp: Optional[datetime] = None
    timeSinceFiringStart: Optional[float] = None
