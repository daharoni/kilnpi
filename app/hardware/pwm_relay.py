import os
import sys
import logging

logger = logging.getLogger("logger")

if (os.name == 'posix' and not os.getenv('CI')):
    try:
        import RPi.GPIO as GPIO
        gpio_class = GPIO
    except ImportError:
        logger.critical("RPi.GPIO module not found, ensure you're running on Raspberry Pi with python3-rpi.gpio installed.")
        sys.exit(1)
else:
    # Mock GPIO for non-POSIX systems (like Windows
    class MockGPIO:
        # Constants to mimic RPi.GPIO constants
        BCM = 'BCM'
        BOARD = 'BOARD'
        OUT = 'OUT'
        IN = 'IN'
        HIGH = True
        LOW = False
        PUD_UP = 'PUD_UP'
        PUD_DOWN = 'PUD_DOWN'
        
        # To store the state of each pin
        pin_states = {}
        pin_modes = {}
        pin_pull_up_down = {}
    
        @staticmethod
        def setmode(mode):
            print(f"GPIO mode set to {mode}")
        
        @staticmethod
        def setup(pin, mode, pull_up_down=None):
            MockGPIO.pin_modes[pin] = mode
            if pull_up_down is not None:
                MockGPIO.pin_pull_up_down[pin] = pull_up_down
            print(f"Pin {pin} set up as {mode} with pull up/down {pull_up_down}")
        
        @staticmethod
        def output(pin, state):
            MockGPIO.pin_states[pin] = state
            print(f"Pin {pin} output set to {state}")
        
        @staticmethod
        def input(pin):
            # Simulate pin input; return a mock state
            state = MockGPIO.pin_states.get(pin, MockGPIO.LOW)
            print(f"Reading {state} from pin {pin}")
            return state
        
        @staticmethod
        def cleanup():
            MockGPIO.pin_states.clear()
            MockGPIO.pin_modes.clear()
            MockGPIO.pin_pull_up_down.clear()
            print("GPIO cleanup called - GPIO state cleared")
        
        @staticmethod
        def setwarnings(flag):
            print(f"GPIO warnings {'enabled' if flag else 'disabled'}")
        
        @staticmethod
        def PWM(pin, frequency):
            # This is a simplified mock; expand as needed
            print(f"Mock PWM on pin {pin} with frequency {frequency}Hz initialized")
            return MockPWM(pin, frequency)

    class MockPWM:
        def __init__(self, pin, frequency):
            self.pin = pin
            self.frequency = frequency
            self.duty_cycle = 0
            print(f"Initializing MockPWM on pin {self.pin} with frequency {self.frequency}Hz")
        
        def start(self, duty_cycle):
            self.duty_cycle = duty_cycle
            print(f"MockPWM started on pin {self.pin} with duty cycle {self.duty_cycle}%")
        
        def ChangeDutyCycle(self, duty_cycle):
            self.duty_cycle = duty_cycle
            print(f"MockPWM duty cycle changed on pin {self.pin} to {self.duty_cycle}%")
        
        def stop(self):
            print(f"MockPWM stopped on pin {self.pin}")

        
    gpio_class = MockGPIO
    
class PWMRelay:
    def __init__(self, gpio_class, pin, frequency):
        if callable(gpio_class):
            self.GPIO = gpio_class()  # If spi_device is a class, instantiate it
        else:
            self.GPIO = gpio_class  # Use the spi_device instance directly
        # The rest of your initialization code
        self.pin = pin
        self.frequency = frequency
        self.pwm = None
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(pin, self.GPIO.OUT)

    def start(self, duty_cycle):
        if self.pwm is None:
            self.pwm = self.GPIO.PWM(self.pin, self.frequency)
            self.pwm.start(duty_cycle)
        else:
            self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Kiln started with duty cycle {duty_cycle}%")

    def stop(self):
        if self.pwm:
            self.pwm.stop()
            self.pwm = None
        print("Kiln PWM relay controller stopped")

    def cleanup(self):
        self.GPIO.cleanup(self.pin)
        print("GPIO cleanup for kiln PWM relay controller")
