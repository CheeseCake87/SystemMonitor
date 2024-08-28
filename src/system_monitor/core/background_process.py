import time

import requests

from .get_stats import (
    get_disk_usage,
    get_cpu_usage,
    get_memory_usage,
    get_processes,
    get_network_info,
    get_windows_uuid
)


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
                config['url'],
                json={
                    "system_id": config['system_id'],
                    "url": config['url'],
                    "interval": config['interval'],
                    "windows_uuid": _uuid,
                    "epoch": int(time.time()),
                    "stats": {
                        "cpu_usage": _cpu,
                        "memory_usage": _memory,
                        "disk_usage": _disk,
                        "processes": _processes,
                        "network_info": _network_info,
                    }
                }
            )
        except Exception as e:
            _ = e
            pass
