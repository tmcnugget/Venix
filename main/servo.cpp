#include "servo.h"

// Initialize Servo objects
Servo myservo1;
Servo myservo2;
Servo myservo3;

// Initialize servo angles
int angle1 = 0;
int angle2 = 0;
int angle3 = 0;

// Function implementations
void addservo1() {
  angle1 = min(angle1 + 2, 180);
  myservo1.write(angle1);
}

void subtractservo1() {
  angle1 = max(angle1 - 2, 0);
  myservo1.write(angle1);
}

void addservo2() {
  angle2 = min(angle2 + 2, 180);
  myservo2.write(angle2);
}

void subtractservo2() {
  angle2 = max(angle2 - 2, 0);
  myservo2.write(angle2);
}

void addservo3() {
  angle3 = min(angle3 + 2, 180);
  myservo3.write(angle3);
}

void subtractservo3() {
  angle3 = max(angle3 - 2, 0);
  myservo3.write(angle3);
}
