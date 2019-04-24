#include <LiquidCrystal.h>

int redPin = 6;
int greenPin = 7;
int bluePin = 8;

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  // set up the LCD's number of columns and rows:
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  
  lcd.begin(16, 2);
  lcd.print("T: ");

  lcd.setCursor(5,0);
  lcd.print("K");

  lcd.setCursor(0,1);
  lcd.print("R:");

  lcd.setCursor(5, 1);
  lcd.print("G:");

  lcd.setCursor(10,1);
  lcd.print("B:");

}

void loop() {
  int Vo = analogRead(0);

  lcd.setCursor(2,0);
  lcd.print(Vo);

  for (int i; i <= 255; i++){
    setColor(i,0,0);
  }

  delay(1000);
  
  for (int i; i <= 255; i++){
    setColor(0,i,0);
  }
  delay(1000);
  
  for (int i; i <= 255; i++){
    setColor(0,0,i);
  }

  delay(1000);
  
}

void setColor(int red, int green, int blue){
  lcd.setCursor(2,1);
  lcd.print("000");
  lcd.setCursor(2,1);
  lcd.print(red);

  lcd.setCursor(7,1);
  lcd.print("000");
  lcd.setCursor(7,1);
  lcd.print(green);  
 
  lcd.setCursor(12,1);
  lcd.print("000");
  lcd.setCursor(12,1);
  lcd.print(blue);
  
  #ifdef COMMON_ANODE
  red = 255 - red;
  green = 255 - green;
  blue = 255 - blue;
  #endif

  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}
