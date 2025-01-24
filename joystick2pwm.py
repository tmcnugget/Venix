import sys
from pca9685 import PCA9685

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

speed = 1

def main():
    getSpeed()
    calculateMotors()  
    setPWM(m1, m2, m3, m4)

def setPWM(*motors):
    for i, m in enumerate(motors):
        if m >= 0:
            pwm.setPWM(i * 2, m)
        else:
            pwm.setPWM(i * 2 + 1, abs(m))

def getSpeed():
    speed = max(0, min(speed + float(sys.argv[4])/10 - float(sys.argv[5])/10, 2))

def calculateMotors():
    lr = float(sys.argv[1])/2 * speed
    fb = float(sys.argv[2])/2 * speed
    r = float(sys.argv[3])/2 * speed

    m1 = fb + lr + r
    m2 = fb - lr - r
    m3 = fb - lr + r
    m4 = fb + lr - r

if __name__ == "__main__":
    main()
