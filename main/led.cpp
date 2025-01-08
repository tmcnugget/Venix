#include "led.h"

Adafruit_NeoPixel pixels(2, 23, NEO_GRB + NEO_KHZ800);
byte hue = 0;  // Initial hue value

uint32_t hueToColor(byte hue) {
  if (hue < 85) return pixels.Color(255 - hue * 3, 0, hue * 3);
  if (hue < 170) return pixels.Color(0, (hue - 85) * 3, 255 - (hue - 85) * 3);
  return pixels.Color((hue - 170) * 3, 255 - (hue - 170) * 3, 0);
}

void addhue() {
  hue = (hue + 1) % 256;
}

void subtracthue() {
  hue = (hue == 0) ? 255 : hue - 1;
}
