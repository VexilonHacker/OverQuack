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
# - Enhanced overall usability, stability and feature set, bringing it closer to a full Rubber Ducky experience
# - Integrated wireless connection support for Pico W/Pico 2 W, enabling FULL wireless control over "OverQuack"
    
import supervisor, json, board, microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)

DEFAULT_PIN_NUM = 5
# please dont sue me :) im still too young
default_manufacturer = "CHICONY"
default_product = "HP Basic USB Keyboard"
default_vid_str = "0x03F0"
default_pid_str = "0x0024"
drive_label = "OVERQUACK"

try:
    with open("config.json", "r") as f:
        config = json.load(f)

    usb_config = config.get("USB_IDENTIFICATION", {})
    manufacturer = usb_config.get("manufacturer", default_manufacturer)
    product = usb_config.get("product", default_product)
    vid_str = usb_config.get("vid", default_vid_str)
    pid_str = usb_config.get("pid", default_pid_str)
    drive_label = config.get("DRIVE_LABEL", "OVERQUACK")

    pin_num = config['BOARD']['controll_mode_pin']
    if not isinstance(pin_num, int) or not hasattr(board, f"GP{pin_num}"):
        print(f"Invalid or missing pin in config, defaulting to GP{DEFAULT_PIN_NUM}")
        pin_num = DEFAULT_PIN_NUM
    else:
        print(f"USED GP{pin_num}")

except (OSError, ValueError, KeyError) as e:
    print(f"Error reading config file: {e}. Using defaults.")
    manufacturer = default_manufacturer
    product = default_product
    vid_str = default_vid_str
    pid_str = default_pid_str
    pin_num = DEFAULT_PIN_NUM

vid = int(vid_str, 16) if isinstance(vid_str, str) and vid_str.startswith("0x") else int(vid_str)
pid = int(pid_str, 16) if isinstance(pid_str, str) and pid_str.startswith("0x") else int(pid_str)

supervisor.set_usb_identification(
    manufacturer=manufacturer,
    product=product,
    vid=vid,
    pid=pid
)



from digitalio import DigitalInOut, Pull

pin_name = f"GP{pin_num}" 
StoragePin = DigitalInOut(getattr(board, pin_name))
StoragePin.switch_to_input(pull=Pull.UP)
StorageStatus = StoragePin.value


import storage
import usb_hid

nvm = microcontroller.nvm # non-volatile memory 256 Byte where we save ATTACKMODE DATA

# NVM indices
NVM_CONSUMED = 0
NVM_MODE     = 1
NVM_LINE_L   = 2
NVM_LINE_H   = 3

MODE_NONE    = 0
MODE_HID     = 1
MODE_STORAGE = 2
MODE_BOTH    = 3

resume_consumed = nvm[NVM_CONSUMED]
resume_mode_raw = nvm[NVM_MODE] if len(nvm) > NVM_MODE else 0

if resume_consumed == 0 and resume_mode_raw != MODE_NONE:
    # Fresh resume: apply the requested USB mode
    if resume_mode_raw == MODE_HID:
        storage.disable_usb_drive()
        usb_hid.enable((
            usb_hid.Device.KEYBOARD,
            usb_hid.Device.MOUSE,
            usb_hid.Device.CONSUMER_CONTROL,
        ))
        print("ATTACKMODE: HID enabled (NVM)")
    elif resume_mode_raw == MODE_BOTH:
        usb_hid.enable((
            usb_hid.Device.KEYBOARD,
            usb_hid.Device.MOUSE,
            usb_hid.Device.CONSUMER_CONTROL,
        ))
        print("ATTACKMODE: HID STORAGE enabled (NVM)")
else:
    usb_hid.enable((
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
    ))
    if StorageStatus:
        print("USB drive enabled")
    else:
        storage.disable_usb_drive()
        storage.remount("/", readonly=False)
        m = storage.getmount("/")
        m.label = drive_label
        print("Disabling USB drive, Starting Keystroke injection")

# storage.remount("/", readonly=False)
