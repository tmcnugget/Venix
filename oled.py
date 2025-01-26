import time
from multiprocessing import Value
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

fb = Value('d', 0.0)
lr = Value('d', 0.0)
r = Value('d', 0.0)

def text(text, size, x, y):
    with canvas(device) as draw:
        font = ImageFont.truetype("font.ttf", size)
        draw.text((x, y), text, font = font, fill="white")

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

if __name__ == "__main__":
    init()
    while True:
        write()
        time.sleep(0.01)
