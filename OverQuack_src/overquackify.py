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

import asyncio, gc, re, traceback, board, microcontroller, json 

from micropython import const
from random import choice, randint
from time import monotonic, sleep

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from board import *
from digitalio import DigitalInOut, Pull
from usb_hid import devices

VERSION = "2.0" # last version 1.5 
PROBLEM_CODE = "?ERR?'"
# constants (micro-optimisation)
DEFAULT_PIN_NUM = const(5)
BLINK_MIN_MS = const(200)
BLINK_MAX_MS = const(600)
RANDOM_DEFAULT_MIN = const(0)
RANDOM_DEFAULT_MAX = const(65535)

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
WHITE = "\033[97m"
GOLD = "\033[38;2;255;215;0m"
SILVER = "\033[38;2;192;192;192m"
BRONZE = "\033[38;2;205;127;50m"
PINK = "\033[38;2;255;105;180m"
STEEL_BLUE = "\033[38;2;70;130;180m"

DUCKYKEYS = {
    'WINDOWS': Keycode.GUI, 'RWINDOWS': Keycode.RIGHT_GUI,
    'GUI': Keycode.GUI, 'RGUI': Keycode.RIGHT_GUI,
    'COMMAND': Keycode.GUI, 'RCOMMAND': Keycode.RIGHT_GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION,
    'SHIFT': Keycode.SHIFT, 'RSHIFT': Keycode.RIGHT_SHIFT,
    'ALT': Keycode.ALT, 'RALT': Keycode.RIGHT_ALT,
    'OPTION': Keycode.ALT, 'ROPTION': Keycode.RIGHT_ALT,
    'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL, 'RCTRL': Keycode.RIGHT_CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,'BACKSPACE': Keycode.BACKSPACE,

    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,

    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,

    'F12': Keycode.F12, 'F13': Keycode.F13, 'F14': Keycode.F14, 'F15': Keycode.F15,
    'F16': Keycode.F16, 'F17': Keycode.F17, 'F18': Keycode.F18, 'F19': Keycode.F19,
    'F20': Keycode.F20, 'F21': Keycode.F21, 'F22': Keycode.F22, 'F23': Keycode.F23,
    'F24': Keycode.F24
}

DUCKYCONSUMERKEYS = {
    'MK_VOLUP': ConsumerControlCode.VOLUME_INCREMENT, 
    'MK_VOLDOWN': ConsumerControlCode.VOLUME_DECREMENT, 
    'MK_MUTE': ConsumerControlCode.MUTE,

    'MK_NEXT': ConsumerControlCode.SCAN_NEXT_TRACK,
    'MK_PREV': ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    'MK_PP': ConsumerControlCode.PLAY_PAUSE,
    'MK_STOP': ConsumerControlCode.STOP
}

LAYOUTS_MAP = {
    "US"      : ("adafruit_hid.keyboard_layout_us", "adafruit_hid.keycode"),
    "US_DVO"  : ("keyboard_layouts.keyboard_layout_us_dvo", "adafruit_hid.keycode"),
    "WIN_BR"  : ("keyboard_layouts.keyboard_layout_win_br", "keycodes.keycode_win_br"),
    "WIN_CZ"  : ("keyboard_layouts.keyboard_layout_win_cz", "keycodes.keycode_win_cz"),
    "WIN_CZ1" : ("keyboard_layouts.keyboard_layout_win_cz1", "keycodes.keycode_win_cz1"),
    "WIN_DA"  : ("keyboard_layouts.keyboard_layout_win_da", "keycodes.keycode_win_da"),
    "WIN_DE"  : ("keyboard_layouts.keyboard_layout_win_de", "keycodes.keycode_win_de"),
    "WIN_ES"  : ("keyboard_layouts.keyboard_layout_win_es", "keycodes.keycode_win_es"),
    "WIN_FR"  : ("keyboard_layouts.keyboard_layout_win_fr", "keycodes.keycode_win_fr"),
    "WIN_HU"  : ("keyboard_layouts.keyboard_layout_win_hu", "keycodes.keycode_win_hu"),
    "WIN_IT"  : ("keyboard_layouts.keyboard_layout_win_it", "keycodes.keycode_win_it"),
    "WIN_PO"  : ("keyboard_layouts.keyboard_layout_win_po", "keycodes.keycode_win_po"),
    "WIN_SW"  : ("keyboard_layouts.keyboard_layout_win_sw", "keycodes.keycode_win_sw"),
    "WIN_TR"  : ("keyboard_layouts.keyboard_layout_win_tr", "keycodes.keycode_win_tr"),
    "WIN_UK"  : ("keyboard_layouts.keyboard_layout_win_uk", "keycodes.keycode_win_uk"),
    "MAC_US"  : ("adafruit_hid.keyboard_layout_us", "adafruit_hid.keycode"),
    "MAC_FR"  : ("keyboard_layouts.keyboard_layout_mac_fr", "keycodes.keycode_mac_fr"),
}

def LoadJsonConf(json_file="config.json"):
    config = {}
    try:
        with open(json_file, "r") as f:
            config = json.load(f)

    except (OSError, ValueError) as e:
        print_with_color(f"ERR: {e}\nconfig = {config}", BRIGHT_RED)
        config['DEFAULT_PAYLOAD'] = "payload.oqs"
        config['ENABLE_SERIAL_DEBUG'] = True
        config['BOARD'] = {
            'controll_mode_pin': DEFAULT_PIN_NUM,
            'enable_auto_switch_mode': True,
            'enable_auto_reload': False
        }
        config['AP'] = {
            "ssid": "OverQuackError",
            "password": "OverQuackItBrother1984",
            "channel": 6,
            "ip_address": "10.10.5.1",
            "ports": 1084
        }
        config['USB_IDENTIFICATION'] = {
            "manufacturer": "CHICONY",
            "product": "HP Basic USB Keyboard",
            "vid": "0x03F0",
            "pid": "0x0024"
        }
    return config

