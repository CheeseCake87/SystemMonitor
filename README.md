# System Monitor

System Monitor is a background service that collects system information and sends it to a server using a POST request.

The data is sent in JSON format.

Settings can be updated in the app.

![img.png](/_assets%2Fimg.png)

**Interval is the amount of time in seconds the app will send a JSON POST request to the URL you set.**

# JSON Sent to Server

```text
system_id: str
url: str
interval: int
windows_uuid: str
epoch: int
stats: object
    cpu_usage: float
    memory_usage: float
    disk_usage: object
        total: int
        used: int
        free: int
    processes: array of objects
        pid: int
        name: str
        username: str
    network_info: object
        <network name>: object
            ip: str
            netmask: str
            bytes_sent: int
            bytes_recv: int
```

# Install on Windows

Download the setup exe in `inno\Output\system_monitor_setup.exe` and run it.

Restart the computer after installation for the background service to start.

# Uninstall on Windows

Go to the settings > apps > System Monitor > uninstall
