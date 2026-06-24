# 🔧 OverQuack Advanced Topics and Internals


This document explains the inner workings of OverQuack for **power‑users, developers, and researchers**. You’ll learn how ATTACKMODE resumes, what the TCP protocol looks like on the wire, how the interpreter executes your script, and how to tune memory for large payloads. OverQuack runs on all Raspberry Pi Pico variants: **Pico, Pico W, Pico 2, and Pico 2 W**. the code automatically detects the hardware at boot and enables Wi‑Fi only when available.


> **For the main project overview, installation, and the language reference, see [README.md](README.md) and [LANGUAGE.md](LANGUAGE.md).**

---

## 📖 Table of Contents

- [ATTACKMODE and NVM Resume](#attackmode-and-nvm-resume)
- [USB Mode Switching (Pin and Auto-Reboot)](#usb-mode)

- [TCP Protocol Reference (Wire Format)](#tcp-protocol-reference-wire-format)
- [Interpreter Internals (overquackifypy)](#interpreter-internals-overquackifypy)
- [Memory and Performance Tuning](#memory-and-performance-tuning)
- [Keyboard Layouts, How They Work and How to Add One](#keyboard-layouts)
- [USB Identification and Spoofing](#usb-identification-and-spoofing)
- [Known Limitations and Edge Cases](#known-limitations-and-edge-cases)
- [Future Technical Roadmap](#future-technical-roadmap)

---

## ATTACKMODE and NVM Resume

OverQuack can switch its USB personality **and resume the payload from the exact next line** after the board resets. This is accomplished with the microcontroller’s non‑volatile memory (NVM).

### How It Works

1. When the interpreter encounters `ATTACKMODE HID` or `ATTACKMODE HID STORAGE`, it calculates the next line index (`ctx.i + 1`).
2. It writes four bytes to NVM (the RP2040/RP2350’s 256‑byte NVM array):
   | Byte | Meaning |
   |------|---------|
   | `0`  | **Consumed flag** – `0` = fresh resume, `1` = already used |
   | `1`  | **USB mode byte** – `1` = HID only, `3` = HID + Storage |
   | `2‑3`| **Line number** (little‑endian) to resume from |
3. The board is then reset with `microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)` and `microcontroller.reset()`.

### What Happens After Reboot

- **`boot.py`** reads NVM. If `NVM[0] == 0` and `NVM[1] != 0`, it applies the requested USB configuration (enabling / disabling storage and HID accordingly) **without consuming the flag**.
- **`code.py`** checks NVM again:
  - If `NVM[0] == 0` and a valid line number exists, it verifies the line exists in the payload file and that the line is **not** another `ATTACKMODE`.
  - If valid, it sets `NVM[0] = 1` (consumed) and starts executing the payload from that line.
  - If invalid, the NVM is wiped.

### Safety Clean‑Up

After the payload finishes (or crashes), `code.py` **always** clears the NVM resume data in a `finally` block. This prevents stale resumes on the next power‑up.

### Edge Cases

- **Power loss between NVM write and reset:** The resume data will remain in NVM. On next boot, `code.py` tries to verify the payload file. If the file can’t be read or the line is out of range, the NVM is cleared automatically.
- **Resume line is another ATTACKMODE:** The resume is aborted to prevent an infinite reset loop.

### Manually Clearing NVM

If you suspect stale NVM data is causing a boot loop, you can clear it from the serial console (REPL):

1. Connect to the board’s serial port (baud 9600) with `picocom`, `screen`, or PuTTY.
2. Press **Ctrl+C** to drop into the REPL.
3. Paste one of the following and press Enter:

   - **Partial wipe** (clears only OverQuack’s 4 bytes – recommended):
     ```python
     import microcontroller
     microcontroller.nvm[0:4] = bytes(4)
     microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
     microcontroller.reset()
     ```

   - **Full wipe** (clears the entire 256‑byte NVM):
     ```python
     import microcontroller
     nvm = microcontroller.nvm
     for i in range(len(nvm)):
         nvm[i] = 0
     microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
     microcontroller.reset()
     ```

4. The board will reboot cleanly.

---

<a id="usb-mode"></a>
## USB Mode Switching (Pin and Auto‑Reboot)

The physical GPIO pin defined in `config.json` (`BOARD.controll_mode_pin`, default GP5) determines whether the Pico acts as a **mass storage device** or a **stealth HID device**.

- **Pin connected to GND** -> **HID mode** (keyboard + mouse, no USB drive visible)
- **Pin floating (open)** -> **Storage mode** (CIRCUITPY drive visible, no HID injection)

When `enable_auto_switch_mode` is `true`, the `BlinkLedPico` task constantly monitors the pin. If the pin state changes, the board **automatically resets** – no need to unplug the USB cable.

---

## TCP Protocol Reference (Wire Format)

The `quackd.py` server listens on port `1084` (configurable via `AP.ports`). Communication is **line‑delimited ASCII**.

### Request Format

Every request is a single line terminated by `\n`:

```
COMMAND [arg1] [arg2]\n
```

### Response Format

Most responses use a **length‑prefixed packet**:

```
SIZE <bytes>\n
<raw data of exactly <bytes> length>
```

- The header line must be `SIZE <integer>\n`.
- The server then sends exactly that many bytes of payload.
- For text responses (like `PING`, `LS`, `VERSION`), the payload is a UTF‑8 string.

**File downloads (`READ`)** use the same framing but stream in 512‑byte chunks internally while keeping the header‑then‑data contract from the client’s perspective.

### Special Handshake for `WRITE`

To prevent out‑of‑memory crashes, the server enforces a **two‑step write sequence**:

1. Client sends `FREE_MEM` -> receives free RAM size.
2. Client sends `WRITE <filename> <size_in_bytes>\n`.
3. Server replies `READY WRITE <filename> <size>\n`.
4. Client sends **exactly `<size>` raw bytes**.
5. Server replies `WRITTEN <filename>\n` or an error.

If the client disconnects during the transfer, the partial file is automatically deleted.

### Protected Files

The following files **cannot** be deleted via `DELETE` (the server refuses):

- `boot.py`
- `code.py`
- `config.json`
- `overquackify.py`
- `quackd.py`
- `settings.toml`

### Blocking Nature of `RUN`

When you send `RUN payload.oqs`, the server calls `runScript()` **synchronously**. The TCP server is blocked until the payload finishes. A hung payload (e.g., infinite loop without `DELAY`) can only be stopped by physically resetting the board. (Future plans include an asynchronous `RUN` with a `STOP` command.)

---

## Interpreter Internals (overquackify.py)

### Execution Model and The Context Stack

OverQuack uses an **iterative, stack‑based execution model**. There is **no recursion**. Each script, function call, or imported file is represented by an `ExecContext` object pushed onto a global `context_stack`.

An `ExecContext` holds:
- `lines` – list of script lines (including trailing newlines)
- `i` – current line index
- `skip_depth` – how many levels of `IF`/`ELSE`/`WHILE` to skip (for conditional branching)
- `branch_taken_stack` – per‑IF‑level boolean indicating if a branch was already taken
- `is_function` – `True` if this context is a function call (to control return behaviour)
- `loop_stack` – stores `(condition_str, start_idx, saved_skip, saved_branch)` for `WHILE` loops
- `previousLines` – stores raw text of executed lines, used by `REPEAT`

- **`IMPORT`** reads the specified file, wraps its lines in a new `ExecContext` (with `is_function=True`), and pushes that context onto the stack. Execution jumps into the imported script; when it finishes, the context is popped and the parent resumes from the next line.

### Expression Evaluation Order

When a line like `STRING Hello $username, counter is $counter` runs, the interpreter applies replacements in this order:

1. **Defines** (`replaceDefines`): substitute all `DEFINE` constants.
2. **Variables** (`replaceVariables`): substitute `$VAR_NAME` with current values, and evaluate system variables like `$_CAPSLOCK_ON`.
3. **Random Variables** (`replaceRandomVariables`): replace `$_RANDOM_*` patterns with freshly generated random values.

After replacement, expressions (e.g., in `DELAY`, `VAR`, or conditions) are passed to `evaluateExpression` which uses Python’s `eval()` with some syntactic sugar (`^` -> `**`, `&&` -> `and`, `||` -> `or`).

### Key Implementation Details

- **`DEFAULT_DELAY`** is added after every executed command (except control structures).
- **`$_JITTER_ENABLED`** adds a random 0–`$_JITTER_MAX` ms delay to **every** sleep call (including the default delay and explicit `DELAY`). The jitter is applied inside `_sleep_jitter()`.
- **`STRING`** only sends characters in the range 32–126. By default, any character outside this range is replaced with `?ERR?` and a warning is printed. Set `$_STRICT = 0` to silently skip unsupported characters instead.
- **`REPEAT`** depends on `previousLines`, which is lost after an `ATTACKMODE` reset. Using `REPEAT` across a mode switch will not work.
- **Comments** (`REM`, `//`, `REM_BLOCK`, `/* */`) are stripped during parsing.
- **Block Comments (`/* */`):** The closing marker `*/` is detected at the start **or** end of a line, so `/* inline comment */` works correctly. Trailing whitespace after `*/` is fine.
- **Block strings** (`STRING_BLOCK` / `STRINGLN_BLOCK`) are **literal** after the recent design update. The global `ENABLE_STRIP` / `DISABLE_STRIP` commands set indentation stripping for all subsequent blocks; no inline toggles or comment processing happens inside a block. This makes blocks safe for injecting arbitrary code.

---

## Memory and Performance Tuning

### Available RAM per Board

| Board    | Approximate Free RAM |
|----------|----------------------|
| Pico     | ~264 KB              |
| Pico W   | ~264 KB              |
| Pico 2   | ~520 KB              |
| Pico 2 W | ~520 KB              |

### Stack Size

By default, CircuitPython allocates a **1536‑byte Python stack**. OverQuack ships with `CIRCUITPY_PYSTACK_SIZE = 6144` in `settings.toml`. This quadruples the stack to support deeply nested function calls and complex expressions. If your payloads still crash, you can increase it further – but remember it consumes RAM from the total pool.

### Avoiding Out‑of‑Memory During Writes

The TCP server **requires** a `FREE_MEM` call before accepting `WRITE`. This lets the client verify that enough RAM is available for the transfer buffer. If you bypass this protocol, the server will reject the write with an error.

---

<a id="keyboard-layouts"></a>
## Keyboard Layouts – How They Work and How to Add One

### Built‑in Layout Support

The active layout is represented by a `KeyboardLayout` instance (from Adafruit HID). When you call `SELECT_LAYOUT WIN_DE`, OverQuack:

1. Looks up the layout key in `LAYOUTS_MAP` (a dictionary in `overquackify.py`).
2. Dynamically imports the correct layout module (e.g., `keyboard_layout_win_de`) and its matching keycode module (e.g., `keycode_win_de`).
3. Creates a new `KeyboardLayout(kbd)` and `Keycode` class, replacing the old ones.

All subsequent `STRING` commands use the new layout.

### Adding a New Layout

**Perform all steps directly on the Pico’s `CIRCUITPY` drive (storage mode).**

1. Switch the Pico to storage mode (mode pin floating). The drive may appear as `CIRCUITPY` or `OVERQUACK` (depending on prior ATTACKMODE usage).
2. Go to [https://www.neradoc.me/layouts/](https://www.neradoc.me/layouts/), generate your layout and download the ZIP.
3. Extract the two `.mpy` files and copy them:
   - `keyboard_layout_<LANGUAGE>.mpy` -> `<drive>/lib/keyboard_layouts/`
   - `keycode_<LANGUAGE>.mpy` -> `<drive>/lib/keycodes/`
4. Edit `<drive>/overquackify.py` and add an entry to `LAYOUTS_MAP` (around line 107‑124):
   ```python
   "WIN_XY": ("keyboard_layouts.keyboard_layout_win_xy", "keycodes.keycode_win_xy"),
   ```
5. Save, eject, and switch back to HID mode. The new layout is immediately available with `SELECT_LAYOUT WIN_XY`.

> 💡 The drive label changes to `DRIVE_LABEL` (default `OVERQUACK`) after the first `ATTACKMODE HID STORAGE` cycle. This is expected and does not affect functionality.

---

## USB Identification and Spoofing

OverQuack allows you to set **custom VID/PID and manufacturer/product strings** in `config.json` under `USB_IDENTIFICATION`. This changes how the device appears to the host (e.g., as a specific keyboard model).

### Default Fallback

If `config.json` is missing or the `USB_IDENTIFICATION` key is not present, the firmware uses:

```json
{
  "manufacturer": "CHICONY",
  "product": "HP Basic USB Keyboard",
  "vid": "0x03F0",
  "pid": "0x0024"
}
```

### Finding Real Device IDs

- **Linux:** `lsusb -v` (look for `idVendor` and `idProduct`)
- **Windows:** Device Manager -> Properties -> Details -> Hardware Ids
- **macOS:** System Information -> USB

Copy the VID/PID (in hex) and the manufacturer/product strings into `config.json`.

---

## Known Limitations and Edge Cases

- **Unsupported Characters:** Only ASCII 32‑126 are supported in `STRING`. By default, everything else becomes `?ERR?`. Set `$_STRICT = 0` to silently skip them instead.
- **`REPEAT` and ATTACKMODE:** `REPEAT` cannot span across a mode switch because `previousLines` is not persisted in NVM.
- **Single TCP Client:** The server handles only one client at a time.
- **Blocking `RUN`:** The TCP server freezes during payload execution – a hung script requires physical reset.
- **No Payload Encryption:** `.oqs` files are stored in plaintext on the CIRCUITPY drive.
- **NVM Resume Sensitivity:** Power loss after writing NVM but before reset may cause unintended resumes; the firmware tries to detect and clear stale data.
- **String Block Behaviour:** Blocks are literal. `//`, `REM`, `ENABLE_STRIP`, etc. inside a block are typed as text – they are not processed as commands or comments.

---

## Future Technical Roadmap

See the main [README.md#roadmap](README.md) for the project’s high‑level plans. From an internals perspective, these are the most significant upcoming changes:

- **Asynchronous payload execution**, so the TCP server can accept a `STOP` command even during a running payload.
- **LED / lock‑key exfiltration**, bit‑banging data through Caps/Num/Scroll lock LEDs (the `FILE_EXFILTRATION` command is already a placeholder in the code).
- **USB CDC middleman**, using CircuitPython 10.2’s USB host capabilities to sit between a keyboard and a host, logging all keystrokes.
- **BLE control**, adding Bluetooth Low Energy as an alternative to Wi‑Fi.
- **Encrypted TCP**, securing the remote control channel with pre‑shared keys.

---

## 📚 Related Documents

- **[README.md](README.md)** – Project overview, quick start, configuration.
- **[LANGUAGE.md](LANGUAGE.md)** – Complete scripting language reference.
- **[FAQ.md](FAQ.md)** – Frequently asked questions and troubleshooting.

---

**Questions?** Open an issue on [GitHub](https://github.com/VexilonHacker/OverQuack) or join the discussion.

[👈 Back to README](README.md)
