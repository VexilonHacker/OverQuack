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

from os import listdir
from os import remove
from storage import remount
import wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp
import wifi

from duckyinpython import runScript, BetterListOutput, LoadJsonConf
import asyncio
import gc 


wsgiServer = None
config = LoadJsonConf()
async def startWebService():
    global wsgiServer  # So we can reset it if needed
    ports = config['AP']['ports']
    completed = 0

    if len(ports) <= 1 or not isinstance(ports, list):
        ports = [80, 8080]


    for _ in range(2):
        for port in ports:
            try:
                wsgiServer = server.WSGIServer(port, application=web_app)
                wsgiServer.start()
                print(f"[AP_STARTED] Open this URL in your browser: http://{str(wifi.radio.ipv4_address_ap)}:{port}/")
                completed = 1
                break
            except OSError as e:
                print(f"[ERROR] Could not start server on PORT={port}: {e}")
        if completed:
            break
    if not wsgiServer :
        print(f"Problem canont assign port to http sever from this list: {ports}. Entering inf WHILE LOOP")
        while 1 :
            continue

    while True:
        try:
            wsgiServer.update_poll()
            gc.collect()
            await asyncio.sleep(0)
        except Exception as e:
            print(f"[ERROR] An error ogc.collecturred in the server loop: {e}")

def CheckIfExists(filename):
    if filename.strip() in listdir():
        return 1 
    return 0 


web_app = WSGIApp()
CheckMemory = 0 

@web_app.route("/c2", methods=['GET', 'POST'])
def cli(req):
    global CheckMemory
    File_data_sep = "<=|^w^|=>"
    Available_operation = ["WRITE", "READ", "DELETE", "RUN"]

    if req.method == 'POST':
        # from post we can send-WRITE payload / DELETE payload /  READ payload
        data = req.body.getvalue()
        print(f"POST_DATA: {data}")
        
        if data.strip().upper() == 'FREE_MEM':
            CheckMemory = 1
            free_mem = str(gc.mem_free())
            return ("200 OK", [('Content-Type', 'text/html')], free_mem)

        elif data.strip().upper() == 'SEP':
            return ("200 OK", [('Content-Type', 'text/html')], File_data_sep)

        elif data.strip().upper() == 'LS':
            return ("200 OK", [('Content-Type', 'text/html')], BetterListOutput(sorted(listdir())))

        elif data.strip().upper()  == 'PAYLOADS':
           oqs_files = BetterListOutput(sorted([file for file in listdir() if file.endswith('.oqs')]))
           return ("200 OK", [('Content-Type', 'text/html')], oqs_files)

        elif not data.strip():
            return ("400 Bad Request", [('Content-Type', 'text/html')], 'Empty post request')

        data = data.split(File_data_sep)
        print(f"data: {data}")
        if data[0].strip().upper() not in Available_operation or len(data) < 2:
            return ("400 Bad Request", [('Content-Type', 'text/html')], f'Invailable operation: {data[0]}')

        data[0] = data[0].strip().upper()
        data[1] = data[1].strip()

            
        if  data[0] == 'WRITE':
            if not CheckMemory:
                return ("400 Bad Request", [('Content-Type', 'text/html')], 'You canont WRITE your payload without checking AVAILABLE_MEMORY\nto bypass it send a post request in body of it word "FREE_MEM"')

            try:
                remount("/", readonly=False)
            except Exception as e:
                return ("500 ERROR", [('Content-Type', 'text/html')], f'[WEB_APP_EDIT] ERROR: {e}')

            try:
                data[2] = data[2].strip()
            except IndexError:
                return ("404 Not Found", [('Content-Type', 'text/html')], "There is not file content in post req")

            with open(data[1].strip(), "w", encoding='utf-8') as payload:
                payload.write(data[2])
            CheckMemory = 0
            remount("/", readonly=True)
            return ("200 OK", [('Content-Type', 'text/html')], f'Writing payload to "{data[1]}" is completed ')

        elif data[0] == 'READ':
            if CheckIfExists(data[1]):
                with open(data[1], "r", encoding='utf-8') as payload:
                    payload_buffer = payload.read()
                return ("200 OK", [('Content-Type', 'text/html')], payload_buffer)
            else:
                return ("404 Not Found", [('Content-Type', 'text/html')], f'payload was not found "{data[1]}"')

        elif data[0] == 'DELETE':
            if not data[1].endswith(".oqs"):
                return ("400 Bad Request", [('Content-Type', 'text/html')], 'You can only delete payloads that ends with  ".oqs" extension')
            try:
                remount("/", readonly=False)
            except Exception as e:
                return ("500 ERROR", [('Content-Type', 'text/html')], f'[WEB_APP_EDIT] ERROR: {e}')

            if CheckIfExists(data[1]):
                remove(data[1])
                remount("/", readonly=True)
                return ("200 OK", [('Content-Type', 'text/html')], f'"{data[1]}" was deleted')
            else:
                return ("404 Not Found", [('Content-Type', 'text/html')], f'payload was not found "{data[1]}"')

        # commands
    
        elif data[0] == 'RUN':
            if CheckIfExists(data[1]) :
                runScript(data[1])
                return ("200 OK", [('Content-Type', 'text/html')], f'"{data[1]}" IS COMPLETED 200')
            else:
                msg = f'payload was not found "{data[1]}"'
                if not data[1].endswith(".oqs"):
                    msg += 'btw your payload should ends_with ".oqs" extension :]'

                return ("404 Not Found", [('Content-Type', 'text/html')], msg)


    return ("200 OK", [('Content-Type', 'text/html')], "Welcome To C2 page")

