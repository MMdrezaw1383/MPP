import tkinter as tk
from tkinter import ttk ,filedialog,Button

def select_file():
    pass
window = tk.Tk()
window.title("Lottery")
window.geometry("500x500")
window.resizable(True,True)
window.configure(background="#2D2727")

file_label = ttk.Label(window,background="#413543",font=("Ariyal",14),text="choose file",foreground="#FFD966")
file_label.pack(pady=20)

style = ttk.Style()
style.configure("TFrame",background="#19A7CE")
file_frame = ttk.Frame(window,style="TFrame")
file_frame.pack()

file_entry = ttk.Entry(file_frame,font=("Ariyal",14))
file_entry.grid(row = 0,column= 0 ,padx=5,pady=5)

file_btn = ttk.Button(file_frame,command=select_file,text="open file")
file_btn.grid(row = 0,column= 1 ,padx=5,pady=5)

window.mainloop()