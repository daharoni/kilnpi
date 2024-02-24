from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List, Any, Dict
from datetime import datetime
from app.models.firing_profile_model import FiringProfilePoint
from app.models.sensor_model import TemperatureData, DutyCyclePoint
    
class AppState(BaseModel):
    """
    Holds a copy of all data that is represented to the user on the front end.
    This should stay in sync with the front end
    """
    isFiring: bool = False
    firingName: str = ""
    isSoak: bool = False
    isDry: bool = False
    isHold: bool = False
    profileID: Optional[int] = None
    startFiringTemperatureData: Optional[TemperatureData] = None
    startFiringTime: Optional[datetime] = None
    kilnTemperatureData: List[FiringProfilePoint] = []
    dutyCycleData: List[DutyCyclePoint] = []
    firingProfile: Optional[Dict[str, Any]] = None # TODO: Make into pydantic model


