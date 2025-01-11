#include "usbh_helper.h"
#include "CytronMotorDriver.h"
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

// Define a global variable to store the most recent HID report (20 bytes in this case)
uint8_t hid[20];  // Adjusted to match the report size of 20 bytes
float speed = 1.00;

const int buzzerPin = 22;

int fb = 0, lr = 0, r = 0;
int m1 = 0, m2 = 0, m3 = 0, m4 = 0;

// Configure the motor driver.
CytronMD motor1(PWM_PWM, 8, 9);  
CytronMD motor2(PWM_PWM, 10, 11);
CytronMD motor3(PWM_PWM, 12, 13);
CytronMD motor4(PWM_PWM, 14, 15);

void hexToDec(byte hexValue, int &result) {
  // If the MSB is set (negative number), convert using 2's complement
  if (hexValue & 0x80) {
    // For negative values, convert the 2's complement representation to negative decimal
    result = (int)hexValue - 256;  // Convert to signed 8-bit value
  } else {
    // If it's not negative, just cast the byte to an int
    result = (int)hexValue;
  }
}

void movemotors() {
  motor1.setSpeed(m1);
  motor2.setSpeed(m2);
  motor3.setSpeed(m3);
  motor4.setSpeed(m4);
}

void getmotorvalues() {
  fb *= speed;
  lr *= speed;
  r *= speed;

  // Adjust the motor values considering the correct layout:
  m1 = fb + lr + r;  // Top left motor
  m2 = fb - lr - r;  // Bottom left motor
  m3 = fb - lr + r;  // Top right motor
  m4 = fb + lr - r;  // Bottom right motor

  m1 = constrain(m1, -255, 255);
  m2 = constrain(m2, -255, 255);
  m3 = constrain(m3, -255, 255);
  m4 = constrain(m4, -255, 255);
}

void slow() {
  Serial.println("Slowing Down...");
  if (speed < 0) speed = 0;  // Ensure speed doesn't go negative
  speed -= 0.05;
}

void fast() {
  Serial.println("Speeding Up...");
  if (speed > 2) speed = 2;
  speed += 0.05;
}

void hhorn() {
  Serial.println("Horn Pitch High...");
  tone(buzzerPin, 1000);
}

void mhorn() {
  Serial.println("Horn Pitch Medium...");
  tone(buzzerPin, 500);
}

void lhorn() {
  Serial.println("Horn Pitch Low...");
  tone(buzzerPin, 200);
}

void mute() {
  Serial.println("Turnung Horn Off...");
  noTone(buzzerPin);
}

#if defined(CFG_TUH_MAX3421) && CFG_TUH_MAX3421
//--------------------------------------------------------------------+
// Using Host shield MAX3421E controller
//--------------------------------------------------------------------+
void setup() {
  Serial.begin(115200);

  // Initialize host stack on controller (rhport) 1
  USBHost.begin(1);

  Serial.println("TinyUSB Dual: HID Device Report Example");

  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  USBHost.task();
  Serial.flush();
}

#elif defined(ARDUINO_ARCH_RP2040)
//--------------------------------------------------------------------+
// For RP2040 use both core0 for device stack, core1 for host stack
//--------------------------------------------------------------------+

//------------- Core0 -------------//
void setup() {
  Serial.begin(115200);
  Serial.println("TinyUSB Dual: HID Device Report Example");
}

void loop() {
  Serial.flush();
}

//------------- Core1 -------------//
void setup1() {
  // Configure pio-usb: defined in usbh_helper.h
  rp2040_configure_pio_usb();

  // Run host stack on controller (rhport) 1
  USBHost.begin(1);
}

void loop1() {
  USBHost.task();
}

#endif

extern "C" {

// Invoked when device with hid interface is mounted
void tuh_hid_mount_cb(uint8_t dev_addr, uint8_t instance, uint8_t const *desc_report, uint16_t desc_len) {
  (void) desc_report;
  (void) desc_len;
  uint16_t vid, pid;
  tuh_vid_pid_get(dev_addr, &vid, &pid);

  Serial.printf("HID device address = %d, instance = %d is mounted\r\n", dev_addr, instance);
  Serial.printf("VID = %04x, PID = %04x\r\n", vid, pid);
  if (!tuh_hid_receive_report(dev_addr, instance)) {
    Serial.printf("Error: cannot request to receive report\r\n");
  }
}

// Invoked when device with hid interface is un-mounted
void tuh_hid_umount_cb(uint8_t dev_addr, uint8_t instance) {
  Serial.printf("HID device address = %d, instance = %d is unmounted\r\n", dev_addr, instance);
}

// Invoked when received report from device via interrupt endpoint
void tuh_hid_report_received_cb(uint8_t dev_addr, uint8_t instance, uint8_t const *report, uint16_t len) {
  Serial.printf("HID report received: ");
  
  // Store the report in the 'hid' variable (make sure the size is not exceeded)
  if (len <= sizeof(hid)) {
    memcpy(hid, report, len);  // Copy the report to the hid variable
  } else {
    Serial.println("Error: Report size exceeds buffer size.");
  }

  // Print the received report for debugging
  for (uint16_t i = 0; i < len; i++) {
    Serial.printf("0x%02X ", report[i]);
  }
  Serial.println();

  // Check the byte of the HID report
  uint8_t byte12 = hid[11];
  uint8_t byte10 = hid[9];
  uint8_t byte8 = hid[7];
  uint8_t byte6 = hid[5];
  uint8_t byte5 = hid[4];
  uint8_t byte4 = hid[3];
  uint8_t byte3 = hid[2];

  getmotorvalues();

  hexToDec(byte8, lr);
  Serial.println(lr);

  hexToDec(byte10, fb);
  Serial.println(fb);
  
  hexToDec(byte12, r);
  Serial.println(r);

  movemotors();
  
  if (byte3 == 0x08) {
    fast();
  }

  if (byte3 == 0x04) {
    slow();
  }

  if (byte3 == 0x80) {
    hhorn();
  }

  if (byte3 == 0xc0) {
    mhorn();
  }

  if (byte4 == 0x03) {
    mhorn();
  }
 
  if (byte3 == 0x40) {
    lhorn();
  }

  if (byte3 == 0x00 && byte4 != 0x03) {
    mute();
  }

  // Continue to request to receive report
  if (!tuh_hid_receive_report(dev_addr, instance)) {
    Serial.printf("Error: cannot request to receive report\r\n");
  }
}
} // extern C
