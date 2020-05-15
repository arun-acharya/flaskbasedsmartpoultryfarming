#include <dht.h>

dht DHT;

#define DHT11_PIN 7

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  if (DHT.temperature >= 32){
     Serial.println("Temperature is high, turning on the fan");
    digitalWrite(13, HIGH);
    digitalWrite(12, LOW);
    }
  else {
    digitalWrite(13, LOW);
    digitalWrite(12, HIGH);
     Serial.println("Temperature is low, turning off the fan");
    }
  delay(20000);
}
