from datetime import datetime
from app.models.kiln_model import KilnParameters

class PIDController:
    def __init__(self, kiln_params: KilnParameters):
        self.Kp = kiln_params.pid_parameters.Kp
        self.Ki = kiln_params.pid_parameters.Ki
        self.Kd = kiln_params.pid_parameters.Kd
        self.min_output = kiln_params.pwm_settings.min_duty_cycle
        self.max_output = kiln_params.pwm_settings.max_duty_cycle
        self.pwm_period = kiln_params.pwm_settings.period
        self.previous_error = 0
        self.integral = 0
        self.last_time = datetime.now()

    def compute(self, setpoint, measured_value):
        error = setpoint - measured_value
        current_time = time.time()
        delta_time = current_time - self.last_time
        delta_error = error - self.previous_error

        if delta_time >= self.pwm_period:
            self.integral += error * delta_time
            derivative = delta_error / delta_time
            output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

            # Limit output to min and max values
            output = max(self.min_output, min(output, self.max_output))

            self.previous_error = error
            self.last_time = current_time

            return output
        else:
            return None
