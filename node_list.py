import tkinter as tk
from tkinter import ttk


class NodeList(tk.Frame):
    """Display list of Node Modules"""
    column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W},
        'Id': {'label': 'ID', 'width': 100},
        'Name': {'label': 'Name', 'width': 100, 'anchor': tk.W},
        'Type': {'label': 'Type', 'width': 100},
        'Version': {'label': 'Version', 'width': 100}
    }
    default_width = 50
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.treeview = ttk.Treeview(self, columns=list(self.column_defs.keys())[1:], selectmode='browse')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.selected_node = tk.IntVar()
        self.treeview.grid(row=0, column=0, sticky='NSEW')
        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.treeview.heading(name, text=label, anchor=anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)
            self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview())
            self.treeview.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Get Parameters", command=self.get_all_parameters)
        self.menu.add_command(label="Get Node Variables")
        self.treeview.bind('<Double-1>', self.on_open_node)
        self.treeview.bind('<<TreeviewSelect>>', self.on_select_node)
        self.treeview.bind('<Button-2>', self.on_right_click)

    def populate(self, rows):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        valuekeys = list(self.column_defs.keys())[1:]
        # print(f"valuekeys {str(valuekeys)}")
        # print(f"rows {str(enumerate(rows))}")
        for rownum, rowdata in enumerate(rows):
            values = [rowdata[key] for key in valuekeys]
            self.treeview.insert('', 'end', iid=str(rownum), text=str(rownum), values=values)
        if len(rows) > 0:
            self.treeview.focus_set()
            self.treeview.selection_set(0)
            self.treeview.focus('0')

    def on_open_node(self, *args):
        selected_id = self.treeview.selection()[0]
        node_id = self.treeview.item(selected_id)['values'][0]
        self.callbacks['on_open_node'](node_id)
        print(f"on_open_node: {str(selected_id)} {self.treeview.selection()} {str(node_id)}")

    def on_select_node(self, *args):
        selected_id = self.treeview.selection()[0]
        self.selected_node.set(self.treeview.item(selected_id)['values'][0])
        node_id = self.treeview.item(selected_id)['values'][0]
        self.callbacks['on_select_node'](node_id)
        print(f"node_list:on_select_node: {str(selected_id)} {self.treeview.selection()}")

    def on_right_click(self, e, *args):
        selected_id = self.treeview.selection()[0]
        node_id = self.treeview.item(selected_id)['values'][0]
        print(f"on_right_click: {str(selected_id)} {node_id}")
        self.menu.tk_popup(e.x_root, e.y_root)

    def get_all_parameters(self):
        print(f"get_all_parameters: {str(self.selected_node.get())}")
        for i in range(21):
            self.callbacks['get_node_parameter'](self.selected_node.get(), i)

