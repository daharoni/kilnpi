from fastapi import APIRouter, HTTPException, Body
import json
from typing import List
from ..services.profiles import get_firing_profiles, get_profile_by_id, updateProfile
from ..models.firing_model import FiringProfile
from app.utils.global_state import firingStartTime, set_isFiring
from database import add_new_firing

router = APIRouter()
isDry = False
isSoak = False
profileID = []

@router.get("/profiles/", response_model=List[FiringProfile])
def read_profiles():
    return get_firing_profiles()

@router.get("/profiles/{profile_id}/", response_model=FiringProfile)
async def read_profile(profile_id: int):
    profileID = profile_id
    profileToPlot = await updateProfile(profileID, isDry, isSoak)
    if profileToPlot is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profileToPlot

@router.get("/firingStartTimestamp/")
def get_firingStartTimestamp():
    return {"firingStartTime": firingStartTime.isoformat()}

@router.post("/start-firing/")
def start_firing(body: dict = Body(...)):
    firing_name = body['firingName']
    add_new_firing(firing_name) # addes a new db entry for tracking this firing
    # TODO: start db logging and PID and GPIO control of relays
    set_isFiring(True)
    print("Firing process started.")
    return {"message": "Firing process started successfully."}

@router.post("/abort-firing/")
def start_firing():
    isFiring = False
    print("Firing process aborted.")
    return {"message": "Firing process aborted successfully."}

@router.post("/dry-change/")
async def start_firing(body: dict = Body(...)):
    isDry = body['isDry']
    profileToPlot = await updateProfile(profileID, isDry, isSoak)
    return profileToPlot

@router.post("/soak-change/")
async def start_firing(body: dict = Body(...)):
    isSoak = body['isSoak']
    profileToPlot = await updateProfile(profileID, isDry, isSoak)
    return profileToPlot
