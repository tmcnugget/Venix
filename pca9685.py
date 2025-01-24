from smbus2 import SMBus
import time
import math

class PCA9685:
    _SUBADR1 = 0x02
    _SUBADR2 = 0x03
    _SUBADR3 = 0x04
    _MODE1 = 0x00
    _PRESCALE = 0xFE
    _LED0_ON_L = 0x06
    _LED0_ON_H = 0x07
    _LED0_OFF_L = 0x08
    _LED0_OFF_H = 0x09
    _ALLLED_ON_L = 0xFA
    _ALLLED_ON_H = 0xFB
    _ALLLED_OFF_L = 0xFC
    _ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.bus = SMBus(1)
        self.address = address
        self.debug = debug
        self.write(self._MODE1, 0x00)

    def write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def read(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def setPWMFreq(self, freq):
        prescaleval = 25000000.0 / 4096.0 / float(freq) - 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = self.read(self._MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.write(self._MODE1, newmode)
        self.write(self._PRESCALE, prescale)
        self.write(self._MODE1, oldmode)
        time.sleep(0.005)
        self.write(self._MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        self.write(self._LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self._LED0_ON_H + 4 * channel, on >> 8)
        self.write(self._LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self._LED0_OFF_H + 4 * channel, off >> 8)
   
    def pwm(self, channel, value):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Value must be between 0.0 and 1.0")
        pulse = int(value * (self.PWM_RESOLUTION - 1))  # Map to 0-4095
        self.setPWM(channel, 0, pulse)

    def write(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