config = LoadJsonConf()

def _capsOn():
    return 1 if kbd.led_on(Keyboard.LED_CAPS_LOCK) else 0
def _numOn():
    return 1 if kbd.led_on(Keyboard.LED_NUM_LOCK) else 0
def _scrollOn():
    return 1 if kbd.led_on(Keyboard.LED_SCROLL_LOCK) else 0

def _get_vid():
    return config.get("USB_IDENTIFICATION", {}).get("vid", "0x0000")
def _get_pid():
    return config.get("USB_IDENTIFICATION", {}).get("pid", "0x0000")
def _get_manf():
    return config.get("USB_IDENTIFICATION", {}).get("manufacturer", "Unknown")
def _get_prod():
    return config.get("USB_IDENTIFICATION", {}).get("product", "Unknown")


INTERNALVARIABLES = {
    "$_CAPSLOCK_ON": _capsOn,
    "$_NUMLOCK_ON": _numOn,
    "$_SCROLLLOCK_ON": _scrollOn,
    "$_BSSID": lambda: _Ap_Info('bssid'),
    "$_SSID": lambda: _Ap_Info('ssid'),
    "$_PASSWD": lambda: _Ap_Info('password'),
    "$_CURRENT_VID": _get_vid,
    "$_CURRENT_PID": _get_pid,
    "$_CURRENT_MANF": _get_manf,
    "$_CURRENT_PROD": _get_prod,
}

variables = {
    "$_RANDOM_MIN": RANDOM_DEFAULT_MIN, 
    "$_RANDOM_MAX": RANDOM_DEFAULT_MAX,
    "$_JITTER_ENABLED": 0,   
    "$_JITTER_MAX": 20,
    "$_STRICT": 1,
}


rng_variables = [
    "$_RANDOM_NUMBER", 
    "$_RANDOM_LOWERCASE_LETTER",
    "$_RANDOM_UPPERCASE_LETTER",
    "$_RANDOM_LETTER",
    "$_RANDOM_SPECIAL", 
    "$_RANDOM_CHAR"
]

defines = {}
functions = {}

letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
specialChars = "!@#$%^&*()"

defaultDelay = 0
oneshot = True
progStatusPin = None

kbd = Keyboard(devices)
consumerControl = ConsumerControl(devices)
layout = KeyboardLayout(kbd)
mouse = Mouse(devices)

_led = None

def set_led(led_obj):
    global _led
    _led = led_obj

def _Ap_Info(elem):
    try:
        import wifi
    except ImportError:
        # Non-WiFi board: return safe defaults
        if elem == 'ssid' or elem == 'password':
            return "N/A"
        elif elem == 'bssid':
            return "00:00:00:00:00:00"
        else:
            return ""

    # WiFi present
    if elem == 'ssid':
        return config['AP']['ssid']
    elif elem == 'password':
        return config['AP']['password']
    elif elem == 'bssid':
        return ":".join("{:02X}".format(b) for b in wifi.radio.mac_address)
    else:
        return "" 


# Utility functions
def print_with_color(STRING, COLOR=WHITE, sep=" ", end="\n"):
    print(f"{COLOR}{STRING}{RESET}", sep=sep, end=end)

ENABLE_DEBUG = config.get("ENABLE_SERIAL_DEBUG", True)

def _getIfCondition(line):
    parts = line.split(None, 1)
    if len(parts) < 2:
        return ""
    return parts[1].strip()

def SelectLayout(layout_key):
    layout_key = layout_key.upper()
    layout_entry = LAYOUTS_MAP.get(layout_key)
    if ENABLE_DEBUG:
        print_with_color(f"LAYOUT_KEY: {layout_key}, LAYOUT_ENTERY: {layout_entry}", STEEL_BLUE)

    if not layout_entry:
        if ENABLE_DEBUG:
            print_with_color(f"[INVALID_LAYOUT] {layout_key}", BRIGHT_RED)
        return None, None
    layout_module_path = layout_entry[0]
    keycode_module_path = layout_entry[1]
    try:
        layout_module = __import__(layout_module_path)
        for part in layout_module_path.split(".")[1:]:
            layout_module = getattr(layout_module, part)
        keycode_module = __import__(keycode_module_path)
        for part in keycode_module_path.split(".")[1:]:
            keycode_module = getattr(keycode_module, part)
    except ImportError as e:
        if ENABLE_DEBUG:
            print_with_color(f"[LAYOUT_ERROR] Cannot import layout '{layout_key}': {e}", BRIGHT_RED)
        return None, None
    KeyboardLayoutClass = getattr(layout_module, "KeyboardLayout")
    KeycodeClass = getattr(keycode_module, "Keycode")
    return KeyboardLayoutClass, KeycodeClass

def evaluateExpression(expression):
    expression = str(expression)
    if ENABLE_DEBUG:
        print_with_color(f'[1_EVALUATE_EXPRESION] BEGIN, expression: "{expression}"', YELLOW)
    expression = expression.replace("^", "**")
    expression = expression.replace("&&", "and")
    expression = expression.replace("||", "or")
    result = PROBLEM_CODE
    try:
        result = eval(expression)
        if ENABLE_DEBUG:
            print_with_color(f'[2_EVALUATE_EXPRESION] expression: "{expression}", result "{result}"', YELLOW)
    except Exception:
        if ENABLE_DEBUG:
            print_with_color(f"[EVALUATE_EXPRESION_ERROR] INVALID EXPRESSION: {expression}, RESULT = {result}", RED)
    return result

