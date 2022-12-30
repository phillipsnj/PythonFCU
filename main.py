from python_fcu import PythonFCU


# class PythonFCU(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # with open('config.json') as f:
#         #     self.data = json.load(f)
#         # print(f"Config {str(self.data['port'])}")
#         self.title("Python FCU Development")
#         self.geometry("800x600")
#         self.resizable(width=False, height=False)
#         self.node_frame = ttk.LabelFrame(self, text=" Modules ")
#         self.node_frame.grid(row=0, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#         self.event_frame = ttk.LabelFrame(self, text=" Events ")
#         self.event_frame.grid(row=1, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#         self.message_frame = ttk.LabelFrame(self, text=" Cbus Messages ")
#         self.message_frame.grid(row=0, column=8, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#         self.clear_button = tk.Button(self.node_frame, text="Clear")
#         self.clear_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='WE')


if __name__ == '__main__':
    print(f'FCU Running')
    app = PythonFCU()
    app.mainloop()
