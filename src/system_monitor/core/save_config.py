import tkinter as tk
from json import dumps

from .walk_find import walk_find_config_file


def save_config(tki, system_id, url, interval):
    saved = tk.Label(tki, text="Config saved, system restart required!", fg="green")
    saved.place(relx=0.5, y=10, anchor=tk.CENTER)

    tki.after(4000, saved.destroy)

    config = {
        "system_id": system_id,
        "url": url,
        "interval": int(interval) if isinstance(interval, str) else 60
    }
    file = walk_find_config_file()
    file.write_text(dumps(config))
