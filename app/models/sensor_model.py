from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class TemperatureData(BaseModel):
    type: str = 'temperature_data'
    temperature: Optional[float] = None
    faults: Optional[Dict[str, bool]] = None
    timestamp: Optional[datetime] = None
    timeSinceFiringStart: Optional[float] = None

class DutyCycleData(BaseModel):
    type: str = 'duty_cycle_data'
    duty_cycle: Optional[float] = None
    timestamp: Optional[datetime] = None
    timeSinceFiringStart: Optional[float] = None
