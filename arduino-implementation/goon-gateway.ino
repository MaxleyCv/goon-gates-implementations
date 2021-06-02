#include <Arduino_JSON.h>
#include "TransmissionModule.h"
#include "constants.h"


int NORMALDISTANCEINCM = 100;
JSONVar messageBuffer;

int trigPin = 19; 
int echoPin = 18;  
double memory[10] = {10, 10, 10, 10, 10, 10, 10, 10, 10, 10};

bool checked = false;


TransmissionModule transmissionModule;
extern int message_sent = 0;

void setup() {
   Serial.begin(9600);
   delay(3000);
   
   Serial.println("Hello");
   transmissionModule.setup_wifi();
   transmissionModule.init();
}

void loop() {

  double duration, distance;
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPin, LOW); 
  duration = pulseIn(echoPin, HIGH); 
  distance = duration/58;
  for (int i = 9; i > 0; --i){
    memory[i] = memory[i - 1];
  }
  memory[0] = distance;
  double shit = 0;
  for (int i = 0; i < 10; i++){
    shit += memory[i];
  }
  shit /= 10;

  
  if(checked){
   messageBuffer["id"] = "CZ1";
   messageBuffer["time"] = shit;
   String stringToSend = JSON.stringify(messageBuffer);
if (!transmissionModule.client.connected()) {
   transmissionModule.reconnect();
   }
   transmissionModule.client.loop();
   while(message_sent == 0){
        
        if (!transmissionModule.client.connected()) {
           transmissionModule.reconnect();
           }
           transmissionModule.client.loop();
        transmissionModule.sendMessage(TOPIC, stringToSend.c_str());
        delay(2000);
   }
   checked = false;
  }
   message_sent = 0;
   Serial.println(stringToSend.c_str());

   if (shit > 4 * NORMALDISTANCEINCM){
      checked = true;    
   }
}
