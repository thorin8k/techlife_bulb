
import paho.mqtt.client as mqtt


class TechlifeControl():
    """Representation of an Awesome Light."""

    def __init__(self, mac, client, name):
        """Initialize an AwesomeLight."""
        self.mac = mac
        self.client = client
        self._name = name
        self._state = None
        self._brightness = None


    def send(self, cmd):
        command = self.calc_checksum(cmd)
        sub_topic = "dev_sub_%s" % self.mac
        self.client.publish(sub_topic, command)

    def dim(self, value):
        v = int(100 * value)
        self.send(self.cmd_brightness(v))

    def on(self):
        self.send(bytearray.fromhex(
            "fa 23 00 00 00 00 00 00 00 00 00 00 00 00 23 fb"))

    def off(self):
        self.send(bytearray.fromhex(
            "fa 24 00 00 00 00 00 00 00 00 00 00 00 00 24 fb"))

    def calc_checksum(self, stream):
        checksum = 0
        for i in range(1, 14):
            checksum = checksum ^ stream[i]
        stream[14] = checksum & 0xFF
        return bytearray(stream)

    def cmd_brightness(self, value):
        assert 0 <= value <= 10000
        payload = bytearray.fromhex(
            "28 00 00 00 00 00 00 00 00 00 00 00 00 f0 00 29")
        payload[7] = value & 0xFF
        payload[8] = value >> 8
        return payload

client = mqtt.Client()
client.username_pw_set("mosquito", "mosquito")

client.connect("192.168.1.146", 1883, 60)

control = TechlifeControl("d2:9b:bd:11:c2:e0", client, "habitacion")

#control.on()
control.off()
#control.dim(10)
