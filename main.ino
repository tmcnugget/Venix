#include "usbh_helper.h"
#include "CytronMotorDriver.h"

// Define a global variable to store the most recent HID report (20 bytes in this case)
uint8_t hid[20];  // Adjusted to match the report size of 20 bytes
int speed = 150;

const int buzzerPin = 22;

// Configure the motor driver.
CytronMD motor1(PWM_PWM, 8, 9);  
CytronMD motor2(PWM_PWM, 10, 11);
CytronMD motor3(PWM_PWM, 12, 13);
CytronMD motor4(PWM_PWM, 14, 15);

// Placeholder function for forward
void forwards() {
  Serial.println("Moving Fowards");
  motor1.setSpeed(speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(speed);
}

// Placeholder function for bckwrds
void backwards() {
  Serial.println("Moving Backwards...");
  motor1.setSpeed(-speed);
  motor2.setSpeed(-speed);
  motor3.setSpeed(-speed);
  motor4.setSpeed(-speed);
}

// Placeholder function for left
void left() {
  Serial.println("Moving Left");
  motor1.setSpeed(-speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(-speed);
}

// Placeholder function for right
void right() {
  Serial.println("Moving Right...");
  motor1.setSpeed(speed);
  motor2.setSpeed(-speed);
  motor3.setSpeed(-speed);
  motor4.setSpeed(speed);
}

// Placeholder function for left
void rleft() {
  Serial.println("Rotating Left");
  motor1.setSpeed(-speed);
  motor2.setSpeed(-speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(speed);
}

// Placeholder function for right
void rright() {
  Serial.println("Rotating Right...");
  motor1.setSpeed(speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(-speed);
  motor4.setSpeed(-speed);
}

void stop() {
  Serial.println("Stopping...");
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
}

void slow() {
  Serial.println("Slowing Down...");
  if (speed < 0) speed = 0;  // Ensure speed doesn't go negative
  speed -= 25;
}

void fast() {
  Serial.println("Speeding Up...");
  if (speed > 255) speed = 25;
  speed += 25;
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

  // Initialize buzzer pin as output
  pinMode(buzzerPin, OUTPUT);

  // Initialize buttons
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);

  // Play melody during start up
  play_melody(buzzerPin);
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
  uint8_t byte3 = hid[2];
  
  // If the 10th byte is between 0x00 and 0x7F, execute fwds
  if (byte10 >= 0x01 && byte10 <= 0x7F) {
    forwards();
  } 
  // If the 10th byte is between 0x80 and 0xFF, execute bckwrds
  else if (byte10 >= 0x80 && byte10 <= 0xFF) {
    backwards();
  }

  // If the 8th byte is between 0x00 and 0x7F, execute right
  if (byte8 >= 0x01 && byte8 <= 0x7F) {
    right();
  } 
  // If the 8th byte is between 0x80 and 0xFF, execute left
  else if (byte8 >= 0x80 && byte8 <= 0xFF) {
    left();
  }

    // If the 8th byte is between 0x00 and 0x7F, execute right
  if (byte12 >= 0x01 && byte12 <= 0x7F) {
    rright();
  } 
  // If the 8th byte is between 0x80 and 0xFF, execute left
  else if (byte12 >= 0x80 && byte12 <= 0xFF) {
    rleft();
  }

  if (byte8 == 0x00 && byte10 == 0x00 && byte12 == 0x00) {
    stop();
  }

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
 
 if (byte3 == 0x40) {
    lhorn();
 }

 if (byte3 == 0x00) {
    mute();
 }

  // Continue to request to receive report
  if (!tuh_hid_receive_report(dev_addr, instance)) {
    Serial.printf("Error: cannot request to receive report\r\n");
  }
}
} // extern C
