#include <Servo.h>

Servo servo1;
int buttonState = 0;
bool toggle = false;

void setup() {
  // put your setup code here, to run once:
  servo1.attach(15);
  pinMode(9, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
   buttonState = digitalRead(9);
   

   if (buttonState == HIGH){
     if (toggle == true){
       servo1.write(45);      // Turn SG90 servo Left to 45 degrees
       delay(1000);          // Wait 1 second
       toggle = false;
     }else{
       servo1.write(90);      // Turn SG90 servo back to 90 degrees (center position)
       delay(1000);          // Wait 1 second
       toggle = true;
     }
     
   }
  

}
