#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# oled.py
# created 30.04.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import subprocess
from sys import stderr
from time import sleep

from PIL import Image, ImageFont
from lib_oled96 import Ssd1306
from smbus import SMBus

from dht import get_values

# Display setup, methods and members
# 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
i2cbus = SMBus(1)
oled = Ssd1306(i2cbus)
draw = oled.canvas
c = '\''

# OLED 0.96" 128*64
left = 5
top = 7

# Fonts
font_arial = ImageFont.truetype('fonts/arial.ttf', 12)
font_free_sans = ImageFont.truetype('fonts/FreeSans.ttf', 12)


def __show_hum_temp(time):
    oled.cls()
    oled.display()
    # Write the lines of text.
    draw.text((left, top), get_values()[0], font=font_free_sans, fill=255)
    draw.text((left, top + 15), get_values()[1], font=font_free_sans, fill=255)
    # draw.text((left, top + 30), get_values()[1], font=font_free_sans, fill=255)
    # draw.text((left, top + 30), "any string", font=font_free_sans, fill=255)
    # draw.text((left, top + 45), "any string", font=font_free_sans, fill=255)
    oled.display()
    sleep(time)


def __get_core_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())
    one = str(temp).__getitem__(0)
    two = str(temp).__getitem__(1)
    temp_str = '{0}{1}{2}{3}'.format(one, two, c, 'C')
    return temp_str


def __show_pi(time):
    oled.cls()
    # image inverted
    draw.rectangle((32, top - 3, 95, 63), outline=1, fill=1)
    draw.bitmap((32, top - 3), Image.open('pi_logo.png'), fill=0)
    oled.display()
    sleep(time)


def __show_state(time):
    """
    Shell scripts for system monitoring from here :
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    oled.cls()
    oled.display()
    cmd = "hostname -I | cut -d\' \' -f1"
    ip = subprocess.check_output(cmd, shell=True)
    cmd = "top - bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | " \
          "awk '{print \"CPU Load : \"100 - $1\"%\"}'"
    # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load : %.2f\", $(NF-2)}'"
    cpu = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem : %s / %s MB %.0f%%\", $3,$2,$3*100/$2 }'"
    mem_usage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk : %d / %d GB %s\", $3,$2,$5}'"
    disk = subprocess.check_output(cmd, shell=True)

    # Write the lines of text.
    draw.text((left, top), "IP : " + str(ip), font=font_free_sans, fill=255)
    draw.text((left, top + 15), str(cpu), font=font_free_sans, fill=255)
    draw.text((left, top + 30), str(mem_usage), font=font_free_sans, fill=255)
    draw.text((left, top + 45), str(disk), font=font_free_sans, fill=255)
    oled.display()
    sleep(time)


if __name__ == '__main__':
    while True:

        try:
            __show_pi(3)
            __show_state(5)
            __show_hum_temp(15)

        except KeyboardInterrupt:
            stderr.write('Oled interrupted.')
            oled.cls()
            exit()

        except:
            stderr.write('Oled: Any error or exception occurred!')
