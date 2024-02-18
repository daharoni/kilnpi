import os
import sys

if os.name == 'posix':
    try:
        import spidev
    except ImportError:
        print("spidev module not found, ensure you're running on Raspberry Pi with spidev installed.")
        sys.exit(1)
else:
    # Mock spidev for non-POSIX systems (like Windows)
    class MockSPI:
        def open(self, bus, device):
            pass
        def xfer2(self, data):
            # Return mock data appropriate for your application
            return [0x00, 0x00, 0x00, 0x00]
        def close(self):
            pass
    spidev = MockSPI()

class SPIDevice:
    def __init__(self, bus, device, max_speed_hz=5000000, mode=0b00):
        self.spi = spidev.SpiDev()
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
