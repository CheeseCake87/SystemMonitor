def load_gui(config, logo) -> None:
    import tkinter as tk

    from .save_config import save_config

    class SystemMonitor(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("System Monitor")
            self.geometry("300x360")
            self.eval('tk::PlaceWindow . center')

            self.value__system_id = tk.StringVar(value=config['system_id'])
            self.value__url = tk.StringVar(value=config['url'])
            self.value__interval = tk.IntVar(value=config['interval'])

            if logo:
                self.logo = tk.PhotoImage(file=logo)
                self.image = tk.Label(self, image=self.logo)
                self.image.pack()

            self.main_frame = tk.Frame(self)
            self.main_frame.pack_configure(pady=20, padx=20, fill=tk.BOTH)

            self.label__app_info = tk.Label(self.main_frame, text="System Monitor: v0.3")
            self.label__app_info.pack(anchor="w")

            self.grid_frame = tk.Frame(self.main_frame, pady=20)
            self.grid_frame.columnconfigure(0, weight=1)
            self.grid_frame.columnconfigure(1, weight=1)
            self.grid_frame.columnconfigure(3, weight=1)

            self.label__system_id = tk.Label(self.grid_frame, text=f"System ID:")
            self.label__system_id.grid(row=0, column=0, sticky=tk.W)
            self.textbox__system_id = tk.Entry(self.grid_frame, textvariable=self.value__system_id)
            self.textbox__system_id.grid(row=0, column=1)

            self.label__url = tk.Label(self.grid_frame, text=f"URL:")
            self.label__url.grid(row=1, column=0, sticky=tk.W)
            self.textbox__url = tk.Entry(self.grid_frame, textvariable=self.value__url)
            self.textbox__url.grid(row=1, column=1)

            self.label__interval = tk.Label(self.grid_frame, text=f"Interval:")
            self.label__interval.grid(row=2, column=0, sticky=tk.W)
            self.textbox__interval = tk.Entry(self.grid_frame, textvariable=self.value__interval)
            self.textbox__interval.grid(row=2, column=1)

            self.grid_frame.pack()

            self.grid_buttons = tk.Frame(self.main_frame, pady=10)
            self.grid_buttons.columnconfigure(0, weight=1)

            self.button__close = tk.Button(self.grid_buttons, text="Close", command=self.quit)
            self.button__close.grid(row=0, column=1, sticky=tk.E)

            self.button__save = tk.Button(self.grid_buttons, text="Save", command=lambda: save_config(
                self,
                self.textbox__system_id.get(),
                self.textbox__url.get(),
                self.textbox__interval.get()
            ))
            self.button__save.grid(row=0, column=0, sticky=tk.W)

            self.grid_buttons.pack(fill=tk.X, padx=10)

            self.main_frame.pack()

    app = SystemMonitor()
    app.mainloop()
