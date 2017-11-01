import pygatt
from binascii import hexlify
import time, signal

adapter = pygatt.BGAPIBackend(serial_port='COM4')

smartDriveName = "Smart Drive DU"

smartDriveChars = [
    "e7add780b0424876aae1112855353cc1",
    "e8add780b0424876aae1112855353cc1",
    "e9add780b0424876aae1112855353cc1",
    "eaadd780b0424876aae1112855353cc1",
    "ebadd780b0424876aae1112855353cc1"
]

dataChar = smartDriveChars[1]

smartDriveAddresses = []

def ctrl_c_handler(signal, frame):
    adapter.stop();
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()

    devices = adapter.scan();

    for dev in devices:
        
        if dev['name'] and dev['name'] == smartDriveName:
            print("Found Smart Drive DU: " + dev['address'])
            smartDriveAddresses.append(dev['address'])

    for addr in smartDriveAddresses:
        device = adapter.connect(addr)
        print('Connected to '+addr)

        for char in smartDriveChars:
            print ('Subscribing to: ' + char)
            device.subscribe(char, callback=handle_data, indication=True)

    print('Subscribed, looping forever; press ctrl+c to quit')
    while True:
        # do nothing
        time.sleep(1)

except:
    print("Stopped")
    adapter.stop()
