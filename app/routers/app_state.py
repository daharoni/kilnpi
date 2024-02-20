from fastapi import APIRouter
from app.models.app_state_model import AppState

# Assuming this is stored in a more persistent manner, e.g., database
router = APIRouter()

current_state = AppState()

@router.get("/state/")
async def get_state():
    global current_state
    return current_state

@router.post("/update_state/")
async def update_state(state: AppState):
    global current_state
    current_state = state
    print(current_state)
    return {"message": "State updated successfully."}