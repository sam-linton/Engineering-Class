#
# BLE Server Test
#
import uasyncio as asyncio
from ble_server import BLEServer
from machine import Pin

button = Pin(0, Pin.IN, Pin.PULL_UP)

def button_pressed():
    if button.value() == 1:
        return 'on'
    else:
        return 'off'

server = BLEServer(
    name='BLE Test',
    create_message_func=button_pressed,
    send_interval_ms=2000)

server.start()