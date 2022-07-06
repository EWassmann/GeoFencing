 #include <Arduino.h>
#include <Servo.h>

Servo servo1;
int servoPin1 = 9;
Servo esc;
int servoPin2 = 10;

void setup() {
  servo1.attach(servoPin1);
  esc.attach (servoPin2);
  Serial.begin(2000000);
  while(!Serial){
    ;//WAITING FOR THE Serial TO CONNECT
  }
  Serial.setTimeout(200);
esc.write(80);

}
int timer;
int last;
int commandfromjetson;
void loop() {
   
  //waiting for jetson command
  if (Serial.available()>0){
  commandfromjetson = Serial.readString().toInt();
 //0 is straight 1 is left 2 is right 3 is bacwards 4 is stop
 if (commandfromjetson != 5){
timer = 0;
  }
 }
 
  if (commandfromjetson == 0){
    servo1.writeMicroseconds(1650);
    esc.write(95);
    last = 0;
  }
  if (commandfromjetson == 1){
  servo1.writeMicroseconds(2200);  
  esc.write(95); 
  last = 1;
  }                       
  if (commandfromjetson ==2){
  servo1.writeMicroseconds(1000);   
  esc.write(95);
  last = 2;
  }
  if (commandfromjetson == 3){
    servo1.writeMicroseconds(1650);
    esc.write(60);
    last = 3;
  }
  if (commandfromjetson == 4){
    servo1.writeMicroseconds(1650);
    esc.write(80);
    last = 4;
  }
  if (commandfromjetson == 5){
    if (timer >=3000){
      servo1.writeMicroseconds(1000);  
  esc.write(95); 
  last = 1;
  delay(1);
  timer = timer + 1;
 
    }
    if (timer <3000){
       servo1.writeMicroseconds(1650);
    esc.write(95);
    last = 0;
    delay(1);
    timer = timer + 1;
    
    }
  if (timer >= 6000){
    timer = 0;
  }
  }
  

  }  
  
