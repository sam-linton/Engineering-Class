import aioble
import bluetooth
import machine
import uasyncio as asyncio

# Bluetooth UUIDS can be found online at https://www.bluetooth.com/specifications/gatt/services/

_REMOTE_UUID = bluetooth.UUID(0x1848) # This should be settable
_ENV_SENSE_UUID = bluetooth.UUID(0x1800) # TODO: this should be settable
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

class BleClient():
    
    def __init__(self, name):
        self._name = name
        self._connected = False
        
    async def find_server(self, name: str) -> Device | None: # Figure out return type
        '''
        Find the server with the given name
        
        '''
        print('scanning...')
        async with aioble.scan(
            5_000,
            interval_us = 30_000,
            window_us = 30_000,
            active = True
        ) as scanner:
            async for result in scanner:
                if result.name() == name:
                    print(f'Found {name} server.')
                    for item in result.services():
                        print(item)
                    if _ENV_SENSE_UUID in result.services():
                        print(f'type of result.device is  + {type(result.device)}')
                        return result.device
        return None
    
    async def connect_to_service(self) -> None:
        '''
        Connect to the server and receive its message
        
        '''
        print('starting peripheral task')
        self._connected = False
        
        # Find the server
        device = await self.find_server(self._name)
        if not device:
            print("server not found")
            return
        
        try:
            print("Connecting to", device)
            connection = await device.connect()
            
        
        except asyncio.TimeoutError:
            print("Timeout during connection")
            return
        
        async with connection:
            print('Connected')
            self._connected = True

            while self._connected:
                try:
                    print('Getting service')
                    print(f'_REMOTE_UUID: {_REMOTE_UUID}')
                    service = await connection.service(_REMOTE_UUID) # TODO: fflexible service
                    print(f'Service: {service}')
                    control_characteristic = await service.characteristic(_REMOTE_CHARACTERISTICS_UUID)
                    print(control_characteristic)
                    
                except asyncio.TimeoutError:
                    print("Timeout discovering services/characteristics")
                    return
                
                while True:
                    if control_characteristic == None:
                        print('no characteristic')
                        await asyncio.sleep_ms(10)
                        return
                    
                    if control_characteristic != None:
                        try:
                            command = await control_characteristic.read()
                            if command != b'': print(command)

#                             if command == b'a':
#                                 print("a button pressed")
#                             elif command == b'b':
#                                 print("b button pressed")
#                             elif command == b'x':
#                                 print("x button pressed")
#                             elif command == b'y':
#                                 print("y button pressed")
                            await asyncio.sleep_ms(1)
                            
                        except TypeError:
                            print(f'something went wrong; remote disconnected?')
                            self._connected = False
                            return
                        except asyncio.TimeoutError:
                            print(f'something went wrong; timeout error?')
                            self._connected = False
                            return
                        except asyncio.GattError:
                            print(f'something went wrong; Gatt error - did the remote die?')
                            self._connected = False
                            return
                    await asyncio.sleep_ms(1)
    
async def main():
    client = BleClient('server')
    tasks = [
        asyncio.create_task(client.connect_to_service())
    ]
    await asyncio.gather(*tasks)
    
    
if __name__ == '__main__':
    asyncio.run(main())
            
            
        
        
        