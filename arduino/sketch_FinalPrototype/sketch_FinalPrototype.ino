//Include Libraries 
  #include <Servo.h>
  #include <LiquidCrystal.h>
  

//Create Servo and LCD Objects
  Servo servo;
  LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Define Constant RGB LED, Servo & Button Pins
  const int redPin = 6;
  const int greenPin = 7;
  const int bluePin = 8;
  const int servoPin = 15;
  const int buttonPin = 9;

  const int blueTemp; //MAX blue temp
  const int greenTemp; //4 degree range
  const int redTemp; // MIN red temp

//Define Servo Variables
  int buttonState = 0;
  bool toggle = false;



//Run once on startup
  void setup() {
    
    //Attach Servo to servoPin
      servo.attach(servoPin);
    
    //Set buttonPin to INPUT mode
      pinMode(buttonPin, INPUT);

    //Set RGB LED's pin to OUTPUT mode
      pinMode(redPin, OUTPUT);
      pinMode(greenPin, OUTPUT);
      pinMode(bluePin, OUTPUT);
  
    //Set LCD's number of columns and rows:
      lcd.begin(16, 2);

    //Print Temperature header as "T:" on LCD
      lcd.print("T: ");

    //Append "K" to the end, defining variable as 'Kelvin', at 6th column, 1st row
      lcd.setCursor(5,0);
      lcd.print("K");

    //Print "Locked: " to 1st column, 2nd row
    lcd.setCursor(0,1);
    lcd.print("Locked: ");
  }



//Run repeatedly
  void loop() {
    
    //Call Temperature function
    temperature();

    //Cal buttonServo function
    buttonServo();
    
  }



//Temperature function
  void temperature(){
      
      //Set temp Variable and request it
        int temp = analogRead(0);
        
      //Print Temperature to 3rd column, 1st row
        lcd.setCursor(2,0);
        lcd.print(temp);
  
      //Temp is less than blueTemp
        if (temp < blueTemp){
            //Set color to BLUE
              setColor(0, 0, 255);
        }
      
      //Temp is greater than blueTemp AND less than redTemp
        if (temp > blueTemp && temp < redTemp){
            //Set color to GREEN
              setColor(0, 255, 0);
        }
  
      //Temp is greater than redTemp
        if (temp > redTemp){
            //Set color to RED
              setColor(255, 0, 0);
        }
}



//Button servo method
  void buttonServo(){

    //Set buttonState variable to the state of the Button
      buttonState = digitalRead(9);

    //Set LCD Cursor pos to 9th column, 2nd row   
    lcd.setCursor(7,1);
     
     //If button is pushed
     if (buttonState == HIGH){

       //
       if (toggle == false){
         servo.write(45);      // Turn SG90 servo Left to 45 degrees
         delay(1000);          // Wait 1 second
         toggle = true;
  
         lcd.print("FALSE");
       }else{
         servo.write(90);      // Turn SG90 servo back to 90 degrees (center position)
         delay(1000);          // Wait 1 second
         toggle = false;

         lcd.print("TRUE ");
       }  
    
    }
  }


//setColor Function
  void setColor(int red, int green, int blue){    
    #ifdef COMMON_ANODE
    red = 255 - red;
    green = 255 - green;
    blue = 255 - blue;
    #endif
  
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);  
  }
