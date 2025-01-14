import os
import pygame
import subprocess
import time

# Set the SDL video driver to dummy for headless operation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# A dictionary to keep track of connected joysticks
joysticks = {}

def main():
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

            lr = joystick.get_axis(0)  # Left/Right
            fb = joystick.get_axis(1)  # Up/Down
            r = joystick.get_axis(2)  # Rotate

            zl = joystick.get_button(6)
            zr = joystick.get_button(7)

            s = joystick.get_button(8)
            f = joystick.get_button(9)

            if lr < -0.01:
                lx = 1
                rx = 0
            elif lr > 0.01:
                lx = 0
                rx = 1
            else:
                lx = 0
                rx = 0

            subprocess.run(["python3", "Venix/joystick2pwm.py", str(lr), str(fb), str(r), str(zl), str(zr)])

            subprocess.run(["python3", "Venix/mode_manager.py", str(s), str(f), str(lx), str(rx)])

            subprocess.run(["python3", "Venix/print_manager.py", str(lr), str(fb), str(r), str(zl), str(zr), str(s), str(f), str(lx), str(rx)])

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
