#
# SYSTEM MONITOR BACKGROUND PROCESS
#
import pathlib
import subprocess
import time
import tomllib

import psutil
import requests


def walk_find_config():
    cwd = pathlib.Path(__file__).parent

    config = cwd / "config.toml"

    if config.exists():
        return tomllib.loads(config.read_text())

    for r in range(3):
        cwd = cwd.parent
        config = cwd / "config.toml"
        if config.exists():
            return tomllib.loads(config.read_text())

    dev_check = pathlib.Path(__file__).parent / "dist" / "config.toml"
    if dev_check.exists():
        return tomllib.loads(dev_check.read_text())

    raise FileNotFoundError("config.toml not found")

CONFIG = walk_find_config()
UUID = None


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
                    "bytes_recv": _network_counters[network].bytes_recv
                }

    return _return


def get_processes() -> list[dict[str, str]]:
    return [p.as_dict(attrs=['pid', 'name', 'username']) for p in psutil.process_iter()]


def disk_usage() -> dict[str, float]:
    return {
        'total': psutil.disk_usage('/').total,
        'used': psutil.disk_usage('/').used,
        'free': psutil.disk_usage('/').free
    }


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)


def get_memory_usage() -> float:
    return psutil.virtual_memory().percent


def get_windows_uuid() -> str:
    if psutil.WINDOWS:
        create_no_window = 0x08000000
        s = subprocess.check_output(
            'wmic csproduct get uuid', creationflags=create_no_window
        ).strip()
        s = s.decode('ascii').split("\n")
        return s[1].strip()
    return "Not Windows"


def gather_info() -> None:
    _disk = disk_usage()
    _processes = get_processes()
    _network_info = get_network_info()

    try:
        requests.post(
            CONFIG['url'],
            json={
                "system_id": CONFIG['system_id'],
                "url": CONFIG['url'],
                "interval": CONFIG['interval'],
                "windows_uuid": UUID,
                "epoch": int(time.time()),
                "stats": {
                    "cpu_usage": get_cpu_usage(),
                    "memory_usage": get_memory_usage(),
                    "disk_usage": _disk,
                    "processes": _processes,
                    "network_info": _network_info,
                }
            }
        )
    except requests.exceptions.ConnectionError:
        pass


if __name__ == '__main__':
    UUID = get_windows_uuid()

    while True:
        time.sleep(CONFIG['interval'])
        gather_info()
