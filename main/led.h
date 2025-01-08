#ifndef LED_H
#define LED_H

#include <Adafruit_NeoPixel.h>

extern Adafruit_NeoPixel pixels;  // NeoPixel object
extern byte hue;  // Hue value

uint32_t hueToColor(byte hue);
void addhue();
void subtracthue();

#endif
