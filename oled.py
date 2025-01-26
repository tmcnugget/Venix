import sys
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

def text(text, size, x, y):
    with canvas(device) as draw:
        font = ImageFont.truetype("font.ttf", size)
        draw.text((x, y), text, font = font, fill="white")

function = sys.argv[1]

def getValues():
    lr = float(sys.argv[2])
    fb = float(sys.argv[3])
    r = float(sys.argv[4])
    return lr, fb, r

def init():
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    
    text("Joystick values:", 25, 5, 0)
    text("left-right:", 15, 5, 25)
    text("fwd-bckwd:", 15, 5, 40)
    text("rotate", 15, 5, 55)
    text("E O", 15, 25, 25)
    text("R R", 15, 25, 40)
    text("R !", 15, 25, 55)

def write():
    text("Joystick values:", 25, 5, 0)
    text("left-right:", 15, 5, 25)
    text("fwd-bckwd:", 15, 5, 40)
    text("rotate", 15, 5, 55)
    text(f"{lr:.2f}", 15, 5, 50)
    text(f"{fb:.2f}", 15, 5, 40)
    text(f"{r:.2f}", 15, 5, 55)

if function == "init":
    init()
elif function == "write":
    getValues()
    write()
