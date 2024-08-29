import platform
import time
import tkinter as tk
from hashlib import md5
from json import dumps, loads
from pathlib import Path
from pprint import pprint
from random import randint
from sys import argv

import psutil
import requests

__version__ = "0.4.3"


####################
####################
####################


# GENERATE SYSTEM ID

def generate_system_id() -> str:
    md5_join = "".join(
        str(_) for _ in [
            int(time.time()),
            psutil.cpu_count(),
            randint(111111111, 999999999),
        ]
    )

    md5_value = md5(md5_join.encode()).hexdigest()

    gather = [
        platform.system(),
        md5_value
    ]
    return '-'.join([str(g) for g in gather])


####################
####################
####################


# WALK FIND


def walk_find_icon() -> Path | None:
    cwd = Path(__file__).parent

    icon = cwd / "app.ico"

    if icon.exists():
        return icon

    for r in range(3):
        cwd = cwd.parent
        icon = cwd / "app.ico"
        if icon.exists():
            return icon

    return None


def walk_find_logo() -> Path | None:
    cwd = Path(__file__).parent

    logo = cwd / "logo.gif"

    if logo.exists():
        return logo

    for r in range(3):
        cwd = cwd.parent
        logo = cwd / "logo.gif"
        if logo.exists():
            return logo

    return None


def load_config(config_file: Path) -> dict[str, str | int]:
    if config_file.exists():
        config = loads(config_file.read_text())

        system_id = config.get("system_id")

        if not system_id:
            config["system_id"] = generate_system_id()
            config_file.write_text(dumps(config))

        return config

    raise FileNotFoundError("config.json not found")


def walk_find_config_file() -> Path:
    cwd = Path(__file__).parent

    config = cwd / "config.json"

    if config.exists():
        return config

    for r in range(3):
        cwd = cwd.parent
        config = cwd / "config.json"
        if config.exists():
            return config

    raise FileNotFoundError("config.json not found")


####################
####################
####################


# GLOBAL VARS


CONFIG_FILE = walk_find_config_file()
CONFIG = load_config(CONFIG_FILE)
LOGO = walk_find_logo()

GUI_SHOW_LOGO = True
GUI_SHOW_SYSTEM_ID = True
GUI_SHOW_SYSTEM_ID_BUTTONS = True
GUI_SHOW_URL = True
GUI_SHOW_URL_BUTTONS = True
GUI_SHOW_INTERVAL = True

GUI_DISABLE_SYSTEM_ID = False
GUI_DISABLE_URL = False
GUI_DISABLE_INTERVAL = False


####################
####################
####################


# GUI SAVE CONFIG


def gui_save_config(tki, system_id, url, interval, _skip_message=False):
    if not _skip_message:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="Config saved, system restart required!", fg="green", bg="lightgrey")
            label.pack()

    CONFIG_FILE.write_text(
        dumps(
            {
                "system_id": system_id,
                "url": url,
                "interval": int(interval) if isinstance(interval, str) else 60,
            }
        )
    )


####################
####################
####################


# GUI NEW SYSTEM ID


def gui_new_system_id(tki, _save=True):
    new_system_id = generate_system_id()
    if _save:
        gui_save_config(tki, new_system_id, CONFIG["url"], CONFIG["interval"], _skip_message=True)
    tki.value__system_id.set(new_system_id)

    with MessageFrame(tki) as message_frame:
        label = tk.Label(message_frame, text="New System ID Generated!", fg="green", bg="lightgrey")
        label.pack()


####################
####################
####################

# GET STATS


def get_network_info() -> dict[str, dict[str, int | str | None]]:
    _networks = psutil.net_if_addrs()
    _network_counters = psutil.net_io_counters(pernic=True)
    _return = {}

    for network, info in _networks.items():
        for i in info:
            if i.family == 2:
                _return[network] = {
                    "ip": i.address,
                    "netmask": i.netmask,
                    "bytes_sent": _network_counters[network].bytes_sent,
                    "bytes_recv": _network_counters[network].bytes_recv,
                }

    return _return


def get_processes() -> list[dict[str, str]]:
    return [p.as_dict(attrs=["pid", "name", "username"]) for p in psutil.process_iter()]


def get_disk_usage() -> dict[str, dict[str, int | str]]:
    disks = {}

    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.mountpoint)
        disks[disk.device] = {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "file_system": disk.fstype,
            "mount_point": disk.mountpoint,
        }

    return disks


def get_memory() -> dict[str, float | int]:
    _memory = psutil.virtual_memory()
    return {
        "total": _memory.total,
        "available": _memory.available,
        "percent_used": _memory.percent,
        "used": _memory.used,
        "free": _memory.free,
    }


