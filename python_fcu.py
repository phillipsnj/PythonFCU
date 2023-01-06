import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from fcu_widgets import display_value, display_label
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

        # self.nodes = self.layout['nodes']
        print(f"Layout Nodes {str(self.layout['nodes'])}")
        self.global_variables = {
            "selected_node": tk.IntVar(),
            "selected_event": tk.StringVar(),
            "com_port": tk.StringVar()
        }
        self.node_events = {}
        self.actions = {}
        self.actions['B6'] = self.pnn
        self.actions['F2'] = self.enrsp
        self.actions['9B'] = self.paran
        self.selected_node = tk.IntVar()
        self.selected_event = tk.StringVar()
        self.selected_node_variables = []
        self.canusb4 = CanUsb4(self.process_incoming_message, self.global_variables)

        self.title("Python FCU Development")
        self.geometry("1000x700")
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
        self.check_button = tk.Button(self, text="Check Modules", command=self.check_nodes)

        self.node_frame = NodeList(self, {
            "on_select_node": self.on_select_node,
            "on_open_node": self.on_open_node,
            "get_node_parameter": self.get_node_parameter
        })

        self.event_frame = NodeEventList(self, {"on_select_event": self.on_select_event})

        self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")

        self.populate_node_list()
        self.message_text = tk.scrolledtext.ScrolledText(self.message_frame, height=15, width=30)

        display_value(self, 3, 1, self.selected_node)
        display_value(self, 5, 1, self.selected_event)
        display_value(self, 6, 1, self.global_variables['com_port'])
        # display_label(self, 5, 0, self.layout['nodes'][self.selected_node.get()]['number_of_node_variables'])
        self.clear_messages_button = tk.Button(self, text="Clear Messages", command=self.clear_messages)

        self.check_button.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.node_frame.grid(row=2, column=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.event_frame.grid(row=4, column=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_frame.grid(row=2, column=8, columnspan=7, rowspan=4, sticky='NW', padx=5, pady=5, ipadx=5, ipady=5)
        self.message_text.grid(row=2, column=0, columnspan=4, rowspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')
        self.clear_messages_button.grid(row=5, column=7, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')

        self.canusb4.start()

    def on_select_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"selected_node changed : {str(self.selected_node.get())}")
        self.selected_event.set('')
        self.get_node_events(node_id)
        self.populate_event_list(node_id)
        self.get_node_parameter(node_id, 8)

    def on_open_node(self, node_id):
        self.selected_node.set(node_id)
        print(f"on_open_node open : {str(self.selected_node.get())}")
        self.get_node_parameter(node_id, 5)
        self.get_node_parameter(node_id, 6)
        self.get_node_parameter(node_id, 7)
        self.get_node_parameter(node_id, 2)
        self.get_node_parameter(node_id, 20)

    def on_select_event(self, event_identifier):
        self.selected_event.set(event_identifier)
        print(f"on_select_event changed : {str(self.selected_node.get())}")

    def populate_node_list(self):
        # print(f"populate_node_list {str(self.layout['nodes'].values())}")
        self.node_frame.populate(list(self.layout['nodes'].values()))

    def populate_event_list(self, node_id):
        # print(f"populate_event_list {str(list(self.layout['nodes'][str(node_id)]['events'].values()))}")
        self.event_frame.populate(list(self.layout['nodes'][str(node_id)]['events'].values()))
        # self.event_frame.populate([
        #     {'Id': 1, 'Identifier': "Module1", 'Event': 'type1', 'Variables': "1.0.1"}
        # ])

    def process_incoming_message(self, msg):
        # print(f"Incoming Message : {msg}")
        output = '<== ' + msg
        self.message_text.insert(tk.END, str(output) + "\n")
        self.message_text.yview(tk.END)
        if cbus_message.opcode(msg) in self.actions:
            func = self.actions[cbus_message.opcode(msg)]
            func(msg)
            # self.actions(msg)
        else:
            print(f'Unsupported OpCode : {cbus_message.opcode(msg)}')

    def process_output_message(self, msg):
        output = '==> ' + msg
        # print(f"Outgoing Message : {msg}")
        self.canusb4.send(msg)
        self.message_text.insert(tk.END, str(output) + "\n")
        self.message_text.yview(tk.END)

    def check_nodes(self):
        self.process_output_message(':SB040N0D;')

    def clear_messages(self):
        self.message_text.delete(1.0, tk.END)
        self.message_text.yview(tk.END)

    def get_node_events(self, node_id):
        """ Send out a NERD Request for all Events for the selected node."""
        output = ':SB040N57' + cbus_message.pad(node_id, 4) + ';'
        self.process_output_message(output)

    def get_node_parameter(self, node_id, parameter_id):
        print(f"get_node_parameter {node_id} {parameter_id}")
        output = ':SB040N73' + cbus_message.pad(node_id, 4) + cbus_message.pad(parameter_id, 2) + ';'
        self.process_output_message(output)
        time.sleep(0.01)

    def save_layout(self):
        with open('layout.json', 'w') as f:
            json.dump(self.layout, f)
        time.sleep(0.01)

    def pnn(self, msg):
        print(f"Processing PNN {cbus_message.opcode(msg)}")
        node_id = cbus_message.node_id(msg)
        flags = cbus_message.flags(cbus_message.get_int(msg, 17, 2))
        # print(f"Module Type is : {module_type}")
        # print(f"Nodes : {str(self.layout['nodes'])}")
        # print(f"Node {str(self.layout['nodes'][str(node_id)])}")
        key = str(node_id)
        if key not in self.layout['nodes']:
            module_identifier = cbus_message.get_str(msg, 13, 4)
            if module_identifier in self.merg['modules']:
                module_type = self.merg['modules'][module_identifier]['name']
            else:
                module_type = 'UNKNOWN'
            print(f"Node does not exist : {node_id} {module_identifier} {str(flags)}")
            parameters = []
            for i in range(21):
                parameters.append('null')
            self.layout['nodes'][str(node_id)] = {
                'Id': node_id,
                'Name': "Node " + str(node_id),
                'Type': module_type,
                'Version': "1.0.1",
                'flags': flags,
                'status': True,
                'parameters': parameters,
                'node_variables': [],
                'events': {}
            }
            self.save_layout()
            # time.sleep(0.01)
            # self.get_node_parameter(node_id, 2)
            self.get_node_parameter(node_id, 6)
            # self.get_node_parameter(node_id, 7)
            self.get_node_parameter(node_id, 5)
            # self.get_node_parameter(node_id, 20)
            self.populate_node_list()
        else:
            print(f"Node does exist : {node_id} ")
            self.layout['nodes'][str(node_id)]['flags'] = flags

    def enrsp(self, msg):
        # print(f"Processing ENRSP {cbus_message.opcode(msg)}")
        node_id = cbus_message.node_id(msg)
        event_identifier = cbus_message.get_str(msg, 13, 8)
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
        # else:
        #     print(f"Event {event_identifier} found for {str(node_id)}")
        self.populate_event_list(node_id)

    def paran(self, msg):
        node_id = cbus_message.node_id(msg)
        parameter_id = cbus_message.get_int(msg, 13, 2)
        parameter_value = cbus_message.get_str(msg, 15, 2)
        print(f"Parameter Received {node_id} {parameter_id} {parameter_value}")
        # key = str(parameter_id)
        self.layout['nodes'][str(node_id)]['parameters'][parameter_id] = parameter_value
        match parameter_id:
            case 6:
                self.layout['nodes'][str(node_id)]['number_of_node_variables'] = int(parameter_value, 16)
                if len(self.layout['nodes'][str(node_id)]['node_variables']) == 0:
                    for i in range(int(parameter_value, 16) + 1):
                        self.layout['nodes'][str(node_id)]['node_variables'].append('null')
            case 5:
                self.layout['nodes'][str(node_id)]['number_of_event_variables'] = int(parameter_value, 16)
            case 4:
                self.layout['nodes'][str(node_id)]['max_number_of_events'] = int(parameter_value, 16)
        self.save_layout()
