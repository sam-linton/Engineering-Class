#
# ultrasonic_sensor
#
# Pins
# ----
# 5V   - VCC
# GND  - GND
# GP12 - Echo
# GP13 - Trig
#
from picozero import DistanceSensor
from machine import Pin
from utime import sleep

sensor = DistanceSensor(echo=12, trigger=13)

while True:
    print(100.0*sensor.distance)
    sleep(0.1)

