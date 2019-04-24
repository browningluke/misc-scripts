float R1 = 10000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int Vo = analogRead(0);
  
  Serial.print("Temperature: "); 
  Serial.print(Vo);
  Serial.println(" K"); 

  delay(500);


}
