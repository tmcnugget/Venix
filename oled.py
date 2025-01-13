from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import ImageFont

# Function to display multiple lines of text on the OLED
def display_text(mode):
    # Create I2C interface
    serial = i2c(port=1, address=0x3C)

    # Create an SSD1306 OLED device
    device = ssd1306(serial)

    # Use a single canvas context to draw all text
    with canvas(device) as draw:
        # Load custom fonts
        large_font = ImageFont.truetype("Venix/font.ttf", 35)
        small_font = ImageFont.truetype("Venix/font.ttf", 20)

        # Draw text on the OLED
        draw.text((5, 0), "Venix", font=large_font, fill="white")    # Large title
        draw.text((5, 40), "Mode:", font=small_font, fill="white")    # Label
        if mode = 0:
            draw.text((70, 40), "Passive", font=small_font, fill="white") # Mode text
        if mode = 1:
            draw.text((70, 40), "LED", font=small_font, fill="white") # Mode text
        if mode = 2:
            draw.text((70, 40), "Buzzer", font=small_font, fill="white") # Mode text

# Call the function to display the text
display_text()
