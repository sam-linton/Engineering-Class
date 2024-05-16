#
# button_press.py
#
# Pins
# ----
# 3.3V - Button
# GP15 - Button
#
from machine import Pin

button = Pin(15, Pin.IN, Pin.PULL_DOWN) # GP15 (20)

while True:
    if button.value():
        print('On!')
        while button.value() == 1:
            pass
    else:
        print('Off!')
        while button.value() == 0:
            pass
    
