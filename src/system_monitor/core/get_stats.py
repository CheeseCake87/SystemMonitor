import subprocess

import psutil


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


def get_disk_usage() -> dict[str, float]:
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
