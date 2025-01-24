class MDD3A:
    from pca9685 import PCA9685

    def __init__(self, address=0x40, frequency=50):
        self.pwm = self.PCA9685(address)
        self.pwm.setPWMFreq(frequency)
        self.speed = 1
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0

    def pwm(self, *motors):
        for i, m in enumerate(motors):
            if m >= 0:
                self.pwm.pwm(i * 2, m)
            else:
                self.pwm.pwm(i * 2 + 1, abs(m))

    def getSpeed(self, increment, decrement):
        self.speed = max(0, min(self.speed + increment/10 - decrement/10, 2))

    def calculateMotors(self, speed, lr, fb, r):
        # Scale the input values with speed
        lr_scaled = lr / 2 * speed
        fb_scaled = fb / 2 * speed
        r_scaled = r / 2 * speed

        # Calculate motor values and store them as instance attributes
        self.m1 = fb_scaled + lr_scaled + r_scaled
        self.m2 = fb_scaled - lr_scaled - r_scaled
        self.m3 = fb_scaled - lr_scaled + r_scaled
        self.m4 = fb_scaled + lr_scaled - r_scaled

        return self.m1, self.m2, self.m3, self.m4

    def setMotors(self, m1, m2, m3, m4):
        self.setPWM(m1, m2, m3, m4)
