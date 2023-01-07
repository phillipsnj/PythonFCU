import tkinter as tk
from tkinter import ttk


class NodeVariablesFrame(tk.Frame):
    def __init__(self, parent, callbacks, node, node_variables, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        self.node_variables = node_variables
        self.node = node
        # ttk.Label(self, text="Node Variables") \
        #     .grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.main_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.main_frame, anchor='ne')

        for i in range(self.node['number_of_node_variables'] + 1):
            self.enter_node_variable(i, 0, self.node_variables[i])
        # enter_node_variable(new_window, 2, 0, self.selected_node_variables[2])

    def enter_node_variable(self, row, column, variable):
        ttk.Label(self.main_frame, text=f"Variable {row} : ")\
            .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        ttk.Entry(self.main_frame, textvariable=variable)\
            .grid(row=row, column=column+1, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

