# 🦆 OverQuack
![Alt text](https://github.com/VexilonHacker/OverQuack/blob/8e53a4e72deef4525c5bb20d7087e893b81223ac/assets/image.png)
<div align="center">
  <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/VexilonHacker/OverQuack">
  <img alt="GitHub license" src="https://img.shields.io/github/license/VexilonHacker/OverQuack">
  <a href="https://github.com/VexilonHacker/OverQuack/graphs/contributors">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/VexilonHacker/OverQuack">
  </a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/VexilonHacker/OverQuack">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/VexilonHacker/OverQuack">
</div>

---

**OverQuack** is an advanced Rubber Ducky-style HID attack tool powered by the Raspberry Pi Pico family — now with **wireless access**, **cross-platform payloads**, and **support for all four Pico variants**.

---

## 🚀 Features

- 🧠 **Full DuckyScrtipt support** – Supporting DuckyScript with all it programming language + additional __KEYWORDS__
- 💡 **Supports all Pico variants** – Pico, Pico_W, Pico 2, Pico_W 2
- 📡 **Wireless control** – Upload and trigger payloads remotely over Wi-Fi 
- 🖥️ **Cross-platform payloads** – Works with Windows, macOS, and Linux
- 🌐 **Client-controlled interface** – Easily control your device with the __"OverQuack_client.go"__ 
- 🔌 **Plug & play HID injection** – No drivers, just plug in and go
-  **🖱 Support mouse injection**
- 🛠️ **Modular and customizable** - Extend with new payloads and tools
- ✅ **Open, hackable, GPLv2.0 licensed**
- ⚙️ **Full configuration** - Configure all from `config.json`


---


## 📂 Getting Started
You can setup your __OverQuack/RubberDucky__ device automaticly by running __"OverQuack_Installer"__:
<br><br>__⚠️ note : This installer only support linux for now__
``` go 
go run OverQuack_Installer.go
```
![auto installation](https://github.com/VexilonHacker/OverQuack/blob/9e5d14ed5526943a0438d4cbcb6acb65a6377a05/assets/auto_installation.gif)

or setup it manually:

1. Download repo: __`https://github.com/VexilonHacker/OverQuack`__

2. Plug your Pico into USB while holding the __BOOTSEL__ button for 3 seconds, then release it. It will show up as __"RPI-RP2"__.

3. Copy `OverQuack_installation/firmwares/flash_nuke.uf2` to the `RPI-RP2` drive and wait for the Pico to finish rebooting.

4. Copy `OverQuack_installation/firmwares/adafruit-circuitpython-raspberry_pi_<YOUR_PICO_MODULE>-en_US-9.2.1.uf2` to the `RPI-RP2` drive and wait for the Pico to finish rebooting and it going to show up as __"CIRCUITPY"__.

    <details>
      <summary>Available firmwares</summary>

      ```text
      adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.1.uf2
      adafruit-circuitpython-raspberry_pi_pico2-en_US-9.2.1.uf2
      adafruit-circuitpython-raspberry_pi_pico2_w-en_US-9.2.1.uf2
      adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.2.1.uf2
      ```
    </details>

5. copy all content of `OverQuack_src` to `CIRCUITPY`

6. Setup complete. __OverQuack__ is ready to use. Proceed with your tasks responsibly.

![Manuall installation](https://github.com/VexilonHacker/OverQuack/blob/9e5d14ed5526943a0438d4cbcb6acb65a6377a05/assets/manual_installation.gif)

## ⚙️ configuration 
you can configure __OverQuack__ completely from `config.json`: 
```json
{
    "DEFAULT_PAYLOAD" :  "payload.oqs",
    "BOARD" : {
        "controll_mode_pin": 5,
        "desc_controll_mode_pin" : "Setting GPIO pin that will change from keystroke mode to storage mode as example pin 2, 6, 10, 13...",

        "enable_auto_switch_mode" : true,
        "desc_enable_auto_switch_mode" : "switch attack mode without  need to replug usb",

        "enable_auto_reload" : false,
        "desc_enable_auto_reload" : "when editing a file in PICO and saving it, it will auto reboot PICO"
    },
    "AP" : {
        "ssid": "1984",
        "password": "OverQuackItBrother1984",
        "channel": "RANDOM",
        "desc_channel" : "You can set random channel  value by using RANDOM or specify channel value as int in range [1,13]",
        "ip_address": "10.10.5.1",
        "ports": [80, 8000, 8080],
        "desc_ports" : "at least you should put 2 ports, other ports are used in emergency"
    }
}
```

### 🔄 USB Interface: Mass Storage ⇄ HID Keyboard
By default, with `control_mode_pin` set to `GPIO 5`, connect a switch between GP5 and GND to toggle modes. 
‼️ __Without any connection, the device will start in Mass Storage mode for safety reasons :^]__
<br><br>
![Pico w connection](https://github.com/VexilonHacker/OverQuack/blob/9e5d14ed5526943a0438d4cbcb6acb65a6377a05/assets/overquack_connection.png)
- 🔁 No need to unplug the USB or manually replug the device after flipping the switch — simply toggle the switch, and OverQuack will automatically reboot into the selected mode.


### 🛜 Wireless HID Control & Remote Payload Delivery

This feature is supported **only** on the `Pico W` and `Pico 2 W`.

#### ✅ Available Operations:
- 📂 List all payloads/files  
- 📥 Upload / 📤 Download payloads  
- 📝 Read / ❌ Delete payloads  
- ▶️ Run payload remotely

#### 💡 Example:

![Remote Control Demo](https://github.com/VexilonHacker/OverQuack/blob/9e5d14ed5526943a0438d4cbcb6acb65a6377a05/assets/client.gif)
- __config.json__ should alwayes be in same dir of __OverQuack_client.go__
---

### ➕ Additional Features

Alongside DuckyScript internal variables like `$_CAPSLOCK_ON`, `$_NUMLOCK_ON`, and `$_SCROLLLOCK_ON`, two **network-related variables** have been added and change in returned value from original internal Vars:

```bash
$_CAPSLOCK_ON, $_NUMLOCK_ON, $_SCROLLLOCK_ON # retuns int value 1 if ON and 0 if OFF
$_SSID     # Returns current AP name as string
$_PASSWD   # Returns AP password as string
$_BSSID    # Returns AP MAC address as string
# Hint: Reverse Shell via Access Point :] I'll leave the rest to your imagination.
```
### 🎲 Random Value Generators:
```bash
$_RANDOM_NUMBER:5              # Returns 5-digit random number
$_RANDOM_LOWERCASE_LETTER:3    # Returns 3 random lowercase letters (e.g., qwe)
$_RANDOM_UPPERCASE_LETTER:7    # Returns 7 uppercase letters (e.g., ZDCFVGY)
$_RANDOM_LETTER:4              # Mixed-case letters (e.g., aWdZ)
$_RANDOM_SPECIAL:6             # Special characters (e.g., !@#$%^)
$_RANDOM_CHAR:8                # Fully random string (e.g., ^&ZaD23?)
```
- Random int value based on intervale :
```bash
$_RANDOM_MIN = 5 
$_RANDOM_MAX = 10 
$Variable_Test = $_RANDOM_INT # it $Variable_Test will equal a random integer in range [5, 10]
```


### 🔤 Layout Selection
To change the keyboard layout, use the `SELECT_LAYOUT` command:

```bash
SELECT_LAYOUT WIN_FR  # Switch to French layout on Windows
```


#### 🗂️ Available Layouts

Here is the list of supported layouts:

```c
SUPPORTED_LAYOUTS = {
    "US_DVO",
    "US",
    "MAC_FR",
    "WIN_BR",
    "WIN_CZ",
    "WIN_CZ1",
    "WIN_DA",
    "WIN_DE",
    "WIN_ES",
    "WIN_FR",
    "WIN_HU",
    "WIN_IT",
    "WIN_PO",
    "WIN_SW",
    "WIN_TR",
    "WIN_UK",
}
```


#### ➕ Add a New Layout

If you want to add a new layout, you can generate one using the <a href="https://www.neradoc.me/layouts/" target="_blank" rel="noopener noreferrer"><strong>keyboard layout generator for CircuitPython / Adafruit HID</strong></a>.

1. Download and unzip the file named:  **`layout_files_<LANGUAGE>-py.zip`**
2. Copy the following files:
   - `keyboard_layout_<LANGUAGE>.py` → to `OverQuack_STORAGE/lib/keyboard_layouts/`
   - `keycode_<LANGUAGE>.py` → to `OverQuack_STORAGE/lib/keycodes/`
<br><br>
3. Finally, add your new layout name to the __`LAYOUTS_MAP`__ dictionary __`duckyinpython.py`__ in approximate line 103-120 103-120.
### :duck: DuckScript scripting language 
- Here’s an example payload demonstrating DuckScript syntax and features:
```bash
REM payload.oqs

DEFINE @sleep 1000 

$username = "Jasper"
$MAX = 5
$INDEX = 0 
$CAPSLOCK_DETECTED = 0 

FUNCTION OPEN_POWERSHELL()
    DELAY @sleep
    GUI r 
    // math operation also supported
    // sleep for 1000 - 200 = 800 ms
    DELAY @sleep - 200 
    STRING powershell 
    SHIFT ENTER
    DELAY 1500 
    ENTER
    STRINGLN 
    echo "Heloo $username"
    echo "what wonderfull day "
    echo "to play ULTRAKILL"
    END_STRINGLN
END_FUNCTION

FUNCTION CheckValue()
    IF $CAPSLOCK_DETECTED == 1
        STRINGLN echo "dont outsmart me =}"
    ELSE 
        STRINGLN echo "Good person"
    END_IF
END_FUNCTION

OPEN_POWERSHELL()
WHILE ($INDEX < $MAX)
    $INDEX = $INDEX + 1 
    $MSG = "$INDEX) From OverQuack =}"
    IF $_CAPSLOCK_ON  == 1 
        // indentation is not necessary, just for better readability
        // Clicking on CAPSLOCK button to turn it off 
        CAPSLOCK 
    ELSE
        STRINGLN echo "Caps Lock is turned off"

    STRINGLN echo "$MSG"
    END_IF

END_WHILE
CheckValue()
```
### 🖱️ Mouse Control Support

```bash
MOUSE_CLICK RIGHT             # Click mouse button: LEFT / RIGHT / MIDDLE
MOUSE_PRESS LEFT              # Press (hold down) mouse button
MOUSE_RELEASE LEFT            # Release previously pressed mouse button
MOUSE_MOVE 10 20              # Move mouse cursor to x=10, y=20
MOUSE_SCROLL 5                # Scroll up 5 lines
MOUSE_SCROLL -5               # Scroll down 5 lines
```
### 〰 Mouse Jiggler
```bash
JIGGLE_MOUSE 5000             # Jiggle mouse for 5000 ms
BACKGROUND_JIGGLE_MOUSE 10000 # Jiggle mouse for 10 seconds after payload ends
BACKGROUND_JIGGLE_MOUSE INF   # Jiggle mouse indefinitely after payload ends
```
### 🔁 REPEAT

You can repeat specific lines multiple times using the `REPEAT` command.

---

✅ **Basic example:**
```bash
STRINGLN echo "hello world"
REPEAT LINES=1 TIMES=3
```

**Result:**
```bash
echo "hello world"
echo "hello world"
echo "hello world"
```

---

✅ **More complex example (Linux payload):**
```bash
STRINGLN echo "unix_time: $(date +%s)"
STRING echo "rng: $RANDOM"
ENTER
REPEAT LINES=3 TIMES=2
```

**Result:**
```bash
unix_time: 441763200
rng: 8238
unix_time: 441849600
rng: 20160
unix_time: 441936000
rng: 4439
```

---

**Explanation:**

- `REPEAT LINES=N TIMES=M` repeats the last **N** lines **M** times.
- This is useful for looping commands or outputs without manually duplicating lines.

### 💬 Improved Commenting Support
- Single-line comments:
    ```bash
    REM This is the original way to write a comment
    // This is the new C-style single-line comment
    ``` 
- Multi-line (block) comments:
    ```bash
    REM_BLOCK
    This is the traditional multi-line
    comment block in DuckScript.
    REM_BLOCK

    /*
        This is a new C-style 
        multi-line comment block 
    */
    ```

### ✊🏻/✋ Supporting HOLD & Release 
```bash
HOLD ENTER 
// HOLDING ENTER key for 5 seconds
DELAY 5000
// Releasing ENTER key
RELEASE ENTER
// release all HOLDED keys
RELEASE_ALL
```
### 💬 Improved STRING / STRINGLN BLOCK 
- Default way: 
    ```bash
    STRING
    echo 'you have something 
    called "determination"
    '
    END_STRING

    STRINGLN 
    echo "Objection! That was... objectionable!"
    echo "->|G_G|->"
    END_STRINGLN
    ```

- new way for better readability: 
    ```bash
    STRING_BLOCK
    echo 'you have something 
    called "determination"
    '
    END_STRING

    STRINGLN_BLOCK
    echo "Objection! That was... objectionable!"
    echo "->|G_G|->"
    END_STRINGLN
    ```
- Enable/Disable keeping indentation: 
    ```bash
    STRINGLN_BLOCK
    echo "Tesing: "
    DISABLE_STRIP
        echo "Strip disabled"
        echo "->|G_G|->"
    ENABLE_STRIP
        echo "Strip enabled"
        echo "->|G_G|->"

    END_STRINGLN
    ```
- Result : 
    ```bash
    echo "Tesing: "
            echo "Strip disabled"
            echo "->|G_G|->"
    echo "Strip enabled"
    echo "->|G_G|->"
    ```
- ❗By default STRIP is enabled which result to remove leading and trailing whitespace to disable it use __`DISABLE_STRIP`__  to keep indentation as previous example

### ⏳ Set delay between each line 
```bash
DEFAULTDELAY 5 // 5 ms between each line  or :
DEFAULT_DELAY 5 // same result 
```

### ⚠️ Note:
- When using `DEFINE`, it's best practice to **start variable names with a unique, uncommon character** to avoid conflicts or parsing errors.
- Avoid using commonly reserved symbols like `$` at the beginning of macro names.

✅ **Recommended Example:**
```c
// Use uncommon prefix characters for safer macro definitions
DEFINE @username  "Ziggy McSnazzlepop"
DEFINE #age       22
DEFINE ^state     "Kansas"
DEFINE !city      "Nowhere"
```

### 📥 Importing Other Payloads

- You can call other payloads stored in **internal_storage** from the main payload to use as second-stage operations.
- This modular approach improves organization and reuse of scripts.

✅ **Example:**
```bash
DELAY 500
GUI R
STRING powershell
SHIFT ENTER
DELAY 1500
ENTER

STRINGLN echo "Starting second stage..."
IMPORT stage2.oqs

// After stage2.oqs finishes, continue with sending data
STRINGLN echo "Sending data..."
IMPORT send_data.oqs

// Perform cleanup and shut down the system
STRINGLN echo "Cleaning up our tracks ^_^"
IMPORT AntiForensics.oqs

STRINGLN echo "See ya!"
STRINGLN shutdown -s -f -t 1
```

### 🛠️ For Developers and Debugging Purposes

- You can use the `PRINT` keyword to write debug messages to the **serial monitor**. This is helpful for troubleshooting or monitoring payload execution in real-time.

✅ **Example:**
```bash
$error = 404
PRINT This message should appear in the serial console
PRINT Error number: $error
```

---

### 🖥️ Accessing the Serial Monitor

#### 🔧 For Linux Users:
You can use [`picocom`](https://github.com/npat-efault/picocom) to access the serial monitor. Install it using your package manager, then run the following command:

```bash
while true; do if [ -e /dev/ttyACM0 ]; then picocom -b 9600 /dev/ttyACM0; fi; sleep 1; done
```

> ℹ️ This command continuously checks for `/dev/ttyACM0` and connects when available.

- You'll see ongoing output in the terminal.
- `PRINT` messages are color-coded for easier readability.
- This works in both **Storage Device Mode** and **HID Mode**.

---

#### 🪟 For Windows Users:
You can use [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) to access the serial monitor.

1. Connect your device via USB.
2. Open the app (PuTTY or Tera Term).
3. Choose **Serial** as the connection type.
4. Set the COM port (e.g., `COM3`) and baud rate to `9600`.
5. Start the session to begin viewing output.

> 💡 Tip: You can find your device's COM port in **Device Manager** under **Ports (COM & LPT)**.


---
## 🫡 Acknowledgments

This project is based on and inspired by the work from the __[dbisu/pico-ducky](https://github.com/dbisu/pico-ducky)__. I would like to sincerely acknowledge and thank the original authors for their foundational work, which served as the basis for this project. The current code extends and enhances their implementation with additional advanced features.
<br><br>
## ⚠️ Disclaimer – Read This or Regret It
This tool is for **educational and ethical use only**. Do **not** use it for illegal activities, unauthorized access. 

The author is **not responsible** for any misuse, data loss, damage, or unexpected visits from law enforcement.

Use it **wisely** — and only on systems you **own** or have **explicit, written permission** to test.

💻 + 🧠 = ✅  
💻 + 🦆 + 😈 = 🚓

**Stay smart. Stay legal. Hack responsibly.**
![OverQuack LOGO](https://github.com/VexilonHacker/OverQuack/blob/9e5d14ed5526943a0438d4cbcb6acb65a6377a05/assets/overquack_logo.png)
<!--this message is for you `aka` and `ytw`: 
mWfw@haDMWO2c1@suZTq_MBP6GXUdy25@sgbxrmJDu6dj277IsVSiL9df.d6cbyR2I6_8bqxa._QLeuBAvTR5qb9wf5IYkm5WvIWsY2uOo3p4TxiJjYFCC3qSEAaw4Ni_IXkjHjjVtyi1mV-iypM@m2tcwvEY@A0boX1-kq6u4hdl-D0pvyVC5SX7KOuz0#T.7r2U0CNxqWeHvf0IOf@30eJX78TRR0JONVG@oRpxVGRz7Val7r6lo4GI76jz6jTlI39kpHKiT8zmjcBj#auX6QeesfeyWTU.-Rp1jj07f4.kd64J2.ITwu6c0cd4yGDOk95eMytU#cogXUIUbDKwjvd.4nHrLQqVj5GtVaGmLYNzA4qNfpgGTGA2CrG1ThZPUTck0Wqt_lFaLHY22IrS8FYQt@sWU-j9yKRkbPZhBIskwCDaW-b9nnbF5POMYYhRuWKWRe9fiPpwXvdmr@p_Z9KHFyELJqoEp38nW.3r6hmTyeRMyWT_uKp.3uhgxd3Bwp5bHBNP2eVGR1ytXC_qUPk@XuLb2ewNCOyRa876KwSWhw_0XnbqJAuUsLILlkOmXMIiyCIbT#4c4OOxZP_btKZJ51woobmxLVX.adUIYH0R-Tqxq_K7Cdtpb3SyYbIYFp7D0LJE1NxeZsv8DnSuQ99j-VsQpV513VrKT9ysGIxsEdunNpy2z6596#Rnmck#8XwpPeBEUJl3vF1q9Jf#chyv@z0Y.VOg8-mMiuN4Jd-NQYluwsDad7CwywLFXpmpM2hCsd1mR1tKhC8_6FvvSFM1VEFpar9EyEXFHgTK#0dfA25YiFUDlzoit2VO.@Hyphk_H8wHjv4od8J05F5KNTqEcc.Oc3AxiRW9rCE38k0hMmkl0IpvNA#D8av07s0Q6l92DB5W#xex#pJm_11T7UTjHfJ1FfIkhl4_vDkjUAQpARCnsQtUrJSeOZzJ4jQWwZr8e366jvYg-dcAHJ.-toOWrdIDO#Lfw7Z_C2.4e2JdCFeiKKMbNyaR@gumqUha4lzgbZs7Q2uHKlL9teZd#Ah#DT-9Y@9Df#d8zps#LCkhXRuv2f#tffnXkL_ScNEIck5#GL7NXTVk6KojqZWs92_nn0XzGpkqLosYaxjk8GnY5gV63yj5afg#4NfPcbTnS121AEdr0jDkmoRLuZuuKFB5X2gaXTmw3pmOo2U1f77QC@Edq0_rfA1qX9jOII@MqGJ5jXb9uTzh@NSzEkKMwydJnKq_br_v.DujdN@3-YEUx40g9h_iTnrkmH#MYvqNd_zTr@V@qjKDLieBSheRrH7xwy2jCQ_CtdaDRouKp9v0#VR0@YeewARThvQ.mjBPOh78l6nNXyDHWE#ADMFYRseoKNklVDJ8ZGXLK6H5M9wx-N@#Xx2AGw2cQR2lgvQkBDGhbioOvVNRGsXDW#O6JVXIybH0gsNc2SUiz1wJ84I26_xOeyPgVbCbikQNXvwAcyGr3GM#UeocG9#lJBD2SW41zdFKXNt3414yNwRJ2VIQMfCJOdqhNY5BwikNWcQc4yK8j5ytFMfcAeYOCxusd#E17R1ckAEGLcyYGWLysl.zw5OA36n0.wJpOXQ#SBOKycFz0YWW3H2QAAy62caC9cUEn.heOGOHJs1AzJP7_4YDZB9f7fIdde9okO9tO@iMhcw1iuKHX3@EVXQ50-Ez69yKwQ0rz81N-r1wBFYdONq#3YYIr1II#nhm#PbeUe0BC2ui.6_8oAn7qqRM949QajnX@Rau6RMVDaboHTrKumHmZ4JU8jC9QLmWGVg4Qkk18s0s9.gmhVuo-UnBmyF35qNpTtkJx7OTAS.J7Jrw0W5xFgKAz.jJN0s.pRTqwR.u6FejzjoET5JQ7zriLbdLq0@mNwIFpx@M6yuVh1O1b-XL3ZfdL.TL1MCfbXp89y-c@KI10x-qydmGUfgDUeA7a.U8Zu_roDUur@Txbnx.h2C8zwzEbq7_esPSTb1BZxE-FCsR.v9Gw968ZEcJuFLF2RPW9VFGVnL8OOQMmh7_TQog0Y1-d8L-U2Hus5sGqn3WHw4keYYWQb65dG8B6vDjFycwALLjcv8j06bQbsNXrheubmJI@jVH7p2R2bLis#HrdVlUAeSdW7j53FOfp@7Zaw3LuYtlkh9l8d1qCJjqW5kgVBh9OEFzhCuiuUeds4VC.HbQE#23Gb#SRoEenCJOSL2eEa0h7x1tEZ_NC_mfiTbcaTNgKuIVoF1h09lZmXjbAlx0h3VFEkvXohZD#7Q5pkC0NCUYJviHSLSC4dt8o_qtFu4uFpKel9HOdUKkxhOJVl7d66sMq#fDSmvh6J7TuXeI07rB-VZeWZwAdI78siWe5CqVQO_Q6nVV6x_MQFgjj9JpjgeLwpPCm.ZS9xawuh6i1Oxic-meF6#ptQD-5_u5ykAHNr5R8oEH@Dkwsk6azZAO0RUEcuAa@G2e18ZdZXjjEEljtXOVY3jEXDlm00ryaIy.hX.@SkagZcpZvTZaBj5linNH@.x0RyMY_IbKv8qwcxnz-e0A601hlw5xspH#BdCB13tKhwVkfMQEMnHI#ZobmdxJ_S7-gCrr89-yPd#lai7i_QbmXqZ.-iayQuUR59MFO0QMZd_MRlqY-#@KY1fECXvKMqlEbSyL64yHDOwKe8KJV8gx7DPVlIX2CNTdwbN2_1HTy#nraRB@x-cmq-QAQhPbNBoV9S.5FIACYjK35c0d8trJ5AEPFuA4cQsN9Vlwc86g6usBUq0k8IGOFmuOikizAnvofUKho1FnQ#7mv1t-V-fwmmVL#2UCcbchdkcHGWcaJgtPxMa.fiGwF4sYAgpRoM1cjH87evEk3Lo@HUSCbTTg.1Nq.7QZmxk_fpFDbnc-CsFC3yk-YoUZbAinX7m-FhcbQ9Urn.jfVRsjwObX.LHJaxpXUfpo461Jg.qv.1DaJ1lCy5hbyc_gto_y#kHkr8AK@0SoJOA-jCXGlH6OI4eub2hYsHtMjTbnaDZjN6u1kZr-_4.6@ehlAl4n0uZ4bIpIsEi2gpWGdiKNcaJymfe7OFoNdN0VNon1boffOQa8YWoLygX6Nk8iLgYEnSPun2uNRCwayUp#bB7kv83f-A-gAQdWm1gjPmJQ@p5xLYqERtnItLBRvnc90pVyjTYcV2DboNarSuV.9M5J4MtA3D#GqPTiOUHn0f@SJ7-CXP0dB_HBmr8Kd7S@GyV#yfHRXjM-_O8v7gX49l5I61CK47vmztr-kdTaexIxEcOB8SgArrhG1zXzpSRQ.fNQvgzaZL8n2s3p-0AjHaQZGEb#a9sUdRCt13aWa7lkFdNlCD#TSGKrvOoiR1dlrmpcy9@O-opXyneF2kjSPEUqYRGkU-LlbuwaD_MiK#QN.k-u5rZDe2ZeBxyOvWggKqQdN4c6btfjocrCeZvHzHfTw_jkuvM1b9yyHs1OC2RzbrvncpZ0-vSn7GBUiC64UN8BSW#rg@fNiWXy9#7NCs9u#NL8LInLGSgaG9pWYhvIvk3gv-KIwy#EafX.o8qJdTg3Qmykky0sYrZ6gu8gBBj.NWTZLlqAIFwoSuRMc4DcvOSQRPl3Ei8nTG_nmYCCUe8lte_z56qEm3Z_bIpektL_JyjS1ixVq#zY8cCxV.FpnmNwas.XO9Iv8sZ.5hJCZ_uUmWmqTKcmp9GMmvPAdOBphVf3Sl6@.9hxIr07qwlnD52DEvow.68cP#3-CEH86mrY9GhEJkb@qI#QEjwHgBtd69L.JNi9Y4ClKsazXHE4tdn5#OSnii.KLTJcxqguQ46xH6lrIhp5iiXcYCObuCjpwsjX.Eo7Q43IL27Sj5FlyhUObj4S2Sxq5Th.4J9T84NXBTQ6qv1UckCum5vW8TpIz#0xs@sOCTp6x3l#L_QBz8m0HFuFQ-jHcg-Ydw-C7j.c#gyfW-UF7QaBzIv6eZldP1xS.mjkdCp_ReCd#icZmxSaV78PkWp92GbOTwjVOL7oc0j2gbO6KPEpd-D5PvVOliCZHnSWdecgI1.TZ.r7M1hr_ELoVxyrYabSEiDopl0AD7EmYhPi.S2AwTnT#._m__f4O_tdsI6npwakN4m21g#zgyfPyzrfttt2xCk_T@Mxghz-whZbqH0zje7huoXgEm9QTN#YxTTf@4h3h_ynFb.W5boo2gOfugM-wzrXzVh0ynXJN1mGlutgPyVJny8wu.veLOZXEG7lvGH8rh0i61#6912Py5Pw.evGBkw6.xEr7Rpd53BG9MKYxsK6dzixYvAnL@-V84Dincj3Eyy9UQ.tirhzraA4q3Hf38zVDrk_Cdh3TXhAhYewsw#ZXCg#bTi-@02c6C3xKzGDHOHk7@MMKQ-b_CMMpcACqLTI6fSh4YrQz9uRWqwkskynOqc-51siyFNj1bRAJV_zWRJmSLK702YPYS16FUdU3i3Nq3ucLOdoiajcsCk8CoNw-5e9WNjotr#MNXItnUt6AISGHjHeG4Syw-RQ64eGkFE7GJz-00X_zGyriBVTmZD_-gTABLFaOF2WjffLjOa.4xdYNchdLkqK_#jxpa0axgj5_YjQ6h2tarG5XzPsuoKT3757dauUpUPM1DCrcZ4OhXz0omApzqswUjO@M@pdcJ7CGYMFqkef7.si3NQTx1DceVjRSo-@e8uVcGTweiHwLE0_Jrk6GM9sBbfClaX_4HXlC_ke0Ti19vr##Ze.LWsaag@HDWp4aycpknrFexPpJw@kw4HB@Me0bikndim-wIc_kPOhKR_KOtoCGI-j5DcEFP-u.IZJwitVRiOd2SPg8LbSED0X04L-.TGNuzob_3WrPE0kLFgodPmZUutTHEHjZ6RwP2fRxoe1rHxLBwXwFNpl--NTubpZbHJ2re5pusa1SK0svF9.KrjbB2S@ObrRVSBtMpPDN_dZdxmK9oNbtXvMyua5StrsGPYZSdae8su4FA3X-dg4yA@V6i82j40orJt@ZpwX-oo.9G_yd7mZ785dle4lH2EcgSBkQudG@jftEwvJ4_u -->
