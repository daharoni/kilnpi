from pydantic import BaseModel

class FiringOptions(BaseModel):
    profile_name: str
    temperature_target: float
    hold_time: int

class FiringProfile(BaseModel):
    id: int
    name: str
    temperature_target: float  # Target temperature in degrees Celsius
    hold_time: int  # Hold time at target temperature in minutes
    ramp_up_rate: float = None  # Degrees Celsius per hour (optional)
    ramp_down_rate: float = None  # Degrees Celsius per hour (optional)

    class Config:
        orm_mode = True
