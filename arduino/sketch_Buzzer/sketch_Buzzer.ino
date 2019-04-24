#include <pitches.h>

int melody[] = {NOTE_DS8, NOTE_DS8, NOTE_DS8, NOTE_C7, NOTE_E7, NOTE_G7, NOTE_G6};
int duration = 500;

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i < 7; i++){
    tone(13, melody[i], duration);
    delay(1000);
  }

  delay(2000);
}
