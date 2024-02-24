import logging
import json
from fastapi import APIRouter, Body
from app.models.app_state_model import AppState
from app.services.profiles import updateProfile
from datetime import datetime
from app.utils.global_state import get_temperature
from app.models.kiln_model import KilnParameters

# Assuming this is stored in a more persistent manner, e.g., database
router = APIRouter()
logger = logging.getLogger("logger")

current_state = AppState()


def get_kiln_parameters() -> KilnParameters:
    """
    Load firing profiles from a JSON file and return them as a list of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing firing profiles.
    """
    global logger
    
    try:
        with open('data/kiln_parameters.json') as f:
            data = json.load(f)
        
            # Parse the JSON data into a Pydantic model
            kiln_params = KilnParameters.model_validate(data)
            logger.info(f"Read kiln parameters file: {kiln_params}")
            return kiln_params
    except IOError as e:
        logger.error(f"Error opening or reading the kiln parameter file: {e}")
        return None
    
@router.get("/state/")
async def get_state():
    global current_state
    global logger
    
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
    global current_state
    
    return {"firingStartTime": current_state.startFiringTime.isoformat()}

@router.post("/start-firing/")
def start_firing(body: dict = Body(...)):
    global current_state
    
    current_state.firingName = body['firingName']
    # TODO: start db logging and PID and GPIO control of relays
    current_state.isFiring = True
    current_state.startFiringTime = datetime.now()
    current_state.startFiringTemperatureData = get_temperature()
    print("Firing process started.")
    return {"firingStartTime": current_state.startFiringTime.isoformat()}

@router.post("/abort-firing/")
def abort_firing():
    global current_state
    
    current_state.isFiring = False
    print("Firing process aborted.")
    return {"message": "Firing process aborted successfully."}

@router.post("/dry-change/")
async def dry_state_change(body: dict = Body(...)):
    global current_state
    
    current_state.isDry = body['isDry']
    profileToPlot = await updateProfile(current_state)
    current_state.firingProfile = profileToPlot
    return profileToPlot

@router.post("/soak-change/")
async def soak_state_change(body: dict = Body(...)):
    global current_state
    
    current_state.isSoak = body['isSoak']
    profileToPlot = await updateProfile(current_state)
    current_state.firingProfile = profileToPlot
    return profileToPlot

@router.post("/hold-change/")
async def dry_state_change(body: dict = Body(...)):
    global current_state
    
    current_state.isHold = body['isHold']
    profileToPlot = await updateProfile(current_state)
    current_state.firingProfile = profileToPlot
    return profileToPlot
