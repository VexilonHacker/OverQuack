#!/usr/bin/env python3
import os, sys, shutil, platform
from pathlib import Path

ICON = r"""
░███████████       ██████████
░█████████████   ██████████████
░█████  ██████   █████  ███████
░███████  █████ ████  ████████
 ░████████   █   █  ███
  ░██████████     ███   ███████
    ░█████           ███████████
           ██████  ████████  ████
  ░█████  ███████  ███████    ████
 ░██████ █████████ █████████████ ███
 ░██████  ████████  █████████    █████████
░█████      █████     ███████   ██
░██    ██████    █████   ████     █████
░███  ████████  ████████  ████
░███ ████████████████████ ██████
░███  ████████  ████████  ██████
░██    ██████    ██████    ████
░███████  █████████  ██████
 ░░░█████  ███████  ██████
    ░░███    ███    ████
      ░░░████   ████
         ░░███████
           ░░░░░░
"""

TITLE = r"""

    ███████                                      ██████                                  █████            
  ███░░░░░███                                  ███░░░░███                               ░░███             
 ███     ░░███ █████ █████  ██████  ████████  ███    ░░███ █████ ████  ██████    ██████  ░███ █████       
░███      ░███░░███ ░░███  ███░░███░░███░░███░███     ░███░░███ ░███  ░░░░░███  ███░░███ ░███░░███        
░███      ░███ ░███  ░███ ░███████  ░███ ░░░ ░███   ██░███ ░███ ░███   ███████ ░███ ░░░  ░██████░         
░░███     ███  ░░███ ███  ░███░░░   ░███     ░░███ ░░████  ░███ ░███  ███░░███ ░███  ███ ░███░░███        
 ░░░███████░    ░░█████   ░░██████  █████     ░░░██████░██ ░░████████░░████████░░██████  ████ █████       
   ░░░░░░░       ░░░░░     ░░░░░░  ░░░░░        ░░░░░░ ░░   ░░░░░░░░  ░░░░░░░░  ░░░░░░  ░░░░ ░░░░░        
                                                                                                          
                                        █████   ███   █████  ███                                     █████
                                       ░░███   ░███  ░░███  ░░░                                     ░░███ 
                                        ░███   ░███   ░███  ████   █████████  ██████   ████████   ███████ 
                                        ░███   ░███   ░███ ░░███  ░█░░░░███  ░░░░░███ ░░███░░███ ███░░███ 
                                        ░░███  █████  ███   ░███  ░   ███░    ███████  ░███ ░░░ ░███ ░███ 
                                         ░░░█████░█████░    ░███    ███░   █ ███░░███  ░███     ░███ ░███ 
                                           ░░███ ░░███      █████  █████████░░████████ █████    ░░████████
                                            ░░░   ░░░      ░░░░░  ░░░░░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░░░ 
                                                                                                          
                                                                                                          
                                                                            Made by VexilonHacker (⌐■_■)
"""

