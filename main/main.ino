#include "usbh_helper.h"         // USB host helper library for handling USB devices
#include "led.h"                 // Make LED control simpler
#include "servo.h"               // Make servo control simpler
#include "CytronMotorDriver.h"   // Motor driver library for motor control
#include <U8g2lib.h>             // OLED display library for visual output
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

// Global Variables
uint8_t hid[20];           // Buffer to store incoming HID reports

int speed = 150;           // Default motor speed
int function = 0;          // Set peripheral/mode to default

const int buzzerPin = 22;  // Pin connected to the buzzer for sound output

// Display Setup for OLED
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, 17, 16, U8X8_PIN_NONE);

// Initialize motor controllers for four motors
CytronMD motors[] = {
  CytronMD(PWM_PWM, 8, 9),   // Motor 1 pins
  CytronMD(PWM_PWM, 10, 11), // Motor 2 pins
  CytronMD(PWM_PWM, 12, 13), // Motor 3 pins
  CytronMD(PWM_PWM, 14, 15)  // Motor 4 pins
};

// Display a message on the OLED screen
void update_oled() {
  u8g2.clearBuffer();                               // Clear previous content
  u8g2.setFont(u8g2_font_ncenB24_tr);               // Set font style and size
  u8g2.drawStr(0, 25, "Venix");                       // Print the message at specified coordinates
  u8g2.setFont(u8g2_font_ncenB12_tr);               // Set font style and size
  u8g2.drawStr(75, 25, "POWERED BY RP2350");          // Print the message at specified coordinates
  u8g2.setFont(u8g2_font_ncenB24_tr);               // Set font style and size
  u8g2.drawStr(25, 50, "Fn:");                        // Print the message at specified coordinates
  if (function == 0) u8g2.drawStr(50, 50, "Passive"); // Print the message at specified coordinates
  if (function == 1) u8g2.drawStr(50, 50, "LED");     // Print the message at specified coordinates
  if (function == 2) u8g2.drawStr(50, 50, "P:ARM");   // Print the message at specified coordinates
  u8g2.sendBuffer();                                // Send data to the OLED display
}

// Control motor speeds for each motor
void moveMotors(int s1, int s2, int s3, int s4) {
  motors[0].setSpeed(s1);  // Set speed for motor 1
  motors[1].setSpeed(s2);  // Set speed for motor 2
  motors[2].setSpeed(s3);  // Set speed for motor 3
  motors[3].setSpeed(s4);  // Set speed for motor 4
}

// Functions
void forwardsright() { moveMotors(speed, 0, 0, speed); }
void backwardsright() { moveMotors(-speed, 0, 0, -speed); }
void backwardsleft() { moveMotors(0, -speed, -speed, 0); }
void forwardsleft() { moveMotors(0, speed, speed, 0); }
void forwards() { moveMotors(speed, speed, speed, speed); }
void backwards() { moveMotors(-speed, -speed, -speed, -speed); }
void left() { moveMotors(-speed, speed, speed, -speed); }
void right() { moveMotors(speed, -speed, -speed, speed); }
void rleft() { moveMotors(-speed, -speed, speed, speed); }
void rright() { moveMotors(speed, speed, -speed, -speed); }
void stop() { moveMotors(0, 0, 0, 0); }
void fast() { speed = constrain(speed + 5, 0, 255); }
void slow() { speed = constrain(speed - 5, 0, 255); }
void beep() { tone(buzzerPin, 800); }
void hhorn() { tone(buzzerPin, 1000); }
void mhorn() { tone(buzzerPin, 500); }
void lhorn() { tone(buzzerPin, 200); }
void mute() { noTone(buzzerPin); }
void addmode() { function = constrain(function + 1, 0, 2); 
  beep();
  delay(250);
}

void subtractmode() { function = constrain(function -1, 0, 2);
  beep();
  delay(250);
}

// Initial setup for the microcontroller
void setup() { // @@@@@@@@@@-----MAIN SETUP-----@@@@@@@@@@
  Serial.begin(115200);       // Start serial communication at 115200 baud rate
  USBHost.begin(1);           // Initialize USB host for HID devices
  
  pinMode(buzzerPin, OUTPUT); // Configure buzzer pin as output
  
  u8g2.begin();               // Initialize OLED display

  pixels.begin();
  pixels.clear();
  pixels.show();

  servo1.attach(0);
  servo2.attach(1);
  servo3.attach(2);

  servo1.write(angle1);
  servo2.write(angle2);
  servo3.write(angle3);
}

