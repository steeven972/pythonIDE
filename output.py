
import tkinter as tk

class Output():
        def __init__(self, root):
            self.root = root
            self.frame = tk.Frame(self.root, bg="white")
            self.frame.grid(row=1, column=1, sticky="nsew")
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)

            self.text = tk.Text(self.frame, bg="#1e1e1e", fg="#dcdcdc")
            self.text.grid(row=0, column=0, sticky="nsew")

            scroll_out = tk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
            scroll_out.grid(row=0, column=1, sticky="ns")