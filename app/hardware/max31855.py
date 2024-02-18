from .spi_devices import SPIDevice

class MAX31855(SPIDevice):
    def __init__(self, spi_device, bus, device):
        super().__init__(spi_device, bus, device, max_speed_hz=5000000, mode=0b00)

    def read_raw_data(self):
        """Read the raw 32-bit data from the MAX31855 sensor."""
        raw_data = self.read_bytes(4)
        return raw_data[0] << 24 | raw_data[1] << 16 | raw_data[2] << 8 | raw_data[3]

    def read_temperature(self):
        """Read the thermocouple temperature data from the MAX31855 sensor."""
        value = self.read_raw_data()
        
        # Check for fault bit (D16)
        if value & 0x00010000:
            return None, self.read_faults(value)
        
        # Process the temperature reading
        if value & 0x80000000:
            # Negative temperature
            value = 0xFFFFC000 | (value >> 18)
        else:
            # Positive temperature
            value = value >> 18
        temperature = value * 0.25
        return temperature, None

    def read_faults(self, raw_value=None):
        """Read and interpret fault bits from the MAX31855 sensor."""
        if raw_value is None:
            raw_value = self.read_raw_data()
        
        faults = {
            "open_circuit": bool(raw_value & 0x01),
            "short_to_gnd": bool(raw_value & 0x02),
            "short_to_vcc": bool(raw_value & 0x04)
        }
        return faults

    def read_internal_temperature(self):
        """Read the internal reference temperature from the MAX31855."""
        value = self.read_raw_data()
        # Extract internal temperature from D15-D4, ignoring fault bits
        internal_temp = ((value >> 4) & 0xFFF) * 0.0625
        if value & 0x8000:  # Check if D15 is set indicating negative temperature
            internal_temp = -((~internal_temp & 0xFFF) + 1)
        return internal_temp
