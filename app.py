import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import sys
import Adafruit_DHT


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
fan = 13
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
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	templateData = {
              'title' : 'Status of the Devices!',
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
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
   
	templateData = {
              'fan'  : fanSts,
              'led'  : ledSts,
              'temp'  : temperature,
              'humi'  : humidity,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='192.168.10.107', port=80, debug=True)