void loop() { // @@@@@@@@@@-----MAIN LOOP-----@@@@@@@@@@
  update_oled();  // Continuously update the OLED display
  pixels.setPixelColor(0, hueToColor(hue));
  pixels.setPixelColor(1, hueToColor(hue));
}

// Setup USB subsystem for secondary core
void setup1() {
  rp2040_configure_pio_usb();  // Configure USB interface on secondary core
  USBHost.begin(1);            // Start USB host services
}

// Continuously poll USB tasks on secondary core
void loop1() {
  USBHost.task();  // Process incoming USB events
}

// HID Callbacks - Handle input events from HID devices
extern "C" {
void tuh_hid_report_received_cb(uint8_t dev_addr, uint8_t instance, const uint8_t *report, uint16_t len) {
  if (len <= sizeof(hid)) memcpy(hid, report, len); // Copy valid report data
  else Serial.println("Report size exceeds buffer size."); // Error for oversized reports

  // Extract bytes from HID report
  uint8_t byte14 = hid[13];
  uint8_t byte12 = hid[11];
  uint8_t byte10 = hid[9];
  uint8_t byte8 = hid[7];
  uint8_t byte6 = hid[5];
  uint8_t byte5 = hid[4];
  uint8_t byte4 = hid[3];
  uint8_t byte3 = hid[2];

  // Control logic based on report bytes
  if (byte3 != 0x10) { // If not holding function key then scan inputs for default car control
    if (byte10 >= 0x01 && byte10 <= 0x7F && byte8 >= 0x01 && byte8 <= 0x7F) forwardsright();
    else if (byte10 >= 0x80 && byte10 <= 0xFF && byte8 >= 0x01 && byte8 <= 0x7F) backwardsright();
    else if (byte10 >= 0x80 && byte10 <= 0xFF && byte8 >= 0x80 && byte8 <= 0xFF) backwardsleft();
    else if (byte10 >= 0x01 && byte10 <= 0x7F && byte8 >= 0x80 && byte8 <= 0xFF) forwardsleft();
    else if (byte10 >= 0x01 && byte10 <= 0x7F) forwards();
    else if (byte6 != 0x00) forwards();
    else if (byte10 >= 0x80 && byte10 <= 0xFF) backwards();
    else if (byte5 != 0x00) backwards();
    else if (byte8 >= 0x01 && byte8 <= 0x7F) right();
    else if (byte8 >= 0x80 && byte8 <= 0xFF) left();
    else if (byte12 >= 0x01 && byte12 <= 0x7F) rright();
    else if (byte4 == 0x02) rright();
    else if (byte12 >= 0x80 && byte12 <= 0xFF) rleft();
    else if (byte4 == 0x01) rleft();
    else if (byte5 == 0x00 && byte6 == 0x00 && byte8 == 0x00 && byte10 == 0x00 && byte12 == 0x00 && byte4 != 0x01 && byte4 != 0x02) stop();
  }

  // Speed and horn controls
  if (byte3 == 0x08) fast();
  if (byte3 == 0x04) slow();
  if (byte3 == 0x80) hhorn();
  if (byte3 == 0xc0 || byte4 == 0x03) mhorn();
  if (byte3 == 0x40) lhorn();
  if (byte3 == 0x00 && byte4 != 0x03) mute();

  // Mode select controls
  if (byte3 == 0x20) {
    if (byte8 >= 0x01 && byte8 <= 0x7F) addmode();
    if (byte8 >= 0x80 && byte8 <= 0xFF) subtractmode();
  }
  
  if (byte3 == 0x10) {
    if (function == 1) { // LED control
      if (byte8 >= 0x01 && byte8 <= 0x7F) addhue();
      if (byte8 >= 0x80 && byte8 <= 0xFF) subtracthue();
    }
    if (function == 2) { // Arm control
      if (byte14 >= 0x01 && byte14 <= 0x7F) addservo1();
      if (byte14 >= 0x80 && byte14 <= 0xFF) subtractservo1();
      if (byte10 >= 0x01 && byte10 <= 0x7F) addservo2();
      if (byte10 >= 0x80 && byte10 <= 0xFF) subtractservo2();
      if (byte3 == 0x40) addservo3();
      if (byte3 == 0x80) subtractservo3();
    }
  }

  tuh_hid_receive_report(dev_addr, instance);  // Request next HID report
}
}
