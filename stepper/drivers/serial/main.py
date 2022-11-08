# Stepper motor control software for ESP8266
# Mitchell Kampert
# V1.0

from machine import Pin 
import utime
import time
import sys

led = Pin(2, Pin.OUT)
led.value(True)

PUL = Pin(12, Pin.OUT)          #D6
DIR = Pin(14, Pin.OUT)          #D5
ENA = Pin(13, Pin.OUT)          #D7

led.value(False)
utime.sleep(1)
led.value(True)
ENA.value(False)
utime.sleep(1)


def to_delay(RPM, setting):
    delay_us = int((10**6)/((RPM/60)*(setting*2)))
    return delay_us
    

def step(delay_us):
    PUL.value(True)
    utime.sleep_us(delay_us)
    PUL.value(False)
    utime.sleep_us(delay_us)


def build(delay_us):
    print("[ starting ] Starting buildup procedure.")
    delay_build = 10*(10**3)
    t0 = time.time_ns()
    while delay_build > delay_us:
        step(delay_build)
        delay_build -= int((time.time_ns() - t0)*(1*10**-7))


def drive(delay_us, duration):
    build(delay_us)
    print("[    ok    ] Buildup completed.")
    led.value(False)
    print("[    ok    ] Nominal motor speed achieved.")
    dt = 0
    t0 = time.time_ns()
    print(f"[    ok    ] Motor timer started. Running {duration} seconds.")
    while dt <= duration*10**9:
        step(delay_us)
        dt = time.time_ns() - t0
    
    led.value(True)
    print("[    ok    ] Motor stopped.")


while True:
    try:
        proceed = False
        speed = int(input("Set RPM: "))
        tspan = int(input("Set Time: "))
        setting = int(input("Steps per revolution: "))
        while not proceed:
            dir = input("Set direction (R/L): ")

            if dir.upper() == "R":
                DIR.value(True)
                proceed = True
            elif dir.upper() == "L":
                DIR.value(False)
                proceed = True
            else:
                print('''
[ error ] Please choose between R or L.
''')

        delay_us = to_delay(speed, setting)
        print("[ starting ] Enabling motor drive.")
        ENA.value(False)
        print("[    ok    ] Motor drive enabled.")
        print('[ starting ] Starting motor.')
        drive(delay_us, tspan)
        ENA.value(True)
        print("[    ok    ] Motor drive disabled.")
        
        proceed = False
        while not proceed:
            stop = input('''
Continue? (Y/n): ''')
            if stop.upper() == "Y" or stop == "":
                proceed = True
                stop = False
            elif stop.upper() == "N":
                print("[    ok    ] Shutdown initiated.")
                proceed = True
                stop = True
            else:
                print('''
[ error ] Please choose y or n.
''')

        if stop:
            break

    except:
        proceed = False

        print('''
[ error ] Please check your input variables.
''')

        while not proceed:
            stop = input('''
Continue? (Y/n): ''')
            if stop.upper() == "Y" or stop == "":
                proceed = True
                stop = False
            elif stop.upper() == "N":
                print("[    ok    ] Shutdown initiated.")
                proceed = True
                stop = True
            else:
                print('''
[ error ] Please choose y or n.
''')

        if stop:
            break