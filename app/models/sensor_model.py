from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class TemperatureData(BaseModel):
    temperature: Optional[float] = None
    faults: Optional[Dict[str, bool]] = None
    timestamp: Optional[datetime] = None
    timeSinceFiringStart: Optional[float] = None
