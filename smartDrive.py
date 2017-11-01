import pygatt
from binascii import hexlify

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

    device.subscribe("e9add780b0424876aae1112855353cc1",
                     callback=handle_data)
finally:
    adapter.stop()
