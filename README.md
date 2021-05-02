## hum-temp-oled

#### sources, helpful links, useful hints

- https://www.raspberry-buy.de/I2C_OLED-Display_Raspberry_Pi_Python_SH1106_SSD1306.html#menu
- https://luma-oled.readthedocs.io/en/develop/python-usage.html
- https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/
- https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi
- https://github.com/adafruit/Adafruit_CircuitPython_Bundle
- https://github.com/adafruit/Adafruit_CircuitPython_DHT
- https://github.com/adafruit/Adafruit_Blinka/issues/259

## Run on boot as service

#### A possibility to enable run at bootup is to use the _systemd_ files.
_systemd_ provides a standard process for controlling what programs run when a Linux system boots up. Note that systemd is available only from the Jessie versions of Raspbian OS.

### Create A Unit File

`sudo nano /lib/systemd/system/oled.service`

```ini
[Unit]
Description = Oled Display service
After = multi-user.target

[Service]
Type = idle
ExecStart = /usr/bin/python3 /home/pi/oled/oled.py

[Install]
WantedBy = multi-user.target
```

`sudo chmod 644 /lib/systemd/system/oled.service`

### Configure systemd

`sudo systemctl daemon-reload`

`sudo systemctl enable oled.service`

`sudo reboot`
