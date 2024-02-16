from fastapi import APIRouter, HTTPException
from typing import List
from database import save_firing_profile, get_firing_profiles, get_past_firing_data
from ..models.firing_model import FiringOptions, FiringProfile

router = APIRouter()

@router.post("/firing/")
async def create_firing_option(firing_option: FiringOptions):
    save_firing_profile(firing_option.dict())
    return {"message": "Firing option created"}

@router.get("/profiles/", response_model=List[FiringProfile])
async def list_profiles():
    return get_firing_profiles()

@router.get("/data/{profile_id}/")
async def firing_data(profile_id: int):
    return get_past_firing_data(profile_id)

