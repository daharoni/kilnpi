from datetime import datetime
from app.models.kiln_model import KilnParameters
import logging

logger = logging.getLogger("logger")

class PIDController:
    def __init__(self, kiln_params: KilnParameters):
        self.pid_params = kiln_params.pid_parameters
        self.last_time = None
        self.previous_error = None
        self.integral = 0

    def compute(self, setpoint, measured_value, current_time: datetime):
        global logger
        
        error = setpoint - measured_value
        if self.last_time:
            # run the PID step only after known the propoer time and error from first attemp at running compute
            
            delta_time = current_time - self.last_time
            delta_time = delta_time.total_seconds()
            if (delta_time > 0):
                delta_error = error - self.previous_error
                self.integral += error * delta_time
                derivative = delta_error / delta_time
                output = self.pid_params.Kp * error + self.pid_params.Ki * self.integral + self.pid_params.Kd * derivative

                # Limit output to min and max values
                output = max(self.pid_params.min_duty_cycle, min(output, self.pid_params.max_duty_cycle))

                self.previous_error = error
                self.last_time = current_time
                
                logger.info(f"PID Controller: kiln_temp= {measured_value}, setpoint= {setpoint}, duty cyle= {output}, p= {error}, i= {self.integral}, d= {derivative}")
                return output
            else:
                return None
        else:
            self.previous_error = error
            self.last_time = current_time
            return None
