import time
import sys
import subprocess
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

select = int(sys.argv[1])
funtion = int(sys.argv[2])

l = int(sys.argv[3])
r = int(sys.argv[4])

mode = 0
modecount = 2 # Excluding passive

if select == 1:
    if 0 <= mode < modecount:
        if r == 1:
            mode += 1
    if 0 < mode <= modecount:
        if l == 1:
            mode -= 1

# Create I2C interface
serial = i2c(port=1, address=0x3C)

# Create an SSD1306 OLED device
device = ssd1306(serial)

while True:
    with canvas(device) as draw:
        # Load custom fonts
        large_font = ImageFont.truetype("Venix/font.ttf", 35)
        small_font = ImageFont.truetype("Venix/font.ttf", 15)

        # Draw text on the OLED
        draw.text((5, 0), "Venix", font=large_font, fill="white")    # Large title
        draw.text((5, 40), "Mode:", font=small_font, fill="white")    # Label
        if mode == 0:
            draw.text((60, 40), "Passive", font=small_font, fill="white") # Mode text
        if mode == 1:
            draw.text((60, 40), "LED", font=small_font, fill="white") # Mode text
        if mode == 2:
            draw.text((60, 40), "Buzzer", font=small_font, fill="white") # Mode text
