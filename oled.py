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

from PIL import ImageFont, Image
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# from dht import get_values

serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial)
draw = canvas(oled)
left = 0
top = 0

# Fonts
font_arial = ImageFont.truetype('fonts/arial.ttf', 12)
font_free_sans = ImageFont.truetype('fonts/FreeSans.ttf', 10)
font_free_sans12 = ImageFont.truetype('fonts/FreeSans.ttf', 12)


def test():
    oled_font = ImageFont.truetype('fonts/FreeSans.ttf', 12)
    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="black", fill="white")
        draw.text((10, 10), "OLED-Display", font=oled_font, fill="black")


def __show_hum_temp():
    oled.clear()
    with canvas(oled) as draw:
        # Write the lines of text.
        draw.text((left, top), "line 1", font=font_free_sans12,
                  fill=255)
        draw.text((left, top + 15), "line 2", font=font_free_sans12,
                  fill=255)
        draw.text((left, top + 30), "line 3", font=font_free_sans12,
                  fill=255)
        draw.text((left, top + 45), "Line 4", font=font_free_sans12,
                  fill=255)


def __get_core_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())
    one = str(temp).__getitem__(0)
    two = str(temp).__getitem__(1)
    temp_str = '{0}{1}{2}{3}'.format(one, two, '°', 'C')
    return temp_str


def __show_pi():
    oled.clear()
    # image inverted
    with canvas(oled) as draw:
        draw.rectangle((32, top - 3, 95, 63), outline=1, fill=1)
        draw.bitmap((32, top - 3), Image.open('pi_logo.png'), fill=0)


def __show_state():
    """
    Shell scripts for system monitoring from here :
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    oled.clear()
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

    with canvas(oled) as draw:
        # Write the lines of text.
        draw.text((left, top), f"IP: {ip.decode('utf-8')}",
                  font=font_free_sans,
                  fill=255)
        draw.text((left, top + 15), f"{cpu.decode('utf-8')}",
                  font=font_free_sans, fill=255)
        draw.text((left, top + 30), f"{mem_usage.decode('utf-8')}",
                  font=font_free_sans,
                  fill=255)
        draw.text((left, top + 45), f"{disk.decode('utf-8')}",
                  font=font_free_sans, fill=255)


if __name__ == '__main__':

    while True:

        try:
            # test()
            # __show_pi()
            # sleep(3)
            __show_state()
            sleep(5)
            __show_hum_temp()
            sleep(15)

        except KeyboardInterrupt:
            stderr.write('Oled interrupted.')
            oled.clear()
            exit()

        except:
            stderr.write('Oled: Any error or exception occurred!')
