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

Download the `SystemMonitorSetupPackage.zip` file.

Extract the contents of the zip file, and run the `install\install.exe` file.

This will move the contents on the folder to the `C:\Program Files\SystemMonitor` directory, and
add a shortcut to the common startup folder (`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`)

You can change the `app.ico` file to change the icon of the application. And you can also change
the `logo.gif` file to change the logo of the application.

Remember to change the `config.toml` file to set the correct system id, server URL, and interval.

# Uninstall on Windows

Remove the `C:\Program Files\SystemMonitor` directory.
Remove the shortcut from the common startup folder `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

# Development and Test Setup

Install Python, navigate to the project directory and run the following commands:

```bash
python -m venv .venv

```

Activate the virtual environment:

```bash
./.venv/Scrips/activate
```

Install the required packages:

```bash
pip install -r requirements/main.txt
```

Run the server:

```bash
flask --app server.py run --debug
```

Run the client:

Option 1, run the .exe found in the `dist\system_monitor` folder.

Option 2, run the following command:

```bash
python system_monitor.py
```

The config file is used to set where the stats are sent to, 
and the interval at which they are sent. You can also set a
system ID value to identify the system.
