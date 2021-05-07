#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 02.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
"""
Possibility to clear display via separate function call if needed
"""


def clear(luma_oled_device):
    """Possibility to clear display via separate function call if needed"""
    luma_oled_device.clear()


if __name__ == '__main__':
    from oled import display

    clear(display)
