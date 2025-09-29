import threading 
import time
import tkinter as tk
import os
import keyword
import re

PY_KEYWORDS = keyword.kwlist
BUILTINS = dir(__builtins__)
    
def start_thread(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=lambda: func(*args, **kwargs))
        t.daemon = True
        t.start()
    return wrapper

def run_task(self):
    for i in range(10):
        time.sleep(1)
        print(f"travail {i}")

        self.after(0, lambda i=i: self.label.config(text=f"Tache {i} en cours..."))
    self.after(0, lambda: self.label.config(text=f"Tache terminée !"))


class FileParcours:
    def __init__(self, location, explorer_frame, input_text, output_text):
        self.location = location
        self.explorer_frame = explorer_frame
        self.input_text = input_text
        self.output_text = output_text

    @start_thread
    def _add_file_to_explorer(self):
        for item in os.listdir(self.location):
            self.full_path = os.path.join(self.location, item)
            if os.path.isdir(self.full_path):
                self.explorer_frame.after(0, lambda full_path = self.full_path, item=item: self.__add_dir_menubtn(full_path, item))
                
            elif os.path.isfile(self.full_path): 
                self.explorer_frame.after(0, lambda full_path = self.full_path, item=item: self._add_file_btn(full_path, item))

    def _add_file_btn(self, full_path, item):
        fileBtn = tk.Button(self.explorer_frame, text=f"{item}",borderwidth=0, bg="#2e2e2e", fg="#dcdcdc",command=lambda full_path = full_path: self.change_file(full_path))
        fileBtn.pack(fill="x")
    
    def __add_dir_menubtn(self, full_path, item):
        mb = tk.Menubutton(self.explorer_frame, text=item, bg="#232323", fg="#dcdcdc", borderwidth=0)
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

    @start_thread
    def _list_files_dirs(self, callback):
        for item in os.listdir(self.location):
            os.path.join(self.location, item)
            self.after(0, lambda: callback(item))

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
        self.input_text.tag_config("keyword", foreground="purple")
        self.input_text.tag_config("builtin", foreground="blue")
        self.input_text.tag_config("string", foreground="orange")
        self.input_text.tag_config("comment", foreground="green")

    def on_text_change(self, event=None):
        self.highlight_python()
