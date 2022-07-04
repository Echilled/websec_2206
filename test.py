import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
# import win32com.client 
import crawler


root = tk.Tk()
v = tk.IntVar()

#setting title
root.title("Test")
#setting window size
width=699
height=519
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)


tk.Label(root, text="Website").grid(row=14, column= 0)
e1 = tk.Entry(root)
e1.grid(row=15, column=0)

#Submit button
def callback():
    crawler.Crawler(e1.get())
    

MyButton1 = Button(root, text="Submit", width=10, command=callback)
MyButton1.grid(row=16, column=0)

root.mainloop()