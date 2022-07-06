 #include <Arduino.h>
#include <Servo.h>
//initalizing the servo pins that will be used, 9 controlls both front servos, 10 is the motor controller
Servo servo1;
int servoPin1 = 9;
Servo esc;
int servoPin2 = 10;
int timer;
//the functions are relatively straighforward, the writeMicroseconds number is what i thought looked like it would work well with testing 
//but this may need to be changed (robot appears to be rubbing) the speed can also be changed here.
//---------------functions-----------------
void Straight(){
  servo1.writeMicroseconds(1650);
    esc.write(95);
}
void Left(){
  servo1.writeMicroseconds(2200);  
  esc.write(95); 
}
void Right(){
   servo1.writeMicroseconds(1000);   
  esc.write(95);
}
void Back(){
  servo1.writeMicroseconds(1650);
    esc.write(60);
}
void Stop(){
  servo1.writeMicroseconds(1650);
    esc.write(80);
}
//the search function has the robot turn right for 3000 iterations and then drive straight for 3000 iteratioins.
//this worked okay in the yard, can be made more complicated, as in adding a spiral and whatnot probably the most complicated part of the code.
void Search(){
  if (timer >=3000){
      servo1.writeMicroseconds(1000);  
  esc.write(95); 
  delay(1);
  timer = timer + 1;
    }
    if (timer <3000){
       servo1.writeMicroseconds(1650);
    esc.write(95);
    delay(1);
    timer = timer + 1;
    }
  if (timer >= 6000){
    timer = 0;
  }
}
//-----------------------------------------



int commandfromjetson;
//attaching servo pins and waiting to connect to the jetson, also trying to initalize the esc, you may need to open up other code of get the main
//function to write 80 to it somehow if the robot is not moving, need to hear the beep!
void setup() {
  servo1.attach(servoPin1);
  esc.attach (servoPin2);
  Serial.begin(2000000);
  while(!Serial){
    ;//WAITING FOR THE Serial TO CONNECT
  }
  Serial.setTimeout(200);
esc.write(80);
commandfromjetson =4;
}



void loop() {
   
  //waiting for jetson command, then goes through the if loops and sees which one it triggers. 
  //any sort of decision on when to go into search needs to be included in the larger python code.
  if (Serial.available()>0){
  commandfromjetson = Serial.readString().toInt();
 //0 is straight 1 is left 2 is right 3 is bacwards 4 is stop
 if (commandfromjetson != 5){
timer = 0;
  }
 }
 
  if (commandfromjetson == 0){
    Straight();
  }
  if (commandfromjetson == 1){
    Left();
  }                       
  if (commandfromjetson ==2){
  Right();
  }
  if (commandfromjetson == 3){
    Back();
  }
  if (commandfromjetson == 4){
    Stop();
  }
  if (commandfromjetson == 5){
  Search();
  }
  

  }  
  
