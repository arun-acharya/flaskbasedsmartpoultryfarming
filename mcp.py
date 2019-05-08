import time
from gpiozero import MCP3008
 
divider = MCP3008(1)
 
while True:
    print(divider.value)
    time.sleep(1.0)
