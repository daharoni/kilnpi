from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List, Any, Dict
from datetime import datetime
from app.models.firing_model import TemperatureProfilePoint
from app.models.sensor_model import TemperatureData

class AppState(BaseModel):
    isFiring: bool = False
    firingName: str = ""
    isSoak: bool = False
    isDry: bool = False
    isHold: bool = False
    profileID: Optional[int] = None
    startFiringTemperatureData: Optional[TemperatureData] = None
    startFiringTime: Optional[datetime] = None
    kilnTemperatureData: List[TemperatureProfilePoint] = []
    firingProfile: Optional[Dict[str, Any]] = None # TODO: Make into pydantic model


