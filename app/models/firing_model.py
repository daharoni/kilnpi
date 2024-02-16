from pydantic import BaseModel

class FiringOptions(BaseModel):
    profile_name: str
    temperature_target: float
    hold_time: int
