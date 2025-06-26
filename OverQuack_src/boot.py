# License: GPLv2.0
# Original copyright (c) 2023 Dave Bailey
# Original Author: Dave Bailey (dbisu, @daveisu)
# Original Project name: PicoDucky 

# Modifications and improvements by: VexilonHacker (@VexilonHacker)
# Copyright (c) 2025 VexilonHacker
# Project name : OverQuack
# Description:
# - Added full Rubber Ducky script functionality including mouse support
# - Introduced randomization features for payloads
# - Enhanced overall usability and feature set, bringing it closer to a full Rubber Ducky experience
# - Integrated wireless connection support for Pico W, enabling FULL wireless control over "OverQuack"

import board 
from digitalio import DigitalInOut, Pull
import storage
import usb_hid 
import json 


DEFAULT_PIN_NUM = 5 
try:
    with open("config.json", "r") as f:
        config = json.load(f)

    pin_num = config['BOARD']['controll_mode_pin']
    # Ensure pin_num is a valid integer and corresponds to a board attribute
    if not isinstance(pin_num, int) or not hasattr(board, f"GP{pin_num}"):
        print(f"Invalid or missing pin in config, defaulting to GP{DEFAULT_PIN_NUM}")
        pin_num = DEFAULT_PIN_NUM
    else :
        print(f"USED GP{pin_num}")
        

except (OSError, ValueError) as e:
    print(f"Error reading config file: {e}. Using default GP{DEFAULT_PIN_NUM}")
    pin_num = DEFAULT_PIN_NUM


pin_name = f"GP{pin_num}" 
StoragePin = DigitalInOut(getattr(board, pin_name))
StoragePin.switch_to_input(pull=Pull.UP)
StorageStatus = StoragePin.value


usb_hid.enable((
    usb_hid.Device.KEYBOARD,
    usb_hid.Device.MOUSE,
    usb_hid.Device.CONSUMER_CONTROL, 
))


if StorageStatus:
    print("USB drive enabled")
else:
    storage.disable_usb_drive()
    print("Disabling USB drive, Starting Keystroke injection")

storage.remount("/", readonly=False)

