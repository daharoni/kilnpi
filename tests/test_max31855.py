import unittest
from app.hardware.max31855 import MAX31855

class MockTestSPI:
    def __init__(self, response):
        self.response = response  # Predefined 32-bit string as a list of 4 bytes
    
    def xfer2(self, _):
        return self.response  # Return the predefined response regardless of input
    
    def open(self, bus, device):
        pass  # No action needed for mock
    
    def close(self):
        pass  # No action needed for mock
    
class TestMAX31855(unittest.TestCase):
    def test_temperature_conversion(self):
        # Example 32-bit response: 0xFA000000 (binary: 11111010000000000000000000000000)
        # This could represent a specific temperature, depending on your conversion logic.
        mock_spi = MockTestSPI(response=[0x05, 0x00, 0x00, 0x00])
        
        # Replace SPIDevice's SPI device with MockSPI
        max31855 = MAX31855(spi_device=mock_spi, bus=0, device=0)
        
        temperature, _ = max31855.read_temperature()
        # Verify the temperature is correctly interpreted (adjust the expected value)
        self.assertEqual(temperature, 80.0)  # Example expected value

    def test_fault_detection(self):
        # Example 32-bit response indicating a fault: 0x00000001
        mock_spi = MockTestSPI(response=[0x00, 0x01, 0x00, 0x01])
        
        # Replace SPIDevice's SPI device with MockSPI
        max31855 = MAX31855(spi_device=mock_spi, bus=0, device=0)
        
        _, faults = max31855.read_temperature()
        # Verify the fault is detected (adjust based on your fault detection logic)
        self.assertTrue(faults['open_circuit'])  # Example fault check

if __name__ == '__main__':
    unittest.main()
