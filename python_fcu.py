import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from fcu_widgets import display_label
from node_list import NodeList
from node_event_list import NodeEventList
from canusb4 import CanUsb4
import cbus_message

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
        with open('merg_config.json') as f:
            self.merg = json.load(f)
        print(f"Config {str(self.data['port'])}")
        self.canusb4 = CanUsb4(self.process_incoming_message)
        # self.nodes = self.layout['nodes']
        print(f"Layout Nodes {str(self.layout['nodes'])}")
        self.node_events = {}
        self.actions = {}
        self.actions['B6'] = self.pnn
        self.actions['F2'] = self.enrsp
        self.selected_node = tk.IntVar()
        self.selected_event = tk.StringVar()
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
        self.event_frame = NodeEventList(self, {"on_select_event": self.on_select_event})
        self.event_frame.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")
        self.message_frame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        # self.node_frame.populate([
        #     {'Id': 1, 'Name': "Module1", 'Type': 'type1', 'Version': "1.0.1"},
        #     {'Id': 2, 'Name': "Module2", 'Type': 'type1', 'Version': "1.2.1"}
        # ])
        self.populate_node_list()
        # self.event_frame.populate([
        #     {'Id': 1, 'Name': "Module1", 'Type': 'type1', 'Version': "1.0.1"},
        #     {'Id': 2, 'Name': "Module2", 'Type': 'type1', 'Version': "1.2.1"}
        # ])
        self.message_text = tk.scrolledtext.ScrolledText(self.message_frame, height=15, width=30)
        self.message_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        display_label(self, 2, 2, self.selected_node)
        display_label(self, 2, 3, self.selected_event)
        # self.clear_button = tk.Button(self.node_frame, text="Clear")
        # self.clear_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.check_button = tk.Button(self.node_frame, text="QNN", command=self.check_nodes)
        self.check_button.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.canusb4.start()

    def on_select_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"selected_node changed : {str(self.selected_node.get())}")
        self.get_node_events(node_id)
        self.populate_event_list(node_id)

    def on_open_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"selected_node open : {str(self.selected_node.get())}")

    def on_select_event(self, event_identifier):
        self.selected_event.set(event_identifier)
        print(f"selected_event changed : {str(self.selected_node.get())}")

    def populate_node_list(self):
        print(f"populate_node_list {str(self.layout['nodes'].values())}")
        self.node_frame.populate(list(self.layout['nodes'].values()))

    def populate_event_list(self, node_id):
        print(f"populate_event_list {str(list(self.layout['nodes'][str(node_id)]['events'].values()))}")
        self.event_frame.populate(list(self.layout['nodes'][str(node_id)]['events'].values()))
        # self.event_frame.populate([
        #     {'Id': 1, 'Identifier': "Module1", 'Event': 'type1', 'Variables': "1.0.1"}
        # ])

    def process_incoming_message(self, msg):
        # print(f"Incoming Message : {msg}")
        output = '<== '+msg
        self.message_text.insert(tk.END, str(output) + "\n")
        self.message_text.yview(tk.END)
        if cbus_message.opcode(msg) in self.actions:
            func = self.actions[cbus_message.opcode(msg)]
            func(msg)
            # self.actions(msg)
        else:
            print(f'Unsupported OpCode : {cbus_message.opcode(msg)}')

    def process_output_message(self, msg):
        output = '==> '+msg
        # print(f"Outgoing Message : {msg}")
        self.canusb4.send(msg)
        self.message_text.insert(tk.END, str(output) + "\n")
        self.message_text.yview(tk.END)

    def check_nodes(self):
        self.process_output_message(':SB040N0D;')

    def get_node_events(self, node_id):
        output = ':SB040N57'+cbus_message.pad(node_id, 4)+';'
        self.process_output_message(output)

    def save_layout(self):
        with open('layout.json', 'w') as f:
            json.dump(self.layout, f)

    def pnn(self, msg):
        # print(f"Processing PNN {cbus_message.opcode(msg)}")
        node_id = cbus_message.node_id(msg)
        module_identifier = cbus_message.get_str(msg, 13, 4)
        flags = cbus_message.flags(cbus_message.get_int(msg, 17, 2))
        if module_identifier in self.merg['modules']:
            module_type = self.merg['modules'][module_identifier]['name']
        else:
            module_type = 'UNKNOWN'
        # print(f"Module Type is : {module_type}")
        # print(f"Nodes : {str(self.layout['nodes'])}")
        # print(f"Node {str(self.layout['nodes'][str(node_id)])}")
        if str(node_id) not in self.layout['nodes']:
            print(f"Node does not exist : {node_id} {module_identifier} {str(flags)}")
            self.layout['nodes'][str(node_id)] = {
                'Id': node_id,
                'Name': "Node "+str(node_id),
                'Type': module_type,
                'Version': "1.0.1",
                'flags': flags,
                'parameters': {},
                'node_variables': {},
                'events': {}
            }
            self.save_layout()
            self.populate_node_list()
        else:
            print(f"Node does exist : {node_id} {module_identifier} {str(flags)}")

    def enrsp(self, msg):
        print(f"Processing ENRSP {cbus_message.opcode(msg)}")
        node_id = cbus_message.node_id(msg)
        event_identifier = cbus_message.get_str(msg, 13,8)
        event_index = cbus_message.get_str(msg, 21, 2)
        # print(f"Node Event : {node_id} {event_identifier} {event_index}")
        # print(f"Node Event for {str(self.layout['nodes'][str(node_id)])}")
        if event_identifier not in self.layout['nodes'][str(node_id)]['events']:
            print(f"Event {event_identifier} is not found for {str(node_id)}")
            self.layout['nodes'][str(node_id)]['events'][event_identifier] = {
                'event_identifier': event_identifier,
                'event_index': event_index,
                'variables': {}
            }
            self.save_layout()
        else:
            print(f"Event {event_identifier} found for {str(node_id)}")


