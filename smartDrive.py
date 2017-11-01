import pygatt
from binascii import hexlify
import time

adapter = pygatt.BGAPIBackend(serial_port='COM4')

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()
    device = adapter.connect('00:07:80:a5:49:8c')
    print('Connected')
    #device.subscribe("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b"
    #"e9add780-b042-4876-aae1-112855353cc1",
    #"e8add780-b042-4876-aae1-112855353cc1",
    device.subscribe("e7add780-b042-4876-aae1-112855353cc1",
                     callback=handle_data)
    device.subscribe("e8add780-b042-4876-aae1-112855353cc1",
                     callback=handle_data)
    device.subscribe("e9add780-b042-4876-aae1-112855353cc1",
                     callback=handle_data)
    device.subscribe("eaadd780-b042-4876-aae1-112855353cc1",
                     callback=handle_data)
    device.subscribe("ebadd780-b042-4876-aae1-112855353cc1",
                     callback=handle_data)

    print('Subscribed, sleeping 10')
    time.sleep(10)

    value = device.char_read("e9add780-b042-4876-aae1-112855353cc1", 10)
    print(value)
    value = device.char_read("e8add780-b042-4876-aae1-112855353cc1", 10)
    print(value)
    value = device.char_read("e7add780-b042-4876-aae1-112855353cc1", 10)
    print(value)
finally:
    print('Failed')
    adapter.stop()
