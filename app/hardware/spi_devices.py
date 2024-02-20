import os
import sys

if (os.name == 'posix' and not os.getenv('CI')):
    try:
        import spidev
        spi_device_class = spidev.SpiDev
    except ImportError:
        print("spidev module not found, ensure you're running on Raspberry Pi with spidev installed.")
        sys.exit(1)
else:
    # Mock spidev for non-POSIX systems (like Windows)
    class MockSPI:
        def __init__(self,spi_response=[0x01, 0x00, 0x00, 0x00]):
            self.spi_response = spi_response
            
        def open(self, bus, device):
            pass
        def xfer2(self, data):
            # Return mock data appropriate for your application
            self.spi_response[0] += 1
            if (self.spi_response[0] > 100):
                self.spi_response[0] = 1
            return self.spi_response
        def close(self):
            pass
    spidev = MockSPI()
    spi_device_class = MockSPI

class SPIDevice:
    def __init__(self, spi_device, bus, device, max_speed_hz=5000000, mode=0b00):
        if callable(spi_device):
            self.spi = spi_device()  # If spi_device is a class, instantiate it
        else:
            self.spi = spi_device  # Use the spi_device instance directly
        # The rest of your initialization code
        self.bus = bus
        self.device = device
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode

    def read_bytes(self, num_bytes):
        """Read a specified number of bytes from SPI."""
        return self.spi.xfer2([0x00] * num_bytes)

    def close(self):
        """Close the SPI connection."""
        self.spi.close()
