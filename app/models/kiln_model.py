from pydantic import BaseModel

class PWMSettings(BaseModel):   
    period: float

class PIDParameters(BaseModel):
    Kp: float
    Ki: float
    Kd: float
    period: float
    min_duty_cycle: float
    max_duty_cycle: float

class SafetyParameters(BaseModel):
    max_temperature: int
    temperature_threshold_for_alert: int
    
class SensorParameters(BaseModel):
    temperature_sampling_period: float
    
class KilnParameters(BaseModel):
    kiln_name: str
    pid_parameters: PIDParameters
    pwm_settings: PWMSettings
    safety_parameters: SafetyParameters
    sensor_parameters: SensorParameters
    notes: str
