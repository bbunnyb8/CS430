import sqlite3
from tkinter import messagebox
from tkinter import *

def createconnection() :
    global conn,cursor
    db_path = 'database/Be_Lune.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

def mainwindow() :
    root = Tk()
    w = 1194
    h = 834
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/2
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    root.config(bg='#FFFFFF')
    root.title("Be Lune : POS")
    root.option_add('*font',"Garamond 24 bold")
    root.rowconfigure((0,1,2,3),weight=1)
    root.columnconfigure((0,1,2,3),weight=1)
    return root

# - MAIN PROGRAM -

root = mainwindow()

root.mainloop()