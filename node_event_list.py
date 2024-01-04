import tkinter as tk
from tkinter import ttk


class NodeEventList(tk.LabelFrame):
    """Display list of Node Modules"""
    column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W},
        'event_index': {'label': 'ID', 'width': 100},
        'event_identifier': {'label': 'Event', 'width': 100, 'anchor': tk.W},
        'variables': {'label': 'Variables', 'width': 100}
    }
    default_width = 50
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(text='Events')
        self.callbacks = callbacks
        self.treeview = ttk.Treeview(self, columns=list(self.column_defs.keys())[1:], selectmode='browse')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
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
        self.treeview.bind('<Double-1>', self.on_open_event)
        self.treeview.bind('<<TreeviewSelect>>', self.on_select_event)

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

    def on_open_event(self, *args):
        selected_id = self.treeview.selection()[0]
        # self.callbacks['on_open_event'][selected_id]
        print(f"on_open_event: {str(selected_id)}")

    def on_select_event(self, *args):
        try:
            selected_id = self.treeview.selection()[0]
            event_id = self.treeview.item(selected_id)['values'][0]
            self.callbacks['on_select_event'](event_id)
            print(f"on_select_event: {str(event_id)} : {str(self.treeview.item(selected_id)['values'])}")
        except IndexError:
            print(f"no events found")
