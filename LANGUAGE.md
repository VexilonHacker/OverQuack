# 📜 OverQuack Scripting Language (OQS) Reference

OverQuack supports a **superset of DuckyScript** with full programming capabilities, variables, functions, loops, randomisation, mouse control, and more. This document is your complete reference for every command, syntax, and feature.

---

## 📖 Table of Contents

- [Basic Keystroke Injection](#basic-keystroke-injection)
- [Delays and Jitter](#delays-and-jitter)
- [Variables and Constants](#variables-and-constants)
- [Control Flow - IF / ELSE / WHILE](#control-flow)
- [Functions and Import](#functions-and-import)
- [Mouse Control and Jiggler](#mouse-control-and-jiggler)
- [HOLD / RELEASE](#hold--release)
- [ATTACKMODE - USB Personality Switch](#attackmode)
- [Keyboard Layout Selection](#keyboard-layout-selection)
- [Block Strings and Indentation Control](#block-strings-and-indentation-control)
- [Random Value Generators](#random-value-generators)
- [Debugging with PRINT](#debugging-with-print)
- [Comments](#comments)
- [REPEAT Command](#repeat-command)
- [Full Demonstration Payload](#demo-payload)
- [Adding New Keyboard Layouts](#adding-layouts)
- [Tips and Best Practices](#tips)

---

## 🚀 Quick Command Index

### Typing
| Command | Description |
|---------|-------------|
| `STRING text` | Types the given text (supports variable expansion) |
| `STRINGLN text` | Types text and presses Enter |
| `STRING_BLOCK ... END_STRING` | Multi-line typing without Enter between lines |
| `STRINGLN_BLOCK ... END_STRINGLN` | Multi-line typing with Enter after each line |
| `IMPORT filename.oqs` | Executes another payload inline |
| `REPEAT LINES=N TIMES=M` | Repeats the last N lines M times |

### Key Combos
| Command | Equivalent Keys |
|---------|-----------------|
| `GUI` / `WINDOWS` / `COMMAND` | Windows / Command key |
| `RGUI` / `RWINDOWS` / `RCOMMAND` | Right Windows / Command key |
| `CTRL` / `CONTROL` | Control key |
| `RCTRL` / `RIGHT_CONTROL` | Right Control key |
| `ALT` / `OPTION` | Alt / Option key |
| `RALT` / `ROPTION` | Right Alt / Option key |
| `SHIFT` | Shift key |
| `RSHIFT` / `RIGHT_SHIFT` | Right Shift key |
| `APP` / `MENU` | Application / Context menu key |
| `ENTER` | Enter / Return |
| `TAB` | Tab |
| `SPACE` | Space bar |
| `BACKSPACE` | Backspace |
| `ESC` / `ESCAPE` | Escape |
| `DELETE` | Delete |
| `HOME` | Home |
| `END` | End |
| `INSERT` | Insert |
| `PAGEUP` | Page Up |
| `PAGEDOWN` | Page Down |
| `CAPSLOCK` | Toggle Caps Lock |
| `NUMLOCK` | Toggle Num Lock |
| `SCROLLLOCK` | Toggle Scroll Lock |
| `PRINTSCREEN` | Print Screen |
| `PAUSE` / `BREAK` | Pause / Break |
| `UPARROW` / `UP` | Up arrow |
| `DOWNARROW` / `DOWN` | Down arrow |
| `LEFTARROW` / `LEFT` | Left arrow |
| `RIGHTARROW` / `RIGHT` | Right arrow |
| `F1` ... `F24` | Function keys |

### Mouse
| Command | Description |
|---------|-------------|
| `MOUSE_MOVE x y` | Move mouse to absolute coordinates |
| `MOUSE_CLICK LEFT/RIGHT/MIDDLE` | Click a mouse button |
| `MOUSE_PRESS LEFT/RIGHT/MIDDLE` | Press (hold) a mouse button |
| `MOUSE_RELEASE LEFT/RIGHT/MIDDLE` | Release a mouse button |
| `MOUSE_SCROLL amount` | Scroll wheel (positive = up, negative = down) |
| `JIGGLE_MOUSE duration [step] [sleep]` | Jiggle mouse for a set time |
| `BACKGROUND_JIGGLE_MOUSE duration/INF [step] [sleep]` | Start a background jiggler when payload ends|

### Timing
| Command | Description |
|---------|-------------|
| `DELAY ms` | Pause for a given number of milliseconds |
| `DEFAULT_DELAY ms` / `DEFAULTDELAY ms` | Set delay between every line |
| `RANDOM_DELAY min max` | Sleep a random number of ms between min and max |
| `$_JITTER_ENABLED = 1` | Enable random micro-delays |
| `$_JITTER_MAX = ms` | Max extra jitter in ms |

### System and Control
| Command | Description |
|---------|-------------|
| `VAR $name = value` | Declare or update a mutable variable |
| `$name = expression` | Assign a value (math supported) |
| `DEFINE @name value` | Create an immutable constant |
| `FUNCTION name ... END_FUNCTION` | Define a reusable function |
| `IF ... ELSE IF ... ELSE ... END_IF` | Conditional branching |
| `WHILE ... END_WHILE` | Loop while condition is true |
| `RESTART_PAYLOAD` | Restart the payload from the beginning |
| `STOP_PAYLOAD` | Stop execution completely |
| `ATTACKMODE HID` | Switch to keyboard + mouse only (reboot) |
| `ATTACKMODE HID STORAGE` | Switch to keyboard + mouse + mass storage (reboot) |
| `RESET` / `RESET_SAFE` / `RESET_UF2` | Reboot the board |
| `SET_RESET_NORMAL` / `SET_RESET_SAFE` / `SET_RESET_UF2` | Set next reset mode |
| `FORMAT` | Wipe the filesystem and reboot |
| `LED_ON` / `LED_OFF` / `LED_R` / `LED_G` | Control the on-board LED |
| `WAIT_FOR_CAPS_ON/OFF/CHANGE` | Pause until Caps Lock changes state |
| `WAIT_FOR_NUM_ON/OFF/CHANGE` | Pause until Num Lock changes state |
| `WAIT_FOR_SCROLL_ON/OFF/CHANGE` | Pause until Scroll Lock changes state |
| `SELECT_LAYOUT LAYOUT` | Switch keyboard layout |
| `PRINT message` | Output to serial monitor |
| `ENABLE_DEBUG` / `DISABLE_DEBUG` | Toggle verbose debug output |
| `ENABLE_STRIP` / `DISABLE_STRIP` | Toggle whitespace stripping in blocks |
| `$_STRICT = 0 or 1` | Control `?ERR?` replacement for unsupported characters (default 1) |


---

## Basic Keystroke Injection

```bash
REM Open Notepad and type something
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 800
STRING Hello from OverQuack!
```

Every command is case‑insensitive. Outside of string blocks, leading/trailing whitespace on a line is ignored. Inside `STRING_BLOCK` / `STRINGLN_BLOCK`, whitespace handling is controlled by `ENABLE_STRIP` (strip, the default) or `DISABLE_STRIP` (preserve).

> ⚠️ `STRING` and `STRINGLN` (and by extension `STRING_BLOCK` / `STRINGLN_BLOCK`) only type **ASCII characters 32–126**.  
> Any character outside that range (e.g., `é`, `€`, or emojis) is replaced with `?ERR?` and a warning is printed to the serial monitor.  
> To type international characters, use the appropriate keyboard layout (`SELECT_LAYOUT`) and the corresponding key combinations instead of placing the raw character in a `STRING`.
> Set `$_STRICT = 0` to silently skip unsupported characters instead of printing `?ERR?`.

## Delays and Jitter

```bash
DELAY 1000                # Wait 1000 ms
DEFAULT_DELAY 50          # Automatically add 50 ms after each command
RANDOM_DELAY 500 1500     # Random sleep between 500 and 1500 ms

$_JITTER_ENABLED = 1      # Enable micro-random delays between lines
$_JITTER_MAX = 30         # Up to 30 ms extra jitter
```

> 💡 Tip: Use `$_JITTER_ENABLED` to mimic human typing speeds and make injection less detectable.

## Variables and Constants

```bash
VAR $username = "Jasper"
DEFINE @sleep 1000        # Constant (recommended prefix: @)
$counter = 1

STRING Hello $username, counter is $counter
DELAY @sleep - 200        # Math expressions supported
```

- **Variables** (`VAR` or `$name =`) are mutable and can hold strings or numbers.
- **Constants** (`DEFINE`) are immutable and replaced everywhere before execution.
- To avoid conflicts, start constant names with a special character like `@`, `#`, `!`  -  but `$` is reserved for variables.


### System Variables (Read-Only)

These are automatically updated by the device:

| Variable | Description |
|----------|-------------|
| `$_CAPSLOCK_ON` | 1 if Caps Lock is on, else 0 |
| `$_NUMLOCK_ON` | 1 if Num Lock is on, else 0 |
| `$_SCROLLLOCK_ON` | 1 if Scroll Lock is on, else 0 |
| `$_BSSID` | MAC address of the Wi-Fi board (Pico W / 2 W) |
| `$_SSID` | Configured Wi-Fi SSID (from `config.json`) |
| `$_PASSWD` | Wi-Fi password (from `config.json`) |
| `$_CURRENT_VID` | USB Vendor ID (hex) |
| `$_CURRENT_PID` | USB Product ID (hex) |
| `$_CURRENT_MANF` | USB Manufacturer string |
| `$_CURRENT_PROD` | USB Product string |

<a id="control-flow"></a>
## Control Flow - IF / ELSE / WHILE

```bash
IF $_CAPSLOCK_ON == 1
    CAPSLOCK
    PRINT Caps Lock was ON - turned it OFF
ELSE IF $_NUMLOCK_ON == 0
    PRINT Num Lock is OFF
ELSE
    PRINT Both locks are fine
END_IF

VAR $i = 0
WHILE $i < 3
    STRING Iteration $i
    ENTER
    $i = $i + 1
END_WHILE
```

Conditions support `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&` (and), `||` (or), and parentheses.  
Indentation is optional but recommended for readability.

## Functions and Import

```bash
FUNCTION openNotepad()
    GUI r
    DELAY 500
    STRING notepad
    ENTER
END_FUNCTION

openNotepad()

IMPORT drop_stage2.oqs       # Execute another payload inline
```

- Functions can call other functions and even import scripts.
- `IMPORT` runs the specified `.oqs` file as a sub-payload; execution resumes after the imported script finishes.

## Mouse Control and Jiggler

```bash
MOUSE_MOVE 100 200      # Absolute coordinates
MOUSE_CLICK LEFT
MOUSE_SCROLL 5

JIGGLE_MOUSE 5000       # Jiggle for 5 seconds
BACKGROUND_JIGGLE_MOUSE INF 10 0.2   # Infinite background jiggling after payload
```

- `MOUSE_MOVE` uses absolute coordinates (0-32767 range depending on display).
- `MOUSE_SCROLL` positive values scroll up, negative scroll down.
- `BACKGROUND_JIGGLE_MOUSE INF` starts an infinite jiggler that runs **after** the payload finishes, until the board is reset.
- **Preventing system lock / sleep :** a background jiggler is perfect for keeping a machine awake during long‑running payloads. Many systems lock the screen or go to sleep after a period of mouse inactivity. a continuous `BACKGROUND_JIGGLE_MOUSE` prevents that without interfering with keystroke injection.

## HOLD / RELEASE

```bash
HOLD CTRL ALT
DELAY 5000
RELEASE CTRL ALT
RELEASE_ALL
```

- `HOLD` keeps the listed keys pressed until a corresponding `RELEASE`.
- `RELEASE_ALL` releases every currently held key.

<a id="attackmode"></a>
## ATTACKMODE - USB Personality Switch

```bash
ATTACKMODE HID              # Keyboard + mouse only
ATTACKMODE HID STORAGE      # Both HID and mass storage
```

The payload **resumes from the next line** automatically after the board reboots!  
Use `ATTACKMODE` to switch between stealth-HID and visible-storage modes without replugging.

## Keyboard Layout Selection

```bash
SELECT_LAYOUT WIN_FR        # Switch to French layout
STRING Bonjour !
SELECT_LAYOUT WIN_ES        # Switch to Spanish layout
STRING ¡Hola!
```

> Here is the list of supported layouts:
>```python
>SUPPORTED_LAYOUTS = {
>    "US_DVO",
>    "US",
>    "WIN_BR",
>    "WIN_CZ",
>    "WIN_CZ1",
>    "WIN_DA",
>    "WIN_DE",
>    "WIN_ES",
>    "WIN_FR",
>    "WIN_HU",
>    "WIN_IT",
>    "WIN_PO",
>    "WIN_SW",
>    "WIN_TR",
>    "WIN_UK",
>    "MAC_FR",
>    "MAC_US",
>}
>```

You can add custom layouts (see [Adding New Keyboard Layouts](#-adding-new-keyboard-layouts) at the end of this document).

## Block Strings and Indentation Control

`STRING_BLOCK` / `STRINGLN_BLOCK` let you inject multiple lines of text.  
They are **literal** regions, only variable, constant, and random‑value expansion is applied.  
Comments and special keywords are **not** recognized inside a block.  

### Basic usage

```duckyscript
STRINGLN_BLOCK
echo "Line 1"
echo "Line 2"
END_STRINGLN

STRING_BLOCK
This text
has no trailing newlines.
END_STRING
```

### Controlling indentation

Two **global** commands set the default whitespace stripping for all subsequent blocks:

| Command          | Effect                                         |
|------------------|------------------------------------------------|
| `ENABLE_STRIP`   | **Remove** leading/trailing whitespace from block lines (default) |
| `DISABLE_STRIP`  | **Preserve** leading/trailing whitespace (keep exact indentation) |

> 💡 These commands act globally, just like `DEFAULT_DELAY`. The setting persists until changed by another `ENABLE_STRIP`/`DISABLE_STRIP` command.

**Example: global control**

```duckyscript
DISABLE_STRIP
STRING_BLOCK
    This line keeps its leading spaces.
    So does this one.
END_STRING

ENABLE_STRIP
STRING_BLOCK
    This line will be trimmed (leading spaces removed).
    This line too.
END_STRING
```




## Random Value Generators

```bash
$_RANDOM_NUMBER:6              # e.g., "482931"
$_RANDOM_LOWERCASE_LETTER:3    # e.g., "qwe"
$_RANDOM_UPPERCASE_LETTER:7    # e.g., "ZDCFVGY"
$_RANDOM_LETTER:4              # Mixed case, e.g., "aWdZ"
$_RANDOM_SPECIAL:6             # e.g., "!@#$%^"
$_RANDOM_CHAR:8                # Fully random, e.g., "^andZaD23?"
$_RANDOM_INT                   # Integer between $_RANDOM_MIN and $_RANDOM_MAX

$_RANDOM_MIN = 5
$_RANDOM_MAX = 10
VAR $random_val = $_RANDOM_INT
```

- The `:N` suffix controls how many characters/digits are generated (default 1).
- `$_RANDOM_INT` respects the current `$_RANDOM_MIN` and `$_RANDOM_MAX` values.

## Debugging with PRINT

```bash
PRINT Starting stage 2...
$var = 42
PRINT Value of var: $var
```

Output appears on the **serial monitor** (colored for readability).  
See the [Serial Monitor / Debug View](../README.md#serial-monitor--debug-view) section in the main README for connection instructions.

## Comments

```bash
REM Traditional single-line comment
// C-style single-line comment

REM_BLOCK
Multi-line
comment
END_REM

/*
  Block comment
  like in C
*/
```

All comment styles are interchangeable.

## REPEAT Command

```bash
STRINGLN echo "hello"
REPEAT LINES=1 TIMES=3
```

Result:
```
echo "hello"
echo "hello"
echo "hello"
```

Works on any preceding lines, including multi-line blocks.  
`REPEAT` takes a snapshot of the specified number of previous lines and replays them.

> 💡 `REPEAT` captures the preceding lines from the **current execution context**.  
> It does **not** replay lines that came before a function call, an `IMPORT`, or an `ATTACKMODE` reset, because those create a fresh context.

---

<a id="demo-payload"></a>
## 🧪 Full Demonstration Payload

![OverQuack Demo Payload on Windows 10](./assets/OverQuack_Gifs/OverQuack_Win.gif)
```bash
/*
======================================================
    OverQuack Demo
    Version: 2.0
    Author: VexilonHacker
    OS: Windows
======================================================
*/

DEFINE @SHORT_DELAY 500
DEFINE @LONG_DELAY 1500
DEFAULT_DELAY 10

VAR $counter = 1
$username = "OverQuackUser"

GUI r
DELAY @SHORT_DELAY
STRINGLN notepad
DELAY @SHORT_DELAY
GUI UPARROW
delay @SHORT_DELAY


STRINGLN_BLOCK
WiFi OverQuack Dynamic Framework Context Profile:
- Active Tracker Code: $_RANDOM_NUMBER:8
- Hardware Identity Target Match: $_BSSID
END_STRINGLN

STRINGLN Hello $username, this is a demo of OverQuack!
STRINGLN Your random session ID: $_RANDOM_NUMBER:12
STRINGLN Your passkey lowercase letter: $_RANDOM_LOWERCASE_LETTER
STRING Your secret special char: $_RANDOM_SPECIAL
ENTER

IF ($_CAPSLOCK_ON == 1)
    STRINGLN Caps Lock is ON, turning it OFF for demo
    CAPSLOCK
ELSE
    STRINGLN Caps Lock is OFF, leaving as is
END_IF

WHILE ($counter <= 3)
    PRINT Loop iteration #$counter
    STRINGLN Loop step $counter completed.
    $counter = $counter + 1
    DELAY @SHORT_DELAY
END_WHILE



MOUSE_SCROLL 3
DELAY @SHORT_DELAY
MOUSE_SCROLL -3


FUNCTION showEndMessage()
    PRINT [DEMO] Function executed.
    STRING All demo features completed successfully!,
    SPACE
    SPACE
    STRINGLN Press ENTER to close Notepad after banner printed...
    ENTER
END_FUNCTION

showEndMessage()

$_STRICT = 0
DISABLE_STRIP
STRINGLN_BLOCK
                                                                                 /$$
                                                                                | $$
  /$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$$| $$   /$$
 /$$__  $$|  $$  /$$//$$__  $$ /$$__  $$ /$$__  $$| $$  | $$ |____  $$ /$$_____/| $$  /$$/
| $$  \ $$ \  $$/$$/| $$$$$$$$| $$  \__/| $$  \ $$| $$  | $$  /$$$$$$$| $$      | $$$$$$/
| $$  | $$  \  $$$/ | $$_____/| $$      | $$  | $$| $$  | $$ /$$__  $$| $$      | $$_  $$
|  $$$$$$/   \  $/  |  $$$$$$$| $$      |  $$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$
 \______/     \_/    \_______/|__/       \____  $$ \______/  \_______/ \_______/|__/  \__/
                                              | $$
                                              | $$
                                              |__/

END_STRINGLN
$_STRICT = 1

$final_msg = Demo finished. Goodbye!
STRINGLN $final_msg  press enter to exit
ALT F4
PRINT $final_msg
```
<br>

> **This is the same demo script shipped as `payload.oqs`. uses nearly every feature.**

---
<a id="adding-layouts"></a>
## 🌍 Adding New Keyboard Layouts

OverQuack supports any layout generated by the [official CircuitPython Layout Generator](https://www.neradoc.me/layouts/).  
**All of the following steps are performed directly on the Pico’s `CIRCUITPY/` drive** – you’re editing the files that live on the device itself.

1. Switch your Pico to **storage mode** (mode pin floating) so the `CIRCUITPY` drive appears on your computer.
2. Visit [https://www.neradoc.me/layouts/](https://www.neradoc.me/layouts/), choose your language, and download the ZIP file.
3. Extract the ZIP. You’ll find two `.mpy` files inside:
   - `keyboard_layout_<LANGUAGE>.mpy`
   - `keycode_<LANGUAGE>.mpy`
4. Copy these two files directly into the corresponding folders on the **CIRCUITPY** drive:
   - `keyboard_layout_<LANGUAGE>.mpy` → `CIRCUITPY/lib/keyboard_layouts/`
   - `keycode_<LANGUAGE>.mpy` → `CIRCUITPY/lib/keycodes/`
5. Open the file `CIRCUITPY/overquackify.py` in a text editor. Locate the `LAYOUTS_MAP` dictionary (around line 107‑124). Add a new entry for your layout using the same pattern:
   ```python
   "WIN_XY": ("keyboard_layouts.keyboard_layout_win_xy", "keycodes.keycode_win_xy"),
   ```
   (Replace `WIN_XY`, `win_xy` with your actual layout name.)
6. Save the file, eject the `CIRCUITPY` drive, and switch back to **HID mode** (mode pin to GND).  
   The new layout is now available immediately with `SELECT_LAYOUT WIN_XY`.

> 💡 The drive label changes to whatever is set in `config.json` -> `DRIVE_LABEL` (default `OVERQUACK`) after the first `ATTACKMODE HID STORAGE` cycle. This is expected and does not affect functionality.


---

<a id="tips"></a>
## 💡 Tips and Best Practices

- **Use `DEFINE` with a special prefix** (like `@`) to avoid accidental conflicts with command names.
- **Indent control blocks** for readability. it's optional but helps debugging.
- **Keep payloads modular**. use `IMPORT` to split large scripts into smaller, reusable files.
- **Test with `PRINT`** before unleashing on a real target; the serial monitor is your best friend.
- **Be aware of the blocking TCP server**. when you `RUN` a payload remotely, the device can't accept new commands until it finishes.
- **After an `ATTACKMODE` switch**, the device continues from the next line automatically. plan your payload accordingly.

[👈 Back to README](README.md)
