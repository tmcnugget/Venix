from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

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
        draw.text((5, 0), "Venix", font=large_font, fill="white")
