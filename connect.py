from tkinter import *
import sqlite3
def db_connection() :
    db_path = 'database/Be_Lune.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn,cursor