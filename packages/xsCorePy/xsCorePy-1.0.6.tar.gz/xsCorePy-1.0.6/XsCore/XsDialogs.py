import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()


def showInfo(msg: str, title='提示'):
    tkinter.messagebox.showinfo(title, msg)


def showWarning(msg: str, title='警告'):
    tkinter.messagebox.showwarning(title, msg)


def showError(msg: str, title='出错了'):
    tkinter.messagebox.showerror(title, msg)


def askAskYesNo(msg: str, title='提示') -> bool:
    return tkinter.messagebox.askyesno(title, msg)


def askAskYesNoCancel(msg: str, title='提示') -> bool:
    return tkinter.messagebox.askyesnocancel(title, msg)


def askOpenfile():
    fileName = filedialog.askopenfilename()
    return fileName


def askOpenFolder():
    folderPath = filedialog.askdirectory()
    return folderPath
