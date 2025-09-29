 
import tkinter as tk
import subprocess
from utils import start_thread

class Input:
        def __init__(self, root, output_text):
            self.root = root
            self.output_text = output_text
            
            self.frame = tk.Frame(self.root, bg="white")
            self.frame.grid(row=0, column=1, sticky="nsew")
            self.frame.grid_rowconfigure(1, weight=1)
            self.frame.grid_columnconfigure(0, weight=3)
        
            self.toolbar = tk.Frame(self.frame, bg="#dcdcdc")
            self.toolbar.grid(row=0, column=0, sticky="nsew")

            self.btn = tk.Button(self.toolbar, text="Run", borderwidth=0, command=self.run)
            self.btn.pack(side="right", padx=70, pady=5)
        
            self.text = tk.Text(self.frame, bg="#2e2e2e", fg="white", insertbackground="white", wrap="none")
            self.text.grid(row=1, column=0, sticky="nsew")

            scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=self.text.yview, bg="blue")
            scroll_y.grid(row=1, column=1, sticky="ns")

            self.text.config(font=("Consolas", 12), yscrollcommand=scroll_y.set)
        
        @start_thread
        def run(self):
            sys_out = self.text.get("1.0", "end-1c")
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

        def get_frame(self):
             return self.frame
        def get_text(self):
             return self.text