import tkinter as tk
import subprocess
import os
from utils import start_thread, FileParcours
from tkinter import messagebox

import keyword
import re

from input import Input
from output import Output

PY_KEYWORDS = keyword.kwlist
BUILTINS = dir(__builtins__)
location = os.getcwd()

class MiniIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Mini IDE python")
        self.createMenu()
        #self.createWidgets()
        self.explorer_frame = tk.Frame(self, width=200, bg="lightgray")
        self.explorer_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.explorer_frame.grid_propagate(False)
        

        self.entryTest = tk.Button(self.explorer_frame, text="EXPLORER", borderwidth=0, width=25)
        self.entryTest.pack(fill="x")

        self.ouput = Output(self)
        self.output_frame = self.ouput.frame
        self.output_text = self.ouput.text

        self.input = Input(self, self.output_text)
        self.input_frame = self.input.frame
        self.input_text = self.input.text
    

        self.file_parcours = FileParcours(location, self.explorer_frame, self.input_text, self.output_text)
        self.file_parcours._add_file_to_explorer()
        
        self.input_text.bind("<KeyRelease>", self.file_parcours.on_text_change)
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-o>", lambda e: self.open())
        self.bind("<Control-r>", lambda e: self.input.run())
    
    def createMenu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
    
        menu_bar.add_command(label="Run",command=lambda: self.input.run())
        self.config(menu=menu_bar)     


    def open(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[("all files", "*.*")])
        self.file_parcours.change_file(filename)

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.input_text.get("1.0", "end-1c"))

    @start_thread
    def save_file(self):
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])

        if filename:
            self.save(filename)
            file_name_only = os.path.basename(filename)
            FileParcours(location, self.explorer_frame, self.input_text, self.output_text)._add_file_btn(filename, file_name_only)
        
  