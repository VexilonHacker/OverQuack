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
    
import supervisor, board, asyncio, microcontroller

from digitalio import DigitalInOut
from overquackify import  getProgrammingStatus, runScript, BlinkLedPico, LoadJsonConf, set_led

config = LoadJsonConf()

def startAP():
    global config
    import wifi, ipaddress, cyw43

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

    cyw43.set_power_management(cyw43.PM_DISABLED)
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
        from quackd import startTcpServer
        tasks.append(asyncio.create_task(startTcpServer()))

    tasks.append(asyncio.create_task(BlinkLedPico(led)))
    await asyncio.gather(*tasks)

def main_code(Default_Payload):

    print('\nWelcome to "OverQuack" Serial monitor')
    led = DigitalInOut(board.LED)
    led.switch_to_output()
    set_led(led)

    autoreload = config['BOARD']['enable_auto_reload']
    if autoreload in [True, "True", "true", 1, "1"]:
        autoreload = True
    else:
        autoreload = False
    supervisor.runtime.autoreload = autoreload

    nvm = microcontroller.nvm
    NVM_CONSUMED = 0
    NVM_MODE     = 1
    NVM_LINE_L   = 2
    NVM_LINE_H   = 3

    resume_line = 0
    resumed = False

    if len(nvm) > NVM_LINE_H and nvm[NVM_CONSUMED] == 0 and nvm[NVM_MODE] != 0:
        resume_line = int.from_bytes(nvm[NVM_LINE_L:NVM_LINE_H+1], 'little')

        try:
            with open(Default_Payload, "r") as f:
                lines = f.readlines()
            if resume_line < len(lines):
                peek = lines[resume_line].strip().upper()
                if peek.startswith("ATTACKMODE"):
                    print("Resume line is an ATTACKMODE – aborting resume (NVM cleared)")
                    nvm[NVM_CONSUMED:NVM_LINE_H+1] = bytes(4)
                else:
                    print(f"Resuming payload from line {resume_line} (NVM)")
                    nvm[NVM_CONSUMED] = 1   # <-- consumed IMMEDIATELY
                    resumed = True
            else:
                print("Resume line out of range – clearing NVM")
                nvm[NVM_CONSUMED:NVM_LINE_H+1] = bytes(4)
        except Exception as e:
            print("Payload verification failed, clearing NVM:", e)
            nvm[NVM_CONSUMED:NVM_LINE_H+1] = bytes(4)

    if getProgrammingStatus() and not resumed:
        print("Update your payload :^]")
    else:
        try:
            runScript(Default_Payload, start_line=resume_line)
        finally:
            # ALWAYS clear NVM resume data, even after a crash 'learned in a hard way'
            nvm[NVM_CONSUMED:NVM_LINE_H+1] = bytes(4)

    asyncio.run(main_loop(led))

payload = config['DEFAULT_PAYLOAD']
if not isinstance(config['DEFAULT_PAYLOAD'], str) or not payload:
    payload = "payload.oqs"

main_code(payload)
