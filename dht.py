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

    try:

        temperature_str_2d = EMPTY
        humidity_str_2d = EMPTY
        temperature_str_f = EMPTY
        humidity_string_f = EMPTY
        summary_string = EMPTY
        stdout.write(
            f"Reading temperature and humidity values from DHT22 sensor...\n")
        humidity = SENSOR.humidity
        temperature = SENSOR.temperature

        if humidity is not None and temperature is not None:
            temperature_str_2d += f"{str(temperature)[0:2]}°C"
            humidity_str_2d += f"{str(humidity)[0:2]}%"
            summary_string += f"{temperature_str_2d} {humidity_str_2d}"
            temperature_str_f += f"{temperature:04.1f}°C"
            humidity_string_f += f"{humidity:04.1f}%"
            stdout.write(f"{summary_string}\n")
        else:
            stderr.write(
                "Failed to get temperature and humidity values. Set to '0'!\n")
            humidity = 0
            temperature = 0
        return \
            humidity_str_2d, \
            temperature_str_2d, \
            summary_string, \
            humidity, \
            temperature, \
            temperature_str_f, \
            humidity_string_f

    except Exception as ex:
        stderr.write(f"Error while reading from DHT22: {ex}\n")


if __name__ == '__main__':
    while True:
        for v in get_values():
            print(f" - {v}")
        sleep(10)