def get_cpu() -> dict[str, float | int]:
    return {
        "count": psutil.cpu_count(),
        "percent_used": psutil.cpu_percent(interval=1),
        "frequency": psutil.cpu_freq().current,
    }


####################
####################
####################

# GUI CHECK URL AVAILABILITY


def gui_check_url_availability(tki):
    status = check_url_availability()

    if status == 0:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="Connection Error", fg="red", bg="lightgrey")
            label.pack()

    if status == 1:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="URL is OK!", fg="green", bg="lightgrey")
            label.pack()


####################
####################
####################

# GUI CHECK SYSTEM ID AVAILABILITY


def gui_check_system_id_availability(tki, system_id):
    status = check_system_id_availability(system_id)

    if status == 0:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="Connection Error", fg="red", bg="lightgrey")
            label.pack()

    if status == 1:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="System ID has NOT been registered!", fg="black", bg="lightgrey")
            label.pack()

    if status == 2:
        with MessageFrame(tki) as message_frame:
            label = tk.Label(message_frame, text="System ID has been registered!", fg="black", bg="lightgrey")
            label.pack()


####################
####################
####################

# CHECK URL AVAILABILITY

def check_url_availability() -> int:
    """
    It is expected that the server will return a 202 status code if the URL service is available.

    0: Connection Error
    1: URL is available
    """

    config = load_config(CONFIG_FILE)

    try:
        response = requests.post(
            config["url"],
            json={
                "action": "check_url",
            }
        )

        if response.status_code == 202:
            return 1

        return 0

    except requests.exceptions.ConnectionError:
        return 0


####################
####################
####################

# CHECK SYSTEM ID AVAILABILITY

def check_system_id_availability(system_id) -> int:
    """
    It is expected that the server will return a 204 status code if the system ID is available.

    0: Connection Error
    1: System ID is available
    2: System ID is not available
    """

    config = load_config(CONFIG_FILE)

    try:
        response = requests.post(
            config["url"],
            json={
                "action": "check_system_id",
                "system_id": system_id.get(),
            }
        )

        if response.status_code == 204:
            return 1

        if response.status_code == 200:
            return 2

        return 0

    except requests.exceptions.ConnectionError:
        return 0


####################
####################
####################

# BACKGROUND PROCESS


def background_process(config) -> None:
    while True:
        _disk = get_disk_usage()
        _processes = get_processes()
        _network_info = get_network_info()
        _cpu = get_cpu()
        _memory = get_memory()

        try:
            requests.post(
                config["url"],
                json={
                    "action": "send_stats",
                    "system_id": config["system_id"],
                    "url": config["url"],
                    "interval": config["interval"],
                    "epoch": int(time.time()),
                    "stats": {
                        "cpu": _cpu,
                        "memory": _memory,
                        "disks": _disk,
                        "processes": _processes,
                        "network": _network_info,
                    },
                },
            )
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(config["interval"])


####################
####################
####################

# GUI FRAMES


class MessageFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="lightgrey")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.place_configure(x=0, y=0, relwidth=1, height=25)
        self.after(3000, self.destroy)


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(padx=15, pady=15, fill=tk.BOTH, expand=True)


class ConfigFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(pady=20, fill=tk.BOTH, expand=True)


class SystemIDFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(pady=5, fill=tk.BOTH)


class SystemIDButtonFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(side=tk.LEFT)


class URLFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(pady=5, fill=tk.BOTH)


class URLButtonFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(side=tk.LEFT)


class BottomButtonsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pack_configure(fill=tk.BOTH, pady=10, anchor=tk.S)


####################
####################
####################

# LOAD GUI