def convertLine(line):
    commands = []
    for key in filter(None, line.split()):
        key = key.upper()
        command_keycode = DUCKYKEYS.get(key, None)
        command_consumer_keycode = DUCKYCONSUMERKEYS.get(key, None)
        if command_keycode is not None:
            commands.append(command_keycode)
        elif command_consumer_keycode is not None:
            commands.append(1000 + command_consumer_keycode)
        elif hasattr(Keycode, key):
            commands.append(getattr(Keycode, key))
        else:
            if ENABLE_DEBUG:
                print_with_color(f"Unknown key: <{key}>", BRIGHT_RED)

    return commands

def runScriptLine(line):
    keys = convertLine(line)
    for k in keys:
        if k > 1000:
            consumerControl.press(int(k-1000))
        else:
            kbd.press(k)
    for k in reversed(keys):
        if k > 1000:
            consumerControl.release()
        else:
            kbd.release(k)

def sendString(line):
    strict = int(variables.get("$_STRICT", 1))
    sanitized = []
    for ch in line:
        if 32 <= ord(ch) <= 126:
            sanitized.append(ch)
        elif strict:
            sanitized.append(PROBLEM_CODE)
            if ENABLE_DEBUG:
                print_with_color(f"[WARNING] Unsupported character '{repr(ch)}' in line: {line}\n[*] character '{repr(ch)}' changed to ?ERR?", GOLD)
    layout.write(''.join(sanitized))


# def sendString(line):
#     layout.write(line)

def replaceDefines(line):
    for define, value in defines.items():
        line = line.replace(define, str(value))
    return line

def replaceVariables(line):
    for var in variables:
        if var in line:
            line = line.replace(var, str(variables[var]))
    for var in INTERNALVARIABLES:
        if var in line:
            line = line.replace(var, str(INTERNALVARIABLES[var]()))
    return line

def replaceRandomVariables(expression):
    if not any(var in expression for var in rng_variables):
        return expression

    pattern = re.compile(r"(\$_RANDOM_[A-Z_]+)(?::(-?\d+))?")

    def _replacer(m):
        rand_type = m.group(1)
        count_str = m.group(2)
        if count_str is None:
            count = 1
        else:
            try:
                count = max(int(count_str), 1)
            except ValueError:
                count = 1
        if rand_type == "$_RANDOM_NUMBER":
            rand_value = ''.join(choice(RandomizeData(numbers)) for _ in range(count))
        elif rand_type == "$_RANDOM_LOWERCASE_LETTER":
            rand_value = ''.join(choice(RandomizeData(letters)) for _ in range(count))
        elif rand_type == "$_RANDOM_UPPERCASE_LETTER":
            rand_value = ''.join(choice(RandomizeData(letters.upper())) for _ in range(count))
        elif rand_type == "$_RANDOM_LETTER":
            rand_value = ''.join(choice(RandomizeData(letters + letters.upper())) for _ in range(count))
        elif rand_type == "$_RANDOM_SPECIAL":
            rand_value = ''.join(choice(RandomizeData(specialChars)) for _ in range(count))
        elif rand_type == "$_RANDOM_CHAR":
            rand_value = ''.join(choice(RandomizeData(letters + letters.upper() + numbers + specialChars)) for _ in range(count))
        else:
            return m.group(0)
        return rand_value

    return pattern.sub(_replacer, expression)

def replaceAll(line, enable_replace_vars=1, enable_replace_defines=1, enable_replace_randoms=1):
    if enable_replace_defines:
        line = replaceDefines(line)
    if enable_replace_vars:
        line = replaceVariables(line)
    if enable_replace_randoms:
        line = replaceRandomVariables(line)
    return line

def RandomizeData(data):
    lst = list(str(data))
    for i in range(len(lst) - 1, 0, -1):
        j = randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def JiggleMouse(jiggle_delay, step=1, slp=0.5):
    start_time = monotonic()
    while (monotonic() - start_time) < jiggle_delay:
        mouse.move(x=step, y=0)
        sleep(slp)
        mouse.move(x=-step, y=0)
        sleep(slp)

async def JiggleMouseInBackground(jiggle_delay, step=1, slp=0.5, INF=0):
    if INF:
        while True:
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)
            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)
    else:
        start_time = monotonic()
        while (monotonic() - start_time) < jiggle_delay:
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)
            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)

def _sleep_jitter(base_ms):
    base_s = base_ms / 1000.0
    if int(variables.get("$_JITTER_ENABLED", 0)) == 1:
        jitter_max = int(variables.get("$_JITTER_MAX", 20))
        extra = randint(0, jitter_max) / 1000.0
        sleep(base_s + extra)
    else:
        sleep(base_s)

class ExecContext:
    __slots__ = ('lines', 'i', 'skip_depth', 'branch_taken_stack', 'is_function', 'loop_stack')
    def __init__(self, lines, start_index=0, is_function=False):
        self.lines = lines          # list of raw lines (including trailing newline)
        self.i = start_index
        self.skip_depth = 0
        self.branch_taken_stack = []   # bool per IF level
        self.is_function = is_function
        self.loop_stack = []
        self.previousLines = []

