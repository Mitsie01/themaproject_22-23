
from machine import Pin 
import utime

led = Pin(2, Pin.OUT)
led.value(True)

step = Pin(12, Pin.OUT)         #D6
direction = Pin(14, Pin.OUT)    #D5
enable = Pin(13, Pin.OUT)       #D7

enable.value(True)

led.value(False)
print(led.value())
utime.sleep(1)
led.value(True)
enable.value(False)
direction.value(True)
utime.sleep(1)


for n in range(1000):
    step.value(True)
    led.value(False)
    utime.sleep_us(2000)
    step.value(False)
    led.value(True)
    utime.sleep_us(10000)

