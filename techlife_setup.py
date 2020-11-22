#!/usr/bin/env python
# 1. Modify the variables according to your setup: ssid, password, bssid, [email]
# 2. Connect the computer to AP-TechLife-xx-xx SSID
# 3. Run the script
import socket

# Variables to change
ssid = '<SSID>'
password = '<WIFIPWD>'
bssid = bytearray([0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa]) # Enter your WiFi router's WiFi interface MAC address in hex (eg. AA:AA:AA:AA:AA:AA) <NOT REALLY NEEDED>
email = 'none@nowhere.com' # not absolutely required

# The bulb's network details
TCP_IP = '192.168.66.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024

# Initialize Payload
payload = bytearray(145)
payload[0x00] = 0xff
payload[0x69] = 0x01

# Add the SSID to the payload
ssid_start = 0x01
ssid_length = 0
for letter in ssid:
    payload[(ssid_start + ssid_length)] = ord(letter)
    ssid_length += 1

# Add the WiFi password to the payload
pass_start = 0x22
pass_length = 0
for letter in password:
    payload[(pass_start + pass_length)] = ord(letter)
    pass_length += 1

# Add the BSSID to the payload
bssid_start = 0x63
bssid_length = 0
for digit in bssid:
    payload[(bssid_start + bssid_length)] = digit
    bssid_length += 1

# Add the email to the payload
email_start = 0x6a
email_length = 0
for letter in email:
    payload[(email_start + email_length)] = ord(letter)
    email_length += 1

checksum = 0
j = 1
while j < 0x8f:
   checksum = (payload[j] ^ checksum)
   checksum = checksum & 0xff
   j += 1

payload[0x8e] = 0xf0
payload[0x8f] = checksum & 0xff
payload[0x90] = 0xef

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(payload)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)