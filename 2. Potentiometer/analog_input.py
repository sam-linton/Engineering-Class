#
# analog_input.py
#
# Pins
# ----
# 3.3V - Pot +
# GP26 - Pot Wiper
# GnD  - Pot -
#
from machine import Pin, ADC
from time import sleep

adc = ADC(Pin(26)) # GP26 (31)

while True:
    print(adc.read_u16())
    sleep(0.1)