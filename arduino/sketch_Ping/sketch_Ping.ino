#include <NewPing.h>

#define TRIGGER_PIN 12
#define ECHO_PIN 11
#define MAX_DISTANCE 200

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int distance = sonar.ping_cm();
  Serial.print("Ping: ");
  Serial.print(distance);
  Serial.println("cm");

  if (distance != 0){
    if (distance < 10){
      digitalWrite(10, HIGH);
    }else{
      digitalWrite(10, LOW);
    }
    digitalWrite(9, LOW);  
  }else{
    digitalWrite(10, LOW);
    digitalWrite(9, HIGH);
  }
  doADelay();
}

void doADelay(){
  delay(500);
}

