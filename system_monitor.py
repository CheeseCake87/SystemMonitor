import tkinter as tk
import pathlib

def walk_find_logo():
    cwd = pathlib.Path(__file__).parent
    print(cwd)

    logo = cwd / "logo.gif"

    if logo.exists():
        return logo

    for r in range(3):
        cwd = cwd.parent
        logo = cwd / "logo.gif"
        if logo.exists():
            return logo

    raise FileNotFoundError("logo.png not found")

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor")
        self.geometry("400x200")

        self.logo = tk.PhotoImage(file=walk_find_logo())
        self.image = tk.Label(self, image=self.logo)
        self.image.pack()

        self.button = tk.Button(self, text="Quit", command=self.quit)
        self.button.pack()


if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()