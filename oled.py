#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# oled.py
# created 30.04.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import subprocess
from io import BytesIO
from sys import stderr, stdout
from time import sleep

from PIL import ImageFont, Image
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from dht import get_values

serial = i2c(port=1, address=0x3C)
display = ssd1306(serial)
SPACE = " "
left = 0
top = 0

# Load fonts
# font = ImageFont.load_default()
# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php

__font_folder = "/home/pi/oled/fonts/"


def __load_font(font_file, size):
    """
     To avoid issue related to how Unicode file paths are handled on platforms,
     read the font file in binary form.

    """

    with open(font_file, "rb") as f:
        bytes_font = BytesIO(f.read())
    return ImageFont.truetype(bytes_font, size)


tahoma = __load_font(f"{__font_folder}tahoma.ttf", 30)
dejavu = __load_font(f"{__font_folder}dejavu.ttf", 28)
arial_10 = __load_font(f"{__font_folder}arial.ttf", 10)
arial_12 = __load_font(f"{__font_folder}arial.ttf", 12)
free_sans_10 = __load_font(f"{__font_folder}FreeSans.ttf", 10)
free_sans_12 = __load_font(f"{__font_folder}FreeSans.ttf", 12)
free_sans_16 = __load_font(f"{__font_folder}FreeSans.ttf", 16)


def __get_core_temp():
    try:
        src = "/sys/class/thermal/thermal_zone0/temp"
        temp = open(src).read()
        temp_str = f"{temp[0]}{temp[1]},{temp[2]}{temp[3]}{temp[4]}°C"
        stdout.write(f"Read from '{src}': {temp}")
        return temp_str
    except Exception as ex:
        stderr.write(f"Error while reading temperature: {ex}\n")


def __show_core_temperature(x=left, font=ImageFont.load_default(),
                            showtime=5.0):
    temp = __get_core_temp()
    with canvas(display) as draw:
        draw.text((x, top),
                  "RasPi Temperature",
                  font=ImageFont.load_default(), fill=255)
        draw.text((x, display.height / 3 - 3),
                  temp, font=font, fill=255)
    sleep(showtime)


def __show_pi(showtime=5.0):
    with canvas(display) as draw:
        draw.rectangle((32, top - 3, 95, 63), outline=1, fill=1)
        draw.bitmap((32, top - 3), Image.open('pi_logo.png'), fill=0)
    sleep(showtime)


def __show_humidity(x=left, font=ImageFont.load_default(), showtime=5.0):
    hum = get_values()[0]
    with canvas(display) as draw:
        draw.text((x, top),
                  "Humidity", font=ImageFont.load_default(), fill=255)
        draw.text((x, display.height / 3 - 3),
                  hum, font=font, fill=255)
    sleep(showtime)


def __show_temperature(x=left, font=ImageFont.load_default(), showtime=5.0):
    temp = get_values()[1]
    with canvas(display) as draw:
        draw.text((x, top),
                  "Temperature", font=ImageFont.load_default(), fill=255)
        draw.text((x, display.height / 3 - 3),
                  temp, font=font, fill=255)
    sleep(showtime)


def __show_hum_temp(line1, line2, x=left,
                    font=ImageFont.load_default(), showtime=5.0):
    hum, temp = get_values()[0:2]
    with canvas(display) as draw:
        draw.text((x, line1), f"H {hum}", font=font, fill=255)
        draw.text((x, line2), f"T {temp}", font=font, fill=255)
    sleep(showtime)


def __show_separate_hum_temp_(x=left, font=ImageFont.load_default(),
                              showtime=5.0):
    hum, temp = get_values()[0:2]
    with canvas(display) as draw:
        draw.text((x, top),
                  "Humidity", font=ImageFont.load_default(), fill=255)
        draw.text((x, display.height / 3 - 3),
                  hum, font=font, fill=255)
    sleep(showtime)
    with canvas(display) as draw:
        draw.text((x, top),
                  "Temperature", font=ImageFont.load_default(), fill=255)
        draw.text((x, display.height / 3 - 3),
                  temp, font=font, fill=255)
    sleep(showtime)


def __show_states(font=ImageFont.load_default(), single_line=False,
                  showtime=5.0):
    """
    Shell scripts for system monitoring from here :
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    try:
        # IP
        cmd = "hostname -I | cut -d\' \' -f1"
        ip = subprocess.check_output(cmd, shell=True).decode('utf-8')
        # CPU load
        cmd = "top - bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* " \
              "id.*/\\1/\" | " \
              "awk '{print \"CPU Load : \"100 - $1\"%\"}'"
        # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load : %.2f\",
        # $(NF-2)}'"
        cpu = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # Memory usage
        cmd = "free -m | awk 'NR==2{printf \"Mem : %s / %s MB %.0f%%\", $3,$2," \
              "$3*100/$2 }' "
        mem_usage = subprocess.check_output(cmd, shell=True).decode('utf-8')

        # HDD usage
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk : %d / %d GB %s\", $3,$2,$5}'"
        disk = subprocess.check_output(cmd, shell=True).decode('utf-8')

        stdout.write(f"Reading system monitoring values...\n")

        if single_line:
            with canvas(display) as draw:
                draw.text((left, display.height / 3),
                          f"IP: {ip}", font=font, fill=255)
                sleep(showtime)
            with canvas(display) as draw:
                draw.text((left, display.height / 3),
                          cpu, font=font, fill=255)
                sleep(showtime)
            with canvas(display) as draw:
                draw.text((left, display.height / 3),
                          mem_usage, font=font, fill=255)
                sleep(showtime)
            with canvas(display) as draw:
                draw.text((left, display.height / 3),
                          mem_usage, font=font, fill=255)
                sleep(showtime)
        else:
            with canvas(display) as draw:
                draw.text((left, top),
                          f"IP: {ip}", font=font, fill="white")
                draw.text((left, top + 15),
                          cpu, font=font, fill="white")
                draw.text((left, top + 30),
                          mem_usage, font=font, fill="white")
                draw.text((left, top + 45),
                          disk, font=font, fill="white")
            sleep(showtime)
    except Exception as xcptn:
        stderr.write(f"Error while system monitoring: {xcptn}")


def run_at_128x64():
    i = 0
    while i < 40:  # about 15 sec?
        __show_states(font=free_sans_10, showtime=0.01)
        i += 1

    i = 0
    while i < 4:
        __show_hum_temp(top + 3, top + 35, x=5, font=tahoma, showtime=4)
        i += 1

    __show_core_temperature(x=5, font=tahoma)


def run_at_128x32():
    __show_states(font=free_sans_10, single_line=True)
    __show_hum_temp(top + 5, top + 37, font=tahoma)


if __name__ == '__main__':
    while True:
        try:
            run_at_128x64()
        except KeyboardInterrupt:
            stderr.write("OLED interrupted.\n")
            exit()
        except Exception as e:
            stderr.write(f"OLED: Any error or exception occurred! , {e}\n")
        finally:
            display.clear()
