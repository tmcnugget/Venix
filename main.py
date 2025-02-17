import os
import pygame
import subprocess
import time
import math
from adafruit_pca9685 import PCA9685
from icm20948 import ICM20948
import board
import busio

# Set the SDL video driver to dummy for headless operation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Set up I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # Set the PWM frequency

imu = ICM20948()

# A dictionary to keep track of connected joysticks
joysticks = {}

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

    print(m1, m2, m3, m4)

def heading():
    global heading
    
    # Read the current, uncalibrated, X, Y & Z magnetic values from the magnetometer and save as a list
    mag = list(imu.read_magnetometer_data())

    # Step through each uncalibrated X, Y & Z magnetic value and calibrate them the best we can
    for i in range(3):
        v = mag[i]
        
        # If our current reading (mag) is less than our stored minimum reading (amin), then save a new minimum reading
        # ie save a new lowest possible value for our calibration of this axis
        if v < amin[i]:
            amin[i] = v
            
        # If our current reading (mag) is greater than our stored maximum reading (amax), then save a new maximum reading
        # ie save a new highest possible value for our calibration of this axis
        if v > amax[i]:
            amax[i] = v

        # Calibrate value by removing any offset when compared to the lowest reading seen for this axes
        mag[i] -= amin[i]

        # Scale value based on the highest range of values seen for this axes
        # Creates a calibrated value between 0 and 1 representing magnetic value
        try:
            mag[i] /= amax[i] - amin[i]
        except ZeroDivisionError:
            pass
        # Shift magnetic values to between -0.5 and 0.5 to enable the trig to work
        mag[i] -= 0.5

    # Convert from Gauss values in the appropriate 2 axis to a heading in Radians using trig
    # Note this does not compensate for tilt
    heading = math.atan2(
            mag[AXES[0]],
            mag[AXES[1]])

    # If heading is negative, convert to positive, 2 x pi is a full circle in Radians
    if heading < 0:
        heading += 2 * math.pi

    # Convert heading from Radians to Degrees
    heading = math.degrees(heading)
    # Round heading to nearest full degree
    heading = round(heading)

def calibrate:
    global AXES = Y, Z

    amin = list(imu.read_magnetometer_data())
    amax = list(imu.read_magnetometer_data())

    setMotors(0, 0, 0.5)
    time.sleep(5)
    setMotors(0, 0, 0)

def main():
    speed = 1
    zl = 0
    zr = 0

    global X = 0
    global Y = 1
    global Z = 2

    heading()
    
    print("Starting headless joystick controller...")

    # Main loop
    try:
        while True:
            # Process joystick events
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    # A new joystick has been connected
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connected")

                if event.type == pygame.JOYDEVICEREMOVED:
                    # A joystick has been disconnected
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")

            for joystick in joysticks.values():
                lr = deadzone(round(joystick.get_axis(0), 3)) / 2 * speed # Left/Right
                fb = deadzone(round(joystick.get_axis(1), 3)) / 2 * speed # Up/Down
                r = -deadzone(round(joystick.get_axis(2), 3)) / 2 * speed # Rotate

                lr = min(lr, 1)
                fb = min(fb, 1)
                r = min(r, 1)

                zl = joystick.get_button(6)
                zr = joystick.get_button(7)
                
            ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    
            temperature = icm20948.read_temperature()
            round(temperate, 2)

            """Adjusts the speed based on joystick button inputs."""
            if zr == 1:
                speed += 0.02
            elif zl == 1:
                speed -= 0.02

            speed = max(0, min(2, speed))

            setMotors(lr, fb, r)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    calibrate()
    main()
