# System Monitor

System Monitor is a background service that collects system information and sends it to a server using a POST request.

The data is sent in JSON format.

Settings can be updated in the app.

![img.png](/_assets%2Fimg.png)

**Interval is the amount of time in seconds the app will wait before checking and sending.**

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


# Development Environment

## Windows

**NOTE:** pyinstaller is required to build the exe, the exe is only built in a Windows environment.

**NOTE:** Inno Setup is required to build the installer.

**Ensure you have python 3.10+ installed.**

Navigate to the project directory.

Create virtual environment

```bash
python -m venv venv
```

This will create a virtual environment in the project directory, like so:

```text
ProjectDir/
    ...
    README.md
    venv/
```

Activate virtual environment

```bash
.\venv\Scripts\activate
```

Install dependencies

```bash
pip install -r .\requirements\main.txt
```

### Run the server

```bash
flask --app .\server.py run --debug
```

### Run the GUI app

```bash
python .\src\system_monitor.py
```

### Run the background service

```bash
python .\src\system_monitor.py background
```

### Build the exe

```bash
pyinstaller src/system_monitor.py -w -D --noconsole
```

### Build the installer

1. Install Inno Setup (https://www.jrsoftware.org/isdl.php)
2. Open the script `inno\system_monitor_setup.iss` in Inno Compiler
3. Click on the Run button


## Darwin / GNU/Linux

**Ensure you have python 3.10+ installed.**

Navigate to the project directory.

Create virtual environment

```bash
python3 -m venv venv
```

This will create a virtual environment in the project directory, like so:

```text
ProjectDir/
    ...
    README.md
    venv/
```

Activate virtual environment

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements/main.txt
```

### Run the server

```bash
flask --app server.py run --debug
```

### Run the GUI app

```bash
python3 src/system_monitor.py
```

### Run the background service

```bash
python3 src/system_monitor.py background
```
