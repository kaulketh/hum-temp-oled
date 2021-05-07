#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# dht.py
# created 30.04.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
from sys import stdout, stderr
from time import sleep

import adafruit_dht

SENSOR = adafruit_dht.DHT22(24)
EMPTY = ""


def get_values() -> tuple:
    """
    Do not call up more often than every 3 seconds!

    :rtype: tuple
    :returns:   Tuple which contains:
                humidity string(human readable),
                temperature string(human readable),
                concatenated string(human readable),
                humidity value,
                temperature value
    """

    temperature_string = EMPTY
    humidity_string = EMPTY
    summary_string = EMPTY
    stdout.write("Get temperature and humidity values: ")
    humidity = SENSOR.humidity
    temperature = SENSOR.temperature

    if humidity is not None and temperature is not None:
        temperature_string += f"{temperature:04.1f}°C"
        humidity_string += f"{humidity:04.1f}%"
        summary_string += f"{temperature_string} {humidity_string}"
        stdout.write(f"{summary_string}\n")
    else:
        stderr.write(
            "Failed to get temperature and humidity values. Set to '0'!\n")
        humidity = 0
        temperature = 0
    return humidity_string, \
           temperature_string, \
           summary_string, \
           humidity, \
           temperature


if __name__ == '__main__':
    while True:
        for v in get_values():
            print(f" - {v}")
        sleep(10)
