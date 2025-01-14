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

            # Process axis data for each connected joystick
            for joystick in joysticks.values():
                lr = joystick.get_axis(0)  # Left/Right
                fb = joystick.get_axis(1)  # Up/Down
                r = joystick.get_axis(2)  # Rotate

                zl = joystick.get_button(6)
                zr = joystick.get_button(7)

                s = joystick.get_button(8)
                f = joystick.get_button(9)

                if lr < 0:
                    l = 1
                    r = 0
                elif lr > 0:
                    l = 0
                    r = 1
                else:
                    l = 0
                    r = 0

                # Format axis data
                data = f"{lr:.3f} {fb:.3f} {r:.3f} {zl:.3f} {zr:.3f} {s:.3f} {f:.3f} {l:.3f} {r:.3f}"
                print(f"Inputs: {data}")

                # Call motor.py and pass the axis data as arguments
                subprocess.run(["python3", "Venix/joystick2pwm.py", str(lr), str(fb), str(r), str(zl), str(zr)])

                subprocess.run(["python3", "Venix/mode_manager.py", str(s), str(f), str(l), str(r)])

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
