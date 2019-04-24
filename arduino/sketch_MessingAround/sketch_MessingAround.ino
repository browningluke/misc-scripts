#include <boarddefs.h>
#include <IRremote.h>
#include <IRremoteInt.h>
#include <ir_Lego_PF_BitStreamEncoder.h>

const int redPin = 6;
const int greenPin = 7;
const int bluePin = 8;
const int IRPin = 2;


IRrecv irrecv(IRPin);
decode_results results;

void setup() {
  // put your setup code here, to run once:
  irrecv.enableIRIn(); // Start the receiver
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  irReciever();

}

void irReciever(){
  if (irrecv.decode(&results)){
    if (results.value != 0xFFFFFFFF){
      Serial.println(results.value, HEX);
    }
    
    if (results.value == 0xFFA25D){
      
    }
    if (results.value == 0xFF906F){
      
    }
    if (results.value == 0xFFE01F){
      
    }
    
    irrecv.resume(); // Receive the next value
  }
}
