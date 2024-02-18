from fastapi import APIRouter, HTTPException
from typing import List
from ..services.profiles import get_firing_profiles, get_profile_by_id
from ..models.firing_model import FiringProfile
from app.utils.global_state import firingStartTime, isFiring

router = APIRouter()

@router.get("/profiles/", response_model=List[FiringProfile])
def read_profiles():
    return get_firing_profiles()

@router.get("/profiles/{profile_id}/", response_model=FiringProfile)
def read_profile(profile_id: int):
    profile = get_profile_by_id(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/firingStartTimestamp/")
def get_firingStartTimestamp():
    return {"firingStartTime": firingStartTime.isoformat()}

@router.post("/start-firing/")
def start_firing():
    isFiring = True
    # TODO: start db logging and PID and GPIO control of relays
    print("Firing process started.")
    return {"message": "Firing process started successfully."}

@router.post("/abort-firing/")
def start_firing():
    isFiring = False
    print("Firing process aborted.")
    return {"message": "Firing process aborted successfully."}

