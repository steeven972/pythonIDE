import threading 
import time
import tkinter as tk



    
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



