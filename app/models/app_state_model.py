from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List

class AppState(BaseModel):
    isFiring: bool = False
    firingName: str = ""
    isSoak: bool = False
    isDry: bool = False
    profileID: Optional[int] = None
    kilnTemperatureData: List = []


