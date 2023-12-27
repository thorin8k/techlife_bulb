"""TechLife Bulb Home Assistant Intergration"""
import paho.mqtt.client as mqtt

import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.light import (SUPPORT_BRIGHTNESS,
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity)
from homeassistant.const import  CONF_NAME

_LOGGER = logging.getLogger(__name__)

CONF_MAC_ADDRESS = 'mac_address'
CONF_BROKER_URL = 'broker_url'
CONF_BROKER_USERNAME = 'broker_username'
CONF_BROKER_PASSWORD = 'broker_password'


# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC_ADDRESS): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_BROKER_URL): cv.string,
    vol.Required(CONF_BROKER_USERNAME): cv.string,
    vol.Required(CONF_BROKER_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    mac = config.get(CONF_MAC_ADDRESS)
    name = config.get(CONF_NAME)
    broker_url = config.get(CONF_BROKER_URL)
    broker_username = config.get(CONF_BROKER_USERNAME)
    broker_password = config.get(CONF_BROKER_PASSWORD)

    try:
        client = mqtt.Client()
        client.username_pw_set(broker_username, broker_password)

        client.connect(broker_url, 1883, 60)
        client.loop_start()

    except:
        _LOGGER.error(
            "Could not connect to mqtt broker. Check credentials or url.")

    add_entities([TechlifeControl(mac, client, name)])


class TechlifeControl(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, mac, client, name):
        """Initialize an AwesomeLight."""
        self.mac = mac
        self.client = client
        self._name = name
        self._state = False
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.
        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    # @property
    # def assumed_state(self):
    #     return True

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS


    def turn_on(self, **kwargs):
        """Instruct the light to turn on.
        You can skip the brightness part if your light does not support
        brightness control.
        """
        if not self._state:
            self.on()
        self._state = True

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]

        if self._brightness is not None:
            br = max(round(self._brightness / 2.55), 1)
            self.dim(br)


    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self.off()
        self._state = False


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