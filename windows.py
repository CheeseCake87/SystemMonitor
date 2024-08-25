#
# WINDOWS MONITORING
#
import pathlib
import subprocess
import time
import tomllib

import psutil
import requests

TOML_FILE = pathlib.Path(__file__).parent / 'config.toml'
CONFIG = tomllib.loads(TOML_FILE.read_text())
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


def get_network_usage() -> dict[str, float]:
    return {
        'sent': psutil.net_io_counters().bytes_sent,
        'recv': psutil.net_io_counters().bytes_recv
    }


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


def set_windows_uuid() -> str:
    global UUID
    if psutil.WINDOWS:
        s = subprocess.check_output('wmic csproduct get uuid').strip()
        s = s.decode('ascii').split("\n")
        UUID = s[1].strip()
    UUID = "Not Windows"


def gather_info() -> None:
    global UUID

    _disk = disk_usage()
    _processes = get_processes()
    _network_info = get_network_info()
    _network_usage = get_network_usage()

    res = requests.post(
        CONFIG['url'],
        json={
            "url": CONFIG['url'],
            "interval": CONFIG['interval'],
            "uuid": UUID,
            "stats": {
                "cpu_usage": get_cpu_usage(),
                "memory_usage": get_memory_usage(),
                "disk_usage": _disk,
                "processes": _processes,
                "network_info": _network_info,
                "network_usage": _network_usage
            }
        }
    )


if __name__ == '__main__':
    set_windows_uuid()

    while True:
        time.sleep(CONFIG['interval'])
        gather_info()
