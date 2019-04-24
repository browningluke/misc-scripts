// Include headers
#include <pitches.h>
#include <NewPing.h>

// Define constants
  #define TRIGGER_PIN 12
  #define ECHO_PIN 11
  #define MAX_DISTANCE 200

//Create NewPing Object, pass it constants
  NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

//Create buzzer variables
  int melody[] = {NOTE_DS8, NOTE_DS8, NOTE_DS8, NOTE_C7, NOTE_E7, NOTE_G7, NOTE_G6};
  int mDuration = 500;

//Define Functions
  //Ping fuction
  void PingSensor(){
    //Create distance variable
      int distance = sonar.ping_cm();
    
    //Print distance to window
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
      delay(500);
    }

  
  void RunBuzzer(){
      for (int i = 0; i < 7; i++){
        tone(13, melody[i], mDuration);
        delay(1000);
      }
  
    delay(2000);
  }
  
// Setup code, to run once:
  void setup() {
    
    
    // Link it to 9600 baud rate
    Serial.begin(9600);
  
    //Set Pin 9 & 10 to output (these are the LED control pins)
    pinMode(10, OUTPUT);
    pinMode(9, OUTPUT);
    
  }

// Loop code, runs repeatedly
  void loop() {
    PingSensor();
  }
