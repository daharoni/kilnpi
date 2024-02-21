import logging
from fastapi import APIRouter, Body
from app.models.app_state_model import AppState
from app.services.profiles import updateProfile
from datetime import datetime
from database import add_new_firing
from app.utils.global_state import get_temperature

# Assuming this is stored in a more persistent manner, e.g., database
router = APIRouter()
logger = logging.getLogger("logger")

current_state = AppState()

@router.get("/state/")
async def get_state():
    global current_state
    global logger
    
    logger.info(current_state)
    return current_state

@router.post("/update_state/")
async def update_state(state: AppState):
    global current_state
    global logger
    
    current_state = state
    logger.info(current_state)
    # print(current_state)
    return {"message": "State updated successfully."}

@router.get("/firingStartTimestamp/")
def get_firingStartTimestamp():
    return {"firingStartTime": current_state.startFiringTime.isoformat()}

@router.post("/start-firing/")
def start_firing(body: dict = Body(...)):
    current_state.firingName = body['firingName']
    add_new_firing(current_state.firingName) # addes a new db entry for tracking this firing
    # TODO: start db logging and PID and GPIO control of relays
    current_state.isFiring = True
    current_state.startFiringTime = datetime.now()
    current_state.startFiringTemperatureData = get_temperature()
    print("Firing process started.")
    return {"firingStartTime": current_state.startFiringTime.isoformat()}

@router.post("/abort-firing/")
def abort_firing():
    current_state.isFiring = False
    print("Firing process aborted.")
    return {"message": "Firing process aborted successfully."}

@router.post("/dry-change/")
async def dry_state_change(body: dict = Body(...)):
  
    
    current_state.isDry = body['isDry']
    profileToPlot = await updateProfile(current_state)
    return profileToPlot

@router.post("/soak-change/")
async def soak_state_change(body: dict = Body(...)):

    
    current_state.isSoak = body['isSoak']
    profileToPlot = await updateProfile(current_state)
    return profileToPlot
