from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

def initOLED()
    # Create I2C interface
    serial = i2c(port=1, address=0x3C)
    # Create an SSD1306 OLED device
    device = ssd1306(serial)

def showOLED()
    drawmain()
        
def writeOLED(lr, fb, r, m1, m2, m3, m4)
    drawmain()
    

def drawmain()
    with canvas(device) as draw:
            # Load custom fonts
            large_font = ImageFont.truetype("font.ttf", 35)
            small_font = ImageFont.truetype("font.ttf", 15)

            # Draw text on the OLED
            draw.text((5, 0), "Venix", font=large_font, fill="white")
