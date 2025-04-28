import sqlite3
from tkinter import *
from tkinter import ttk, Menu, messagebox


def db_connection():
    db_path = 'database/Be_Lune.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn,cursor

def fetch_data():
    conn, cursor = db_connection()
    cursor.execute("SELECT product_id, name, price FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def populate_treeview():
    for row in fetch_data():
        tree.insert("", "end", values=row)

def show_context_menu(event):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)

def edit_item():
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        messagebox.showinfo("Edit", f"แก้ไขข้อมูล: {item}")

def delete_item():
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        confirm = messagebox.askyesno("Delete", f"ต้องการลบข้อมูล: {item} หรือไม่?")
        if confirm:
            conn, cursor = db_connection()
            cursor.execute("DELETE FROM products WHERE product_id=?", (item[0],))
            conn.commit()
            conn.close()
            tree.delete(selected)
            messagebox.showinfo("Delete", "ลบข้อมูลสำเร็จแล้ว!")

# ---------- GUI ----------

root = Tk()
root.title("Treeview ดึงข้อมูลจาก DB + คลิกขวาเมนู")
root.geometry("500x400")

# Treeview
columns = ("id", "name", "price")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("price", text="Price")

for col in columns:
    tree.column(col, width=150, anchor=W)

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

populate_treeview()

# Context Menu
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Edit", command=edit_item)
context_menu.add_command(label="Delete", command=delete_item)

tree.bind("<Button-3>", show_context_menu)

root.mainloop()
