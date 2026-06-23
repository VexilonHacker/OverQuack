#!/usr/bin/env python3

import argparse, json, os, socket, sys

from pathlib import Path
from typing import List, Optional, Callable, Dict
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from rich_argparse import RichHelpFormatter

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

                                                                            Made by VexilonHacker (⌐■_■)
"""

DEFAULT_HOST = "10.10.5.1"
DEFAULT_PORT = 1084
DEFAULT_TIMEOUT = 10


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



console = Console()

# tcp client for overquack tcp protocol
class OverQuackClient:
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, debug: bool = True):
        self.host = host
        self.port = port
        self.debug = debug
        self.sock: Optional[socket.socket] = None

    def _cprint(self, msg: str, color=Colors.GREEN, end="\n"):
        if not self.debug:
            return
        print(f"{color}{msg}{Colors.RESET}", end=end)

    def connect(self) -> bool:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(DEFAULT_TIMEOUT)
            self.sock.connect((self.host, self.port))
            self._cprint(f"[CONNECTED] {self.host}:{self.port}", Colors.CYAN)
            return True

        except Exception as e:
            if self.sock:
                self.sock.close()
                self.sock = None

            self._cprint(f"[ERROR] Connection failed: {e}", Colors.RED)
            return False

    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()

            except Exception:
                pass
            self.sock = None

        self._cprint("[DISCONNECTED]", Colors.CYAN)

    def is_connected(self) -> bool:
        return self.sock is not None

    def _send_line(self, line: str):
        self._cprint(f"[SEND] {line}", Colors.BLUE)
        self.sock.sendall((line + "\n").encode())

    def _recv_line(self) -> str:
        buf = bytearray()
        while True:
            ch = self.sock.recv(1)
            if not ch:
                raise ConnectionError("Connection closed while reading line")
            if ch == b"\n":
                break
            buf.extend(ch)

        line = buf.decode(errors="replace") # replace any corrupted byte error char
        self._cprint(f"[HEADER] {line}", Colors.MAGENTA)
        return line

    def _recv_exact(self, size: int, progress_cb=None) -> bytes:
        buf = bytearray()
        remaining = size
        while remaining > 0:
            chunk = self.sock.recv(min(remaining, 4096))
            if not chunk:
                raise ConnectionError("Connection closed during payload")
            buf.extend(chunk)
            remaining -= len(chunk)
            if progress_cb:
                progress_cb(size - remaining, size)
        return bytes(buf)

    def _recv_packet_bytes(self, progress_cb=None) -> bytes:
        header = self._recv_line()
        if not header.startswith("SIZE "):
            raise RuntimeError(f"Unexpected header: {header}")
        try:
            size = int(header.split()[1])
        except ValueError:
            raise RuntimeError(f"Bad SIZE header: {header}")
        return self._recv_exact(size, progress_cb)

    def _recv_packet_text(self, progress_cb=None) -> str:
        payload = self._recv_packet_bytes(progress_cb)
        self._cprint(f"[PAYLOAD] {len(payload)} bytes", Colors.GOLD)
        return payload.decode(errors="replace")

    def _run_simple_cmd(self, cmd: str) -> str:
        self._send_line(cmd)
        return self._recv_packet_text()

    def free_mem(self) -> str:
        return self._run_simple_cmd("FREE_MEM")

    def ping(self) -> str:
        return self._run_simple_cmd("PING")

    def help(self) -> str:
        return self._run_simple_cmd("HELP")

    def version(self) -> str:
        return self._run_simple_cmd("VERSION")

    def get_config(self) -> str:
        return self._run_simple_cmd("GET_CONFIG")

    def wifi_scan(self) -> str:
        return self._run_simple_cmd("WIFI_SCAN")

    def list_files(self) -> List[str]:
        return self._run_simple_cmd("LS").splitlines()

    def list_payloads(self) -> List[str]:
        return self._run_simple_cmd("PAYLOADS").splitlines()

    def read_file(self, filename: str) -> str:
        self._send_line(f"READ {filename}")
        return self._recv_packet_text()

    def delete_file(self, filename: str) -> str:
        return self._run_simple_cmd(f"DELETE {filename}")

    def run_payload(self, filename: str) -> str:
        self._send_line(f"RUN {filename}")
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(None)
        try:
            return self._recv_packet_text()
        finally:
            self.sock.settimeout(old_timeout)

    def write_file(self, filename: str, content: bytes) -> str:
        mem = self.free_mem()
        self._cprint(f"[FREE_MEM] {mem}", Colors.CYAN)

        self._send_line(f"WRITE {filename} {len(content)}")
        ready = self._recv_packet_text()
        if not ready.startswith("READY WRITE"):
            raise RuntimeError(f"Server refused write: {ready}")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Uploading {filename}...", total=len(content))
            sent = 0
            chunk_size = 4096
            while sent < len(content):
                chunk = content[sent : sent + chunk_size]
                self.sock.sendall(chunk)
                sent += len(chunk)
                progress.update(task, completed=sent)

        return self._recv_packet_text()

    def reboot(self, mode: str = "NORMAL") -> str:
        cmd_map = {"NORMAL": "REBOOT", "UF2": "REBOOT_UF2", "SAFE": "REBOOT_SAFE"}
        self._send_line(cmd_map.get(mode.upper(), "REBOOT"))
        try:
            return self._recv_packet_text()
        except ConnectionError:
            return "Board rebooting (connection closed)"

    def format_disk(self, force: bool = False) -> str:
        self._send_line("FORMAT")
        resp = self._recv_packet_text()
        if force:
            self._send_line("FORMAT_CONFIRM")
            try:
                return self._recv_packet_text()
            except ConnectionError:
                return "Format triggered – board resetting."
        return resp

    def format_confirm(self) -> str:
        self._send_line("FORMAT_CONFIRM")
        try:
            return self._recv_packet_text()
        except ConnectionError:
            return "Format triggered – board resetting."


# shell mode 
class OverQuackShell:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = OverQuackClient(host, port, debug=False)
        self.connected = False
        self.format_waiting = False
        self._setup_prompt()
        self._build_command_map()

    def _setup_prompt(self):
        self.static_commands = [
            "connect", "disconnect", "exit", "quit",
            "free_mem", "ping", "help", "ls", "payloads",
            "read", "delete", "run", "write",
            "version", "get_config", "wifi_scan",
            "reboot", "reboot_uf2", "reboot_safe",
            "format", "format_confirm", "local_ls",
        ]
        history_file = Path.home() / ".overquack_history"
        kb = KeyBindings()

        @kb.add("c-c")
        def _(event):
            raise KeyboardInterrupt

        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=WordCompleter(self.static_commands, ignore_case=False, sentence=True),
            style=Style.from_dict({"prompt": "bold"}),
            key_bindings=kb,
        )

    def _build_command_map(self):
        self.command_map: Dict[str, Callable] = {
            "connect":       self._cmd_connect,
            "disconnect":    self._cmd_disconnect,
            "free_mem":      lambda _: self._generic("free_mem"),
            "ping":          lambda _: self._generic("ping"),
            "help":          lambda _: self._show_help(),
            "ls":            lambda _: self._generic("ls"),
            "payloads":      lambda _: self._generic("payloads"),
            "read":          self._cmd_read,
            "delete":        self._cmd_delete,
            "run":           self._cmd_run,
            "write":         self._cmd_write,
            "version":       lambda _: self._generic("version"),
            "get_config":    lambda _: self._generic("get_config"),
            "wifi_scan":     lambda _: self._generic("wifi_scan"),
            "reboot":        lambda args: self._cmd_reboot(args, "NORMAL"),
            "reboot_uf2":    lambda _: self._cmd_reboot([], "UF2"),
            "reboot_safe":   lambda _: self._cmd_reboot([], "SAFE"),
            "format":        self._cmd_format,
            "format_confirm":self._cmd_format_confirm,
            "local_ls":      lambda _: self._local_ls(),
        }

    def require_connection(func):
        def wrapper(self, *args, **kwargs):
            if not self.connected:
                console.print("[red]Not connected[/red]")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def _cmd_connect(self, args: List[str]):
        if args:
            self.host = args[0]
            if len(args) > 1:
                try:
                    self.port = int(args[1])
                except ValueError:
                    console.print("[red]Invalid port number[/red]")
                    return
        self.client.disconnect()
        self.connected = False
        self.format_waiting = False
        self.client.host = self.host
        self.client.port = self.port

        with console.status(f"[cyan]Connecting to {self.host}:{self.port}..."):
            if self.client.connect():
                self.connected = True
                console.print(f"[green]+ Connected to {self.host}:{self.port}[/green]")
                self._update_completer()
            else:
                console.print(f"[red]* Could not connect to {self.host}:{self.port}[/red]")

    def _cmd_disconnect(self, args: List[str] = None):
        self.client.disconnect()
        self.connected = False
        self.format_waiting = False
        console.print("[yellow]Disconnected[/yellow]")

    def _update_completer(self):
        if self.connected:
            try:
                payloads = self.client.list_payloads()
            except Exception:
                payloads = []
            self.session.completer = WordCompleter(
                self.static_commands + payloads, ignore_case=False, sentence=True
            )

    @require_connection
    def _cmd_write(self, args: List[str]):
        if len(args) < 1:
            console.print("[red]Usage: write <remote_filename> [local_file][/red]")
            console.print("[yellow]Tip: Upload a local file: write remote.txt local.txt[/yellow]")
            console.print("[yellow]Or enter content interactively (Ctrl+D to finish).[/yellow]")
            return
        filename = args[0]
        if len(args) >= 2:
            # local file path given
            try:
                with open(args[1], "rb") as f:
                    content = f.read()
            except Exception as e:
                console.print(f"[red]Failed to read local file: {e}[/red]")
                return
        else:
            # interactive multiline input
            from prompt_toolkit import prompt as ptprompt
            console.print("[yellow]Enter payload content. Press Ctrl+D on a new line to finish.[/yellow]")
            try:
                content_str = ptprompt("", multiline=True)
            except EOFError:
                console.print("[red]Input aborted[/red]")
                return
            content = content_str.encode()
        try:
            resp = self.client.write_file(filename, content)
            console.print(f"[orange1]{resp}[/orange1]")
            self._update_completer()
        except Exception as e:
            console.print(f"[red]Write failed: {e}[/red]")

    @require_connection
    def _cmd_read(self, args: List[str]):
        if len(args) < 1:
            console.print("[red]Usage: read <filename>[/red]")
            return
        filename = args[0]
        try:
            content = self.client.read_file(filename)
            ext = os.path.splitext(filename)[1].lstrip(".")
            lexer = ext if ext else "text"
            syntax = Syntax(content, lexer, theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"📄 {filename}", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Read failed: {e}[/red]")

    @require_connection
    def _cmd_run(self, args: List[str]):
        if len(args) < 1:
            console.print("[red]Usage: run <payload>[/red]")
            return
        filename = args[0]
        console.print(f"[yellow]Running {filename}...[/yellow]")
        try:
            output = self.client.run_payload(filename)
            console.print(Panel(output, title=f"🏃 {filename}", border_style="green"))
        except Exception as e:
            console.print(f"[red]Run failed: {e}[/red]")

    @require_connection
    def _cmd_delete(self, args: List[str]):
        if len(args) < 1:
            console.print("[red]Usage: delete <filename>[/red]")
            return
        try:
            resp = self.client.delete_file(args[0])
            console.print(f"[orange1]{resp}[/orange1]")
            self._update_completer()
        except Exception as e:
            console.print(f"[red]Delete failed: {e}[/red]")

    @require_connection
    def _cmd_reboot(self, args: List[str], mode: str):
        try:
            resp = self.client.reboot(mode)
            console.print(f"[orange1]{resp}[/orange1]")
        except Exception as e:
            console.print(f"[red]Reboot failed: {e}[/red]")
        finally:
            self.client.disconnect()
            self.connected = False
            self.format_waiting = False

    def _cmd_format(self, args: List[str]):
        if not self.connected:
            console.print("[red]Not connected[/red]")
            return
        force = "--force" in args
        if self.format_waiting and not force:
            # cancel pending format
            self.format_waiting = False
            console.print("[yellow]Format cancelled.[/yellow]")
            try:
                self.client._send_line("FORMAT")
                self.client._recv_packet_text()
            except Exception:
                pass
            return
        resp = self.client.format_disk(force=force)
        if "WARNING" in resp and not force:
            self.format_waiting = True
            console.print(Panel(resp, title="!!  FORMAT", border_style="red"))
            console.print("[yellow]Type [bold]format_confirm[/bold] to proceed or [bold]format[/bold] again to cancel.[/yellow]")
        else:
            console.print(f"[orange1]{resp}[/orange1]")
            if "triggered" in resp.lower():
                self.client.disconnect()
                self.connected = False
                self.format_waiting = False

    def _cmd_format_confirm(self, args: List[str] = None):
        if not self.format_waiting:
            console.print("[red]No pending format. Send [bold]format[/bold] first.[/red]")
            return
        self._cmd_format(["--force"])

    def _local_ls(self):
        files = sorted(os.listdir("."))
        table = Table(title="📁 Local Directory")
        table.add_column("Files", style="cyan")
        for f in files:
            table.add_row(f)
        console.print(table)

    def _show_help(self):
        if self.connected:
            result = self.client.help()
            console.print(f"[orange1]{result}[/orange1]")
        console.print("\n[bold cyan]Client tips:[/bold cyan]")
        console.print("[yellow]  write <remote> <local>[/yellow] – upload a local file")
        console.print("[yellow]  local_ls[/yellow] – list files in current local directory")
        console.print("[yellow]  connect <host> [port][/yellow] – reconnect to a different device")

    @require_connection
    def _generic(self, cmd: str):
        try:
            if cmd == "ls":
                lines = self.client.list_files()
                if not lines:
                    console.print("[dim]Empty[/dim]")
                    return
                table = Table()
                table.add_column("Files", style="cyan")
                for line in lines:
                    table.add_row(line)
                console.print(table)

            elif cmd == "payloads":
                lines = self.client.list_payloads()
                if not lines:
                    console.print("[dim]Empty[/dim]")
                    return
                table = Table()
                table.add_column("Payloads", style="cyan")
                for line in lines:
                    table.add_row(line)
                console.print(table)

            elif cmd == "get_config":
                raw = self.client.get_config()
                try:
                    parsed = json.loads(raw)
                    from rich.json import JSON
                    console.print(Panel(JSON.from_data(parsed), title="⚙️ Config", border_style="blue"))
                except Exception:
                    console.print(Panel(raw, title="⚙️ Config (raw)", border_style="red"))

            elif cmd == "wifi_scan":
                raw = self.client.wifi_scan()
                lines = raw.splitlines()
                colored_lines = []
                for line in lines:
                    if line.startswith("SSID"):
                        colored_lines.append(f"[bold cyan]{line}[/bold cyan]")
                    elif line.startswith("BSSID"):
                        colored_lines.append(f"[yellow]{line}[/yellow]")
                    elif line.startswith("RSSI"):
                        colored_lines.append(f"[green]{line}[/green]")
                    elif line.startswith("CHANNEL"):
                        colored_lines.append(f"[magenta]{line}[/magenta]")
                    elif line.startswith("COUNTRY"):
                        colored_lines.append(f"[blue]{line}[/blue]")
                    elif line.startswith("AUTH"):
                        auth = line.split(":")[1].strip()
                        if auth == "OPEN":
                            colored_lines.append(f"[red]{line}[/red]")
                        else:
                            colored_lines.append(f"[orange1]{line}[/orange1]")
                    else:
                        colored_lines.append(line)
                console.print(Panel("\n".join(colored_lines), title="📡 Wi-Fi Scan", border_style="blue"))

            else:
                method = getattr(self.client, cmd)
                if not callable(method):
                    console.print(f"[red]Unknown internal command: {cmd}[/red]")
                    return
                result = method()
                console.print(f"[orange1]{result}[/orange1]")

        except Exception as e:
            console.print(f"[red]Command failed: {e}[/red]")

    def run(self):
        console.print(
            "[bold cyan]OverQuack Interactive Shell[/bold cyan]\n"
            f"Target: {self.host}:{self.port}\n"
            "Type [yellow]help[/yellow] for commands, [yellow]exit[/yellow] to quit.\n"
            "Auto-connects on startup.",
        )
        self._cmd_connect([])

        while True:
            try:
                prompt = "🦆 overquack >> " if self.connected else "🔌 overquack >> "
                user_input = self.session.prompt(prompt)
                if user_input is None:
                    break
                if not user_input.strip():
                    continue
            except EOFError:
                break
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting...[/yellow]")
                break

            parts = user_input.strip().split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ("exit", "quit"):
                self.client.disconnect()
                console.print("[yellow]Goodbye! (˶˃ ᵕ ˂˶)[/yellow]")
                break

            handler = self.command_map.get(cmd)
            if handler:
                handler(args)
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
                console.print(
                    "Available: connect, disconnect, free_mem, ping, help, ls, payloads, "
                    "read, delete, run, write, version, get_config, wifi_scan, "
                    "reboot, reboot_uf2, reboot_safe, format, exit, local_ls"
                )


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

    banner = "\033[38;2;255;215;0m"  # gold
    for il, tl in zip(icon_lines, text_lines):
        banner += f"{' ' * left_pad}{il.ljust(icon_width)}{' ' * gap}{tl}\n"
    banner += "\033[0m"
    return banner

def one_shot_mode(args: argparse.Namespace):
    client = OverQuackClient(args.host, args.port, debug=True)
    if not client.connect():
        sys.exit(1)

    try:
        cmd = args.command
        if cmd == "free_mem":
            result = client.free_mem()
        elif cmd == "ping":
            result = client.ping()
        elif cmd == "help":
            result = client.help()
        elif cmd == "ls":
            result = "\n".join(client.list_files())
        elif cmd == "payloads":
            result = "\n".join(client.list_payloads())
        elif cmd == "read":
            result = client.read_file(args.filename)
        elif cmd == "delete":
            result = client.delete_file(args.filename)
        elif cmd == "run":
            result = client.run_payload(args.filename)
        elif cmd == "write":
            content = None
            # priority: --file > --content > stdin pipe
            if args.file:
                with open(args.file, "rb") as f:
                    content = f.read()
            elif args.content is not None:
                content = args.content.encode()
            elif not sys.stdin.isatty():
                content = sys.stdin.buffer.read()
            else:
                console.print("[red]No content provided. Use --content, --file, or pipe data.[/red]")
                sys.exit(1)
            result = client.write_file(args.filename, content)
            console.print(f"[orange1]{result}[/orange1]")
            return
        elif cmd == "version":
            result = client.version()
        elif cmd == "get_config":
            result = client.get_config()
            try:
                parsed = json.loads(result)
                result = json.dumps(parsed, indent=2)
            except Exception:
                pass
        elif cmd == "wifi_scan":
            result = client.wifi_scan()
        elif cmd in ("reboot", "reboot_uf2", "reboot_safe"):
            mode = "NORMAL"
            if cmd == "reboot_uf2":
                mode = "UF2"
            elif cmd == "reboot_safe":
                mode = "SAFE"
            result = client.reboot(mode)
        elif cmd == "format":
            if args.force:
                result = client.format_disk(force=True)
            else:
                result = client.format_disk(force=False)
                if "WARNING" in result:
                    console.print(result)
                    confirm = input("Type 'yes' to confirm format: ").strip().lower()
                    if confirm == "yes":
                        result = client.format_confirm()
                    else:
                        result = "Aborted."
        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")
            sys.exit(1)

        console.print(f"[orange1]{result}[/orange1]")

    except Exception as e:
        console.print(f"[red]Error: {type(e).__name__}: {e}[/red]")
    finally:
        client.disconnect()


def main():
    parser = argparse.ArgumentParser(
        description="OverQuack TCP Client",
        formatter_class=RichHelpFormatter,
        usage="%(prog)s [-h] [--host HOST] [--port PORT] COMMAND",
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Device IP")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port")
    parser.add_argument("--no-banner", action="store_true", help="Suppress the animated banner")

    sub = parser.add_subparsers(dest="command")

    for cmd in (
        "free_mem", "ping", "help", "ls", "payloads",
        "version", "get_config", "wifi_scan",
        "reboot", "reboot_uf2", "reboot_safe",
    ):
        sub.add_parser(cmd, help=f"Run {cmd} command", formatter_class=RichHelpFormatter)

    for cmd in ("read", "delete", "run"):
        p = sub.add_parser(cmd, help=f"Perform {cmd} on a file", formatter_class=RichHelpFormatter)
        p.add_argument("filename", help="Target file")

    write_parser = sub.add_parser("write", help="Upload a file", formatter_class=RichHelpFormatter)
    write_parser.add_argument("filename", help="Remote filename")
    content_group = write_parser.add_mutually_exclusive_group()
    content_group.add_argument("--content", help="Literal text content to upload")
    content_group.add_argument("--file", help="Local file to upload")

    format_parser = sub.add_parser("format", help="Format device (erases everything)", formatter_class=RichHelpFormatter)
    format_parser.add_argument("--force", action="store_true", help="Skip confirmation")

    args = parser.parse_args()

    if not args.no_banner: 
        print("\n" + generate_banner(ICON, TITLE))


    if args.command is None:
        shell = OverQuackShell(args.host, args.port)
        try:
            shell.run()
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/yellow]")
        except Exception as e:
            console.print(f"[red]Fatal error: {e}[/red]")
    else:
        one_shot_mode(args)


if __name__ == "__main__":
    main()
