from pydantic import BaseModel

class PWMSettings(BaseModel):
    min_duty_cycle: float
    max_duty_cycle: float
    period: float

class PIDParameters(BaseModel):
    Kp: float
    Ki: float
    Kd: float

class SafetyParameters(BaseModel):
    max_temperature: int
    temperature_threshold_for_alert: int
    
class KilnParameters(BaseModel):
    kiln_name: str
    pid_parameters: PIDParameters
    pwm_settings: PWMSettings
    safety_parameters: SafetyParameters
    notes: str