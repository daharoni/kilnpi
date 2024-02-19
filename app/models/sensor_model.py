from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class TemperatureData(BaseModel):
    temperature: Optional[float] = None
    flags: Optional[Dict[str, bool]] = None
    timestamp: datetime
    timeSinceFiringStart: float
