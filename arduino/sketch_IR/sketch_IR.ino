#include <boarddefs.h>
#include <IRremote.h>
#include <IRremoteInt.h>
#include <ir_Lego_PF_BitStreamEncoder.h>

int RECV_PIN = 13;
IRrecv irrecv(RECV_PIN);
decode_results results;

const String powerOn = "FD00FF";
const String powerOff = "FD40BF";

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

void loop()
{
  if (irrecv.decode(&results))
    {
     Serial.println(results.value, HEX);
      if (results.value == 0xFFA25D){
        Serial.println("On");
        digitalWrite(8, HIGH);
      }
      if (results.value == 0xFFE21D){
          Serial.println("Off");
          digitalWrite(8, LOW);
      }
     irrecv.resume(); // Receive the next value
    }


}
