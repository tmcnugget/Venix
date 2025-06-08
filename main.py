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

mode = 0

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

    m1 = max(-1, min(m1, 1))
    m2 = max(-1, min(m2, 1))
    m3 = max(-1, min(m3, 1))
    m4 = max(-1, min(m4, 1))


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
    pcaServo.servo[8].angle = x
    pcaServo.servo[9].angle = y

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

def main():
    global mode
    
    armx = 90
    army = 90

    abal0 = 90
    abal1 = 0
    
    speed = 1
    zl = 0
    zr = 0

    global X, Y, Z
    X, Y, Z = 0, 1, 2
    
    print("Starting headless joystick controller...")
  
    with ControllerResource() as controller:
        print('Controller connected!')
        while controller.connected:

            s, l1, r1 = controller['select', 'l1', 'r1']
            
            presses = controller.check_presses()
            if s and r1:
                mode = min(2, mode + 1)

            elif s and l1:
                mode = max(0, mode - 1)
                
            # Reading the left joystick's X and Y axes
            lr = controller['lx']  # Left X axis (lr)
            fb = controller['ly']  # Left Y axis (fb)
            du, dd, dl, dr = controller['triangle', 'cross', 'square', 'circle']

            lx = controller['lx']
            ly = controller['ly']
            rx = controller['rx']
            ry = controller['ry']
            
            
            # Reading the right joystick's X axis
            r = controller['rx']  # Right X axis (r)
        
            # Checking the left and right trigger buttons (zl and zr)
            zl = controller['l2']
            zr = controller['r2']
                
            lr = deadzone(min(lr, 1)) * speed
            fb = deadzone(min(fb, 1)) * speed
            r = deadzone(min(r, 1)) * speed 
            speed = max(0, min(2, speed))

            if mode == 0 or mode == 1:
                if zl is not None:
                    speed -= 0.05
                if zr is not None:
                    speed += 0.05
                setMotors(lr, fb, r)
            
            if mode == 1:
                if any(x is not None for x in [du, dd, dl, dr]):
                    if du is not None:
                        army -= 10
                    if dd is not None:
                        army += 10
                    if dl is not None:
                        armx += 10
                    if dr is not None:
                        armx -= 10
                    armx = max(0, min(armx, 180))
                    army = max(0, min(army, 180))
                    setServos(armx, army)

            if mode == 2:
                if any(x is not None for x in [lx, ly, rx, ry]):
                    abal0 += lx * 3
                    abal1 += ly * 3
                    abal0 -= rx
                    abal1 += ry
                    abal0 = max(0, min(abal0, 180))
                    abal1 = max(0, min(abal1, 90))
                setServos(abal0, abal1)
            
            ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    
            dir = heading()
            #print(dir)

            print(abal0, abal1)

            time.sleep(0.05)

if __name__ == "__main__":
    calibrate()
    main()
