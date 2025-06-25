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

import asyncio
import gc
import re
from random import choice, randint
from time import monotonic, sleep

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from board import *
import board
from digitalio import DigitalInOut, Pull
from microcontroller import reset
from usb_hid import devices

def _Ap_Info(elem):
    import wifi 


    if elem == 'ssid' :
        return config['AP']['ssid']
    elif elem == 'password' :
        return config['AP']['password']
    elif elem == 'bssid':
        return ":".join("{:02X}".format(b) for b in wifi.radio.mac_address)
    else :
        return ""


def _capsOn():
    if kbd.led_on(Keyboard.LED_CAPS_LOCK):
        return 1
    else:
        return 0

def _numOn():
    if kbd.led_on(Keyboard.LED_NUM_LOCK):
        return 1
    else:
        return 0

def _scrollOn():
    if kbd.led_on(Keyboard.LED_SCROLL_LOCK):
        return 1
    else:
        return 0

duckyKeys = {
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

duckyConsumerKeys = {
    'MK_VOLUP': ConsumerControlCode.VOLUME_INCREMENT, 'MK_VOLDOWN': ConsumerControlCode.VOLUME_DECREMENT, 'MK_MUTE': ConsumerControlCode.MUTE,
    'MK_NEXT': ConsumerControlCode.SCAN_NEXT_TRACK, 'MK_PREV': ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    'MK_PP': ConsumerControlCode.PLAY_PAUSE, 'MK_STOP': ConsumerControlCode.STOP
}

LAYOUTS_MAP = {
    "US_DVO"  : ("keyboard_layouts.keyboard_layout_us_dvo", "adafruit_hid.keycode"),  
    "US"      : ("adafruit_hid.keyboard_layout_us", "adafruit_hid.keycode"),
    "MAC_FR"  : ("keyboard_layouts.keyboard_layout_mac_fr", "keycodes.keycode_mac_fr"),
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
}


variables = {"$_RANDOM_MIN": 0, "$_RANDOM_MAX": 65535}
internalVariables = {   "$_CAPSLOCK_ON": _capsOn,
                        "$_NUMLOCK_ON": _numOn, 
                        "$_SCROLLLOCK_ON": _scrollOn,
                        "$_BSSID": lambda: _Ap_Info('bssid'),
                        "$_SSID": lambda: _Ap_Info('ssid'),
                        "$_PASSWD": lambda: _Ap_Info('password'),
                     }
rng_variables = ["$_RANDOM_NUMBER", "$_RANDOM_LOWERCASE_LETTER", "$_RANDOM_UPPERCASE_LETTER", 
                 "$_RANDOM_LETTER", "$_RANDOM_SPECIAL", "$_RANDOM_CHAR"]
letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
specialChars = "!@#$%^&*()"

defines = {}
functions = {}
defaultDelay = 0
DEFAULT_PIN_NUM = 5 
oneshot = True 
progStatusPin = None

kbd = Keyboard(devices)
consumerControl = ConsumerControl(devices)
layout = KeyboardLayout(kbd)
mouse = Mouse(devices)
# i should added : MOUSE jiggler
PROBLEM_CODE = "ERROR404"

RESET       = "\033[0m"
BLACK       = "\033[30m"
RED         = "\033[31m"
GREEN       = "\033[32m"
YELLOW      = "\033[33m"
BLUE        = "\033[34m"
MAGENTA     = "\033[35m"
CYAN        = "\033[36m"
BRIGHT_BLACK     = "\033[90m"
BRIGHT_RED       = "\033[91m"
BRIGHT_GREEN     = "\033[92m"
BRIGHT_YELLOW    = "\033[93m"
BRIGHT_BLUE      = "\033[94m"
BRIGHT_MAGENTA   = "\033[95m"
BRIGHT_CYAN      = "\033[96m"
WHITE            = "\033[37m"
GOLD       = "\033[38;2;255;215;0m"
SILVER     = "\033[38;2;192;192;192m"
BRONZE     = "\033[38;2;205;127;50m"
PINK       = "\033[38;2;255;105;180m"
STEEL_BLUE = "\033[38;2;70;130;180m"


class IF:
    def __init__(self, condition, codeIter):
        codeIter = TrackIterator(codeIter)

        self.condition = condition
        self.codeIter = codeIter.remaining()
        self.lastIfResult = None


    def _exitIf(self):
        _depth = 0
        for line in self.codeIter:
            line = self.codeIter.pop(0)
            line = line.strip()
            if line.upper().startswith("END_IF"):
                _depth -= 1
            elif line.upper().startswith("IF"):
                _depth += 1
            if _depth < 0:
                break
        return(self.codeIter)

    def runIf(self):
        if isinstance(self.condition, str):
            self.lastIfResult = evaluateExpression(self.condition)
        elif isinstance(self.condition, bool):
            self.lastIfResult = self.condition
        else:
            raise ValueError("Invalid condition type BROTHER")

        depth = 0
        for line in self.codeIter:
            line = self.codeIter.pop(0)
            line = line.strip()
            if line == "":
                continue
            # print(line)

            if line.startswith("IF"):
                depth += 1
            elif line.startswith("END_IF"):
                if depth == 0:
                    return(self.codeIter, -1)
                depth -=1

            elif line.startswith("ELSE") and depth == 0:
                # print(f"ELSE LINE {line}, lastIfResult: {self.lastIfResult}")
                if self.lastIfResult is False:
                    line = line[4:].strip()  # Remove 'ELSE' and strip whitespace
                    if line.startswith("IF"):
                        nestedCondition = _getIfCondition(line)
                        # print(f"nested IF {nestedCondition}")
                        self.codeIter, self.lastIfResult = IF(nestedCondition, self.codeIter).runIf()
                        if self.lastIfResult == -1 or self.lastIfResult == True:
                            # print(f"self.lastIfResult {self.lastIfResult}")
                            return(self.codeIter, True)
                    else:
                        # codeIter = TrackIterator(self.codeIter)
                        return IF(True, self.codeIter).runIf()                        #< Regular ELSE block
                else:
                    self._exitIf()
                    break

                # Process regular lines
            elif self.lastIfResult:
                # print(f"running line {line}")
                self.codeIter = list(parseLine(line, self.codeIter))
        # print("end of if")
        return(self.codeIter, self.lastIfResult)

class TrackIterator:
    def __init__(self, iterable):
        self._it = iter(iterable)
        self.consumed = []

    def __iter__(self):
        return self

    def __next__(self):
        val = next(self._it)
        self.consumed.append(val)
        return val

    def remaining(self):
        # Return a list of remaining items WITHOUT consuming the iterator
        # We convert to list but keep a buffer for next calls
        remaining_items = list(self._it)
        self._it = iter(remaining_items)
        return remaining_items

    def all_items(self):
        return self.consumed + self.remaining()



def print_with_color(STRING, COLOR=WHITE, sep=" ", end="\n"):
    print(f"{COLOR}{STRING}{RESET}", sep=sep, end=end)

def LoadJsonConf(json_file="config.json"):
    import json 

    config = {}
    try:
        with open(json_file, "r") as f:
            config = json.load(f)

    except (OSError, ValueError) as e:
        print_with_color(f"ERR: {e}", RED)
        config['BOARD'] = {}
        config['BOARD']['enable_auto_reload'] = False
        config['BOARD']['enable_auto_switch_mode'] = True
        config['BOARD']['controll_mode_pin'] = 5

        config['AP'] = {}
        config['AP']["ssid"] = "OverQuackError"
        config['AP']["password"] = "NeonBeonError"
        config['AP']["channel"] = 6
        config['AP']["ip_address"] = "192.168.4.1"
        config['AP']["ports"] = [80, 8000, 8080]

    return config 


config = LoadJsonConf()
def _getIfCondition(line):
    return str(line.split("IF")[1].strip())

def _isCodeBlock(line):
    line = line.upper().strip()
    if line.startswith("IF") or line.startswith("WHILE"):
        return True
    return False

def _getCodeBlock(linesIter):
    """Returns the code block starting at the given line."""
    print(f'[_getCodeBlock] : inside')

    code = []
    depth = 1
    for line in linesIter:
        line = line.strip()
        print(f'[_getCodeBlock] {line}')
        if line.upper().startswith("END_"):
            print(f'[_getCodeBlock] you found THE END_')
            depth -= 1
        elif _isCodeBlock(line):
            print(f'[_getCodeBlock] you found THE SUSY')
            depth += 1
        if depth <= 0:
            print(f'[_getCodeBlock] DEPTH = 0')
            break
        code.append(line)
        print(f'[_getCodeBlock] line was added to code : {code}')

    return code


def SelectLayout(layout_key):
    layout_key = layout_key.upper()
    layout_entry = LAYOUTS_MAP.get(layout_key)
    print_with_color(f"LAYOUT_KEY: {layout_key}, LAYOUT_ENTERY: {layout_entry}", STEEL_BLUE)
    if not layout_entry:
        print(f"[INVALID_LAYOUT] {layout_key}")
        return None, None

    # import layout module
    layout_module_path = layout_entry[0]
    layout_module = __import__(layout_module_path)
    for part in layout_module_path.split(".")[1:]:
        layout_module = getattr(layout_module, part)

    # import keycode module
    keycode_module_path = layout_entry[1]
    keycode_module = __import__(keycode_module_path)
    for part in keycode_module_path.split(".")[1:]:
        keycode_module = getattr(keycode_module, part)

    # access class objects
    KeyboardLayoutClass = getattr(layout_module, "KeyboardLayout")
    KeycodeClass = getattr(keycode_module, "Keycode")

    return KeyboardLayoutClass, KeycodeClass



# here is where is support for operation because of eval nice 
def evaluateExpression(expression):
    """Evaluates an expression with variables and returns the result."""
    # Ensure the input is a string FOR EVAL
    expression = str(expression)   

    print_with_color(f'[1_EVALUATE_EXPRESION] BEGIN, expression: "{expression}"', YELLOW)


    expression = expression.replace("^", "**")     #< Replace ^ with ** for exponentiation
    expression = expression.replace("&&", "and")
    expression = expression.replace("||", "or")
    result = PROBLEM_CODE
    try :
        result = eval(expression)
        print_with_color(f'[2_EVALUATE_EXPRESION] expression: "{expression}", result "{result}"', YELLOW)
    except Exception :
        print_with_color(f"[EVALUATE_EXPRESION_ERRO] INVALID EXPRESSION: {expression}, RESULT = {result}", RED)

    return result 

# def deepcopy(List):
#     return(List[:])

def convertLine(line):
    commands = []
    # print(line)
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyKeys.get(key, None)
        command_consumer_keycode = duckyConsumerKeys.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            commands.append(command_keycode)
        elif command_consumer_keycode is not None:
            # if it exists in the list, use it
            commands.append(1000+command_consumer_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            commands.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    # print(commands)
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

#Send String via HID Keyboard
def sendString(line):
    layout.write(line)

def replaceDefines(line):
    for define, value in defines.items():
        line = line.replace(define, str(value))
    return line


def replaceVariables(line):
    for var in variables:
        line = line.replace(var, str(variables[var]))
    for var in internalVariables:
        line = line.replace(var, str(internalVariables[var]()))
    return line

def replaceRandomVariables(expression):

    if not any(var in expression for var in rng_variables):
        print_with_color(f"[RANDOM_DEBUG] Expression \"{expression}\" not in \"RNG_VARIABLES_LIST\" = {BetterListOutput(rng_variables)}", BLUE)
        return expression


    # Find all placeholders FOR $_RANDOM_[A-Z]_
    Random_matches, expression_edited, original_number = extract_random_placeholders(expression) 

    print_with_color(f"\[DEBUG_Random_matches] {Random_matches}", YELLOW)

    
    rand_value = None 

    if Random_matches :
        # Loop through matches and print details
        for random_value in Random_matches:

            rand_type = random_value[0]
            count = int(random_value[1])
            # Generate random value based on type
            if rand_type == "$_RANDOM_NUMBER":
                rand_value = ''.join(choice(RandomizeData(numbers)) for _ in range(count))

            elif rand_type == "$_RANDOM_LOWERCASE_LETTER":
                rand_value = ''.join(choice(RandomizeData(letters)) for _ in range(count))

            elif rand_type == "$_RANDOM_UPPERCASE_LETTER":
                rand_value = ''.join(choice(RandomizeData(letters.upper())) for _ in range(count))

            elif rand_type == "$_RANDOM_LETTER":
                rand_value = ''.join(choice(RandomizeData(letters + letters.upper()) ) for _ in range(count))

            elif rand_type == "$_RANDOM_SPECIAL":
                rand_value = ''.join(choice(RandomizeData(specialChars)) for _ in range(count))

            elif rand_type == "$_RANDOM_CHAR":
                rand_value = ''.join(choice(RandomizeData(letters + letters.upper() + numbers + specialChars)) for _ in range(count))

            # Replace the placeholder in expression
            if expression_edited:
                count = original_number


            placeholder = f"{rand_type}:{count}"

            print_with_color(f"[RANDOM_REPLACING] Replacing '{placeholder}' with '{rand_value}' in expression '{expression}'", GREEN)

            expression = expression.replace(placeholder, rand_value)
            print_with_color(f"[RANDOM_REPLACING_UPDATE] Updated expression: {expression}", GREEN)
            
            try : 
                rand_value = int(rand_value)
                print_with_color(f"[DEBUG_RNG] next_Value_is_int = {rand_value} nice", MAGENTA)
            except ValueError:
                print_with_color(f"[DEBUG_RNG] value = {rand_value}", RED)

    return expression

def replaceAll(line, enable_replace_vars=1, enable_replace_defines=1, enable_replace_randoms=1):
    if enable_replace_defines:
        line = replaceDefines(line)
    if enable_replace_vars:
        line = replaceVariables(line)
    if enable_replace_randoms:
        line  = replaceRandomVariables(line)

    return line

def random_output(line, randomized_output=numbers):
    ls = line.split()

    if len(ls) < 2 :
        print(f"[DEBUG_RANDOMIZATION_SYNTAX_ERROR]: Empty Value for {ls[0]}")

    else :
        times = 0
        try :
            times = int(ls[1])
            print(f'[DEBUG_RANDOMIZATION]: Writing "{ls[0]}" {times} times')
        except ValueError :
            print(f"[ERROR_RANDOMIZATION]: Value of \"{ls[0]}\" is not an INT: {ls[1]}")
            return
        except Exception as e :
            print(f"[ERROR_RANDOMIZATION]: {e}")
            return

        rng = ""
        for _ in range(times):
            rng += choice(randomized_output)

        sendString(rng)

def extract_random_placeholders(text):
    """
    Extracts all $_RANDOM_<NAME> or $_RANDOM_<NAME>:<NUMBER> patterns.
    If number is not provided or not integer , defaults to "0".
    Returns:
        List of tuples: [(placeholder_name, number_as_string), ...]
        Example: [("$_RANDOM_NAME", "10"), ("$_RANDOM_AGE", "0")]
    """
    expression_edited = False
    pattern = re.compile(r"(\$_RANDOM_[A-Z_]+)(?::(-?\d+))?")
    print_with_color(f"[EXTRACT_RADNOM] text : {text}", CYAN)

    matches = []
    pos = 0
    
    Original_number = None
    number = None
    while True:
        match = pattern.search(text, pos)
        print_with_color(f"[EXTRACT_RADNOM] bool match : {match}", YELLOW)
        if not match:
            break

        name = match.group(1)
        number = match.group(2)
        Original_number = number
        print_with_color(f"[EXTRACT_RADNOM] name : {name}, number : {number}", RED)

        if number is None:
            number = "1"
        else:
            try:
                number = str(max(int(number), 1))
            except ValueError:
                number = "1"  # fallback in case of unexpected input

        matches.append((name, number))
        pos = match.end()

    if number == "1" :
        expression_edited = True

    print_with_color(f"[EXTRACT_RADNOM] matches: {matches}", RED)
    return matches, expression_edited, Original_number


def RandomizeData(data):
    lst = list(str(data))
    for i in range(len(lst) - 1, 0, -1):
        j = randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)


def BetterListOutput(ls):
    return "[\n\t" + ",\n\t".join(
        str(i).strip() for i in ls if str(i).strip()
    ) + "\n]"

def JiggleMouse(jiggle_delay, step=1, slp=0.5):
    print(f"jiggle_delay: {jiggle_delay}, step: {step}")
    start_time = monotonic()
    while (monotonic() - start_time) < jiggle_delay:
        print(f"Moving mouse right {step} pixels")
        mouse.move(x=step, y=0)
        sleep(slp)

        print(f"Moving mouse left {step} pixels")
        mouse.move(x=-step, y=0)
        sleep(slp)
        
async def JiggleMouseInBackground(jiggle_delay, step=1, slp=0.5, INF=0):
    print_with_color(f"[BACKGROUND_JIGGLE_MOUSE]: jiggle_delay={jiggle_delay}, sleep={slp}, pixle_jiggle_intervale=[{-step},{step}]", BRIGHT_MAGENTA)

    if INF:
        while 1:
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)

            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)

    else:
        start_time = monotonic()
        while (monotonic() - start_time) < jiggle_delay or INF:
            print_with_color(f"Moving mouse right {step} pixels", BRIGHT_MAGENTA)
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)

            print_with_color(f"Moving mouse left {step} pixels", BRIGHT_MAGENTA)
            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)


