import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from fcu_widgets import display_label
from node_list import NodeList
from node_event_list import NodeEventList
# import serial
import time
import json


class PythonFCU(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('config.json') as f:
            self.data = json.load(f)
        with open('layout.json') as f:
            self.layout = json.load(f)
        print(f"Config {str(self.data['port'])}")
        self.nodes = self.layout['nodes']
        print(f"Nodes {str(self.nodes)}")
        self.node_events = {}
        self.selected_node = tk.IntVar()
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
        self.node_frame = NodeList(self, {"on_select_node": self.on_select_node, "on_open_node": self.on_open_node})
        self.node_frame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.event_frame = NodeEventList(self, "callback")
        self.event_frame.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")
        self.message_frame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        # self.node_frame.populate([
        #     {'Id': 1, 'Name': "Module1", 'Type': 'type1', 'Version': "1.0.1"},
        #     {'Id': 2, 'Name': "Module2", 'Type': 'type1', 'Version': "1.2.1"}
        # ])
        self.populate_node_list()
        self.event_frame.populate([
            {'Id': 1, 'Name': "Module1", 'Type': 'type1', 'Version': "1.0.1"},
            {'Id': 2, 'Name': "Module2", 'Type': 'type1', 'Version': "1.2.1"}
        ])
        self.out_text = tk.scrolledtext.ScrolledText(self.message_frame, height=15, width=30)
        self.out_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        display_label(self, 2, 2, self.selected_node)
        # self.clear_button = tk.Button(self.node_frame, text="Clear")
        # self.clear_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')

    def on_select_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"selected_node changed : {str(self.selected_node.get())}")

    def on_open_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"selected_node open : {str(self.selected_node.get())}")

    def populate_node_list(self):
        print(f"populate_node_list {str(self.nodes.values())}")
        self.node_frame.populate(list(self.nodes.values()))



