from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

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

def write(device):
    """Update joystick values on the OLED display"""
    # Clear the display and update with dynamic values
    with canvas(device) as draw:
        font = ImageFont.truetype("font.ttf", 15)
        draw.text((5, 25), "E O", font=font, fill="white")
        draw.text((5, 40), "R R", font=font, fill="white")
        draw.text((5, 55), "R !", font=font, fill="white")

init()
write()
