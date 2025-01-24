class MDD3A:
    from pca9685 import PCA9685

    def __init__(self, address=0x40, frequency=50):
        self.pca9685 = self.PCA9685(address)
        self.pca9685.setPWMFreq(frequency)
        self.speed = 1
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0

    def pwm(self, m1, m2, m3, m4):
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

    def calculateMotors(self, speed, lr, fb, r):

        # Calculate motor values and store them as instance attributes
        self.m1 = fb / 2 * speed + lr / 2 * speed + r / 2 * speed
        self.m2 = fb / 2 * speed - lr / 2 * speed - r / 2 * speed
        self.m3 = fb / 2 * speed - lr / 2 * speed + r / 2 * speed
        self.m4 = fb / 2 * speed + lr / 2 * speed - r / 2 * speed

        return self.m1, self.m2, self.m3, self.m4

    def setMotors(self, m1, m2, m3, m4):
        self.pwm(m1, m2, m3, m4)
