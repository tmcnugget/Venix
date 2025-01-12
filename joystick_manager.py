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

                # Format axis data
                data = f"{lr:.3f} {fb:.3f} {r:.3f} {zl:.3f} {zr:.3f}"
                print(f"Sending data: {data}")

                # Call motor.py and pass the axis data as arguments
                subprocess.run(["python3", "Venix/joystick2pwm.py", str(axis_0), str(axis_1), str(axis_2)])

            # Sleep to reduce CPU usage (adjust as needed for responsiveness)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
