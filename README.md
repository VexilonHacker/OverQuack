# 🦆 OverQuack
![Alt text](https://raw.githubusercontent.com/VexilonHacker/OverQuack/refs/heads/main/assets/image.png?token=GHSAT0AAAAAADGIESQ474QFMIKUPDYHSES62C5HJMQ)
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

``` go 
go run OverQuack_Installer.go
```
![auto installation](https://raw.githubusercontent.com/VexilonHacker/OverQuack/refs/heads/main/assets/auto_installation.gif?token=GHSAT0AAAAAADGIESQ5Y7Q6WW33LG7OYYVC2C5HJYA)

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

![Manuall installation](https://raw.githubusercontent.com/VexilonHacker/OverQuack/refs/heads/main/assets/manual_installation.gif?token=GHSAT0AAAAAADGIESQ5S4THAIXWHB5BSS4A2C5HKFQ)

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
![Pico w connection](https://raw.githubusercontent.com/VexilonHacker/OverQuack/refs/heads/main/assets/wow_NEW._neonpng.png?token=GHSAT0AAAAAADGIESQ5AOHXCKMVNVMM6U3S2C5HLIQ)

### 🛜 Wireless HID Control & Remote Payload Delivery

This feature is supported **only** on the `Pico W` and `Pico 2 W`.

#### ✅ Available Operations:
- 📂 List all payloads/files  
- 📥 Upload / 📤 Download payloads  
- 📝 Read / ❌ Delete payloads  
- ▶️ Run payload remotely

#### 💡 Example:

![Remote Control Demo](https://raw.githubusercontent.com/VexilonHacker/OverQuack/refs/heads/main/assets/client.gif?token=GHSAT0AAAAAADGIESQ4RSQGABQRXP5GIE3U2C5HKUA)

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
