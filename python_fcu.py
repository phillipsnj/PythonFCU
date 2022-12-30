import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
# import serial
import time
import json


class PythonFCU(tk.Tk):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # with open('config.json') as f:
        #     self.data = json.load(f)
        # print(f"Config {str(self.data['port'])}")
        self.title("Python FCU Development")
        self.geometry("800x600")
        self.resizable(width=False, height=False)
        self.node_frame = ttk.LabelFrame(self, text=" Modules ")
        self.node_frame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.event_frame = ttk.LabelFrame(self, text=" Events ")
        self.event_frame.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")
        self.message_frame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

