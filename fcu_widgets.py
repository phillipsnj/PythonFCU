import tkinter as tk
from tkinter import ttk


def display_button(parent, row, column, name, text):
    print("Button")
    output = str(text + "\r")
    ttk.Button(parent, text=name, command=lambda text=output: ButtonPress(uart, text)) \
        .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


def display_value(parent, row, column, name):
    print("Label")
    ttk.Label(parent, textvariable=name) \
        .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)


def display_label(parent, row, column, name):
    print("Label")
    ttk.Label(parent, text=name) \
        .grid(row=row, column=column, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)