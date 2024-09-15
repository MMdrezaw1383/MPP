from tkinter import filedialog, messagebox, Button, Tk, Label
# baraye ye halat grafiki bara entekhab file ha
# neshan dadan yek message
# neveshtan button ha
import shutil
import os, sys, subprocess
import easygui


def file_open_box():
    path = easygui.fileopenbox()
    return path


# print(file_open_box())

def directory_open_box():
    path = filedialog.askdirectory()
    return path


# print(directory_open_box()

def open_file():
    path = file_open_box()
    try:
        # os.startfile(path)
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, path])
    except TypeError:
        messagebox.showinfo("error", "couldn't open file!")


def copy_file():
    source = file_open_box()
    destination = directory_open_box()
    try:
        shutil.copy(source, destination)
        messagebox.showinfo("succeed", "succeed!")
    except TypeError:
        messagebox.showinfo("error", "not succeed!")


def delete_file():
    path = file_open_box()
    try:
        os.remove(path)
        messagebox.showinfo("mmm", "file deleted!")
    except TypeError:
        messagebox.showinfo("error", "error!")


def rename_file():
    try:
        file = file_open_box()
        path = os.path.dirname(file)
        extention = os.path.splitext(file)[1]
        # print(extention)
        if file:
            new_name = input("enter name: ")
        path2 = os.path.join(path, new_name + extention)
        # print(path2)
        os.rename(file, path2)
        messagebox.showinfo("mmd", "succeed!")
    except TypeError:
        messagebox.showinfo("error", "error!")


def move_file():
    src = file_open_box()
    des = directory_open_box()
    if src == des:
        pass
    else:
        try:
            shutil.move(src, des)
            messagebox.showinfo("mmd", "succeed!")
        except TypeError:
            messagebox.showinfo("error", "not succeed!")


def make_dir():
    path = directory_open_box()
    dirname = input("enter name: ")
    dirpath = os.path.join(path, dirname)
    os.mkdir(dirpath)


def remove_directory():
    try:
        path = directory_open_box()
        if path:
            os.remove(path)
            messagebox.showinfo("mmd", "succeed!")
    except TypeError:
        messagebox.showinfo("error", "not succeed!")


def list_files():
    path = directory_open_box()
    listfiles = sorted(os.listdir(path))
    for i in listfiles:
        print(i)


window = Tk()
window.title("file manager")
window.geometry("400x500")
window.configure(bg="black")
Label(window, text="what do you want to do?", width="50").pack()

Button(window, command=open_file, text="open file"
       , fg="blue", activebackground="red", background="white", width="15").pack()
Button(window, command=copy_file, text="copy file"
       , fg="blue", activebackground="red", background="white", width="15").pack()
Button(window, command=rename_file, text="rename file"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()
Button(window, command=delete_file, text="delete file"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()
Button(window, command=move_file, text="move file"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()
Button(window, command=make_dir, text="make directory"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()
Button(window, command=remove_directory, text="remove directory"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()
Button(window, command=list_files, text="all files"
       , fg="blue", activeforeground="red", bg="white", width="15").pack()

window.mainloop()