# I MIGHT ADD THIS FEATURE IN FUTURE
# def file_exfil_receive(filename, byte_count, bit_time_ms=200, led='CAPSLOCK', stop_led=None):
    # """
    # Edge-driven LED exfiltration receiver.
    # Uses WAIT_FOR_CAPS_CHANGE-style polling – zero timing assumptions.
    # If stop_led is given, auto-stop is used (byte_count ignored).
    # """

def execute_line(line, ctx):
    global defaultDelay, variables, functions, defines, ENABLE_DEBUG
    line = line.strip()

    # random integer replacement
    rmin = int(variables.get("$_RANDOM_MIN", RANDOM_DEFAULT_MIN))
    rmax = int(variables.get("$_RANDOM_MAX", RANDOM_DEFAULT_MAX))
    while "$_RANDOM_INT" in line:
        line = line.replace("$_RANDOM_INT", str(randint(rmin, rmax)), 1)


    if line.startswith("VAR"):
        if ENABLE_DEBUG:
            print_with_color("Command: VAR (early)", BRIGHT_GREEN)
        match = re.match(r"VAR\s+\$(\w+)\s*=\s*(.+)", line)
        if match:
            varName = "$" + match.group(1)
            varValue = match.group(2)
            varValue = replaceAll(varValue, 1, 1, 0)   # expand only the value
            val = evaluateExpression(varValue)
            if val == PROBLEM_CODE:
                val = varValue
            variables[varName] = val
        return True

    if line.startswith("$"):
        if ENABLE_DEBUG:
            print_with_color("Command: variable assignment (early)", BRIGHT_GREEN)
        match = re.match(r"\$(\w+)\s*=\s*(.+)", line)
        if match:
            varName = "$" + match.group(1)
            expr = match.group(2)
            expr = replaceAll(expr, 1, 1, 0)           # expand only the expression
            val = evaluateExpression(expr)
            if val == PROBLEM_CODE:
                val = expr
            variables[varName] = val
        return True

    if line.startswith("DEFINE"):
        if ENABLE_DEBUG:
            print_with_color("Command: DEFINE (early)", BRIGHT_GREEN)
        after_def = line[len("DEFINE"):].strip()
        first_space = after_def.find(" ")
        if first_space >= 0:
            define_name = after_def[:first_space]
            define_value = after_def[first_space+1:].strip()
            if define_value:
                # Expand only the value part
                define_value = replaceAll(define_value, 1, 1, 0)
                calc = evaluateExpression(define_value)
                if calc != PROBLEM_CODE:
                    define_value = calc
                defines[define_name] = define_value
        return True

    line = replaceAll(line, 1, 1, 0)
    if ENABLE_DEBUG:
        print_with_color("replaceAll completed successfully", CYAN)
        print_with_color(f"After replaceAll: {repr(line)}", CYAN)

    # Helper to extract the argument while preserving spaces
    def get_arg(cmd_line):
        space_pos = cmd_line.find(' ')
        if space_pos != -1:
            return cmd_line[space_pos+1:]
        return ""

    # MOUSE commands
    if line.startswith("JIGGLE_MOUSE"):
        if ENABLE_DEBUG:
            print_with_color("Command: JIGGLE_MOUSE", BRIGHT_GREEN)
        try:
            arg = get_arg(line)
            if arg:
                parts = arg.strip().split()
                dur = float(parts[0]) / 1000.0
                step = int(parts[1]) if len(parts) >= 2 else 1
                slp = float(parts[2]) if len(parts) >= 3 else 0.5
                JiggleMouse(dur, step=step, slp=slp)
        except Exception as e:
            print_with_color(f"JIGGLE_MOUSE error: {e}", BRIGHT_RED)
        return True

    if line.startswith("BACKGROUND_JIGGLE_MOUSE"):
        if ENABLE_DEBUG:
            print_with_color("Command: BACKGROUND_JIGGLE_MOUSE", BRIGHT_GREEN)
        try:
            arg = get_arg(line)
            if arg:
                parts = arg.strip().split()
                if parts[0].upper() == "INF":
                    # Infinite background jiggle, starts after payload, runs forever
                    step = int(parts[1]) if len(parts) >= 2 else 1
                    slp = float(parts[2]) if len(parts) >= 3 else 0.5
                    asyncio.create_task(JiggleMouseInBackground(0, step=step, slp=slp, INF=1))
                    if ENABLE_DEBUG:
                        print_with_color("Scheduled infinite background jiggle", MAGENTA)
                else:
                    dur = float(parts[0]) / 1000.0
                    step = int(parts[1]) if len(parts) >= 2 else 1
                    slp = float(parts[2]) if len(parts) >= 3 else 0.5
                    asyncio.create_task(JiggleMouseInBackground(dur, step=step, slp=slp))
                    if ENABLE_DEBUG:
                        print_with_color(f"Scheduled background jiggle for {dur}s", MAGENTA)

        except Exception as e:
            print(f"BACKGROUND_JIGGLE_MOUSE error: {e}")
        return True


    if line.startswith("MOUSE_CLICK"):
        try:
            arg = get_arg(line)
            if arg:
                btn = arg.upper()
                if btn == "LEFT":
                    mouse.click(Mouse.LEFT_BUTTON)
                elif btn == "RIGHT":
                    mouse.click(Mouse.RIGHT_BUTTON)
                elif btn == "MIDDLE":
                    mouse.click(Mouse.MIDDLE_BUTTON)
        except Exception as e:
            print(f"MOUSE_CLICK error: {e}")
        return True

    if line.startswith("MOUSE_PRESS"):
        try:
            arg = get_arg(line)
            if arg:
                btn = arg.upper()
                if btn == "LEFT":
                    mouse.press(Mouse.LEFT_BUTTON)
                elif btn == "RIGHT":
                    mouse.press(Mouse.RIGHT_BUTTON)
                elif btn == "MIDDLE":
                    mouse.press(Mouse.MIDDLE_BUTTON)
        except Exception as e:
            print(f"MOUSE_PRESS error: {e}")
        return True

    if line.startswith("MOUSE_RELEASE"):
        try:
            arg = get_arg(line)
            if arg:
                btn = arg.upper()
                if btn == "LEFT":
                    mouse.release(Mouse.LEFT_BUTTON)
                elif btn == "RIGHT":
                    mouse.release(Mouse.RIGHT_BUTTON)
                elif btn == "MIDDLE":
                    mouse.release(Mouse.MIDDLE_BUTTON)
        except Exception as e:
            print(f"MOUSE_RELEASE error: {e}")
        return True

    if line.startswith("MOUSE_MOVE"):
        try:
            arg = get_arg(line)
            if arg:
                args = arg.replace(",", "").split()
                if len(args) >= 2:
                    x, y = int(args[0]), int(args[1])
                    mouse.move(x=x, y=y)
        except Exception as e:
            print(f"MOUSE_MOVE error: {e}")
        return True

    if line.startswith("MOUSE_SCROLL"):
        try:
            arg = get_arg(line)
            if arg:
                w = int(arg.split()[0])
                mouse.move(wheel=w)
        except Exception as e:
            print(f"MOUSE_SCROLL error: {e}")
        return True

    # HOLD / RELEASE
    if line.startswith("HOLD"):
        arg = get_arg(line)
        if arg:
            key = replaceAll(arg.strip(), 1, 1, 0).upper()
            for k in key.split():
                kc = DUCKYKEYS.get(k, None)
                if kc:
                    kbd.press(kc)
                else:
                    print_with_color(f"Unknown key to HOLD: <{k}>", BRIGHT_RED)
            sleep(0.01)

        return True

    if line.startswith("RELEASE"):
        if line.upper() == "RELEASE_ALL":
            kbd.release_all()
            return True
        arg = get_arg(line)
        if arg:
            key = replaceAll(arg.strip(), 1, 1, 0).upper()
            for k in key.split():
                kc = DUCKYKEYS.get(k, None)
                if kc:
                    kbd.release(kc)
                else:
                    print_with_color(f"Unknown key to RELEASE: <{k}>", BRIGHT_RED)
        return True

    # DELAY
    if line.startswith("DELAY"):
        arg = get_arg(line)
        if arg:
            d = replaceAll(arg.strip())
            d = evaluateExpression(d)
            try:
                sleep(int(d) / 1000.0)
            except Exception as e:
                print(f"DELAY error: {e}")
        return True

    # RANDOM_DELAY min max
    if line.upper().startswith("RANDOM_DELAY"):
        arg = get_arg(line)
        if arg:
            parts = arg.strip().split()
            if len(parts) >= 2:
                try:
                    min_ms = int(parts[0])
                    max_ms = int(parts[1])
                    rdelay = randint(min_ms, max_ms) / 1000.0
                    sleep(rdelay)
                except Exception as e:
                    print(f"RANDOM_DELAY error: {e}")
            else:
                print_with_color("RANDOM_DELAY requires two arguments: min and max (ms)", BRIGHT_RED)
        return True

    # STRING, STRINGLN
    if line.startswith("STRINGLN"):
        arg = get_arg(line)
        if arg:
            v = replaceAll(arg)
            sendString(v)
        kbd.press(Keycode.ENTER)
        kbd.release(Keycode.ENTER)
        return True

    if line.startswith("STRING"):
        arg = get_arg(line)
        if arg:
            v = replaceAll(arg)
            sendString(v)
        return True

    # PRINT
    if line.startswith("PRINT"):
        arg = get_arg(line)
        if arg:
            print(replaceAll(arg))
        return True

    # IMPORT
    if line.startswith("IMPORT"):
        arg = get_arg(line)
        if arg:
            fname = replaceAll(arg.strip().replace("'", "").replace('"', ''), 1, 1, 0)
            if fname:
                try:
                    with open(fname, "r") as f:
                        imported_lines = f.readlines()
                    new_ctx = ExecContext(imported_lines, start_index=0, is_function=True)
                    context_stack.append(new_ctx)
                except OSError:
                    print_with_color(f'Unable to open import file "{fname}"', RED)

        return True

    # DEFAULT_DELAY / DEFAULTDELAY
    if line.startswith("DEFAULT_DELAY") or line.startswith("DEFAULT_DELAY"):
        arg = get_arg(line)
        if arg:
            d = replaceAll(arg.strip())
            try:
                defaultDelay = int(d)
            except:
                pass
        return True

    # LED control
    if line.startswith("LED_ON") or line.startswith("LED_R") or line.startswith("LED_G"):
        if _led is not None:
            _led.value = 1
        else:
            print_with_color("LED not initialised", BRIGHT_RED)
        return True

    if line.startswith("LED_OFF"):
        if _led is not None:
            _led.value = 0
        else:
            print_with_color("LED not initialised", BRIGHT_RED)
        return True

    # WAIT_FOR cmdss
    if line.upper().startswith("WAIT_FOR_CAPS_ON"):
        while not kbd.led_on(Keyboard.LED_CAPS_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_CAPS_OFF"):
        while kbd.led_on(Keyboard.LED_CAPS_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_CAPS_CHANGE"):
        initial = kbd.led_on(Keyboard.LED_CAPS_LOCK)
        while kbd.led_on(Keyboard.LED_CAPS_LOCK) == initial:
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_NUM_ON"):
        while not kbd.led_on(Keyboard.LED_NUM_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_NUM_OFF"):
        while kbd.led_on(Keyboard.LED_NUM_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_NUM_CHANGE"):
        initial = kbd.led_on(Keyboard.LED_NUM_LOCK)
        while kbd.led_on(Keyboard.LED_NUM_LOCK) == initial:
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_SCROLL_ON"):
        while not kbd.led_on(Keyboard.LED_SCROLL_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_SCROLL_OFF"):
        while kbd.led_on(Keyboard.LED_SCROLL_LOCK):
            sleep(0.01)
        return True

    if line.upper().startswith("WAIT_FOR_SCROLL_CHANGE"):
        initial = kbd.led_on(Keyboard.LED_SCROLL_LOCK)
        while kbd.led_on(Keyboard.LED_SCROLL_LOCK) == initial:
            sleep(0.01)
        return True 

    # VOILA CREME DE LA CREME | ATTACK MODES 
    # ATTACKMODE
    if line.upper().startswith("ATTACKMODE"):
        arg = get_arg(line).strip().upper()
        if arg == "HID":
            mode_byte = 1
        elif arg in ("STORAGE", "HID STORAGE", "STORAGE HID"):
            mode_byte = 3
        else:
            print_with_color(f"Invalid ATTACKMODE: {arg}. Use HID or HID STORAGE", BRIGHT_RED)
            return True

        next_line = ctx.i + 1
        try:
            nvm = microcontroller.nvm
            nvm[0] = 0                  # consumed flag = 0 (fresh resume)
            nvm[1] = mode_byte
            nvm[2] = next_line & 0xFF   # line LSB
            nvm[3] = (next_line >> 8) & 0xFF
            print_with_color(f"ATTACKMODE {arg} line {next_line} – resetting (NVM)", BRIGHT_GREEN)
        except Exception as e:
            print_with_color(f"NVM write failed: {e}", BRIGHT_RED)
            return True

        microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
        microcontroller.reset()

    # RESET and NEXT-RESET MODE commands
    if line == "RESET":
        if ENABLE_DEBUG:
            print_with_color("Command: RESET (normal mode)", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
        microcontroller.reset()
        return True

    if line == "RESET_SAFE":
        if ENABLE_DEBUG:
            print_with_color("Command: RESET_SAFE (safe mode)", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
        microcontroller.reset()
        return True

    if line == "RESET_UF2":
        if ENABLE_DEBUG:
            print_with_color("Command: RESET_UF2 (UF2 bootloader)", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.UF2)
        microcontroller.reset()
        return True

    if line == "SET_RESET_NORMAL":
        if ENABLE_DEBUG:
            print_with_color("Command: SET_RESET_NORMAL", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
        return True

    if line == "SET_RESET_SAFE":
        if ENABLE_DEBUG:
            print_with_color("Command: SET_RESET_SAFE", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
        return True

    if line == "SET_RESET_UF2":
        if ENABLE_DEBUG:
            print_with_color("Command: SET_RESET_UF2", BRIGHT_GREEN)
        microcontroller.on_next_reset(microcontroller.RunMode.UF2)
        return True

    if line == "ENABLE_DEBUG":
        ENABLE_DEBUG = True

    if line == "DISABLE_DEBUG":
        ENABLE_DEBUG = False

    if line == "FORMAT":
        if ENABLE_DEBUG:
            print_with_color("Command: FORMAT (erasing filesystem)", BRIGHT_RED)

        print("FORMAT: Wiping all files and rebooting…")
        try:
            import storage
            storage.erase_filesystem()
        except Exception as e:
            print_with_color("FORMAT failed: {}".format(repr(e)), BRIGHT_RED)
        return True

    # FILE EXFILTRATION
    # if line.upper().startswith("FILE_EXFILTRATION"):
    #     parts = line.split()
    #     if len(parts) < 3:
    #         print_with_color("FILE_EXFILTRATION <filename> <byte_count|0> [bit_time_ms] [LED] [STOP_LED]", BRIGHT_RED)
    #         return True
    #
    #     fname = parts[1]
    #     try:
    #         bcount = int(parts[2])
    #     except ValueError:
    #         print_with_color("Invalid byte count", BRIGHT_RED)
    #         return True
    #     bt = 200
    #     led = 'SCROLLLOCK'
    #     stop_led = None
    #
    #     if len(parts) >= 4:
    #         try:
    #             bt = int(parts[3])
    #         except ValueError:
    #             pass
    #     if len(parts) >= 5:
    #         led = parts[4].upper()
    #     if len(parts) >= 6:
    #         stop_led = parts[5].upper()
    #
    #     file_exfil_receive(fname, bcount, bt, led, stop_led)
    #     return True


    runScriptLine(line)
    return True

# Main interpreter (iterative, context stack)
context_stack = []
global_strip = 1


def runScript(QuackScriptPath, start_line=0):
    global defaultDelay, defines, variables, KeyboardLayout, Keycode, layout, context_stack, functions, global_strip
    line = ""
    restart = True
    try:
        print(f'[RUN] Injecting Keystrokes from "{QuackScriptPath}" ')
        while restart:
            restart = False
            with open(QuackScriptPath, "r", encoding='utf-8') as f:
                lines = f.readlines()

            ctx = ExecContext(lines, start_index=start_line, is_function=False)
            context_stack = [ctx]

            while context_stack:
                ctx = context_stack[-1]
                if ctx.i >= len(ctx.lines):
                    context_stack.pop()
                    if context_stack:
                        parent = context_stack[-1]
                        if ctx.is_function:
                            parent.i += 1
                    continue

                raw_line = ctx.lines[ctx.i]
                line = raw_line.strip()
                if not line:
                    ctx.i += 1
                    continue


                if ENABLE_DEBUG:
                    print_with_color(f"[line_index={ctx.i:04d}] {line}", GOLD)


                # SELECT_LAYOUT, REPEAT, RESTART, STOP
                if line.startswith("SELECT_LAYOUT"):
                    parts = line.split()
                    if len(parts) >= 2:
                        new_layout, new_kc = SelectLayout(parts[1])
                        if new_layout and new_kc:
                            KeyboardLayout = new_layout
                            Keycode = new_kc
                            layout = KeyboardLayout(kbd)
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if line.startswith("REPEAT"):
                    line_up = replaceAll(line).upper()
                    line_up = line_up.replace(" =", "=").replace("= ", "=")
                    repeat_ls = line_up.split()
                    line_idx = time_idx = -1
                    for idx, val in enumerate(repeat_ls):
                        if val.startswith("LINES="):
                            line_idx = idx
                        elif val.startswith("TIMES="):
                            time_idx = idx
                    if line_idx >= 0 and time_idx >= 0 and len(ctx.previousLines) > 0:
                        try:
                            lines_val = int(repeat_ls[line_idx].split("=")[1])
                            times_val = int(repeat_ls[time_idx].split("=")[1])
                            to_repeat = ctx.previousLines[-lines_val:]
                            for _ in range(times_val):
                                temp_ctx = ExecContext(to_repeat)
                                while temp_ctx.i < len(to_repeat):
                                    l = to_repeat[temp_ctx.i].strip()
                                    if l:
                                        execute_line(l, temp_ctx)
                                    temp_ctx.i += 1
                                    _sleep_jitter(defaultDelay)

                        except Exception as e:
                            print(f"REPEAT error: {e}")
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)

                    continue

                if line.startswith("RESTART_PAYLOAD"):
                    restart = True
                    break
                if line.startswith("STOP_PAYLOAD"):
                    restart = False
                    break

                # BLOCK COMMENTS (REM_BLOCK, /* ... */)
                if line.startswith("REM_BLOCK") or line.startswith("/*"):
                    if line.startswith("REM_BLOCK"):
                        end_marker = "END_REM"
                    else:
                        end_marker = "*/"
                    ctx.i += 1
                    while ctx.i < len(ctx.lines):
                        l = ctx.lines[ctx.i].strip()
                        if l.startswith(end_marker) or l.endswith(end_marker):
                            break
                        ctx.i += 1
                    ctx.i += 1
                    continue

                if line.startswith("REM") or line.startswith("//"):
                    ctx.i += 1
                    continue

                if line == "ENABLE_STRIP":
                    global global_strip
                    global_strip = 1
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if line == "DISABLE_STRIP":
                    global global_strip
                    global_strip = 0
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                # MULTI-LINE STRINGS (STRING_BLOCK, STRINGLN_BLOCK)
                if line.startswith("STRINGLN_BLOCK") or line.startswith("STRING_BLOCK"):
                    is_ln = line.startswith("STRINGLN_BLOCK")
                    ctx.i += 1
                    enable_strip = global_strip
                    while ctx.i < len(ctx.lines):
                        raw = ctx.lines[ctx.i]
                        l = raw.strip()
                        if l.startswith("END_STRINGLN") or (not is_ln and l.startswith("END_STRING")):
                            break
                        if l.startswith("DISABLE_STRIP"):
                            enable_strip = 0
                            ctx.i += 1
                            continue
                        if l.startswith("ENABLE_STRIP"):
                            enable_strip = 1
                            ctx.i += 1
                            continue

                        text = raw if not enable_strip else l
                        text = replaceAll(text, 1, 1, 1)
                        sendString(text)
                        if is_ln:
                            kbd.press(Keycode.ENTER)
                            kbd.release(Keycode.ENTER)
                        ctx.i += 1
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                # FUNCTION definition
                if line.upper().startswith("FUNCTION"):
                    parts = line.split()
                    if len(parts) >= 2:
                        func_name = parts[1].strip()
                        if func_name.endswith("()"):
                            func_name = func_name[:-2]
                        func_lines = []
                        ctx.i += 1
                        while ctx.i < len(ctx.lines):
                            l = ctx.lines[ctx.i].rstrip("\n")
                            if l.strip().upper().startswith("END_FUNCTION"):
                                break
                            func_lines.append(l)
                            ctx.i += 1
                        functions[func_name] = func_lines
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                # IF / ELSE / END_IF 
                if line.upper().startswith("IF"):
                    ctx.branch_taken_stack.append(False)
                    condition = _getIfCondition(line)
                    condition = replaceAll(condition)
                    result = evaluateExpression(condition)
                    if result == True:
                        ctx.branch_taken_stack[-1] = True
                        if ctx.skip_depth > 0:
                            ctx.skip_depth += 1
                    else:
                        if ctx.skip_depth == 0:
                            ctx.skip_depth = 1
                        else:
                            ctx.skip_depth += 1
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if line.upper().startswith("ELSE"):
                    upper = line.upper()
                    if upper.startswith("ELSE IF") or upper.startswith("ELSEIF"):
                        idx = upper.find("IF")
                        cond_part = line[idx+2:].strip()
                        condition = replaceAll(cond_part)
                        result = evaluateExpression(condition)
                        if ctx.branch_taken_stack[-1]:
                            ctx.skip_depth += 1
                        else:
                            if result:
                                ctx.branch_taken_stack[-1] = True
                                if ctx.skip_depth > 0:
                                    ctx.skip_depth -= 1
                            else:
                                pass
                    else:
                        if ctx.branch_taken_stack[-1]:
                            ctx.skip_depth += 1
                        else:
                            ctx.branch_taken_stack[-1] = True
                            if ctx.skip_depth > 0:
                                ctx.skip_depth -= 1
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if line.upper().startswith("END_IF"):
                    if ctx.skip_depth > 0:
                        ctx.skip_depth -= 1
                    if ctx.branch_taken_stack:
                        ctx.branch_taken_stack.pop()
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                # WHILE / END_WHILE
                if line.upper().startswith("WHILE"):
                    condition_str = line[5:].strip()
                    cond_replaced = replaceAll(condition_str)
                    if evaluateExpression(cond_replaced):
                        ctx.loop_stack.append((condition_str, ctx.i, ctx.skip_depth, ctx.branch_taken_stack.copy()))
                        ctx.i += 1
                    else:
                        depth = 1
                        ctx.i += 1
                        while ctx.i < len(ctx.lines):
                            l = ctx.lines[ctx.i].strip()
                            if l.upper().startswith("WHILE"):
                                depth += 1
                            elif l.upper().startswith("END_WHILE"):
                                depth -= 1
                                if depth == 0:
                                    ctx.i += 1
                                    break
                            ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if line.upper().startswith("END_WHILE"):
                    if ctx.loop_stack:
                        cond_str, start_idx, saved_skip, saved_branch = ctx.loop_stack[-1]
                        cond_replaced = replaceAll(cond_str)
                        if evaluateExpression(cond_replaced):
                            ctx.skip_depth = saved_skip
                            ctx.branch_taken_stack = saved_branch.copy()
                            ctx.i = start_idx + 1
                        else:
                            ctx.loop_stack.pop()
                            ctx.i += 1
                    else:
                        ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                if ctx.skip_depth > 0:
                    ctx.i += 1
                    _sleep_jitter(defaultDelay)
                    continue

                # Function call
                func_name = line.rstrip("()")
                if func_name in functions:
                    if ENABLE_DEBUG:
                        print_with_color(f"Calling function: {func_name}", GOLD)
                    new_ctx = ExecContext(functions[func_name], start_index=0, is_function=True)
                    context_stack.append(new_ctx)
                    continue

                # Execute normal command
                print_with_color(">>> Calling execute_line", BRIGHT_YELLOW)
                execute_line(line, ctx)
                ctx.previousLines.append(raw_line.rstrip("\n"))
                ctx.i += 1
                _sleep_jitter(defaultDelay)

    except OSError:
        print_with_color(f'Unable to open file "{QuackScriptPath}"', RED)

    except Exception as e:
        gc.collect()
        print_with_color("\n=== OVERQUACK CRASH ===", RED)
        print_with_color(f"FREE RAM: {gc.mem_free()/1000}KB  ALLOC RAM: {gc.mem_alloc()/1000}KB", RED)
        try:
            print_with_color(f"Last payload line: {line}", RED)
        except NameError:
            print_with_color("Last payload line: (unknown)", RED)


        print_with_color(f"Exception type: {type(e).__name__}", RED)
        print_with_color(f"Exception args: {e.args}", RED)
        print_with_color("--- FULL EXCEPTION ---", RED)
        print(f"{GOLD}", end="")
        traceback.print_exception(e)
        print(f"{RESET}", end="")
        print_with_color("--- END TRACEBACK ---", RED)


    variables = {"$_RANDOM_MIN": RANDOM_DEFAULT_MIN, "$_RANDOM_MAX": RANDOM_DEFAULT_MAX}
    defines = {}
    functions = {}
    context_stack = []
    defaultDelay = 0
    print(f"[{QuackScriptPath.upper()}_COMPLETED] 200")

# LED blink and mode switch
async def BlinkLedPico(led):
    led_state = False
    initial_status = getProgrammingStatus()
    print_with_color(f"[BLINK] delay_intervale = [{BLINK_MIN_MS}, {BLINK_MAX_MS}] ms", BRIGHT_YELLOW)
    while True:
        if config['BOARD']['enable_auto_switch_mode'] in [True, "True", "true", 1, 1] and initial_status != getProgrammingStatus():
            print_with_color("* [RESET] Changing OverQuack MODE ", BRIGHT_MAGENTA)
            microcontroller.reset()

        seconds = randint(BLINK_MIN_MS, BLINK_MAX_MS) / 1000
        if led_state:
            led.value = 1
            await asyncio.sleep(seconds)
            led_state = False
        else:
            led.value = 0
            await asyncio.sleep(seconds)
            led_state = True

def getProgrammingStatus():
    global oneshot, progStatusPin
    pin_num = config['BOARD']['controll_mode_pin']
    if not isinstance(pin_num, int) or not hasattr(board, f"GP{pin_num}"):
        print(f"Invalid pin, defaulting to GP{DEFAULT_PIN_NUM}")
        pin_num = DEFAULT_PIN_NUM
    pin_name = f"GP{pin_num}"
    if oneshot:
        progStatusPin = DigitalInOut(getattr(board, pin_name))
        oneshot = False
    progStatusPin.switch_to_input(pull=Pull.UP)
    return progStatusPin.value
