import sys
import paho.mqtt.client as mqtt
import time
import binascii
import traceback

print 'Argument List:', str(sys.argv)

mqtt_broker = sys.argv[1] #your MQTT broker's IP address
mac_address = sys.argv[2] #your bulb's MAC Address 
pub_topic = "dev_pub_%s" % mac_address # MQTT topic to receive responses
sub_topic = "dev_sub_%s" % mac_address # MQTT topic to send the query commands to
debug = False #Set to True if you want more verbosed output

############### MQTT callbacks ########################
def on_connect(client, userdata, flags, rc):
    if debug: print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(pub_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    parsePayload(msg.topic, msg.payload)


def calcChecksum(stream):
    checksum = 0
    for i in range(1, 14):
        checksum = checksum ^ stream[i]
    stream[14] = checksum & 255

    return bytearray(stream)

############### Techlife commands ########################
def turnOff():
    payload = bytearray.fromhex("FA 24 00 00 00 00 00 00 00 00 00 00 00 00 24 FB")
    return calcChecksum(payload)

def turnOn():
    payload = bytearray.fromhex("FA 23 00 00 00 00 00 00 00 00 00 00 00 00 23 FB")
    return calcChecksum(payload)


############### Main ########################
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('mosquito','mosquito')

client.connect(mqtt_broker, 1883, 60)
client.loop_start()


if sys.argv[3] == "ON":
    client.publish(sub_topic, turnOn())
elif sys.argv[3] == "OFF":
    client.publish(sub_topic, turnOff())


time.sleep(1)

client.loop_stop()
client.disconnect()