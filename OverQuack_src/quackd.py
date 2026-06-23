# quackd.py – CircuitPython 10.2.1 TCP server with detailed debug

import asyncio, gc, os, supervisor, microcontroller, sys, json, wifi, socketpool

from storage import remount
from overquackify import LoadJsonConf, runScript
from overquackify import VERSION

RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[97m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"

DEBUG_PROTOCOL = True
DEBUG_STATE = True

PROTECTED_FILES = (
    "boot.py",
    "code.py",
    "config.json",
    "overquackify.py",
    "quackd.py",
    "settings.toml",
)

CheckMemory = False

def cprint(msg, color=WHITE):
    print(f"{color}{msg}{RESET}")

def info(msg):
    cprint(msg, BRIGHT_GREEN)

def warn(msg):
    cprint(msg, BRIGHT_YELLOW)

def err(msg):
    cprint(msg, BRIGHT_RED)

def dump_previous_traceback():
    try:
        tb = supervisor.get_previous_traceback()
        if tb:
            cprint("[PREVIOUS TRACEBACK DETECTED]", BRIGHT_RED)
            print(tb)
    except Exception as e:
        cprint("Could not read previous traceback: {}".format(repr(e)), BRIGHT_RED)


def log_exception(context, exc):
    cprint("[EXCEPTION] {}".format(context), BRIGHT_RED)
    cprint("Type: {}".format(type(exc)), BRIGHT_RED)
    cprint("Value: {}".format(repr(exc)), BRIGHT_RED)

def safe_decode(b):
    try:
        return b.decode()
    except Exception:
        try:
            return str(b)
        except Exception:
            return ""


def read_config():
    cfg = LoadJsonConf()
    if DEBUG_STATE:
        cprint("[CONFIG] loaded", BRIGHT_CYAN)
        try:
            cprint("[CONFIG] DEFAULT_PAYLOAD = {}".format(cfg.get("DEFAULT_PAYLOAD", "?")), BRIGHT_CYAN)
            ap = cfg.get("AP", {})
            cprint("[CONFIG] AP.ip_address = {}".format(ap.get("ip_address", "?")), BRIGHT_CYAN)
            cprint("[CONFIG] AP.ports = {}".format(ap.get("ports", [])), BRIGHT_CYAN)
        except Exception as e:
            cprint("[CONFIG] debug print failed: {}".format(repr(e)), BRIGHT_RED)
    return cfg

config = read_config()

def check_exists(filename):
    return filename.strip() in os.listdir()

def sock_recv(sock, max_bytes=1024):
    buf = bytearray(max_bytes)
    try:
        n = sock.recv_into(buf)
        if n == 0:
            return b""
        return bytes(buf[:n])
    except OSError as e:
        errno = getattr(e, "errno", None)
        if errno == 11:
            return None
        if errno == 9:
            return b""
        raise


class TCPServer:
    def __init__(self, port=80):
        self.port = port
        self.pool = socketpool.SocketPool(wifi.radio)
        self.server_sock = None
        self.client_sock = None
        self.client_addr = None
        self.read_buffer = b""
        self.pending_write = None

    def log(self, msg, color=WHITE):
        cprint("[TCP] {}".format(msg), color)

    def state_log(self, msg, color=BRIGHT_BLACK):
        if DEBUG_STATE:
            cprint("[STATE] {}".format(msg), color)

    def protocol_log(self, msg, color=BRIGHT_CYAN):
        if DEBUG_PROTOCOL:
            cprint("[PROTO] {}".format(msg), color)

    def close_client(self, reason=None):
        if reason:
            self.log("closing client: {}".format(reason), BRIGHT_YELLOW)

        if self.client_sock:
            try:
                self.client_sock.close()
            except Exception as e:
                self.log("client close failed: {}".format(repr(e)), BRIGHT_RED)

        self.client_sock = None
        self.client_addr = None
        self.read_buffer = b""
        self.pending_write = None

    def _send_packet_bytes(self, payload):
        if not self.client_sock:
            self.log("send called with no client", BRIGHT_RED)
            return False

        try:
            if isinstance(payload, str):
                payload = payload.encode()

            header = "SIZE {}\n".format(len(payload)).encode()

            self.client_sock.sendall(header)
            self.client_sock.sendall(payload)

            self.protocol_log(
                "packet sent size={} bytes".format(len(payload)),
                BRIGHT_MAGENTA,
            )
            return True

        except Exception as e:
            self.log("send error: {}".format(repr(e)), BRIGHT_RED)
            log_exception("send packet", e)
            self.close_client("send failed")
            return False

    def _send_packet_text(self, text):
        return self._send_packet_bytes(text.encode())

    def _send_file_packet(self, filename):
        if not self.client_sock:
            self.log("send_file_packet called with no client", BRIGHT_RED)
            return False

        try:
            size = os.stat(filename)[6]
        except Exception as e:
            self.log("stat failed for {}: {}".format(filename, repr(e)), BRIGHT_RED)
            self._send_packet_text("ERROR: cannot stat file: {}".format(filename))
            return False

        try:
            self.client_sock.sendall("SIZE {}\n".format(size).encode())

            sent = 0
            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    self.client_sock.sendall(chunk)
                    sent += len(chunk)
                    self.protocol_log(
                        "streamed file {} {}/{} bytes".format(filename, sent, size),
                        BRIGHT_MAGENTA,
                    )

            self.protocol_log(
                "file packet sent {} size={} bytes".format(filename, size),
                BRIGHT_MAGENTA,
            )
            return True

        except Exception as e:
            self.log("file send error: {}".format(repr(e)), BRIGHT_RED)
            log_exception("send file packet", e)
            self.close_client("file send failed")
            return False

    def start(self):
        self.server_sock = self.pool.socket(self.pool.AF_INET, self.pool.SOCK_STREAM)
        self.server_sock.setsockopt(self.pool.SOL_SOCKET, self.pool.SO_REUSEADDR, 1)
        self.server_sock.bind(("0.0.0.0", self.port))
        self.server_sock.listen(1)
        self.server_sock.setblocking(False)

        try:
            ip = wifi.radio.ipv4_address_ap
        except Exception:
            ip = "0.0.0.0"

        self.log("listening on {}:{}".format(ip, self.port), BRIGHT_GREEN)

    def accept_if_needed(self):
        if self.client_sock:
            return

        try:
            self.client_sock, self.client_addr = self.server_sock.accept()
            self.client_sock.setblocking(False)
            self.read_buffer = b""
            self.pending_write = None
            self.format_pending = False

            free_ram = gc.mem_free()
            used_ram = gc.mem_alloc()
            total_ram = free_ram + used_ram
            self.log(
                "connection from {} FREE_RAM/TOTAL_AVAILABLE_RAM: {:.1f}KB/{:.1f}KB".format(
                    self.client_addr,
                    free_ram / 1024,
                    total_ram / 1024
                ),
                BRIGHT_GREEN
            )

        except OSError as e:
            errno = getattr(e, "errno", None)
            if errno != 11:
                self.log("accept error: {}".format(repr(e)), BRIGHT_RED)
                log_exception("accept", e)

    def looks_like_http(self, line):
        u = line.upper()
        return (
            u.startswith("GET ")
            or u.startswith("POST ")
            or u.startswith("HEAD ")
            or u.startswith("HTTP/")
            or u.startswith("HOST:")
            or u.startswith("USER-AGENT:")
            or u.startswith("ACCEPT:")
            or u.startswith("CONNECTION:")
            or u.startswith("UPGRADE-INSECURE-REQUESTS:")
        )

    def _cleanup_partial_write(self, delete_file=True):
        state = self.pending_write
        if not state:
            return

        f = state.get("file")
        filename = state.get("filename")

        try:
            if f:
                f.close()
        except Exception as e:
            self.log("partial file close failed: {}".format(repr(e)), BRIGHT_RED)

        if delete_file and filename:
            try:
                remount("/", readonly=False)
                try:
                    if check_exists(filename):
                        os.remove(filename)
                finally:
                    remount("/", readonly=True)
            except Exception as e:
                self.log("partial file delete failed: {}".format(repr(e)), BRIGHT_RED)

        self.pending_write = None

    def write_begin(self, filename, size):
        global CheckMemory

        try:
            remount("/", readonly=False)
            f = open(filename, "wb")

        except Exception as e:
            try:
                remount("/", readonly=True)
            except Exception:
                pass

            self.log("write begin failed: {}".format(repr(e)), BRIGHT_RED)
            log_exception("write_begin", e)

            msg = repr(e)

            if "visible via USB" in msg:
                self._send_packet_text(
                    "ERROR: USB storage is mounted on host. Disconnect USB and retry."
                )
            else:
                self._send_packet_text(
                    "ERROR opening file: {}".format(msg)
                )

            return False
        self.pending_write = {
            "filename": filename,
            "size": size,
            "remaining": size,
            "file": f,
        }

        self.state_log(
            "write begun: file={} size={}".format(filename, size),
            BRIGHT_YELLOW,
        )

        if not self._send_packet_text("READY WRITE {} {}".format(filename, size)):
            self._cleanup_partial_write(delete_file=True)
            try:
                remount("/", readonly=True)
            except Exception:
                pass
            CheckMemory = False
            return False

        return True

    def write_service(self):
        global CheckMemory

        if not self.pending_write:
            return True

        if not self.client_sock:
            self.log("pending write without client", BRIGHT_RED)
            self._cleanup_partial_write(delete_file=True)
            CheckMemory = False
            return True

        state = self.pending_write
        expected = state["size"]
        remaining = state["remaining"]
        f = state["file"]

        try:
            # Consume buffered bytes first
            if self.read_buffer:
                take = min(remaining, len(self.read_buffer))
                if take > 0:
                    f.write(self.read_buffer[:take])
                    self.read_buffer = self.read_buffer[take:]
                    remaining -= take
                    state["remaining"] = remaining

                    self.state_log(
                        "write buffered progress: {}/{} bytes".format(
                            expected - remaining, expected
                        ),
                        BRIGHT_BLUE,
                    )

            # Then read from socket
            while remaining > 0:
                more = sock_recv(self.client_sock, min(1024, remaining))

                if more is None:
                    return False

                if more == b"":
                    self.log("client disconnected during WRITE", BRIGHT_RED)
                    self._cleanup_partial_write(delete_file=True)
                    try:
                        remount("/", readonly=True)
                    except Exception:
                        pass
                    CheckMemory = False
                    self.close_client("disconnect during WRITE")
                    return True

                f.write(more)
                remaining -= len(more)
                state["remaining"] = remaining

                self.state_log(
                    "write socket progress: {}/{} bytes".format(
                        expected - remaining, expected
                    ),
                    BRIGHT_BLUE,
                )

            # Finish it
            try:
                f.close()
            except Exception as e:
                self.log("file close failed: {}".format(repr(e)), BRIGHT_RED)

            try:
                remount("/", readonly=True)
            except Exception as e:
                self.log("remount readonly restore failed: {}".format(repr(e)), BRIGHT_RED)

            self.pending_write = None
            CheckMemory = False

            self.log(
                "write complete: {} ({} bytes)".format(state["filename"], expected),
                BRIGHT_GREEN,
            )
            self._send_packet_text("WRITTEN {}".format(state["filename"]))
            return True

        except Exception as e:
            self.log("write service exception: {}".format(repr(e)), BRIGHT_RED)
            log_exception("write_service", e)

            try:
                f.close()
            except Exception:
                pass

            self._cleanup_partial_write(delete_file=True)
            try:
                remount("/", readonly=True)
            except Exception:
                pass

            CheckMemory = False
            return True

    def handle_command(self, cmd_line):
        global CheckMemory

        if not cmd_line:
            return True

        if self.looks_like_http(cmd_line):
            self.protocol_log("ignored HTTP line: {}".format(cmd_line), BRIGHT_BLACK)
            return True

        parts = cmd_line.split()
        if not parts:
            return True

        cmd = parts[0].upper()
        self.protocol_log("command received: {}".format(repr(cmd_line)), BRIGHT_CYAN)

        if cmd == "PING":
            self._send_packet_text("PONG")
            return True

        if cmd == "HELP":
            self._send_packet_text(
                "CMDS: PING HELP  FREE_MEM LS PAYLOADS READ <f> DELETE <f> "
                "RUN <f> WRITE <f> <size> REBOOT REBOOT_UF2 REBOOT_SAFE "
                "GET_CONFIG WIFI_SCAN VERSION FORMAT"
            )

            return True

        if cmd == "REBOOT":
            self._send_packet_text("REBOOTING")
            microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
            # give the client time to read the response before we reset
            self.close_client("rebooting")
            microcontroller.reset()
            return True

        if cmd == "REBOOT_UF2":
            self._send_packet_text("REBOOTING to UF2 bootloader")
            microcontroller.on_next_reset(microcontroller.RunMode.UF2)
            self.close_client("rebooting to UF2")
            microcontroller.reset()
            return True

        if cmd == "REBOOT_SAFE":
            self._send_packet_text("REBOOTING to safe mode")
            microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
            self.close_client("rebooting to safe mode")
            microcontroller.reset()
            return True


        if cmd == "FREE_MEM":
            CheckMemory = True
            mem = gc.mem_free()
            self._send_packet_text(str(mem))
            self.log("FREE_MEM -> {}".format(mem), BRIGHT_GREEN)
            return True

        if cmd == "LS":
            files = sorted(os.listdir())
            reply = "\n".join(files)
            self._send_packet_text(reply)
            self.log("LS -> {} files".format(len(files)), BRIGHT_GREEN)
            return True

        if cmd == "PAYLOADS":
            oqs = []
            for f in os.listdir():
                if f.endswith(".oqs"):
                    oqs.append(f)
            oqs = sorted(oqs)
            reply = "\n".join(oqs)
            self._send_packet_text(reply)
            self.log("PAYLOADS -> {} payloads".format(len(oqs)), BRIGHT_GREEN)
            return True

        if cmd == "READ":
            if len(parts) < 2:
                self._send_packet_text("ERROR: missing filename")
                return True

            filename = parts[1]
            if not check_exists(filename):
                self._send_packet_text("ERROR: file not found: {}".format(filename))
                self.log("READ miss: {}".format(filename), BRIGHT_RED)
                return True

            if not self._send_file_packet(filename):
                self.log("READ failed streaming: {}".format(filename), BRIGHT_RED)
            else:
                self.log("READ {} streamed".format(filename), BRIGHT_GREEN)
            return True

        if cmd == "DELETE":
            if len(parts) < 2:
                self._send_packet_text("ERROR: missing filename")
                return True

            filename = parts[1]
            if filename.lower() in PROTECTED_FILES:
                self._send_packet_text(
                    "ERROR: protected system file"
                )
                self.log(
                    "DELETE rejected protected file: {}".format(filename),
                    BRIGHT_RED
                )

                return True
            if not check_exists(filename):
                self._send_packet_text("ERROR: file not found: {}".format(filename))
                self.log("DELETE miss: {}".format(filename), BRIGHT_RED)
                return True

            try:
                remount("/", readonly=False)
                try:
                    os.remove(filename)
                    self._send_packet_text("DELETED {}".format(filename))
                    self.log("DELETE success: {}".format(filename), BRIGHT_GREEN)
                finally:
                    remount("/", readonly=True)
            except Exception as e:
                self._send_packet_text("ERROR deleting file: {}".format(repr(e)))
                self.log("DELETE failed: {} -> {}".format(filename, repr(e)), BRIGHT_RED)
                log_exception("DELETE {}".format(filename), e)
            return True

        if cmd == "RUN":
            if len(parts) < 2:
                self._send_packet_text("ERROR: missing filename")
                return True

            filename = parts[1]
            if not check_exists(filename):
                self._send_packet_text("ERROR: payload not found: {}".format(filename))
                self.log("RUN miss: {}".format(filename), BRIGHT_RED)
                return True

            if not filename.endswith(".oqs"):
                self._send_packet_text(
                    "ERROR: only .oqs files may be executed"
                )
                return True

            self.log("RUN blocking payload: {}".format(filename), BRIGHT_YELLOW)
            try:
                runScript(filename)
                self._send_packet_text("RUN_COMPLETED {}".format(filename))
                self.log("RUN completed: {}".format(filename), BRIGHT_GREEN)
            except Exception as e:
                self._send_packet_text("ERROR running payload: {}".format(repr(e)))
                self.log("RUN failed: {} -> {}".format(filename, repr(e)), BRIGHT_RED)
                log_exception("RUN {}".format(filename), e)
            return True

        if cmd == "WRITE":
            if len(parts) < 3:
                self._send_packet_text("ERROR: WRITE requires filename and size")
                self.log("WRITE rejected: missing args", BRIGHT_RED)
                return True

            if not CheckMemory:
                self._send_packet_text("ERROR: send FREE_MEM before WRITE")
                self.log("WRITE rejected: FREE_MEM not called", BRIGHT_RED)
                return True

            filename = parts[1]
            if filename.lower() in PROTECTED_FILES:
                self._send_packet_text(
                    "ERROR: protected system file"
                )
                self.log(
                    "WRITE rejected protected file: {}".format(filename),
                    BRIGHT_RED
                )
                return True
            try:
                size = int(parts[2])
            except Exception:
                self._send_packet_text("ERROR: invalid size: {}".format(parts[2]))
                self.log("WRITE rejected: invalid size {}".format(parts[2]), BRIGHT_RED)
                return True

            if size < 0:
                self._send_packet_text("ERROR: invalid size")
                return True

            self.write_begin(filename, size)
            if self.pending_write:
                self.write_service()
            return True

        if cmd == "WIFI_SCAN":
            try:
                nets = list(wifi.radio.start_scanning_networks())
                wifi.radio.stop_scanning_networks()
                lines = []
                for net in nets:
                    ssid = net.ssid if net.ssid else "<hidden>"
                    bssid = ":".join("%02X" % b for b in net.bssid)
                    rssi = net.rssi
                    channel = net.channel
                    country = net.country if net.country else "unknown"
                    authmode = net.authmode

                    lines.append("SSID    : {}".format(ssid))
                    lines.append("BSSID   : {}".format(bssid))
                    lines.append("RSSI    : {}".format(rssi))
                    lines.append("CHANNEL : {}".format(channel))
                    lines.append("COUNTRY : {}".format(country))
                    lines.append("AUTH    : {}".format(authmode))
                    lines.append("-" * 40)
                reply = "\n".join(lines) if lines else "No networks found"
                self._send_packet_text(reply)
            except Exception as e:
                self._send_packet_text("ERROR scanning: {}".format(repr(e)))
                log_exception("WIFI_SCAN", e)
            return True

        if cmd == "VERSION":
            cirpy = os.uname()
            reply = f"CircuitPython ({cirpy.version}) - OverQuack v{VERSION} - Platform {cirpy.machine}"
            self._send_packet_text(reply)
            return True

        if cmd == "GET_CONFIG":
            try:
                cfg = LoadJsonConf()
                cfg_json = json.dumps(cfg)
                self._send_packet_text(cfg_json)
                self.log("GET_CONFIG sent as JSON", BRIGHT_GREEN)
            
            except Exception as e:
                self._send_packet_text("ERROR reading config: {}".format(repr(e)))
                self.log("GET_CONFIG failed: {}".format(repr(e)), BRIGHT_RED)
            return True

        # BEWARE 
        if cmd == "FORMAT":
            if not self.format_pending:
                self.format_pending = True
                self._send_packet_text("WARNING: This will erase ALL files. Send FORMAT_CONFIRM to proceed.")
            else:
                # Already pending -> reset the flag and ask again
                self.format_pending = False
                self._send_packet_text("Confirmation timeout. Send FORMAT again if you're sure.")
            return True

        if cmd == "FORMAT_CONFIRM":
            if not self.format_pending:
                self._send_packet_text("No pending FORMAT. Send FORMAT first.")
                return True
            self.format_pending = False
            try:
                remount("/", readonly=False)
                import storage
                storage.erase_filesystem()
                # will reset automatically after erase. if not, force a reset.
                microcontroller.reset()
            except Exception as e:
                remount("/", readonly=True)
                self._send_packet_text("FORMAT failed: {}".format(repr(e)))
                log_exception("FORMAT", e)
            return True

        self._send_packet_text("ERROR: unknown command {}".format(cmd))
        self.log("unknown command: {}".format(repr(cmd_line)), BRIGHT_RED)
        return True

    def update_poll(self):
        if not self.server_sock:
            return

        if not self.client_sock:
            self.accept_if_needed()
            if not self.client_sock:
                return

        if self.pending_write:
            self.state_log("servicing pending WRITE", BRIGHT_YELLOW)
            self.write_service()
            if self.client_sock is None:
                return
            if self.pending_write:
                return

        try:
            chunk = sock_recv(self.client_sock, 1024)
            if chunk is None:
                return

            if chunk == b"":
                self.log("client disconnected", BRIGHT_YELLOW)
                self.close_client("remote closed")
                return

            self.read_buffer += chunk
            self.protocol_log(
                "recv {} bytes, buffer now {} bytes".format(len(chunk), len(self.read_buffer)),
                BRIGHT_BLACK,
            )

        except Exception as e:
            self.log("read error: {}".format(repr(e)), BRIGHT_RED)
            log_exception("socket read", e)
            self.close_client("read failed")
            return

        while b"\n" in self.read_buffer:
            line, self.read_buffer = self.read_buffer.split(b"\n", 1)
            cmd_line = safe_decode(line).strip()

            self.protocol_log("raw line: {}".format(repr(line)), BRIGHT_BLACK)
            self.protocol_log("cmd line: {}".format(repr(cmd_line)), BRIGHT_CYAN)

            try:
                cont = self.handle_command(cmd_line)
            except Exception as e:
                self.log("command handler error: {}".format(repr(e)), BRIGHT_RED)
                log_exception("handle_command", e)
                self.close_client("command handler crashed")
                return

            if self.pending_write:
                self.state_log("WRITE pending, stopping line parsing", BRIGHT_YELLOW)
                return

            if not cont:
                return

    def close(self):
        self.close_client("server close")
        if self.server_sock:
            try:
                self.server_sock.close()
            except Exception as e:
                self.log("server close failed: {}".format(repr(e)), BRIGHT_RED)
            self.server_sock = None


server = None

async def startTcpServer():
    global server

    port = config.get("AP", {}).get("ports", 1084)
    server = TCPServer(port)
    server.start()

    while True:
        try:
            server.update_poll()
        except Exception as e:
            cprint("[FATAL] update_poll crash: {}".format(repr(e)), BRIGHT_RED)
            log_exception("startTcpServer loop", e)
            try:
                server.close()
            except Exception:
                pass
            raise

        gc.collect()
        await asyncio.sleep(0.01)


dump_previous_traceback()
