# Complete project details at https://RandomNerdTutorials.com
try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'happy2'
password = 'polotence123'

station = network.WLAN(network.STA_IF)

station.active(True)
# station.ifconfig(("192.168.0.105", "255.255.255.0", "xxx.xxx.x.xx", "8.8.8.8"))
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
data_pin = Pin(5, Pin.OUT)
