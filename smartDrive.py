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
ctrlChar = smartDriveChars[2]

smartDriveAddresses = []
smartDrives = {}

PacketTypes = [
    "None",
    "Data",
    "Command",
    "Error",
    "OTA"
]

DataTypes = [
    "MotorDistance",
    "Speed",
    "CoastTime",
    "Pushes",
    "MotorState",
    "BatteryLevel",
    "VersionInfo",
    "DailyInfo",
    "JourneyInfo",
    "MotorInfo",
    "DeviceInfo",
    "Ready",
    "BatteryInfo",
]

CommandTypes = [
    "SetAcceleration",
    "SetMaxSpeed",
    "Tap",
    "DoubleTap",
    "SetControlMode",
    "SetSettings",
    "TurnOffMotor",
    "StartJourney",
    "StopJourney",
    "PauseJourney",
    "SetTime",
    "StartOTA",
    "StopOTA",
    "OTAReady",
    "CancelOTA",
    "Wake",
    "StartGame",
    "StopGame",
    "ConnectMPGame",
    "DisconnectMPGame"
]

OTATypes = [
    "SmartDrive",
    "SmartDriveBluetooth",
    "PushTracker"
]

TypeToSubType = {
    "Data": DataTypes,
    "Command": CommandTypes,
    "OTA": OTATypes,
}

def printPacket(p):
    print hexlify(p)

def makePacket(Type, SubType, data, length):
    packet = bytearray(length + 2)
    packet[0] = PacketTypes.index(Type)
    packet[1] = TypeToSubType[Type].index(SubType)
    for i in range(0,length):
        packet[2 + i] = data[i]
    return packet

def makeHeader(version, checksum):
    length = 16
    data = bytearray(length)
    data[0] = version
    data[4] = checksum & 0xFF
    data[5] = (checksum >> 8) & 0xFF
    data[6] = (checksum >> 16) & 0xFF
    data[7] = (checksum >> 24) & 0xFF
    return makePacket("OTA", "SmartDrive", data, length)

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
