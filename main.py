import os
import pygame
import subprocess
import time
from mdd3a import MDD3A

# Set the SDL video driver to dummy for headless operation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

mdd3a = MDD3A()

# A dictionary to keep track of connected joysticks
joysticks = {}

def deadzone(number):
    if abs(number) < 0.005:  # Deadzone range (-0.005, 0.005)
        return 0
    return number

def main():
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
                lr = deadzone(round(joystick.get_axis(0), 3)) # Left/Right
                fb = deadzone(round(joystick.get_axis(1), 3)) # Up/Down
                r = deadzone(round(joystick.get_axis(2), 3)) # Rotate

                zl = joystick.get_button(6) / 10
                zr = joystick.get_button(7) / 10

            m1, m2, m3, m4 = mdd3a.calculateMotors(lr, fb, r)

            print(f"Calculated Motor Values: M1={m1}, M2={m2}, M3={m3}, M4={m4}")
            
            mdd3a.setMotors(m1, m2, m3, m4)

            mdd3a.getSpeed(increment=zr, decrement=zl)

            print(lr, fb, r, zl, zr)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
