#
# blink.py
#
# Pins
# ----
# GP16 - LED +
# GND  - LED -
#
from machine import Pin
from utime import sleep

led = Pin(16, Pin.OUT) # GP16 (21)

while True:
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
