import os
import pygame
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

# Set the SDL video driver to dummy for headless operation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# A dictionary to keep track of connected joysticks
joysticks = {}

def deadzone(number):
    if abs(number) < 0.005:  # Deadzone range (-0.005, 0.005)
        return 0
    return number

def text(draw, text, size, x, y):
    """Function to display text on the OLED display"""
    font = ImageFont.truetype("font.ttf", size)
    draw.text((x, y), text, font=font, fill="white")

def init():
    """Initialize the OLED display and display static text"""
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    return device

def write(device, fb, lr, r, speed):
    """Update joystick values on the OLED display"""
    with canvas(device) as draw:  # Correct use of canvas context
        draw.rectangle((0, 0, device.width, device.height), outline="black", fill="black")  # Clear the screen
        text(draw, f"x1: {lr}", 15, 10, 0)
        text(draw, f"y: {fb}", 15, 10, 20)
        text(draw, f"x2: {r}", 15, 10, 40)
        text(draw, f"{speed}", 35, 45, 0)

def main(device):
    speed = 1
    zl = 0
    zr = 0
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
                lr = deadzone(round(joystick.get_axis(0), 3))
                fb = deadzone(round(joystick.get_axis(1), 3))
                r = -deadzone(round(joystick.get_axis(2), 3))

                # Ensure values are within range
                lr = min(lr, 1)
                fb = min(fb, 1)
                r = min(r, 1)

                zl = joystick.get_button(6)
                zr = joystick.get_button(7)

                """Adjusts the speed based on joystick button inputs."""
                if zr == 1:
                    speed += 0.02
                elif zl == 1:
                    speed -= 0.02
    
                speed = max(0, min(2, speed))

                write(device, fb, lr, r, speed)
    
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    device = init()  # Initialize the device before passing it to main
    main(device)
