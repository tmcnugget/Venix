from smbus2 import SMBus

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
   
    def pwm(self, channel, pwm_value):
        if pwm_value < 0 or pwm_value > 1:
            raise ValueError("PWM value must be between 0 and 1.")

        # Convert the pwm_value to a 12-bit PWM duty cycle (0 to 4095)
        on_time = 0
        off_time = int(pwm_value * 4095 / 10000)  # 12-bit resolution

        self.setPWM(channel, on_time, off_time)

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

m1 = float(sys.argv[1])
m2 = float(sys.argv[2])
m3 = float(sys.argv[3])
m4 = float(sys.argv[4])

if m1 > 0:
    pwm.pwm(0, m1)
else:
    pwm.pwm(1, abs(m1))

if m2 > 0:
    pwm.pwm(2, m2)
else:
    pwm.pwm(3, abs(m2))

if m3 > 0:
    pwm.pwm(4, m3)
else:
    pwm.pwm(5, abs(m3))

if m4 > 0:
    pwm.pwm(6, m4)
else:
    pwm.pwm(7, abs(m4))
