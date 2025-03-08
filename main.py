import os
from approxeng.input.selectbinder import ControllerResource
import subprocess
import time
import math
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from icm20948 import ICM20948
import board
import busio

pcaServo = ServoKit(channels=16)

# Set up I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # Set the PWM frequency

imu = ICM20948()

def deadzone(number):
    if abs(number) < 0.005:  # Deadzone range (-0.005, 0.005)
        return 0
    return number

def pwm(channel, speed):
    """
    Set the motor speed on the given channel (0–15).
    Speed range: 0 (off) to 65535 (full speed)
    """
    pwm_value = int(speed * 65535)  # Convert speed to PWM range (0-65535)
    if pwm_value > 65535:
        print(f"ERROR: PWM VALUE SURPASSES MAX ALLOWED: {pwm_value}")
        pwm_value = 65535
    pca.channels[channel].duty_cycle = pwm_value

def setMotors(lr, fb, r):
    m1 = fb + lr + r
    m2 = fb - lr - r
    m3 = fb - lr + r
    m4 = fb + lr - r

    m1 = min(m1, 1)
    m2 = min(m2, 1)
    m3 = min(m3, 1)
    m4 = min(m4, 1)

    if m1 > 0:
        pwm(1, m1)
    elif m1 < 0:
        pwm(0, abs(m1))
    else:
        pwm(0, 0)
        pwm(1, 0)

    if m2 > 0:
        pwm(2, m2)
    elif m2 < 0:
        pwm(3, abs(m2))
    else:
        pwm(2, 0)
        pwm(3, 0)

    if m3 > 0:
        pwm(5, m3)
    elif m3 < 0:
        pwm(4, abs(m3))
    else:
        pwm(4, 0)
        pwm(5, 0)

    if m4 > 0:
        pwm(6, m4)
    elif m4 < 0:
        pwm(7, abs(m4))
    else:
        pwm(6, 0)
        pwm(7, 0)

    #print(m1, m2, m3, m4)

def setServos(x, y):
    s1, s2 = ik(x, y)
    if any(x is not None for x in [s1, s2]):
        
        pcaServo.servo[8].angle = s1
        pcaServo.servo[9].angle = s2
    else:    
        print("Target arm out of reach!")

def heading():
    global amin, amax  # Ensure these are properly referenced
    current_heading = 0  # Avoid overwriting the function name

    # Read magnetometer data
    mag = list(imu.read_magnetometer_data())

    # Calibrate magnetometer values
    for i in range(3):
        v = mag[i]

        # Update calibration values
        if v < amin[i]:
            amin[i] = v
        if v > amax[i]:
            amax[i] = v

        # Normalize magnetometer readings
        mag[i] -= amin[i]
        try:
            mag[i] /= amax[i] - amin[i]
        except ZeroDivisionError:
            pass

        mag[i] -= 0.5  # Center values around 0

    # Calculate heading
    current_heading = math.atan2(mag[AXES[0]], mag[AXES[1]])

    # Convert to degrees and ensure positive value
    if current_heading < 0:
        current_heading += 2 * math.pi
    current_heading = round(math.degrees(current_heading))
    return current_heading  # Return the heading value

def calibrate():
    global AXES, amin, amax
    AXES = [1, 2]  # Y, Z axes

    amin = list(imu.read_magnetometer_data())
    amax = list(imu.read_magnetometer_data())

    pcaServo.servo[8].angle = 90
    pcaServo.servo[9].angle = 90
    
    setMotors(0, 0, 0.5)
    time.sleep(2)
    setMotors(0, 0, 0)

def ik(x, y, l1=70, l2=100):
    """
    Computes inverse kinematics for a 2DOF robot arm with servo constraints.
    :param x: Target x position
    :param y: Target y position
    :param l1: Length of the first arm segment
    :param l2: Length of the second arm segment
    :return: Tuple of (theta1, theta2) in degrees, or None if unreachable
    """
    dist_sq = x**2 + y**2
    if dist_sq > (l1 + l2) ** 2:
        return None  # Target is out of reach
    
    cos_theta2 = (dist_sq - l1**2 - l2**2) / (2 * l1 * l2)
    if abs(cos_theta2) > 1:
        return None  # No valid solution
    
    sin_theta2 = math.sqrt(1 - cos_theta2**2)  # Elbow-down solution
    theta2 = math.atan2(sin_theta2, cos_theta2)
    
    k1 = l1 + l2 * cos_theta2
    k2 = l2 * sin_theta2
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)
    
    theta1 = round(math.degrees(theta1) + 90)  # Shift 90° to make middle of servo 90°
    theta2 = round(math.degrees(theta2) + 90)
    
    # Constrain angles to 0 - 180 degrees
    theta1 = max(0, min(180, theta1))
    theta2 = max(0, min(180, theta2))
    
    return theta1, theta2

def main():
    armx = -170
    army = 0
    
    speed = 1
    zl = zr = 0

    global X, Y, Z
    X, Y, Z = 0, 1, 2
    
    print("Starting headless joystick controller...")
  
    with ControllerResource() as controller:
        print('Controller connected!')
        while controller.connected:
            presses = controller.check_presses()
            # Reading the left joystick's X and Y axes
            lr = controller['lx']  # Left X axis (lr)
            fb = controller['ly']  # Left Y axis (fb)
            du, dd, dl, dr = controller['triangle', 'cross', 'square', 'circle']
        
            # Reading the right joystick's X axis
            r = controller['rx']  # Right X axis (r)
        
            # Checking the left and right trigger buttons (zl and zr)
            zl = controller['l2']
            zr = controller['r2']
                
            lr = deadzone(min(lr, 1)) * speed
            fb = deadzone(min(fb, 1)) * speed
            r = deadzone(min(r, 1)) * speed 

            """Adjusts the speed based on joystick button inputs."""

            if zl is not None:
                speed -= 0.05
            if zr is not None:
                speed += 0.05
                
            if any(x is not None for x in [du, dd, dl, dr]):
                if du is not None:
                    army += 0.5
                    army = round(army)
                if dd is not None:
                    army -= 0.5
                    army = round(army)
                if dl is not None:
                    armx -= 0.5
                    armx = round(armx)
                if dr is not None:
                    armx += 0.5
                    armx = round(armx)

            speed = max(0, min(2, speed))
            #print(speed)

            setMotors(lr, fb, r)
            setServos(armx, army)
            ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

            print(dup, ddown, dleft, dright)
    
            dir = heading()
            #print(dir)

            time.sleep(0.05)

if __name__ == "__main__":
    calibrate()
    main()
