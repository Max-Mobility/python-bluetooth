smartDriveName = "Smart Drive DU"

smartDriveService = [u'0x0C:D5:16:66:E7:CB:46:9B:8E:4D:27:42:F1:BA:77:23'] #"0cd51666e7cb469b8e4d2742f1ba7723"

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

'''
{
'rssi': -71, 
'packet_data': 
{
  'scan_response_packet': 
  {
    'complete_local_name': u'Smart Drive DU'
  }, 
  'connectable_advertisement_packet': 
  {
    'complete_list_128-bit_service_class_uuids': [u'0x0C:D5:16:66:E7:CB:46:9B:8E:4D:27:42:F1:BA:77:23'], 
    'flags': bytearray(b'\x06')
  }
}, 
'name': u'Smart Drive DU', 
'address': u'00:07:80:A5:49:8C'
}
'''
