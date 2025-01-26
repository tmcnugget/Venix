import os
from multiprocessing import Process, Value
import pygame
import time
from adafruit_pca9685 import PCA9685
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

lr = 0.0
fb = 0.0
r = 0.0

def setVars():
    lr.value = lr
    fb.value = fb
    r.value = r

def main():
    speed = 1
    
    print("Starting headless joystick controller...")

    # Shared float variables (using double precision 'd')
    fb = Value('d', 0.0)   # 'd' for double precision float
    lr = Value('d', 0.0)
    r = Value('d', 0.0)

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
                    
                zl = joystick.get_button(6)
                zr = joystick.get_button(7)

                """Adjusts the speed based on joystick button inputs."""
                if zr == 1:
                    speed += 0.02
                elif zl == 1:
                    speed -= 0.02

            speed = max(0, min(2, speed))

            setMotors(lr, fb, r)

            setVars()

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()
        pwm(0, 0)
        pwm(1, 0)
        pwm(2, 0)
        pwm(3, 0)
        pwm(4, 0)
        pwm(5, 0)
        pwm(6, 0)
        pwm(7, 0)

process = Process(target=setVars)
process.start()

if __name__ == "__main__":
    main()
