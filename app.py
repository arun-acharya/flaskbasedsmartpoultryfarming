import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import sys
import Adafruit_DHT
from gpiozero import MCP3008
import time

mq135 = MCP3008(0)
mq2 = MCP3008(1)
 

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
fan = 21
led = 26
#initialize GPIO status variables
fanSts = 0
ledSts = 0
# Define pins as output
GPIO.setup(fan, GPIO.OUT)    
GPIO.setup(led, GPIO.OUT) 
# turns OFF at startup 
GPIO.output(fan, GPIO.LOW)
GPIO.output(led, GPIO.LOW)
	
@app.route("/")
def index():
	# Read Sensors Status
	fanSts = GPIO.input(fan)
	ledSts = GPIO.input(led)
	mq135Sts = mq135.value
	mq2Sts = mq2.value
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	templateData = {
              'title' : 'Status of the Devices!',
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
              'mq135' : mq135Sts,
              'mq2' : mq2Sts,
       }
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'fan':
		actuator = fan

	if deviceName == 'led':
		actuator = led   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
	if action == "check":
                humidity, temperature = Adafruit_DHT.read_retry(11, 4)
                
	fanSts = GPIO.input(fan)
	ledSts = GPIO.input(led)
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	mq135Sts = mq135.value
	mq2Sts = mq2.value
   
	templateData = {
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
              'mq135' : mq135Sts,
              'mq2' : mq2Sts,
	}
	return render_template('index.html', **templateData)

def InterruptFanOn(fanon):
  print("Fan ON Interrupt")
  if GPIO.input(fan) == 0 :
          GPIO.output(fan, GPIO.HIGH)
  else:
          print('Fan on ignored')

def InterruptFanOff(fanoff):
  print("Fan OFF Interrupt")
  if GPIO.input(fan) == 1 :
          GPIO.output(fan, GPIO.LOW)
  else:
          print('Fan off ignored')


fanon = 20
GPIO.setup(fanon, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(fanon, GPIO.RISING, callback=InterruptFanOn)

fanoff = 16
GPIO.setup(fanoff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(fanoff, GPIO.RISING, callback=InterruptFanOff)



if __name__ == "__main__":
   app.run(host="192.168.1.86", port=80, debug=True)

        

