# Stepper motor control software for Raspberry RP2
# Mitchell Kampert
# V1.0

from machine import Pin, PWM
import utime

led = Pin(25, Pin.OUT)
led.value(False)

PUL = Pin(2, Pin.OUT)          #GP2
DIR = Pin(3, Pin.OUT)          #GP3
ENA = Pin(4, Pin.OUT)          #GP4

led.value(True)
utime.sleep(1)
led.value(False)
ENA.value(False)
utime.sleep(1)

DIR.value(False)

pwm = PWM(PUL)

pwm.duty_u16(0)

pwm.freq(10)

while True:
    error = True

    while error:
        go = input("Continue? (Y/n)")

        if go.upper() == "Y" or go == "":
            error = False
            stop = False
        elif go.upper() == "N":
            error = False
            stop = True
        else:
            print("Please type y or n.")


    if stop:
        break

    f_max = int(input("Set max frequency: "))

    ENA.value(True)

    pwm.duty_u16(32768) # duty 50% (65535/2)

    for f in range(50, f_max):

        pwm.freq(f+1)
        utime.sleep_us(5000)
        
    led.value(True)

    print(f"Max frequency of {f_max} reached.")
    print("Running for 5 seconds.")
    utime.sleep(5)
    ENA.value(False)
    pwm.duty_u16(0)
    pwm.freq(10)
    print("Motor stopped.")
    led.value(False)
