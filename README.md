# System Monitor

System Monitor is a background service that collects system information and sends it to a server using a POST request.

The data is sent in JSON format.

Settings can be updated in the app.

![img_1.png](/_assets%2Fimg_1.png)

**Interval is the amount of time in seconds the app will wait before checking and sending.**

<!-- TOC -->
* [System Monitor](#system-monitor)
  * [JSON Sent to Server](#json-sent-to-server)
  * [Install on Windows](#install-on-windows)
  * [Uninstall on Windows](#uninstall-on-windows)
  * [Development Environment](#development-environment)
    * [Windows](#windows)
      * [Setup](#setup)
      * [Run the server](#run-the-server)
      * [Run the GUI app](#run-the-gui-app)
      * [Run the background service](#run-the-background-service)
      * [Build the exe](#build-the-exe)
      * [Build the installer](#build-the-installer)
    * [Darwin / GNU/Linux](#darwin--gnulinux)
      * [Setup](#setup-1)
      * [Run the server](#run-the-server-1)
      * [Run the GUI app](#run-the-gui-app-1)
      * [Run the background service](#run-the-background-service-1)
  * [Available CLI Commands](#available-cli-commands)
  * [Server API](#server-api)
    * [action](#action)
    * [Responses](#responses)
<!-- TOC -->

## JSON Sent to Server

```text
action: str
system_id: str
url: str
interval: int
epoch: int
stats: object
    cpu: object
        count: int
        frequency: int
        percent_used: float
    memory: object
        total: int
        available: int
        percent_used: float
        used: int
        free: int
    processes: array of objects
        pid: int
        name: str
        username: str
    disks: object
        <device>: object
            file_system: str
            mount_point: str
            total: int
            used: int
            free: int
    network: object
        <network name>: object
            ip: str
            netmask: str
            bytes_sent: int
            bytes_recv: int
```

## Install on Windows

Download the setup exe in `inno\Output\system_monitor_setup.exe` and run it or click here:

[system_monitor_setup.exe](inno%2FOutput%2Fsystem_monitor_setup.exe)

Restart the computer after installation for the background service to start.

## Uninstall on Windows

Go to the settings > apps > System Monitor > uninstall

## Development Environment

* [Windows](#windows)
* [Darwin / GNU/Linux](#darwin--gnulinux)

### Windows

**NOTE:** pyinstaller is required to build the exe, the exe is only built in a Windows environment.

**NOTE:** Inno Setup is required to build the installer.

**Ensure you have python 3.10+ installed.**

#### Setup

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

#### Run the server

```bash
flask --app .\server.py run --debug
```

#### Run the GUI app

```bash
python .\src\system_monitor.py
```

#### Run the background service

```bash
python .\src\system_monitor.py background
```

#### Build the exe

```bash
pyinstaller .\src\system_monitor.py -w -D --noconsole
```

#### Build the installer

1. Install Inno Setup (https://www.jrsoftware.org/isdl.php)
2. Open the script `inno\system_monitor_setup.iss` in Inno Compiler
3. Click on the Run button

### Darwin / GNU/Linux

**Ensure you have python 3.10+ installed.**

#### Setup

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

#### Run the server

```bash
flask --app server.py run --debug
```

#### Run the GUI app

```bash
python3 src/system_monitor.py
```

#### Run the background service

```bash
python3 src/system_monitor.py background
```

## Available CLI Commands

Show stats > cpu

```bash
python3 src/system_monitor.py cpu
```

Show stats > memory

```bash
python3 src/system_monitor.py memory
```

Show stats > processes

```bash
python3 src/system_monitor.py processes
```

Show stats > disks

```bash
python3 src/system_monitor.py disks
```

Show stats > network

```bash
python3 src/system_monitor.py network
```

Generate system id

```bash
python3 src/system_monitor.py generate_system_id
```

Run the background service

```bash
python3 src/system_monitor.py background
```

## Server API

The example server is Flask, but this can be any server that can accept POST requests 
and send the appropriate responses.

### action

The system monitor reports its action when sending data to the server. 

This is included in the JSON data sent to the server.

```json
{
  "action": <action here>,
  ...
}
```

These actions are:

* `check_url` - The system monitor is checking the server URL.
* `check_system_id` - The system monitor is checking if the system ID is available.
* `send_stats` - The system monitor is sending stats to the server.

### Responses

The server is expected to use HTTP status codes to respond to the system monitor.

For `check_url`:

A response of `202` is expected to pass the check.

Any other response will be considered a connection error.

For `check_system_id`:

A response of `200` is expected to let the system
monitor know that the username exists on the system.

A response of `204` is expected to let the system monitor
know that the connection is fine and that the username does
not exist on the system.

Any other response will be considered a connection error.

For `send_stats`:

A response of `200` is expected to let the system monitor know
that the stats were received successfully.