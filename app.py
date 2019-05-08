import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import sys
import Adafruit_DHT
from gpiozero import MCP3008
import time

mq135 = MCP3008(0)  #setting up mq135 sensor at pin 0 of mcp3008 ADC IC
mq2 = MCP3008(1)        #setting up mq2 sensor at pin 1 of mcp3008 ADC IC
 

app = Flask(__name__) #starting flask
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
	
@app.route("/")#creation of landing page
def index():
	# Read Sensors Status
	fanSts = GPIO.input(fan)
	ledSts = GPIO.input(led)
	mq135Sts = mq135.value
	mq2Sts = mq2.value
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        #storing into variables to pass to html file
	templateData = {
              'title' : 'Status of the Devices!',
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
              'mq135' : mq135Sts,
              'mq2' : mq2Sts,
       }
	return render_template('index.html', **templateData)   #redirecting landing page to use external file and passing data to it

	
@app.route("/<deviceName>/<action>") #creating other pages for other actions
def action(deviceName, action):
	if deviceName == 'fan': #checks if fan's button was pressed
		actuator = fan

	if deviceName == 'led': #checks if led's button was pressed
		actuator = led   
	if action == "on": #checks wether on or off button was pressed
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off": #checks wether on or off button was pressed
		GPIO.output(actuator, GPIO.LOW)
	if action == "check": #checks if temprature and humudity check button was pressed
                humidity, temperature = Adafruit_DHT.read_retry(11, 4)
                
        #reads the current status of actuators
	fanSts = GPIO.input(fan)
	ledSts = GPIO.input(led)
	#reads the sensor's values
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	mq135Sts = mq135.value
	mq2Sts = mq2.value
        #storing into variables to pass to html file
	templateData = {
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
              'mq135' : mq135Sts,
              'mq2' : mq2Sts,
	}
	return render_template('index.html', **templateData)    #redirecting landing page to use external file and passing data to it

def InterruptFanOn(fanon): #function for turning on fan if it is  off when temprature is high
  print("Fan ON Interrupt")
  if GPIO.input(fan) == 0 :
          GPIO.output(fan, GPIO.HIGH)
  else:
          print('Fan on ignored')

def InterruptFanOff(fanoff): #function for turning offf fan if it is on when temprature is low
  print("Fan OFF Interrupt")
  if GPIO.input(fan) == 1 :
          GPIO.output(fan, GPIO.LOW)
  else:
          print('Fan off ignored')

#setting up interrupt to detect High temprature status from arduino
fanon = 20
GPIO.setup(fanon, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #reads the pin state
GPIO.add_event_detect(fanon, GPIO.RISING, callback=InterruptFanOn)#creates interrupt event when the pin is High and calls fanon function 

#setting up interrupt to detect Low temprature status from arduino
fanoff = 16
GPIO.setup(fanoff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #reads the pin state
GPIO.add_event_detect(fanoff, GPIO.RISING, callback=InterruptFanOff)#creates interrupt event when the pin is Low and calls fanoff function 



if __name__ == "__main__": #starts flask server on specified IP address
   app.run(host="192.168.1.86", port=80, debug=True)

        

