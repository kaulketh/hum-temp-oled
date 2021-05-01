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

from dht import get_values

serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial)
SPACE = " "
left = 0
top = 0

# Load fonts
# Load default font.
# font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
tahoma = ImageFont.truetype('fonts/tahoma.ttf', 30)
dejavu = ImageFont.truetype('fonts/dejavu.ttf', 28)
arial_10 = ImageFont.truetype('fonts/arial.ttf', 10)
arial_12 = ImageFont.truetype('fonts/arial.ttf', 12)
free_sans_10 = ImageFont.truetype('fonts/FreeSans.ttf', 10)
free_sans_12 = ImageFont.truetype('fonts/FreeSans.ttf', 12)
free_sans_16 = ImageFont.truetype('fonts/FreeSans.ttf', 16)


def test():
    oled_font = ImageFont.truetype('fonts/FreeSans.ttf', 12)
    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="black", fill="white")
        draw.text((10, 10), "OLED-Display", font=oled_font, fill="black")


def __show_hum_temp(line1, line2, left=left, font=ImageFont.load_default()):
    hum, temp = get_values()[0], get_values()[1]
    oled.clear()
    with canvas(oled) as draw:
        # Write the lines of text.
        draw.text((left, line1), f"H {hum}", font=font, fill=255)
        draw.text((left, line2), f"T {temp}", font=font, fill=255)


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


def __show_state(font=ImageFont.load_default()):
    """
    Shell scripts for system monitoring from here :
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    oled.clear()
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

    with canvas(oled) as draw:
        # Write the lines of text.
        draw.text((left, top), f"IP: {ip}", font=font, fill=255)
        draw.text((left, top + 15), cpu, font=font, fill=255)
        draw.text((left, top + 30), mem_usage, font=font, fill=255)
        draw.text((left, top + 45), disk, font=font, fill=255)


def run_at_128x64():
    __show_state(font=free_sans_10)
    sleep(5)
    __show_hum_temp(top + 3, top + 35, left=5, font=dejavu)
    sleep(15)


def run_at_128x32():
    # __show_state()
    # sleep(5)
    __show_hum_temp(top + 5, top + 37, font=tahoma)
    sleep(15)


if __name__ == '__main__':

    while True:

        try:
            run_at_128x64()
            # run_at_128x32()

        except KeyboardInterrupt:
            stderr.write("Oled interrupted.\n")
            oled.clear()
            exit()

        except Exception as e:
            stderr.write(f"OLED: Any error or exception occurred! , {e}\n")
