import subprocess
import time
from pathlib import Path
from sys import argv

from json import dumps, loads

import tkinter as tk

import psutil
import requests


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
        return loads(config_file.read_text())
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


####################
####################
####################


# SAVE CONFIG


def save_config(tki, system_id, url, interval):
    saved = tk.Label(tki, text="Config saved, system restart required!", fg="green")
    saved.place(relx=0.5, y=10, anchor=tk.CENTER)

    tki.after(4000, saved.destroy)

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


def get_disk_usage() -> dict[str, float]:
    return {
        "total": psutil.disk_usage("/").total,
        "used": psutil.disk_usage("/").used,
        "free": psutil.disk_usage("/").free,
    }


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)


def get_memory_usage() -> float:
    return psutil.virtual_memory().percent


def get_windows_uuid() -> str:
    if psutil.WINDOWS:
        create_no_window = 0x08000000
        s = subprocess.check_output(
            "wmic csproduct get uuid", creationflags=create_no_window
        ).strip()
        s = s.decode("ascii").split("\n")
        return s[1].strip()
    return "Not Windows"


####################
####################
####################

# BACKGROUND PROCESS


def background_process(config) -> None:
    _uuid = get_windows_uuid()

    while True:
        _disk = get_disk_usage()
        _processes = get_processes()
        _network_info = get_network_info()
        _cpu = get_cpu_usage()
        _memory = get_memory_usage()

        try:
            requests.post(
                config["url"],
                json={
                    "system_id": config["system_id"],
                    "url": config["url"],
                    "interval": config["interval"],
                    "windows_uuid": _uuid,
                    "epoch": int(time.time()),
                    "stats": {
                        "cpu_usage": _cpu,
                        "memory_usage": _memory,
                        "disk_usage": _disk,
                        "processes": _processes,
                        "network_info": _network_info,
                    },
                },
            )
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(config["interval"])


####################
####################
####################

# LOAD GUI


def load_gui(config, logo) -> None:
    class SystemMonitor(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("System Monitor")
            self.geometry("260x340")
            self.eval("tk::PlaceWindow . center")
            self.resizable(False, False)
            self.iconbitmap(walk_find_icon())

            self.value__system_id = tk.StringVar(value=config["system_id"])
            self.value__url = tk.StringVar(value=config["url"])
            self.value__interval = tk.IntVar(value=config["interval"])

            if logo:
                self.logo = tk.PhotoImage(file=logo)
                self.image = tk.Label(self, image=self.logo)
                self.image.pack()

            self.main_frame = tk.Frame(self)
            self.main_frame.pack_configure(pady=20, padx=20, fill=tk.BOTH)

            self.label__app_info = tk.Label(
                self.main_frame, text="System Monitor: v0.3.0"
            )
            self.label__app_info.pack(anchor="w")

            self.grid_frame = tk.Frame(self.main_frame, pady=20)
            self.grid_frame.columnconfigure(0, weight=1)
            self.grid_frame.columnconfigure(1, weight=1)
            self.grid_frame.columnconfigure(3, weight=1)

            self.label__system_id = tk.Label(self.grid_frame, text=f"System ID:")
            self.label__system_id.grid(row=0, column=0, sticky=tk.W)
            self.textbox__system_id = tk.Entry(
                self.grid_frame, textvariable=self.value__system_id
            )
            self.textbox__system_id.grid(row=0, column=1, sticky=tk.E + tk.W)

            self.label__url = tk.Label(self.grid_frame, text=f"URL:")
            self.label__url.grid(row=1, column=0, sticky=tk.W)
            self.textbox__url = tk.Entry(self.grid_frame, textvariable=self.value__url)
            self.textbox__url.grid(row=1, column=1, sticky=tk.E + tk.W)

            self.label__interval = tk.Label(self.grid_frame, text=f"Interval:")
            self.label__interval.grid(row=2, column=0, sticky=tk.W)
            self.textbox__interval = tk.Entry(
                self.grid_frame, textvariable=self.value__interval
            )
            self.textbox__interval.grid(row=2, column=1, sticky=tk.E + tk.W)

            self.grid_frame.pack(fill=tk.BOTH)

            self.grid_buttons = tk.Frame(self.main_frame, pady=10)
            self.grid_buttons.columnconfigure(0, weight=1)

            self.button__close = tk.Button(
                self.grid_buttons, text="Close", command=self.quit, padx=20, pady=5
            )
            self.button__close.grid(row=0, column=1, sticky=tk.E)

            self.button__save = tk.Button(
                self.grid_buttons,
                text="Save",
                command=lambda: save_config(
                    self,
                    self.textbox__system_id.get(),
                    self.textbox__url.get(),
                    self.textbox__interval.get(),
                ),
                padx=20,
                pady=5,
            )
            self.button__save.grid(row=0, column=0, sticky=tk.W)

            self.grid_buttons.pack(fill=tk.X, padx=20)

            self.main_frame.pack()

    app = SystemMonitor()
    app.mainloop()


if __name__ == "__main__":
    args = argv[1:]
    if args:
        if args[0] == "background":
            background_process(CONFIG)

    else:
        load_gui(CONFIG, LOGO)