class Colors:
    RESET   = "\033[0m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    GOLD    = "\033[38;2;255;215;0m"
    BOLD    = "\033[1m"


BASE_DIR = Path(__file__).resolve().parent
FIRMWARE_DIR = BASE_DIR / "OverQuack_Cirpy_firmwaresen_10.2.1"
SRC_DIR = BASE_DIR / "OverQuack_src"
CURRENT_OS = platform.system()
BOARDS = {
    1: ("Pico",     "adafruit-circuitpython-raspberry_pi_pico-en_US-10.2.1.uf2",    "RPI-RP2"),
    2: ("Pico W",   "adafruit-circuitpython-raspberry_pi_pico_w-en_US-10.2.1.uf2",  "RPI-RP2"),
    3: ("Pico 2",   "adafruit-circuitpython-raspberry_pi_pico2-en_US-10.2.1.uf2",   "RP2350"),
    4: ("Pico 2 W", "adafruit-circuitpython-raspberry_pi_pico2_w-en_US-10.2.1.uf2", "RP2350"),
}
VERSION = "2.0"

def cprint(msg, color=Colors.GREEN, end="\n"):
    print(f"{color}{msg}{Colors.RESET}", end=end)

def generate_banner(icon: str, text: str, gap: int = 3) -> str:
    icon_lines = icon.strip("\n").splitlines()
    text_lines = text.strip("\n").splitlines()

    icon_width = max(len(l) for l in icon_lines)
    text_width = max(len(l) for l in text_lines)
    icon_height = len(icon_lines)
    text_height = len(text_lines)

    height = max(icon_height, text_height)
    icon_top = (height - icon_height) // 2
    text_top = (height - text_height) // 2

    icon_lines = [""] * icon_top + icon_lines + [""] * (height - icon_top - icon_height)
    text_lines = [""] * text_top + text_lines + [""] * (height - text_top - text_height)

    banner_width = icon_width + gap + text_width
    term_width = os.get_terminal_size().columns
    left_pad = max(0, (term_width - banner_width) // 2)

    banner = Colors.GOLD
    for il, tl in zip(icon_lines, text_lines):
        banner += f"{' ' * left_pad}{il.ljust(icon_width)}{' ' * gap}{tl}\n"
    banner += Colors.RESET

    return banner

def drive_example(label: str) -> str:
    if CURRENT_OS == "Linux":
        return f"/run/media/user/{label}" # meh i think this is most used mount point in most DE
    elif CURRENT_OS == "Darwin":
        return f"/Volumes/{label}"
    else:
        return "D:\\ or E:\\"


def banner():
    print("\n" + generate_banner(ICON, TITLE, gap=0))
    cprint(f"Cross-platform installation wizard v{VERSION}\n", Colors.CYAN)

def ask_path(label: str, example: str = "") -> str:
    cprint(f"\n* Drive needed: {label}", Colors.YELLOW)
    if example:
        cprint(f"   Example for {CURRENT_OS}: {example}", Colors.BLUE)

    while True:
        path = input(f"   Path to {label}: ").strip()
        if not path:
            cprint("   Please enter a valid path.", Colors.RED)
            continue

        path = path.strip('"').strip("'")
        if not os.path.isdir(path):
            cprint(f"   - Directory not found: {path}", Colors.RED)
        else:
            cprint(f"   + {label} found at {path}", Colors.GREEN)
            return path

def board_selection() -> tuple:
    cprint("\n* Select your Pico board:", Colors.MAGENTA)
    for idx, (name, _, boot_label) in BOARDS.items():
        cprint(f"   {idx}) {name:<8}  (BOOTSEL drive: {boot_label})", Colors.GREEN)

    choice = 0
    while choice not in BOARDS:
        try:
            choice = int(input("Enter choice (1-4): ").strip())
        except ValueError:
            pass

    name, fw, label = BOARDS[choice]
    return choice, name, fw, label

def copy_file_verbose(src: Path, dst_dir: str):
    shutil.copy2(src, dst_dir)
    cprint(f"   + Copied {src.name}", Colors.GREEN)

def copy_directory_verbose(src: Path, dst_dir: Path):
    count = 0
    for item in src.rglob("*"):
        relative = item.relative_to(src)
        target = dst_dir / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            shutil.copy2(item, target)
            count += 1
    cprint(f"   + Installed {count} files from {src.name}", Colors.GREEN)

def wait_for_enter(message="Press Enter to continue..."):
    input(f"\n{Colors.YELLOW}{message}{Colors.RESET}")

def prechecks():
    cprint("* Checking required folders...", Colors.CYAN)
    if not FIRMWARE_DIR.is_dir():
        cprint(f"- Missing directory: {FIRMWARE_DIR}", Colors.RED)
        sys.exit(1)

    if not SRC_DIR.is_dir():
        cprint(f"- Missing directory: {SRC_DIR}", Colors.RED)
        sys.exit(1)

    for fname in [b[1] for b in BOARDS.values()]:
        if not (FIRMWARE_DIR / fname).exists():
            cprint(f"- Missing firmware file: {fname}", Colors.RED)
            sys.exit(1)

    cprint("+ All required folders and firmware files are present.\n", Colors.GREEN)

def main():
    banner()
    prechecks()

    _ , board_name, firmware_file, boot_label = board_selection()
    cprint(f"\n+ Selected board: {board_name}", Colors.CYAN)
    cprint(f"   Its BOOTSEL drive will appear as: {Colors.BOLD}{boot_label}{Colors.RESET}", Colors.CYAN)
    cprint("\n!! IMPORTANT", Colors.RED)
    cprint("This tool is for educational and ethical use only. You are responsible for your own actions.\n", Colors.YELLOW)
    cprint("The installation will erase all existing data on your Pico.", Colors.RED)
    agree = input("Type 'yes' to continue: ").strip().lower()

    if agree != "yes" and agree != 'y':
        cprint("Installation cancelled.", Colors.RED)
        sys.exit(0)

    # NUKE IT 
    cprint("\n" + "=" * 50, Colors.CYAN)
    cprint("STEP 1: Flash Nuke (wipe the board)", Colors.GOLD)
    cprint("="*50, Colors.CYAN)
    cprint("* BOOTSEL INSTRUCTIONS:", Colors.YELLOW)
    cprint("    1. Connect your Pico to USB while holding the BOOTSEL button.", Colors.BLUE)
    cprint("    2. Hold for 3 seconds, then release.", Colors.BLUE)
    cprint(f"   3. The board will appear as a drive named {Colors.BOLD}'{boot_label}'.\n", Colors.BLUE)
    wait_for_enter("Press Enter when you see the drive...")

    rp_path = ask_path(boot_label, example=drive_example(boot_label))
    nuke_uf2 = FIRMWARE_DIR / "flash_nuke_all_boards.uf2"
    copy_file_verbose(nuke_uf2, rp_path)

    cprint("\n* Nuke copied. The board will restart back into BOOTSEL mode.", Colors.YELLOW)
    cprint(f"   (If it doesn't, reconnect while holding BOOTSEL – it should appear as '{Colors.BOLD}{boot_label}'{Colors.BLUE} again.)", Colors.BLUE)
    wait_for_enter("Press Enter after the board reboots...")

    # Flash CircuitPython 
    cprint("\n" + "=" * 50, Colors.CYAN)
    cprint("STEP 2: Flash CircuitPython", Colors.GOLD)
    cprint("="*50, Colors.CYAN)
    cprint(f"The board should now show up as '{boot_label}' again.\n", Colors.BLUE)

    rp_path2 = ask_path(boot_label, example=drive_example(boot_label))
    firmware_path = FIRMWARE_DIR / firmware_file
    copy_file_verbose(firmware_path, rp_path2)

    cprint("\n* CircuitPython firmware copied. The board will reboot into 'CIRCUITPY'.", Colors.YELLOW)
    wait_for_enter("Press Enter when you see the CIRCUITPY drive...")

    # Copy OverQuack source
    cprint("\n" + "=" * 50, Colors.CYAN)
    cprint("STEP 3: Copy OverQuack files", Colors.GOLD)
    cprint("="*50, Colors.CYAN)
    cprint("The board should now appear as 'CIRCUITPY'.\n", Colors.BLUE)

    circuitpy_path = ask_path("CIRCUITPY", example=drive_example("CIRCUITPY"))
    copy_directory_verbose(SRC_DIR, Path(circuitpy_path))

    # done
    cprint("\n" + "=" * 50, Colors.CYAN)
    cprint("+ Installation complete!", Colors.GREEN)
    cprint("="*50, Colors.CYAN)
    cprint("Your OverQuack is ready. Disconnect and reconnect to use it.", Colors.CYAN)
    cprint("Happy (ethical) hacking! 🦆", Colors.GOLD)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n\nInstallation cancelled by user.", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n- An unexpected error occurred: {e}", Colors.RED)
        sys.exit(1)
