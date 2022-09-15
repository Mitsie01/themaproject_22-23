try:
  import usocket as socket
except:
  import socket
  
from time import sleep
from machine import Pin
import onewire, ds18x20

import config

import network
import time

import esp
esp.osdebug(None)

import gc
gc.collect()

ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


#create config.py file with network credentials
for x in range(config.Credentials.n):
  num = "n" + str(x+1)
  ssid = (getattr(config, num).network)
  password = (getattr(config, num).password)
  
  print(f"Attempting connection to {ssid}")

  station = network.WLAN(network.STA_IF)

  station.active(True)
  station.connect(ssid, password)

  start = time.time_ns()
  current = time.time_ns()
  while station.isconnected() == False and (current-start) <= 10*(10**9):
    current = time.time_ns()
    pass

  if station.isconnected() == True:
    print('[CONNECTED] Connection successful.')
    print(station.ifconfig())
    break
  else:
    print("[FAILED] Connection failed.")

if station.isconnected() == False:
  print("No connections found. Shutting down.")
  exit(0)