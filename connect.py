import sqlite3
import os

def db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database", "Be_Lune.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor
