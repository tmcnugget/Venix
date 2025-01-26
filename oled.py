import time
from multiprocessing import Value
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

# Shared variables
fb = Value('d', 0.0)
lr = Value('d', 0.0)
r = Value('d', 0.0)

def text(device, text, size, x, y):
    """Function to display text on the OLED display"""
    with canvas(device) as draw:
        font = ImageFont.truetype("font.ttf", size)
        draw.text((x, y), text, font=font, fill="white")

def init():
    """Initialize the OLED display and display static text"""
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    
    # Display static text once
    text(device, "Joystick values:", 25, 5, 0)
    text(device, "left-right:", 15, 5, 25)
    text(device, "fwd-bckwd:", 15, 5, 40)
    text(device, "rotate:", 15, 5, 55)

    return device

def write(device):
    """Update joystick values on the OLED display"""
    # Clear the display and update with dynamic values
    with canvas(device) as draw:
        font = ImageFont.truetype("font.ttf", 15)
        draw.text((5, 25), f"{lr.value:.2f}", font=font, fill="white")
        draw.text((5, 40), f"{fb.value:.2f}", font=font, fill="white")
        draw.text((5, 55), f"{r.value:.2f}", font=font, fill="white")

if __name__ == "__main__":
    # Initialize the device and display static text
    device = init()
    
    # Main loop to continuously update joystick values
    while True:
        write(device)
        time.sleep(0.01)
