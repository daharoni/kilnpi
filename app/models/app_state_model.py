from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class AppState(BaseModel):
    isFiring: bool = False
    firingName: str = ""
    isSoak: bool = False
    isDry: bool = False
    profileID: Optional[int] = None


