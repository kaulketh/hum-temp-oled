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

import Adafruit_DHT
from Adafruit_DHT import Raspberry_Pi_2

SENSOR = Adafruit_DHT.AM2302
PIN = 24
PLAT = Raspberry_Pi_2
SPACE = " "


def get_values():
    temp_str = SPACE
    hum_str = SPACE
    ret_str = SPACE
    stdout.write("Get temperature and humidity values: ")
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR,
                                                    PIN,
                                                    platform=PLAT)

    if humidity is not None and temperature is not None:
        temp_str = f"{temperature:04.1f}°C"
        hum_str = f"{humidity:05.2f}%"
        ret_str = f"{temp_str}{SPACE}{hum_str}"
        stdout.write(f"{ret_str}\n")
    else:
        stderr.write(
            "Failed to get temperature and humidity values. Set to '0'!\n")
        humidity = 0
        temperature = 0
    return hum_str, temp_str, ret_str, humidity, temperature


if __name__ == '__main__':
    while True:
        for v in get_values():
            print(f" - {v}")
        sleep(10)
