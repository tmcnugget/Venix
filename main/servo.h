#ifndef SERVO_H
#define SERVO_H

#include <Servo.h>

// Servo objects
extern Servo servo1;
extern Servo servo2;
extern Servo servo3;

// Servo angles (global variables)
extern int angle1;
extern int angle2;
extern int angle3;

// Function declarations
void addservo1();
void subtractservo1();
void addservo2();
void subtractservo2();
void addservo3();
void subtractservo3();

#endif
