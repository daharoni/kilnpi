from fastapi import APIRouter, HTTPException
from ...database import save_firing_profile, get_firing_profile
from ..models.firing_model import FiringOptions

router = APIRouter()

@router.post("/firing/")
async def create_firing_option(firing_option: FiringOptions):
    save_firing_profile(firing_option.dict())
    return {"message": "Firing option created"}
