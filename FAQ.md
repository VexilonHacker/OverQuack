# ❓ OverQuack FAQ and Troubleshooting

> **Before you dig in:**  
> - [README :](README.md) install, config, quick start  
> - [LANGUAGE :](LANGUAGE.md) every command and syntax  
> - [ADVANCED :](ADVANCED.md) internals, NVM, TCP protocol  

---

## 🔍 Quick Diagnostics

### My board isn't doing what I expect
1. **Open the serial monitor** (baud 9600), if `ENABLE_SERIAL_DEBUG` is `true` you'll see exactly what the interpreter is doing.  
2. Check the **LED**, steady blink means the device is in HID attack mode and the AP/TCP server is running. Fast, erratic blinks may indicate a boot loop.  
3. Verify the **mode pin**, floating = storage mode (payload won't run), grounded = attack mode. If you're using a switch, try wiggling it.

---

## 🧪 Payloads

<details>
<summary><strong>My payload works in the IDE but not on the board</strong></summary>

- The **Web IDE** does its own validation and doesn't execute code. Syntax that passes the IDE may still fail on the device due to memory, unsupported characters, or logic errors.  
- Always test with `ENABLE_SERIAL_DEBUG: true` and check the serial output for runtime errors.  
- The board runs the interpreter in a **single thread**, an infinite loop without a `DELAY` will freeze everything.
</details>

<details>
<summary><strong>I see `?ERR?` in the output / characters are missing</strong></summary>

Only **ASCII 32--126** characters are supported. Everything outside that range is replaced with `?ERR?` by default.

**Quick fix:** add `$_STRICT = 0` to your payload to silently skip unsupported characters instead of printing `?ERR?`.

**Workaround:** use `SELECT_LAYOUT` and type the character via its key combination (e.g., `ALT` codes) instead of putting it directly in a `STRING`.

**Common cause:** carriage returns (`\r`) from Windows‑style line endings inside `STRING_BLOCK`. Run `sed -i 's/\r$//' payload.oqs` to clean them.
</details>

<details>
<summary><strong>REPEAT isn't repeating the lines I expected</strong></summary>

`REPEAT` replays the **last N lines from the same context**. If you're inside a function, an imported script, or after an `ATTACKMODE`, the `previousLines` buffer may be empty or hold different lines than you think.  
> Avoid using `REPEAT` across `FUNCTION` / `IMPORT` boundaries or after a reboot.
</details>

<details>
<summary><strong>ATTACKMODE doesn't resume at the right line</strong></summary>

- The resume line is stored in **NVM**. If the board loses power *after* writing NVM but *before* the reset, stale data might survive. On next boot, `code.py` checks if the line exists and is **not** another `ATTACKMODE`. If the check fails, NVM is wiped and the payload runs from the start.  
- You can't resume a line that is itself an `ATTACKMODE`, the resume is intentionally aborted to prevent infinite resets.

**To manually clear the NVM using the serial console (no file editing needed):**

1. Connect to the board's serial port (baud 9600) with `picocom`, `screen`, or PuTTY.  
2. Press **Ctrl+C** when you see the CircuitPython output. This drops you into the **REPL** (interactive interpreter).  
3. Paste one of the following code blocks and press Enter. The board will clear NVM and reset itself.

   - **Partial wipe** (clears only OverQuack's NVM data, recommended):  
     ```python
     import microcontroller
     microcontroller.nvm[0:4] = bytes(4)
     microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
     microcontroller.reset()
     ```

   - **Full wipe** (clears the entire 256-byte NVM):  
     ```python
     import microcontroller
     nvm = microcontroller.nvm
     for i in range(len(nvm)):
         nvm[i] = 0
     microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
     microcontroller.reset()
     ```

4. The board will reboot cleanly. If it was stuck in a boot loop due to a bad resume, it should now start normally.

> 💡 Normally the firmware handles this automatically. This manual procedure is only needed if you're stuck in a boot loop or the board repeatedly tries to resume a bad line.
</details>


---

## 🌐 Wi-Fi and TCP

<details>
<summary><strong>The AP appears but I can't connect or the client times out</strong></summary>

- Make sure you're connecting to the **exact** SSID in `config.json`.  
- The TCP server may take 5-10 seconds **after** the AP appears to start listening. Wait a moment and try again.  
- If you're using the desktop client, double-check `--host` matches `AP.ip_address` (default `10.10.5.1`).  
- Firewalls on your computer can block outgoing connections to non-standard ports like `1084`. **(im talking about you. Windows)**
</details>

<details>
<summary><strong>The board becomes unresponsive after a WRITE or RUN command</strong></summary>

- `WRITE` requires the **full** payload size to be sent after the server replies `READY WRITE`. If the connection drops mid-transfer, the partial file is deleted and the server waits for a new connection.  
- `RUN` is **synchronous**, the server won't respond until the payload finishes. If your script enters an infinite loop without a `DELAY`, the board will hang. **Always add a `DELAY` inside loops.**
</details>

---

## 🖥️ Web IDE

<details>
<summary><strong>The IDE shows errors but the payload seems fine</strong></summary>

The IDE's live validation is a **static checker**, it can't know about variable values at runtime or dynamic imports. Orange underlines ("unused variable/function") are warnings, not errors. Only **red markers** indicate syntax that will definitely fail on the device.
</details>

<details>
<summary><strong>I lost my tabs, can I recover them?</strong></summary>

The IDE saves tabs to your browser's `localStorage` **only when the "Auto-save" checkbox is ticked**. If it was off, the tabs are gone. Clearing your browser data also deletes them.
</details>

---

## 🔧 Hardware and Phone support

<details>
<summary><strong>The board resets repeatedly (boot loop)</strong></summary>

- Bare wires or loose pins shorting against each other can trigger constant resets.  
- If you're toggling the mode pin with a switch, make sure it's wired firmly and not floating, add a pull-up or pull-down resistor if needed.  
- As a last resort, flash the **Nuke UF2** from **`OverQuack_Cirpy_firmwaresen_10.2.1/flash_nuke_all_boards.uf2`** to wipe the entire flash and start clean.
</details>

<details>
<summary><strong>Does OverQuack work on Android or iPhone?</strong></summary>
<br> 

<p align="center">
  <strong>Yes – provided the device supports USB HID via OTG or USB‑C.</strong><br/>
  <img src="./assets/OverQuack_Gifs/OverQuack_Android.gif" alt="OverQuack Android Demo" width="450" />
</p>

### Android
- Most modern Android phones support **USB OTG (On-The-Go)**.  
- Connect the Pico through an **OTG adapter** (USB-A female to USB-C / micro-USB male). The phone will recognise it as a standard keyboard + mouse.  
- Keystroke injection and mouse control work exactly as they would on a computer.  
- Some Android skins hide an "OTG" toggle in settings, and a few devices limit USB power output. If the Pico doesn't power up, try a powered USB hub or a small power bank inline.

### iPhone (Lightning)
- Lightning-based iPhones have **very limited generic USB HID support**.  
- With an **Apple Lightning to USB Camera Adapter**, the Pico *might* appear as a keyboard, but reliability varies across iOS versions and is **not guaranteed**.  
- For consistent results, Lightning iPhones are not recommended.

### iPhone (USB-C ,  iPhone 15 and later)
- USB-C iPhones handle standard USB peripherals more reliably.  
- A simple **USB-C to USB-A adapter** is enough. The Pico will show up as a keyboard/mouse and injection works as expected.

</details>

---

## 🧠 Advanced / Power-User


<details>
<summary><strong>How do I update OverQuack without losing my payloads?</strong></summary>

1. Switch the device to **storage mode** (pin floating).  
2. Replace **only** the files that changed, typically `boot.py`, `code.py`, `overquackify.py`, `quackd.py`, and any updated libraries.  
3. **Don't overwrite** `config.json`, your `.oqs` files, or `settings.toml` unless you intend to.  
4. Eject the drive and switch back to HID mode.
</details>

<details>
<summary><strong>I accidentally deleted `config.json`, what now?</strong></summary>

The firmware has sensible **fallback defaults** (Hp keyboard VID/PID, GP5 mode pin, no Wi-Fi, default payload `payload.oqs`). The device will still work. Just copy the original `config.json` from the repository back to the CIRCUITPY drive when you're in storage mode.
</details>

<details>
<summary><strong>Can I run more than one payload at a time?</strong></summary>

No. The interpreter is **single-threaded** and executes one script at a time, line by line. A keyboard, and OverQuack, can only perform one keystroke or mouse action at a time.

You **can** chain multiple `.oqs` files together using the `IMPORT` command inside a main payload, so they run sequentially as a single combined script.
</details>

---

## 📚 Still Stuck?

- Turn on `ENABLE_SERIAL_DEBUG` in `config.json` and capture the serial output.  
- Open a [GitHub Issue](https://github.com/VexilonHacker/OverQuack/issues) with:
  - Board model
  - The exact payload (or the smallest script that reproduces the problem)
  - The serial output
  - What you expected to happen

We'll get you quacking again ;] 🦆

[👈 Back to README](README.md)
