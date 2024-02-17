from fastapi import APIRouter, HTTPException
from typing import List
from database import get_firing_profiles, get_profile_by_id
from ..models.firing_model import FiringProfile

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

