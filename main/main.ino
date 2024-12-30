#include <thread>
#include "usbh_helper.h"
#include "CytronMotorDriver.h"
#include <U8g2lib.h>
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

// Define a global variable to store the most recent HID report (20 bytes in this case)
uint8_t hid[20];  // Adjusted to match the report size of 20 bytes
int speed = 150;

int sonar = 0;

const int buzzerPin = 22;

// defines pins numbers
const int echoPin = 16;
const int trigPin = 17;

// defines variables
long duration;
int distance;

U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ 17, /* data=*/ 16, /* reset=*/ U8X8_PIN_NONE);    //Low speed I2C

unsigned long previousMillisOLED = 0;
const long intervalOLED = 1000;
unsigned long previousMillisLED = 0;
const long intervalLED = 20;
unsigned long previousMillisSonar = 0;
const long intervalSonar = 500;

// Configure the motor driver.
CytronMD motor1(PWM_PWM, 8, 9);  
CytronMD motor2(PWM_PWM, 10, 11);
CytronMD motor3(PWM_PWM, 12, 13);
CytronMD motor4(PWM_PWM, 14, 15);

void startup() {
  // Initialize buzzer pin as output
  pinMode(buzzerPin, OUTPUT);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication

  u8g2.begin();

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication

  u8g2.begin();

  // Initialize buzzer pin as output
  pinMode(buzzerPin, OUTPUT);
}

void repeat() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillisSonar >= intervalSonar) {
    previousMillisSonar = currentMillis;
    get_distance();
  }
  
  if (currentMillis - previousMillisLED >= intervalLED) {
    previousMillisLED = currentMillis;
    update_led();
  }
  
  if (currentMillis - previousMillisOLED >= intervalOLED) {
    previousMillisOLED = currentMillis;
    update_oled();
  }
}

void get_distance() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2;
}

void update_led() {

}

void update_oled() {
  Serial.println("Updating OLED");
  u8g2.clearBuffer();                   // clear the internal memory
  u8g2.setFont(u8g2_font_ncenB24_tr);   // choose a suitable font
  u8g2.drawStr(0,25,"Venix");
  u8g2.setFont(u8g2_font_ncenB12_tr);   // choose a suitable font
  u8g2.drawStr(0,50,"Distance:");
  char distanceStr[10]; // Buffer to hold the string representation of distance
  sprintf(distanceStr, "%d", distance); // Convert integer to string

  if (sonar == 0) {
    u8g2.drawStr(85, 50, "Off");
  } else {
    u8g2.drawStr(85, 50, distanceStr); // Use the string representation
  }
  u8g2.sendBuffer(); 
}

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
  speed -= 1;
}

void fast() {
  Serial.println("Speeding Up...");
  if (speed > 255) speed = 255;
  speed += 1;
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

  startup()
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
  
  // If the 10th byte is between 0x00 and 0x7F, execute fwds
  if (byte10 >= 0x01 && byte10 <= 0x7F) {
    forwards();
  }

  else if (byte6 != 0x00) {
    forwards();
  }

  // If the 10th byte is between 0x80 and 0xFF, execute bckwrds
   else if (byte10 >= 0x80 && byte10 <= 0xFF) {
    backwards();
  }

  else if (byte5 != 0x00) {
    backwards();
  }

  // If the 8th byte is between 0x00 and 0x7F, execute right
  else if (byte8 >= 0x01 && byte8 <= 0x7F) {
    right();
  } 
  // If the 8th byte is between 0x80 and 0xFF, execute left
  else if (byte8 >= 0x80 && byte8 <= 0xFF) {
    left();
  }

    // If the 8th byte is between 0x00 and 0x7F, execute right
  else if (byte12 >= 0x01 && byte12 <= 0x7F) {
    rright();
  }

  // If the 8th byte is between 0x00 and 0x7F, execute right
  else if (byte4 == 0x02) {
    rright();
  }  
  
  // If the 8th byte is between 0x80 and 0xFF, execute left
  else if (byte12 >= 0x80 && byte12 <= 0xFF) {
    rleft();
  }
  
  // If the 8th byte is between 0x80 and 0xFF, execute left
  else if (byte4 == 0x01) {
    rleft();
  }

  if (byte5 == 0x00 && byte6 == 0x00 && byte8 == 0x00 && byte10 == 0x00 && byte12 == 0x00 && byte4 != 0x01 && byte4 != 0x02) {
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
