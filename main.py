import pygatt
from binascii import hexlify
import time, signal

from smartDrive import *

from packet import *

adapter = pygatt.BGAPIBackend(serial_port='COM4')

def stop(code):
    print("Stopping")
    adapter.stop()
    exit(code)

def ctrl_c_handler(signal, frame):
    stop(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

def main():
    makeSettings("Advanced", "English", 0x01, 1.0, 0.5, 0.5)
    try:
        adapter.start()
    except:
        stop(-1)

    devices = adapter.scan();

    for dev in devices:
        
        if dev['name'] and dev['name'] == smartDriveName:
            print("Found Smart Drive DU: " + dev['address'])
            smartDriveAddresses.append(dev['address'])

    for addr in smartDriveAddresses:
        try:
            device = adapter.connect(addr)
        except:
            print("Couldn't connect to: "+addr)
            continue

        smartDrives[addr] = device
        print('Connected to '+addr)

        for char in smartDriveChars:
            print ('Subscribing to: ' + char)
            try:
                device.subscribe(char, callback=handle_data, indication=True)
            except:
                print("Couldn't subscribe to: " + char)

    print('Subscribed, looping forever; press ctrl+c to quit')
    while True:
        # do nothing
        for k,v in smartDrives.iteritems():
            try:
                v.char_write(
                    ctrlChar,
                    makePacket("Command", "Tap", [], 0)
                )
            except:
                print("Couldn't write to: "+k)
        time.sleep(1)


if __name__ == "__main__":
    main()
