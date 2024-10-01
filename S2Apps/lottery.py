import tkinter as tk
from tkinter import ttk ,filedialog,Button,messagebox
import random
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text file","*.txt")])
    file_entry.delete(0,tk.END)
    file_entry.insert(tk.END,file_path)

def select_winners():
    file_path = file_entry.get()
    try:
        num = int(winners_entry.get())
        if num<= 0:
            messagebox.showinfo("Invalid input","please enter an integer number!")
            return
    except ValueError:
        messagebox.showwarning("Invalid input","please enter a number!")
        return
        
    try:
        with open(file_path,"r") as file:
            name_list = file.read().splitlines()
            if len(name_list) < num :
                messagebox.showwarning("Invalid input","please enter a valid number!")
                return
            winners_list = random.sample(name_list,num)
            top_window = tk.Toplevel()
            top_window.title("Winners")
            top_window.resizable(1,1)
            top_window.geometry("400x600")
            top_window.configure(background="#9E4784")
            won_label = ttk.Label(top_window,background="#7A3E65",font=("Ariyal",24),text="Winners",foreground="White")
            won_label.pack(pady=10)
            winners_list = [f"{i+1}-{j}"for i,j in enumerate(winners_list)]
            winners = "\n".join(winners_list)
            show_winners = ttk.Label(top_window,background="#7A3E65",font=("Ariyal",24),text=winners,foreground="White")
            show_winners.pack(pady=10)
            top_window.mainloop() 

    except FileNotFoundError:
        messagebox.showwarning("File error","file not found!")

    
    except Exception as e:
        messagebox.showwarning("Error",str(e))

    
        
window = tk.Tk()
window.title("Lottery")
window.geometry("500x500")
window.resizable(True,True)
window.configure(background="#2D2727")

file_label = ttk.Label(window,background="#413543",font=("Ariyal",24),text="Choose file",foreground="#FFD966")
file_label.pack(pady=10)

style = ttk.Style()
style.configure("TFrame",background="#19A7CE")

file_frame = ttk.Frame(window,style="TFrame")
file_frame.pack()

file_entry = ttk.Entry(file_frame,font=("Ariyal",14))
file_entry.grid(row = 0,column= 0 ,padx=5,pady=5)

file_btn = ttk.Button(file_frame,command=select_file,text="open file")
file_btn.grid(row = 0,column= 1 ,padx=5,pady=5)


winners_label = ttk.Label(window,background="#413543",font=("Ariyal",20),text="How many winners?",foreground="#FFD966")
winners_label.pack(pady=10)

winners_entry = ttk.Entry(window,font=("Ariyal",20),width=10)
winners_entry.pack()

select_btn = ttk.Button(window,command=select_winners,text="Select Winners")
select_btn.pack(pady=5)

window.mainloop()