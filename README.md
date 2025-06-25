# 🦆 OverQuack

**OverQuack** is an advanced Rubber Ducky-style HID attack platform built on the Raspberry Pi Pico family — now featuring **wireless control**, **cross-platform payload support**, and full compatibility with **all four Pico variants**.

---

## 🚀 Features

- 🧠 **Rubber Ducky functionality** – Emulates keystrokes for scripted attacks and automation
- 💡 **Supports all Pico variants** – Pico, Pico H, Pico W, Pico WH (and Pico W 2 if applicable)
- 📡 **Wireless control** – Manage payloads remotely over Wi-Fi  
  <details>
    <summary>Show supported operations</summary>

    - Upload new payloads  
    - List stored scripts  
    - Trigger specific payloads  
    - Monitor execution status  
    - Update or delete existing payloads

  </details>

- 🖥️ **Cross-platform compatibility** – Works seamlessly with Windows, macOS, and Linux targets
- 🌐 **Client-controlled interface** – Manage your device using the `OverQuack_client.go` script
- 🔌 **Plug & play HID injection** – No drivers or setup required; just connect and deploy
- 🛠️ **Unlimited payloads** – Store as many payloads as your Pico’s storage capacity allows

---

## 📦 Supported Devices

| Device      | HID Support | Wi-Fi Support |
|-------------|-------------|----------------|
| Pico        | ✅           | ❌              |
| Pico H      | ✅           | ❌              |
| Pico W      | ✅           | ✅              |
| Pico WH     | ✅           | ✅              |

---

## 📂 Getting Started

1. **Flash the firmware** – Load the provided `.uf2` firmware file onto your Pico.
2. **Connect via USB** – The device will register as a standard HID keyboard.
3. **Manage payloads** – Use the `OverQuack_client.go` tool to upload and control scripts.
4. **Deploy attacks** – Trigger payloads directly from your client or via remote access.

---

## 🔐 Disclaimer

OverQuack is intended strictly for **educational, ethical hacking, and authorized penetration testing** purposes.  
**Do not use this tool on systems without explicit permission.**

---

## ❤️ Contributing

We welcome contributions!  
Found a bug or have an idea for improvement? Open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

