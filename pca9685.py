class PCA9685:
    import smbus2
    def __init__(self, address, bus=None):
        self.address = address
        self.bus = smbus.SMBus(1) if bus is None else bus
        self.write(PCA9685_MODE1, 0x00)  # Initialize
        self.PWM_RESOLUTION = 4096  # 12-bit resolution (0 to 4095)
    
    def setPWMFreq(self, freq):
        prescale_value = int(round(25000000.0 / (4096.0 * freq)) - 1)
        self.write(PCA9685_MODE1, 0x10)  # Go to sleep
        self.write(PCA9685_PRESCALE, prescale_value)
        self.write(PCA9685_MODE1, 0x00)
        time.sleep(0.005)
        self.write(PCA9685_MODE1, 0x80)

    def setPWM(self, channel, on, off):
        self.write(LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(LED0_ON_H + 4 * channel, on >> 8)
        self.write(LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(LED0_OFF_H + 4 * channel, off >> 8)

    def pwm(self, channel, value):
        """Set PWM using a normalized value (0.0 to 1.0)."""
        if not 0.0 <= value <= 1.0:
            raise ValueError("Value must be between 0.0 and 1.0")
        pulse_length = int(value * (self.PWM_RESOLUTION - 1))  # Map to 0-4095
        self.setPWM(channel, 0, pulse_length)

    def write(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
