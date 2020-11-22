# TechLife Bulb - Custom Integration
This light integration controls your techlife bulbs without flashing or modifying.


## Requirements:

In order to make the bulb (or bulbs) work you will need to:

- Connect the bulbs to your wifi (Using app or custom script)
- Create an user in your HA called `testuser` with password `testpassword` 
- Redirect bulb traffic to your custom mqtt server redirecting dns entries:
  - Im using **dnsmasq** inside HA with this configuration:
  ``` yaml
    hosts:
      - host: cloud.qh-tek.com
        ip: 192.168.0.0 #brokerip
      - host: cloud.hq-tek.com
        ip: 192.168.0.0 #brokerip
  ```
- Install this in your custom_components folder
- Restart HA


Once you have restarted, the custom_component will be available in your system (check home_assistant.log) so now you can configure your bulbs folowing the **Example Configuration**

Check the links on 'Credits and Info' to know more info about this integration.



## Example Configuration

Example configuration to create an entity called `light.yourbulb`.

``` yaml
light: 
    - platform: techlife_bulb_control
      mac_address: "00:00:00:00:00:00" # Get this from your router in my case lights have this name: lwipr91h_sta
      name: "YourBulb"
      broker_url: 192.168.0.0
      broker_username: !secret broker_username
      broker_password: !secret broker_password
```


## Connecting to wifi - Custom Script

If the bulb is already connected to your wifi yoy can skip this step.
- Download 'techlife_setup.py'
- Ensure python installed in your system.
- Modify ssid, password and bssid inside the script.
- Connect the bulb (Reset if needed turning on / off 6 times)
- Connect your computer to the wifi made by the bulb
- Run `> python techlife_setup.py`


## Credits and Info
I used the following articles and forum posts to make this work, all credit to this people who have extracted all the commands needed to change bulbs state. I only packed all in this custom_component.

- Original Post: https://community.home-assistant.io/t/integrating-techlife-pro-light-bulbs-without-opening-or-soldering/178423


- Python control lib: https://github.com/sergachev/techlife_control


- Base Doc for custom_component: https://github.com/home-assistant/example-custom-config/blob/master/custom_components/example_light






