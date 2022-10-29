
from machine import Pin 
import utime
import time

led = Pin(2, Pin.OUT)
led.value(True)

PUL = Pin(12, Pin.OUT)          #D6
DIR = Pin(14, Pin.OUT)          #D5
ENA = Pin(13, Pin.OUT)          #D7

ENA.value(True)

led.value(False)
utime.sleep(1)
led.value(True)
ENA.value(False)
DIR.value(True)
utime.sleep(1)


def to_delay(RPM):
    delay_us = int((10**6)/((RPM/60)*400))
    return delay_us
    


def step(delay_us):
    PUL.value(True)
    utime.sleep_us(delay_us)
    PUL.value(False)
    utime.sleep_us(delay_us)


def build(delay_us):
    start = 2500
    t0 = time.time_ns()
    while start < delay_us:
        step(start)
        start += (time.time_ns() - t0)/(5*10**7)




def drive(delay_us, duration):
    build(delay_us)
    led.value(False)
    dt = 0
    t0 = time.time_ns()
    while dt <= duration*10**9:
        step(delay_us)
        dt = time.time_ns() - t0
    
    led.value(True)



while True:
    try:
        speed = int(input("Set RPM: "))
        tspan = int(input("Set Time: "))
        dir = input("Set direction (R/L): ")

        if dir.upper() == "R":
            DIR.value(True)
        elif dir.upper() == "L":
            DIR.value(False)
        else:
            raise Exception("Please type R or L.")

        delay_us = to_delay(speed)
        drive(delay_us, tspan)
    except:
        print("An error has occurred. Please check your input statements and try again.")