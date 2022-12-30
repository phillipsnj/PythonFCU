import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
# import serial
import time
import json


class PythonFCU(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('config.json') as f:
            self.data = json.load(f)
        print(f"Config {str(self.data['port'])}")
        self.title("Python FCU Development")
        self.geometry("1000x600")
        self.resizable(width=False, height=False)
        self.option_add('*tearOff', False)
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        main_menu.add('command', label='Refresh')
        main_menu.add('command', label='Quit', command=self.quit())
        fcu_menu = tk.Menu(main_menu, tearoff=False)
        fcu_menu.add_command(label='Refresh')
        fcu_menu.add_command(label="Quit FCU", command=self.quit())
        main_menu.add_cascade(label="FCU", menu=fcu_menu)
        self.node_frame = ttk.LabelFrame(self, text=" Modules ")
        self.node_frame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.event_frame = ttk.LabelFrame(self, text=" Events ")
        self.event_frame.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")
        self.message_frame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.node_list = ttk.Treeview(self.node_frame, columns=['NodeID', 'Name', 'Type', 'Version'], selectmode='browse')
        self.node_list.column('#0', width=0, stretch=True)
        self.node_list.column('NodeID', width=20)
        self.node_list.column('Name', width=200)
        self.node_list.column('Type', width=200)
        self.node_list.column('Version', width=200)
        self.node_list.heading('#0', text="")
        self.node_list.heading('NodeID', text="Node ID")
        self.node_list.heading('Name', text="Name")
        self.node_list.heading('Type', text="Type")
        self.node_list.heading('Version', text="Version")
        self.node_list.grid(row=0, column=0, columnspan=7, sticky='WE')
        self.node_list.insert(parent='', index='end', iid=1, text='Node 1', values=[1, "Module1", "type1", "1.0.1"])
        self.node_list.insert(parent='', index='end', iid=2, text='Node 2', values=[1, "Module2", "type1", "1.2.0"])
        self.out_text = tk.scrolledtext.ScrolledText(self.message_frame, height=15, width=30)
        self.out_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.clear_button = tk.Button(self.node_frame, text="Clear")
        self.clear_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
