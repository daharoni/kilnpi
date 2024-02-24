from fastapi import APIRouter, HTTPException
import json
from typing import List
from ..services.profiles import get_firing_profiles, get_profile_by_id, updateProfile
from ..models.firing_profile_model import FiringProfile
from app.routers.app_state import current_state


router = APIRouter()
isDry = False
isSoak = False
profileID = []

@router.get("/profiles/", response_model=List[FiringProfile])
def read_profiles():
    return get_firing_profiles()

@router.get("/profiles/{profile_id}/", response_model=FiringProfile)
async def read_profile(profile_id: int):
    current_state.profileID = profile_id
    profileToPlot = await updateProfile(current_state)
    current_state.firingProfile = profileToPlot # TODO: should be done in a better way
    if profileToPlot is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profileToPlot