#main code handler
def parseLine(line, script_lines):
    global defaultDelay, variables, functions, defines
    
    line = line.strip()
    replaced_element_rng = str(
        randint(
            int(variables.get("$_RANDOM_MIN", 0)),
            int(variables.get("$_RANDOM_MAX", 65535))
        )
    )

    line = line.replace("$_RANDOM_INT", replaced_element_rng)
    line = replaceAll(line, 0, 1, 0)

    # JIGGLE_MOUSE
    if line.startswith("JIGGLE_MOUSE"):
        jiggle_delay  = replaceAll(line[12:].strip())
        print(f"jiggle_delay: {jiggle_delay}")
        try:
            jiggle_delay = float(jiggle_delay) / 1000
        except ValueError:
            return script_lines 

        JiggleMouse(jiggle_delay)
        
    elif line.startswith("BACKGROUND_JIGGLE_MOUSE"):
        try:
            jiggle_delay  = replaceAll(line[23:].upper().split()[0].strip())
        except IndexError:
            jiggle_delay = "INF"

        print_with_color(f"[BACKGROUND_JIGGLE_DELAY]: jiggle_delay: {jiggle_delay}, condition: {'INF' in jiggle_delay}", BRIGHT_MAGENTA)
        if "INF" in jiggle_delay:
            asyncio.create_task(JiggleMouseInBackground(jiggle_delay, INF=1))
        else:
            try:
                jiggle_delay = float(jiggle_delay) / 1000
            except ValueError:
                return script_lines 
            asyncio.create_task(JiggleMouseInBackground(jiggle_delay))

        print_with_color("CREATING_TASK: JiggleMouseInBackground", BRIGHT_MAGENTA)

    elif line.startswith("MOUSE_CLICK"):
        try:
             button = replaceAll(line[11:].upper().split()[0].strip())
        except IndexError:
            return script_lines

        print_with_color(f"[MOUSE_CLICK] button={button}", STEEL_BLUE) 
        if button == "LEFT":
            mouse.click(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.click(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.click(Mouse.MIDDLE_BUTTON)

    elif line.startswith("MOUSE_PRESS"):
        try:
             button = replaceAll(line[11:].upper().split()[0].strip())
        except IndexError:
            return script_lines

        print_with_color(f"[MOUSE_PRESS] button={button}", STEEL_BLUE) 
        if button == "LEFT":
            mouse.press(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.press(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.press(Mouse.MIDDLE_BUTTON)


    elif line.startswith("MOUSE_RELEASE"):
        try:
             button = replaceAll(line[13:].upper().split()[0].strip())
        except IndexError:
            return script_lines

        print_with_color(f"[MOUSE_RELEASE] button={button}", STEEL_BLUE) 
        if button == "LEFT":
            mouse.release(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.release(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.release(Mouse.MIDDLE_BUTTON)

    elif line.startswith("MOUSE_MOVE"):
        line = replaceAll(line[10:].replace(",", ""))
        x, y = line.split()
        print_with_color(f"[MOUSE_MOVE] x={x}, y={y}", BRIGHT_YELLOW)
        try:
            x , y  = int(x), int(y)
        except ValueError:
            print_with_color("VALUE ERROR MOUSE_MOVE", RED)
            return script_lines
        mouse.move(x=x, y=y)

    elif line.startswith("MOUSE_SCROLL"):
        line = replaceAll(line[12:].replace(",", ""))
        direction = line.upper().split()[0]

        print_with_color(f"[MOUSE_SCROLL] direction: {direction}", BRIGHT_YELLOW)
        try :
            direction = int(direction)
        except ValueError:
            print_with_color("VALUE ERROR MOUSE_SCROLL", RED)
            return script_lines
        
        # negative number == scroll down else : scroll up
        mouse.move(wheel=direction)

    elif line.startswith("REM_BLOCK") or line.startswith("/*"):
        while not (line.startswith("END_REM") or line.startswith("*/")):
            line = next(script_lines).strip()
            continue

    elif line.startswith("REM") or line.startswith("//"):
        while line.startswith("REM") or line.startswith("//"):
            line = next(script_lines).strip()
            continue

    elif line.startswith("HOLD"):
        # HOLD command to press and hold a key
        key = line[4:].strip()
        key = replaceAll(key, 1, 1, 0)
        key = key.upper()
        keys_ls = key.split()

        print_with_color(f"[DEBUG_HOLD] key: {key}, keys_ls: {keys_ls}", BRIGHT_CYAN)
        if not keys_ls :
            return
        
        for commandKeycode in keys_ls:
            commandKeycode = duckyKeys.get(commandKeycode, None)
            if commandKeycode:
                kbd.press(commandKeycode)
            else:
                print(f"Unknown key to RELEASE: <{key}>")

    elif line.startswith("RELEASE"):
        # RELEASE command to release a held key
        key = line[8:].strip()
        key = replaceAll(key, 1, 1, 0)
        key = key.upper()
        keys_ls = key.split()
        
        print_with_color(f"[DEBUG_RELEASE] key: {key}, keys_ls: {keys_ls}", BRIGHT_CYAN)
        if not keys_ls :
            return
        
        for commandKeycode in keys_ls:
            commandKeycode = duckyKeys.get(commandKeycode, None)
            if commandKeycode:
                kbd.release(commandKeycode)
            else:
                print(f"Unknown key to RELEASE: <{key}>")

    elif line == "RELEASE_ALL":
        #releases all keys that might be pressed, ensuring nothing is stuck
        kbd.release_all()

    elif(line[0:5] == "DELAY"):
        delay = line[5:].strip()
        delay = replaceAll(delay)
        print(f"[0_DELAY_DEBUG]: line={line}, delay={delay}")

        try:
            delay = int(delay) 
            sleep(float(line[6:])/1000)
        except ValueError:
            print(f"[ANGRY_DEBUG]: Really BRO >:\ Entering This Value to DELAY: \"{delay}\" !!!!")


    elif line.startswith("STRINGLN_BLOCK") or line == "STRINGLN":             
        print_with_color("INSIDE_STRINGLN_BLOCK")
        line = next(script_lines).strip()
        print_with_color(f'[LINE_BLOCK] {line}', YELLOW)
        line = replaceAll(line)
        Enable_strip = 1

        while not line.startswith("END_STRINGLN") :
            if line.startswith("DISABLE_STRIP"):
                Enable_strip = 0 
                line = next(script_lines)
                continue
            elif line.startswith("ENABLE_STRIP"):
                Enable_strip =  1 
                line = next(script_lines).strip()
                continue
            elif line.startswith("//") or line.startswith("REM"):
                line = next(script_lines).strip()
                continue

            sendString(line)
            kbd.press(Keycode.ENTER)
            kbd.release(Keycode.ENTER)
            if Enable_strip:
                line = next(script_lines).strip()
            else :
                line = next(script_lines)

            line = replaceAll(line)
            

    elif line.startswith("STRING_BLOCK") or line == "STRING" :                 #< string block
        line = next(script_lines).strip()
        line = replaceAll(line)
        print_with_color("INSIDE_STRING_BLOCK", SILVER) 

        Enable_strip = 1
        while not line.startswith("END_STRING") :
            if line.startswith("DISABLE_STRIP"):
                Enable_strip = 0 
                line = next(script_lines)
                continue
            elif line.startswith("ENABLE_STRIP"):
                Enable_strip =  1 
                line = next(script_lines).strip()
                continue
            elif line.startswith("//") or line.startswith("REM"):
                line = next(script_lines).strip()
                continue


            sendString(line)
            if Enable_strip:
                line = next(script_lines).strip()
            else :
                line = next(script_lines)

            line = replaceAll(line)

    elif(line[0:5] == "PRINT"):
        line = replaceAll(line[6:])
        print(f"[FROM_SCRIPT_TO_SERIAL_MONITOR ->\^w^\-> ]: {line}")

    elif line[0:8] == "STRINGLN" :
        vle = replaceAll(line[9:])
        print(f"[STRINGLN_VALUE] {vle}")
        sendString(vle)
        kbd.press(Keycode.ENTER)
        kbd.release(Keycode.ENTER)
    

    elif(line[0:6] == "STRING"):
        sendString(replaceAll(line[7:]))




    elif(line[0:6] == "IMPORT"):
        imported_script = replaceAll(line[7:].strip().replace("'", "").replace('"', ''), 1, 1, 0)

        print(f"[IMPORTING]: {imported_script}")
        if imported_script:
            runScript(imported_script)
        else:
            print("[WARNING]: Empty import script")
        
    elif(line[0:13] == "DEFAULT_DELAY"):
        defaultDelay = line[14:].replace("=", "").strip()
        defaultDelay = replaceAll(defaultDelay)
        try:
            defaultDelay = int(defaultDelay)
        except ValueError :
            return script_lines

        print_with_color(f"[DEFAULT_DELAY]: {defaultDelay} ms", STEEL_BLUE)

    elif(line[0:12] == "DEFAULTDELAY"):
        defaultDelay = line[13:].replace("=", "").strip()
        defaultDelay = replaceAll(defaultDelay)
        try:
            defaultDelay = int(defaultDelay)
        except ValueError :
            return script_lines
        
        print_with_color(f"[DEFAULTDELAY]: {defaultDelay} ms", STEEL_BLUE)



    elif line.startswith("VAR"):
        match = re.match(r"VAR\s+\$(\w+)\s*=\s*(.+)", line)
        if match:
            varName = f"${match.group(1)}"
            varValue = match.group(2)
            
            print_with_color(f"[0_DEBUG_VAR] expression: {varValue}", BLUE)
            varValue = replaceAll(varValue)
            print_with_color(f"[1_DEBUG_VAR] expression: {varValue}", BLUE)            

            value = evaluateExpression(varValue)
            if value == PROBLEM_CODE:
                value = varValue

            variables[varName] = value
            print(f"variable: {varName}, value: {value}")

        else:
            print(f"Invalid variable declaration: {line}")

    elif line.startswith("$"):
        match = re.match(r"\$(\w+)\s*=\s*(.+)", line)
        if match:
            # EXAMPLE : $FOO = 42 + 3
            varName = f"${match.group(1)}" # $FOO
            expression = match.group(2) # 42 + 3

            expression = replaceAll(expression)
            print_with_color(f"[DEBUG] expression: {expression}, ", BLUE)            
            print_with_color(f'[0_EVALUATE_EXPRESION] BEGIN, expression: "{expression}"', GREEN)

            value = evaluateExpression(expression) # DO MATH OPERATION AND CONDITION 
            if value == PROBLEM_CODE:
                value  = expression 

            variables[varName] = value
            print_with_color(f"[VARIABLE_ASSIGNING] variable: {varName}, value: {value}", GREEN)
                


        else:
            print(f"[VARIABLE_ASSIGNING_ERROR] Invalid variable update, declare variable first: {line}")


    elif line.startswith("DEFINE"):
        define_ls = line.split()
        if len(define_ls) < 2 :
            return


        defineName = define_ls[1]
        defineValue = line.split(defineName, 1)[1].strip()


        print_with_color(f"[DEFINE] line={line}, defineName={defineName}, defineValue={defineValue}", BRIGHT_BLUE)
        Calc_value = evaluateExpression(defineValue)
        if Calc_value != PROBLEM_CODE:
            defineValue  = Calc_value
        defines[defineName] = defineValue
        print_with_color(f"[DEFINE] defineName={defineName}, defineValue={defineValue}", BRIGHT_BLUE)

    elif line.startswith("FUNCTION"):
        func_name = line.split()[1]
        print(f"[FUNCTION]: {func_name}")
        functions[func_name] = []
        line = next(script_lines).strip()
        while line != "END_FUNCTION":
            functions[func_name].append(line)
            line = next(script_lines).strip()

    elif line.startswith("WHILE"):
        condition = line[5:].strip()
        # list
        rem_script_lines = script_lines.remaining() 
        print(f'[WHILE_LOOP]:  CONDITION = "{condition}"')
        print(f'[SCRIPT_LINES_REM]: {BetterListOutput(rem_script_lines)}\n')
        
        loopCode = _getCodeBlock(script_lines) # loopCode type is list
        print(f'\n0 [LOOP_CODE]: {BetterListOutput(loopCode)}\n')


        while evaluateExpression(replaceAll(condition)) == True:
            currentIterCode = TrackIterator(loopCode.copy())  # fresh copy for each iteration

            while True:
                try:
                    loopLine = next(currentIterCode)
                    # parseLine now receives the iterator itself (not a rebuilt list iterator)
                    currentIterCode = TrackIterator(list(parseLine(loopLine, currentIterCode)))
                except StopIteration:
                    break
                gc.collect()
            gc.collect()

    elif line.upper().startswith("IF"):
        condition = _getIfCondition(line)
        print_with_color(f"[IF_STATEMENT_START] line={line}, condition={condition}", BRIGHT_MAGENTA)
        condition = replaceAll(condition)
        print_with_color(f"[IF_STATEMENT_START] line={line}, condition_replaced={condition}", BRIGHT_MAGENTA)
        script_lines, ret = IF(condition, script_lines).runIf()
        print_with_color(f"[IF_RETURNED_CODE]: {ret}", YELLOW)


    # Random Values as example :
    # RANDOM_LOWERCASE_LETTER 5 
    # ouput : azxcd

    elif line[0:23] == "RANDOM_LOWERCASE_LETTER":
        random_output(line, letters)

    elif line[0:23] == "RANDOM_UPPERCASE_LETTER":
        random_output(line, letters.upper())

    elif line[0:13] == "RANDOM_LETTER":
        random_output(line, letters + letters.upper())

    elif line[0:13] == "RANDOM_NUMBER":
        random_output(line, numbers)

    elif line[0:14] == "RANDOM_SPECIAL":
        random_output(line ,specialChars)

    elif line[0:11] == "RANDOM_CHAR":
        random_output(line ,letters + letters.upper() + numbers + specialChars)
    
    # FUNCTION'S EXCUTION
    elif line in functions:
        updated_lines = []
        inside_while_block = False
        for func_line in functions[line]:
            if func_line.startswith("WHILE"):
                inside_while_block = True  # Start skipping lines
                updated_lines.append(func_line)

            elif func_line.startswith("END_WHILE"):
                inside_while_block = False  # Stop skipping lines
                updated_lines.append(func_line)
                WHILE_FUNC = TrackIterator(updated_lines)
                parseLine(updated_lines[0], WHILE_FUNC)
                updated_lines = []  # Clear updated_lines after parsing

            elif inside_while_block:
                updated_lines.append(func_line)

            elif not (func_line.startswith("END_WHILE") or func_line.startswith("WHILE")):
                # print(f"[LINE_ITER_FUNC_LINE] {func_line}\n[functions[line]] {functions[line]}")
                LINE_ITER = TrackIterator(functions[line])
                # print(f"[LINE_ITER_REMANNING] {LINE_ITER.remaining()}")
                parseLine(func_line, LINE_ITER)
            gc.collect()
    else:
        runScriptLine(line) # THE GOAT
        gc.collect()

    return script_lines


def getProgrammingStatus():
    global oneshot, progStatusPin
    
    pin_num = config['BOARD']['controll_mode_pin']
    if not isinstance(pin_num, int) or not hasattr(board, f"GP{pin_num}"):
        print(f"Invalid or missing pin in config, defaulting to GP{DEFAULT_PIN_NUM}")
        pin_num = DEFAULT_PIN_NUM

    pin_name = f"GP{pin_num}" 
    # check GP5 for setup mode
    if oneshot:
        progStatusPin =DigitalInOut(getattr(board, pin_name))
        oneshot = False

    progStatusPin.switch_to_input(pull=Pull.UP)
    return progStatusPin.value



def runScript(duckyScriptPath):
    global defaultDelay, defines, variables,  KeyboardLayout, Keycode, layout
    restart = True
    try:
        print(f'[RUN] Injecting Keystrokes from "{duckyScriptPath}" ')
        while restart:
            restart = False
            with open(duckyScriptPath, "r", encoding='utf-8') as f:
                lines = f.readlines()
                script_lines = TrackIterator(lines)

                previousLines = []
                for line in script_lines:
                    line = line.strip()
                    if not line:
                        continue

                    gc.collect()
                    free_memory = gc.mem_free()
                    allocated_memory = gc.mem_alloc()
                    print_with_color(f"free_memory: {free_memory}, allocated_memory: {allocated_memory}", SILVER)

                    print(f"[LINE] {line}")
                    
                    if line.startswith("SELECT_LAYOUT"):
                        ls = line.split()
                        if len(ls) < 2 :
                            continue
                        new_KeyboardLayout, new_Keycode = SelectLayout(ls[1])
                        if new_KeyboardLayout and new_Keycode:
                            KeyboardLayout = new_KeyboardLayout
                            Keycode = new_Keycode
                            layout = KeyboardLayout(kbd)


                    if line.startswith("REPEAT") :
                        line = replaceAll(line)
                        line = line.upper()

                        while " =" in line or "= " in line:
                            line = line.replace(" =", "=").replace("= ", "=")

                        print(f"traited line : {line}")
                        repeat_ls = line.split()
                        print(f"repeat_ls: {repeat_ls}")

                        if not (len(repeat_ls) >= 3 and "LINES=" in line and "TIMES=" in line):
                            print("[ERRPR]")
                            continue

                        line_idx, time_idx = 0, 0

                        for index, value in enumerate(repeat_ls):
                            value = value.replace(" ", "")
                            if value.startswith("LINES="):
                                line_idx = index
                            elif value.startswith("TIMES="):
                                time_idx = index
                
                        print(f"LINES index: {line_idx}, TIMES index: {time_idx}")
                        if not line_idx or not time_idx:
                            continue

                        
                        lines_value , times_value = 0, 0 
                        try:
                            lines_value = int(repeat_ls[line_idx].split("=")[1].strip())
                            times_value = int(repeat_ls[time_idx].split("=")[1].strip())
                        except ValueError:
                            continue
                        print("[STARTING_REPEATING]")
                        for _ in range(times_value) :
                            #repeat the last command
                            for repeated_line in previousLines[-lines_value:]:
                                parseLine(repeated_line, script_lines)
                                sleep(float(defaultDelay) / 1000)

                    elif line.startswith("RESTART_PAYLOAD"):
                        restart = True
                        break
                    elif line.startswith("STOP_PAYLOAD"):
                        restart = False
                        break
                    else:
                        parseLine(line, script_lines)
                        previousLines.append(line)

                    sleep(float(defaultDelay) / 1000)

    except OSError :
        print(f'Unable to open file "{duckyScriptPath}"')

    variables = {"$_RANDOM_MIN": 0, "$_RANDOM_MAX": 65535}
    defines = {}
    functions = {}
    print(f"[{duckyScriptPath.upper().replace('dd', '')}_COMPLETED] 200")
    gc.collect()


async def blink_led(led):
    print("Blink")
    BlinkLedPico(led)


async def BlinkLedPico(led):
    led_state = False
    min_ms = 100 
    max_ms = 600
    initial_status = getProgrammingStatus()
    print(f"[BLINK] delay_intervale = [{min_ms}, {max_ms}] ms")

    while True:
        if config['BOARD']['enable_auto_switch_mode'] in [True, "True", "true", "1", 1] and  initial_status != getProgrammingStatus():
            print_with_color("Changing OverQuack MODE")
            reset()

        seconds = (randint(min_ms, max_ms)) / 1000
        if led_state:
            led.value = 1
            await asyncio.sleep(seconds)
            led_state = False
        else:
            led.value = 0
            await asyncio.sleep(seconds)
            led_state = True
