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

import supervisor
from time import sleep
from digitalio import DigitalInOut
import board
import asyncio
from duckyinpython import  getProgrammingStatus, runScript, BlinkLedPico, LoadJsonConf

config = LoadJsonConf()

def startAP():
    global config
    import wifi
    import ipaddress

    try : 
        int(config['AP']['channel'])
    except Exception:
        print(config['AP']['channel'])
        if config['AP']['channel'].strip().upper() == "RANDOM":
            from random import randint as rng
            config['AP']['channel'] = rng(1, 13)
        else :
            print(f"Error in setting channel : {config['AP']['channel']}, replacing it with number 1")
            config['AP']['channel'] = 1


    wifi.radio.start_ap(
        config['AP']['ssid'], 
        config['AP']['password'],
        channel=config['AP']['channel']
    )

    check_correct_ip_addrs = len(config['AP']['ip_address'].strip().split("."))
    if check_correct_ip_addrs != 4 :
        print(f"Invalid ip_address in config.json! using 192.168.1.1")
        config['AP']['ip_address'] = "192.168.1.1"

    wifi.radio.set_ipv4_address_ap(
        ipv4=ipaddress.IPv4Address(config['AP']['ip_address']),
        netmask=ipaddress.IPv4Address("255.255.255.0"),
        gateway=ipaddress.IPv4Address(config['AP']['ip_address'])
    )

    ap_info_str = (
        "AP_INFO: {\n" + 
        f"    \"SSID\": \"{config['AP']['ssid']}\",\n" + 
        f"    \"PASSWD\": \"{config['AP']['password']}\",\n" + 
        f"    \"IP_ADDRS\": \"{config['AP']['ip_address']}\",\n" + 
        f"    \"CHANNEL\": {config['AP']['channel']}\n" +
        "}"
    )
    print(ap_info_str)
    del config

async def main_loop(led):
    tasks = []
    # collecting all parallel tasks
    if board.board_id == 'raspberry_pi_pico_w' or board.board_id == 'raspberry_pi_pico2_w':
        startAP()
        from webapp import startWebService
        tasks.append(asyncio.create_task(startWebService()))

    tasks.append(asyncio.create_task(BlinkLedPico(led)))
    # start tasks
    await asyncio.gather(*tasks)

def main_code(Default_Payload):
    # sleep at the start for 100 ms to allow the device to be recognized by the host computer
    sleep(.1)
    print('\nWelcome to "OverQuack" Serial monitor')
    led = DigitalInOut(board.LED)
    led.switch_to_output()

    # if changed to True, when editing payload in mass device it will auto reboot and load new changes
    autoreload = config['BOARD']['enable_auto_reload'] 
    if autoreload in [True, "True", "true", 1, "1"]:
        autoreload = True 
    else :
        autoreload = False

    supervisor.runtime.autoreload = autoreload

    # getProgrammingStatus is function to detect MODE
    if getProgrammingStatus():
        print("Update your payload :^]")
    else:
        runScript(Default_Payload)

    # Run Default_Payload, then start LED blinking and Wi-Fi AP
    asyncio.run(main_loop(led))

payload = config['DEFAULT_PAYLOAD']
if not isinstance(config['DEFAULT_PAYLOAD'], str) or not payload:
    payload = "payload.oqs"

main_code(payload)