def load_gui(config, logo) -> None:
    class SystemMonitor(tk.Tk):

        def _set_window(self):

            if psutil.WINDOWS:
                _height = 160
            else:
                _height = 200

            if GUI_SHOW_LOGO:
                _height += 120
            if GUI_SHOW_SYSTEM_ID:
                _height += 40

                if GUI_SHOW_SYSTEM_ID_BUTTONS:
                    _height += 40

            if GUI_SHOW_URL:
                _height += 40

                if GUI_SHOW_URL_BUTTONS:
                    _height += 40

            if GUI_SHOW_INTERVAL:
                _height += 40

            self.title("System Monitor")
            self.geometry(f"400x{_height}")
            self.eval("tk::PlaceWindow . center")
            self.resizable(False, False)
            self.iconbitmap(walk_find_icon())

        def _set_values(self):
            self.value__status = tk.StringVar(value="")
            self.value__system_id = tk.StringVar(value=config["system_id"])
            self.value__url = tk.StringVar(value=config["url"])
            self.value__interval = tk.IntVar(value=config["interval"])

        def _logo(self, frame_: tk.Frame):
            if logo and GUI_SHOW_LOGO:
                self.logo = tk.PhotoImage(file=logo)
                self.image = tk.Label(frame_, image=self.logo)
                self.image.pack()

        def _system_version(self, frame_: tk.Frame):
            self.label__app_info = tk.Label(
                frame_, text=f"System Monitor: v{__version__}"
            )
            self.label__app_info.pack()

        def _system_id_fieldset(self, frame_: tk.Frame):
            with SystemIDFrame(frame_) as system_id_frame:
                self.label__system_id = tk.Label(system_id_frame, text="System ID:")
                self.label__system_id.pack(anchor=tk.W)

                self.textbox__system_id = tk.Entry(
                    system_id_frame, textvariable=self.value__system_id,
                    state="readonly" if GUI_DISABLE_SYSTEM_ID else "normal"
                )
                self.textbox__system_id.pack(fill=tk.BOTH)

                if GUI_SHOW_SYSTEM_ID_BUTTONS:
                    with SystemIDButtonFrame(system_id_frame) as system_id_button_frame:
                        self.button__check = tk.Button(
                            system_id_button_frame,
                            text="Check",
                            command=lambda: gui_check_system_id_availability(self, self.value__system_id),
                            padx=5,
                            pady=2,
                        )
                        self.button__check.grid(row=0, column=0)

                        self.button__new_system_id = tk.Button(
                            system_id_button_frame,
                            text="Generate New",
                            command=lambda: gui_new_system_id(self, _save=False),
                            padx=5,
                            pady=2,
                        )
                        self.button__new_system_id.grid(row=0, column=1)

        def _url_fieldset(self, frame_: tk.Frame):
            with URLFrame(frame_) as url_frame:
                self.label__url = tk.Label(url_frame, text="URL:")
                self.label__url.pack(anchor=tk.W)

                self.textbox__url = tk.Entry(
                    url_frame, textvariable=self.value__url,
                    state="readonly" if GUI_DISABLE_URL else "normal"
                )
                self.textbox__url.pack(fill=tk.BOTH, pady=2)

                if GUI_SHOW_URL_BUTTONS:
                    with URLButtonFrame(url_frame) as url_button_frame:
                        self.button__check = tk.Button(
                            url_button_frame,
                            text="Check",
                            command=lambda: gui_check_url_availability(self),
                            padx=5,
                            pady=2,
                        )
                        self.button__check.grid(row=0, column=0)

        def _interval_fieldset(self, frame_: tk.Frame):
            self.label__interval = tk.Label(frame_, text="Interval:")
            self.label__interval.pack(anchor=tk.W)
            self.textbox__interval = tk.Entry(
                frame_, textvariable=self.value__interval,
                state="readonly" if GUI_DISABLE_INTERVAL else "normal"
            )
            self.textbox__interval.pack(fill=tk.BOTH, pady=2)

        def _bottom_buttons(self, frame_: tk.Frame):
            with BottomButtonsFrame(frame_) as grid_buttons:
                self.button__close = tk.Button(
                    grid_buttons, text="Close", command=self.quit, padx=20, pady=5
                )
                self.button__close.grid(row=0, column=1, sticky=tk.E)

                self.button__save = tk.Button(
                    grid_buttons,
                    text="Save",
                    command=lambda: gui_save_config(
                        self,
                        self.textbox__system_id.get(),
                        self.textbox__url.get(),
                        self.textbox__interval.get(),
                    ),
                    padx=20,
                    pady=5,
                )
                self.button__save.grid(row=0, column=0, sticky=tk.W)

        def __init__(self):
            super().__init__()

            self._set_window()
            self._set_values()

            with MainFrame(self) as main_frame:
                self._logo(main_frame)
                self._system_version(main_frame)

                with ConfigFrame(main_frame) as config_frame:
                    if GUI_SHOW_SYSTEM_ID:
                        self._system_id_fieldset(config_frame)

                    if GUI_SHOW_URL:
                        self._url_fieldset(config_frame)

                    if GUI_SHOW_INTERVAL:
                        self._interval_fieldset(config_frame)

                self._bottom_buttons(main_frame)

            self.message_frame = MessageFrame(self)

    app = SystemMonitor()
    app.mainloop()


if __name__ == "__main__":
    args = argv[1:]
    if args:

        match args[0]:
            case "cpu":
                pprint(get_cpu())

            case "memory":
                pprint(get_memory())

            case "processes":
                pprint(get_processes())

            case "disks":
                pprint(get_disk_usage())

            case "network":
                pprint(get_network_info())

            case "generate_system_id":
                pprint(generate_system_id())

            case "background":
                background_process(CONFIG)

            case _:
                raise SystemExit("Invalid argument")

    else:
        load_gui(CONFIG, LOGO)
