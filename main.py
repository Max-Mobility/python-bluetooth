import pygatt
from binascii import hexlify
import time, signal

from smartDrive import *
from app import *

from packet import *

#import logging
#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.BGAPIBackend(serial_port='COM4')

def stop(code):
    print("Stopping")
    adapter.stop()
    exit(code)

def ctrl_c_handler(signal, frame):
    stop(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

motorOn = False

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was
              received on
    value -- bytearray, the data returned in the notification
    """
    #print("Received data: %s" % hexlify(value))
    if len(value) == 18:
        motorOn = bool(value[2])
        print("Motor status: " + ("On" if motorOn else "Off"))

def handle_app_data(handle, value):
    print("Received data: %s" % hexlify(value))

def main():
    settings = makeSettings({
        "ControlMode": "Advanced",
        "Units": "English",
        "Flags": 0x01,
        "TapSensitivity": 1.0,
        "Acceleration": 0.5,
        "MaxSpeed": 0.5
    })
    print(hexlify(settings))
    adapter.start()

    devices = adapter.scan(timeout=1);

    for dev in devices:
        #print(dev)
        if dev.has_key('packet_data') and\
           dev['packet_data'].has_key('connectable_advertisement_packet') and\
           dev['packet_data']['connectable_advertisement_packet'].has_key('complete_list_128-bit_service_class_uuids') and\
           dev['packet_data']['connectable_advertisement_packet']['complete_list_128-bit_service_class_uuids'][0] == smartDriveService[0] and\
           dev['rssi'] > -80:
            print("Found Smart Drive DU: " + dev['address'] + ' ' + str(dev['rssi']))
            smartDriveAddresses.append(dev['address'])

        elif dev.has_key('packet_data') and\
           dev['packet_data'].has_key('connectable_advertisement_packet') and\
           dev['packet_data']['connectable_advertisement_packet'].has_key('complete_list_128-bit_service_class_uuids') and\
           dev['packet_data']['connectable_advertisement_packet']['complete_list_128-bit_service_class_uuids'][0] == appService[0] and\
           dev['rssi'] > -80:
            print("Found PushTracker App: " + dev['address'] + ' ' + str(dev['rssi']))
            appAddresses.append(dev['address'])

    '''
    for addr in smartDriveAddresses:
        try:
            device = adapter.connect(addr)
        except:
            print("Couldn't connect to SmartDrive at: "+addr)
            continue

        smartDrives[addr] = device
        print('Connected to '+addr)

        for char in smartDriveChars:
            print ('Subscribing to: ' + char)
            try:
                device.subscribe(char, callback=handle_data, indication=True)
            except:
                print("Couldn't subscribe to: " + char)
    '''

    for addr in appAddresses:
        try:
            device = adapter.connect(
                address=addr,
                timeout=10,
                address_type=pygatt.BLEAddressType.random,
                interval_min=60,
                interval_max=75,
                supervision_timeout=100,
                latency=0
            )
        except pygatt.exceptions.NotConnectedError:
            print("Couldn't connect to app at: "+addr)
            continue
        except pygatt.exceptions.BLEError:
            print("Unknown error connecting to app at: "+addr)
            stop(-1)

        apps[addr] = device
        print('Connected to '+addr)

        for char in appChars:
            print ('Subscribing to: ' + char)
            try:
                device.subscribe(char, callback=handle_app_data, indication=True)
                device.char_write(char, [0x01, 0x00])
            except:
                print("Couldn't subscribe to: " + char)

    print('Subscribed, looping forever; press ctrl+c to quit')
        
    time.sleep(1)
    sentSettings = False
    doubleTapped = False
    while True:
        time.sleep(0.5)
        # do nothing
        for k,v in smartDrives.iteritems():
            try:
                if not sentSettings:
                    v.char_write(
                        ctrlChar,
                        makePacket("Command", "SetSettings",
                                   settings, 16),
                        True
                    )
                    sentSettings = True
                    print('Sent Settings')
                else:
                    if doubleTapped:
                        time.sleep(3)
                        doubleTapped = False
                    else:
                        doubleTapped = True
                    v.char_write(
                        ctrlChar,
                        #makePacket("Command", "StartOTA", [0x00], 1),
                        makePacket("Command", "Tap", [], 0),
                        True
                    )
                    print('Sent Tap')
            except:
                print("Couldn't write to: "+k)


if __name__ == "__main__":
    main()
