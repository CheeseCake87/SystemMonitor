import tkinter as tk
import pathlib
import tomllib



def walk_find_logo() -> pathlib.Path | None:
    cwd = pathlib.Path(__file__).parent

    logo = cwd / "logo.gif"

    if logo.exists():
        return logo

    for r in range(3):
        cwd = cwd.parent
        logo = cwd / "logo.gif"
        if logo.exists():
            return logo

    dev_check = pathlib.Path(__file__).parent / "dist" / "logo.gif"
    if dev_check.exists():
        return dev_check

    return None


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

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor")
        self.geometry("300x350")

        logo = walk_find_logo()

        if logo:
            self.logo = tk.PhotoImage(file=walk_find_logo())
            self.image = tk.Label(self, image=self.logo)
            self.image.pack()

        self.label = tk.Label(self, text="System Monitor: v0.2", justify=tk.LEFT, anchor=tk.W)
        self.label.pack()

        self.Label = tk.Label(self, text=f"System ID: {CONFIG['system_id']}", justify=tk.LEFT, anchor=tk.W)
        self.Label.pack()

        self.Label = tk.Label(self, text=f"URL: {CONFIG['url']}", justify=tk.LEFT, anchor=tk.W)
        self.Label.pack()

        self.Label = tk.Label(self, text=f"Interval: {CONFIG['interval']}", justify=tk.LEFT, anchor=tk.W)
        self.Label.pack()

        self.Label = tk.Label(self, text="", pady=2)
        self.Label.pack()

        self.close_button = tk.Button(self, text="Close", command=self.quit, padx=10)
        self.close_button.pack()


if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()