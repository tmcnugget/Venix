from pca9685 import PCA9685

class MDD3A:

    def __init__(self, address=0x40, frequency=50):
        self.pca9685 = PCA9685(address)  # Changed to instance attribute
        self.pca9685.setPWMFreq(frequency)

    def pwm(self, m1, m2, m3, m4):  # Added self parameter
        if m1 >= 0:
            self.pca9685.pwm(0, m1)
        else:
            self.pca9685.pwm(1, abs(m1))

        if m2 >= 0:
            self.pca9685.pwm(2, m2)
        else:
            self.pca9685.pwm(3, abs(m2))

        if m3 >= 0:
            self.pca9685.pwm(4, m3)
        else:
            self.pca9685.pwm(5, abs(m3))

        if m4 >= 0:
            self.pca9685.pwm(6, m4)
        else:
            self.pca9685.pwm(7, abs(m4))

    def setMotors(self, lr, fb, r):  # Added self parameter
        # Calculate motor values and store them as instance attributes
        m1 = fb + lr + r
        m2 = fb - lr - r
        m3 = fb - lr + r
        m4 = fb + lr - r

        self.pwm(m1, m2, m3, m4)
