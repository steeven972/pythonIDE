import tkinter as tk
import subprocess
import os
from utils import start_thread
from tkinter import messagebox

import keyword
import re

PY_KEYWORDS = keyword.kwlist
BUILTINS = dir(__builtins__)
location = os.getcwd()


class MiniIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Mini IDE python")
        self.createMenu()
        self.createWidgets()
        self.input_text.bind("<KeyRelease>", self.on_text_change)
        
    
    def createMenu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
    
        menu_bar.add_command(label="Run", command=self.run)
        self.config(menu=menu_bar)

    def createWidgets(self):
        
        self.explorer_frame = tk.Frame(self, width=200, bg="lightgray")
        self.explorer_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.explorer_frame.grid_propagate(False)

        self._add_file_to_explorer()

        self.entryTest = tk.Button(self.explorer_frame, text="EXPLORER", borderwidth=0, width=25)
        self.entryTest.pack(fill="x")

        self.input_frame = tk.Frame(self, bg="white")
        self.input_frame.grid(row=0, column=1, sticky="nsew")
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=3)

       
    
        self.toolbar = tk.Frame(self.input_frame, bg="black")
        self.toolbar.grid(row=0, column=0, sticky="nsew")

        self.btn = tk.Button(self.toolbar, text="Run", borderwidth=0, command=self.run)
        self.btn.pack(side="right", padx=70, pady=5)

     
        self.input_text = tk.Text(self.input_frame)
        self.input_text.grid(row=1, column=0, sticky="nsew")

        scroll_y = tk.Scrollbar(self.input_frame, orient="vertical", command=self.input_text.yview, bg="blue")
        self.input_text.config(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=1, column=1, sticky="ns")
      
        self.output_frame = tk.Frame(self, bg="white")
        self.output_frame.grid(row=1, column=1, sticky="nsew")
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(self.output_frame, bg="black", fg="white")
        self.output_text.grid(row=0, column=0, sticky="nsew")

        self.input_text.config(font=("Consolas", 12))
        self.output_text.config(font=("Consolas", 11))


    @start_thread
    def _add_file_to_explorer(self):
        for item in os.listdir(location):
            full_path = os.path.join(location, item)
            if os.path.isdir(full_path):
                self.explorer_frame.after(0, lambda full_path = full_path, item=item: self.__add_dir_menubtn(full_path, item))
                
            elif os.path.isfile(full_path): 
                self.explorer_frame.after(0, lambda full_path = full_path, item=item: self._add_file_btn(full_path, item))

    def _add_file_btn(self, full_path, item):
        fileBtn = tk.Button(self.explorer_frame, text=f"{item}",borderwidth=0, bg="red",command=lambda: self.change_file(full_path))
        fileBtn.pack(fill="x")

    def __add_dir_menubtn(self, full_path, item):
        mb = tk.Menubutton(self.explorer_frame, text=item, bg="lightblue", borderwidth=0)
        mb.menu = tk.Menu(mb, tearoff=0)
        mb["menu"] = mb.menu       
        self._populate_menu(full_path, mb.menu)
        mb.pack(fill="x")
        
    @start_thread
    def _populate_menu(self, folder_path, menu):
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            if os.path.isdir(full_path):
                menu.after(0, lambda full_path=full_path, item=item, menu=menu: self.__add_sub_menu(full_path, item, menu))
            else:
                menu.after(0, lambda full_path=full_path, item=item: menu.add_command(label=item, command=lambda: self.change_file(full_path)) )
                

    def __add_sub_menu(self, full_path, item, menu):
        sub_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label=item, menu=sub_menu)
        self._populate_menu(full_path, sub_menu)

    def _list_files_dirs(self, callback):
        for item in os.listdir(location):
            os.path.join(location, item)
            self.after(0, lambda: callback(item))
            
    @start_thread
    def run(self):
        sys_out = self.input_text.get("1.0", "end-1c")
        self.output_text.delete("1.0", "end")

        with open("temp_code.py", "w", encoding="utf-8") as f:
            f.write(sys_out)

        result = subprocess.run(
            ["python", "temp_code.py"],
            capture_output=True,
            text=True
        )

        self.output_text.after(0, lambda: self.show_output(result))
        
    def show_output(self, result):
        self.output_text.config(state="normal")

        if result.stdout:
            self.output_text.insert("end", result.stdout)
        else:
            self.output_text.insert("end", result.stderr)

    def open(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[("all files", "*.*")])
        self.change_file(filename)

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
            self._add_file_btn(filename, file_name_only)
        
    def change_file(self, path):
        try:
            if os.path.isfile(path):  
                with open(path, "r") as f:
                    content = f.read()
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("end", content)
                    self.highlight_python() 
            else:
                self.output_text.delete("1.0", "end")
                self.output_text.insert("end", f"{path} n'est pas un fichier et ne peut pas être ouvert.")
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", e )
    
    def highlight_python(self):
        content = self.input_text.get("1.0", "end-1c")
        self.input_text.tag_remove("keyword", "1.0", "end")
        self.input_text.tag_remove("builtin", "1.0", "end")
        self.input_text.tag_remove("string", "1.0", "end")
        self.input_text.tag_remove("comment", "1.0", "end")

        # Mots-clés
        for kw in PY_KEYWORDS:
            for match in re.finditer(rf'\b{kw}\b', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.input_text.tag_add("keyword", start, end)

        # Fonctions/objets builtins
        for bi in BUILTINS:
            for match in re.finditer(rf'\b{bi}\b', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.input_text.tag_add("builtin", start, end)

        # Chaînes de caractères
        for match in re.finditer(r'(\".*?\"|\'.*?\')', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.input_text.tag_add("string", start, end)

        # Commentaires
        for match in re.finditer(r'#[^\n]*', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.input_text.tag_add("comment", start, end)

        # Appliquer les couleurs
        self.input_text.tag_config("keyword", foreground="blue")
        self.input_text.tag_config("builtin", foreground="purple")
        self.input_text.tag_config("string", foreground="green")
        self.input_text.tag_config("comment", foreground="gray")

    def on_text_change(self, event=None):
        self.highlight_python()

    



screen = MiniIDE()
print("MiniIDE is running...")
screen.mainloop()
print("MiniIDE closed !!")
        