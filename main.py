import os
import pygame
import subprocess
import time
from pca9685 import PCA9685

# Set the SDL video driver to dummy for headless operation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

pca9685 = PCA9685(0x40)
pca9685.setPWMFreq(50)

# A dictionary to keep track of connected joysticks
joysticks = {}

def deadzone(number):
    if abs(number) < 0.005:  # Deadzone range (-0.005, 0.005)
        return 0
    return number

def setMotors(lr, fb, r):
    m1 = fb + lr + r
    m2 = fb - lr - r
    m3 = fb - lr + r
    m4 = fb + lr - r

    m1 = min(m1, 1)
    m2 = min(m2, 1)
    m3 = min(m3, 1)
    m4 = min(m4, 1)

    m1 = scale(m1)
    m2 = scale(m2)
    m3 = scale(m3)
    m4 = scale(m4)
    
    if lr == 0 and fb == 0 and r == 0:
        m1, m2, m3, m4 = 0, 0, 0, 0

    print(m1, m2, m3, m4)

def main():
    speed = 1
    
    print("Starting headless joystick controller...")
    
    subprocess.Popen(["python3", "Venix/oled.py"])

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
                r = deadzone(round(joystick.get_axis(2), 3)) / 2 * speed # Rotate

                zl = joystick.get_button(6)
                zr = joystick.get_button(7)

            """Adjusts the speed based on joystick button inputs."""
            if zr == 1:
                speed += 0.05
            elif zl == 1:
                speed -= 0.05

            speed = max(0, min(2, speed))

            setMotors(lr, fb, r)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
