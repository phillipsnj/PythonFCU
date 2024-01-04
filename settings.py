import tkinter as tk
from tkinter import ttk


class SettingsFrame(tk.Frame):
    def __init__(self, parent, callbacks, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        self.settings = settings
