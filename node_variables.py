import tkinter as tk
from tkinter import ttk


class NodeList(tk.Frame):
    def __init__(self, parent, callbacks, node, node_variables, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.node_variables = node_variables
        self.node = node
