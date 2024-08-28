#
# SYSTEM MONITOR
#
import pathlib
import shutil
import pylnk3
import tkinter as tk

CWD = pathlib.Path(__file__)
PROGRAM_FILES = pathlib.Path("C:/Program Files")
STARTUP_DIR = pathlib.Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp")
PF_FOLDER = PROGRAM_FILES / "SystemMonitor"


def walk_system_monitor_lnk():
    this_cwd = CWD

    lnk = this_cwd / "SystemMonitor.lnk"

    if lnk.exists():
        return lnk

    for r in range(3):
        this_cwd = this_cwd.parent
        lnk = this_cwd / "SystemMonitor.lnk"
        if lnk.exists():
            return lnk

    raise FileNotFoundError("SystemMonitor.lnk not found")


def walk_system_monitor_background_process_lnk():
    this_cwd = CWD

    lnk = this_cwd / "SystemMonitorBackgroundProcess.lnk"

    if lnk.exists():
        return lnk

    for r in range(3):
        this_cwd = this_cwd.parent
        lnk = this_cwd / "SystemMonitorBackgroundProcess.lnk"
        if lnk.exists():
            return lnk

    raise FileNotFoundError("SystemMonitorBackgroundProcess.lnk not found")


def walk_find_icon():
    this_cwd = CWD

    icon = this_cwd / "app.ico"

    if icon.exists():
        return icon

    for r in range(3):
        this_cwd = this_cwd.parent
        icon = this_cwd / "app.ico"
        if icon.exists():
            return icon

    return None


def walk_find_logo():
    this_cwd = CWD

    icon = this_cwd / "logo.gif"

    if icon.exists():
        return icon

    for r in range(3):
        this_cwd = this_cwd.parent
        icon = this_cwd / "logo.gif"
        if icon.exists():
            return icon

    return None


def walk_find_config():
    this_cwd = CWD

    config = this_cwd / "config.toml"

    if config.exists():
        return config

    for r in range(3):
        this_cwd = this_cwd.parent
        config = this_cwd / "config.toml"
        if config.exists():
            return config

    raise FileNotFoundError("config.toml not found")


def walk_find_system_monitor():
    this_cwd = CWD

    system_monitor = this_cwd / "system_monitor"

    if system_monitor.exists():
        return system_monitor

    for r in range(3):
        this_cwd = this_cwd.parent
        system_monitor = this_cwd / "system_monitor"
        if system_monitor.exists():
            return system_monitor

    raise FileNotFoundError("system_monitor not found")


def walk_find_system_monitor_background_process():
    this_cwd = CWD

    system_monitor = this_cwd / "system_monitor_background_process"

    if system_monitor.exists():
        return system_monitor

    for r in range(3):
        this_cwd = this_cwd.parent
        system_monitor = this_cwd / "system_monitor_background_process"
        if system_monitor.exists():
            return system_monitor

    raise FileNotFoundError("system_monitor_background_process not found")


def install():
    if PF_FOLDER.exists():
        shutil.rmtree(PF_FOLDER)

    pf_system_monitor_folder = PF_FOLDER / "system_monitor"
    pf_system_monitor_bp_folder = PF_FOLDER / "system_monitor_background_process"

    pf_system_monitor_exe = pf_system_monitor_folder / "system_monitor.exe"
    pf_system_monitor_bp_exe = pf_system_monitor_bp_folder / "system_monitor_background_process.exe"

    PF_FOLDER.mkdir(exist_ok=True)
    pf_system_monitor_folder.mkdir(exist_ok=True)
    pf_system_monitor_bp_folder.mkdir(exist_ok=True)

    icon_file = walk_find_icon()
    logo_file = walk_find_logo()
    config_file = walk_find_config()
    system_monitor_folder = walk_find_system_monitor()
    system_monitor_bp_folder = walk_find_system_monitor_background_process()

    shutil.copy(config_file, PF_FOLDER)
    shutil.copy(logo_file, PF_FOLDER)
    shutil.copytree(system_monitor_folder, pf_system_monitor_folder, dirs_exist_ok=True)
    shutil.copytree(system_monitor_bp_folder, pf_system_monitor_bp_folder, dirs_exist_ok=True)

    if pf_system_monitor_exe.exists():
        pylnk3.for_file(
            str(pf_system_monitor_exe),
            lnk_name="SystemMonitor.lnk",
            icon_file=str(icon_file) if icon_file else None,
        )
        system_monitor_lnk = walk_system_monitor_lnk()
        shutil.copy(system_monitor_lnk, PF_FOLDER / "SystemMonitor.lnk")
        system_monitor_lnk.unlink()

    if pf_system_monitor_bp_exe.exists():
        pylnk3.for_file(
            str(pf_system_monitor_bp_exe),
            lnk_name="SystemMonitorBackgroundProcess.lnk",
            icon_file=str(icon_file) if icon_file else None,
            window_mode=pylnk3.WINDOW_MINIMIZED,
        )
        system_monitor_background_process_lnk = walk_system_monitor_background_process_lnk()
        shutil.copy(system_monitor_background_process_lnk, PF_FOLDER / "SystemMonitorBackgroundProcess.lnk")
        shutil.copy(system_monitor_background_process_lnk, STARTUP_DIR / "SystemMonitorBackgroundProcess.lnk")
        system_monitor_background_process_lnk.unlink()


if __name__ == '__main__':
    install()
    app = tk.Tk()
    app.title("System Monitor Installed")
    app.geometry("400x140")

    app.space_one = tk.Label(app, text="", pady=2)
    app.space_one.pack()

    app.label = tk.Label(app, text="System Monitor Installed")
    app.label.pack()

    app.location = tk.Label(app, text=f"Location: {PF_FOLDER}")
    app.location.pack()

    app.space_two = tk.Label(app, text="", pady=2)
    app.space_two.pack()

    app.close_button = tk.Button(app, text="Close", command=app.quit, padx=10)
    app.close_button.pack()
    app.mainloop()
