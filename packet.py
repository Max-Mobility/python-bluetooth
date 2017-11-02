import struct
from binascii import hexlify

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

ControlMode = [
    "Beginner",
    "Intermediate",
    "Advanced",
    "Off"
]

Units = [
    "English",
    "Metric"
]

def printPacket(p):
    print hexlify(p)

def makeSettings(s):
    settings = bytearray(16)
    settings[0] = ControlMode.index(s['ControlMode'])
    settings[1] = Units.index(s['Units'])
    settings[2] = s['Flags']

    b = struct.pack('fff', *[s['TapSensitivity'], s['Acceleration'], s['MaxSpeed']])
    for i in range(0,12):
        settings[4+i] = b[i]

    #print hexlify(settings)
    return settings

def makePacket(Type, SubType, data, length):
    packet = bytearray(length + 2)
    packet[0] = PacketTypes.index(Type)
    packet[1] = TypeToSubType[Type].index(SubType)
    for i in range(0,length):
        packet[2 + i] = data[i]
    print(hexlify(packet))
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
