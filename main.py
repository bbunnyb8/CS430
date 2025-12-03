from tkinter import *
import sqlite3
from tkinter import messagebox, Menu
from tkinter.ttk import Treeview
from tkinter import ttk, messagebox 
from connect import *
from config import *
from datetime import date, datetime, timedelta

""" FRONT END """
def create_window():
    root = Tk()
    root.title("Back office : Be Lune")
    root.geometry("1194x834")
    root.configure(bg=cl_white)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    return root
def create_layout(root):
    fm_main = Frame(root,bg=cl_white,padx=24,pady=24)
    fm_main.grid_rowconfigure(0, weight=1)
    fm_main.grid_columnconfigure(0, weight=1)
    fm_main.grid(row=0, column=0, sticky=NSEW)
    return fm_main
# เคลียร์ widget ทั้งหมดใน fm_main ก่อนเปลี่ยนหน้า
def clear_main_frame():
    for widget in fm_main.winfo_children():
        widget.destroy()

#Menu Bar
def bar_login():
    menu_bar = Menu(root, tearoff=0) 
    menu_bar.add_command(label='login', command=login) 
    menu_bar.add_command(label='exit', command=lambda: exit(0))  
    root.configure(menu=menu_bar)

def bar_home(user):
    if user[7] == "admin":
        menu_bar = Menu(root, tearoff=0)
        menu_bar.add_command(label='dashboard', command=lambda: dashboard(user))
        menu_bar.add_command(label='books', command=lambda: books(user))
        menu_bar.add_command(label='catagory', command=lambda: catagory(user))
        menu_bar.add_command(label='shelves', command=lambda: shelves(user))
        menu_bar.add_command(label='userManagement', command=lambda: userManagement(user))
        menu_bar.add_command(label='profile', command=lambda: profileUser(user))
        menu_bar.add_command(label='log out', command=login)
        root.configure(menu=menu_bar)

    elif user[7] == "librarian":
        menu_bar = Menu(root, tearoff=0)
        borrow_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_command(label='dashboard', command=lambda: dashboard(user))
        menu_bar.add_cascade(label='borrow', menu=borrow_menu)
        borrow_menu.add_command(label='borrowing', command=lambda: BorrowPageUser(user))  # เปลี่ยนได้ตามที่ต้องการ
        borrow_menu.add_command(label='history', command=lambda: history(user))
        menu_bar.add_command(label='books', command=lambda: books(user))
        menu_bar.add_command(label='category', command=lambda: catagory(user))
        menu_bar.add_command(label='shelves', command=lambda: shelves(user))
        menu_bar.add_command(label='profile', command=lambda: profileUser(user))
        menu_bar.add_command(label='log out', command=login)
        root.configure(menu=menu_bar)



# =========================
#      BORROW PAGE NEW
# =========================
# ==========================================================
#                      BORROW PAGE (NEW)
# ==========================================================
def BorrowPageUser(user):
    """
    หน้า Borrowing System + History
    - ค้นหานักศึกษา
    - เลือกนักศึกษา -> แสดงโปรไฟล์
    - เลือกหนังสือที่ว่าง -> ยืม
    - แสดงประวัติการยืม / คืน
    - คืนหนังสือ + คำนวณค่าปรับ
    - ลบรายการยืม (กรณีบันทึกผิด)
    """
    clear_main_frame()
    bar_home(user)

    # ค่าปรับต่อวัน (บาท)
    FINE_PER_DAY = 10

    fm = Frame(fm_main, bg=cl_white, padx=20, pady=20)
    fm.grid(row=0, column=0, sticky="nsew")

    fm.grid_rowconfigure(0, weight=0)   # title
    fm.grid_rowconfigure(1, weight=0)   # search
    fm.grid_rowconfigure(2, weight=1)   # student list
    fm.grid_rowconfigure(3, weight=0)   # profile
    fm.grid_rowconfigure(4, weight=0)   # select book
    fm.grid_rowconfigure(5, weight=1)   # history
    fm.grid_columnconfigure(0, weight=1)

    # ------------------ Title ------------------
    Label(
        fm,
        text="Borrowing System",
        bg=cl_white,
        fg="black",
        font=("Kanit", 22, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(0, 10))

    # ------------------ Search Student ------------------
    search_frame = Frame(fm, bg=cl_white)
    search_frame.grid(row=1, column=0, sticky="w", pady=(0, 10))

    Label(
        search_frame,
        text="ค้นหานักศึกษา:",
        bg=cl_white,
        font=font_h5
    ).pack(side=LEFT)

    v_search = StringVar()
    ent_search = Entry(search_frame, textvariable=v_search, width=30, bg=cl_white_gray)
    ent_search.pack(side=LEFT, padx=8, ipady=2)

    def do_search(event=None):
        load_students(v_search.get().strip())

    Button(
        search_frame,
        text="ค้นหา",
        bg=cl_red,
        fg="white",
        font=font_h5,
        command=do_search
    ).pack(side=LEFT, padx=5)

    ent_search.bind("<Return>", do_search)

    # ------------------ Student List ------------------
    Label(
        fm,
        text="รายชื่อนักศึกษา",
        bg=cl_white,
        font=("Kanit", 14, "bold")
    ).grid(row=2, column=0, sticky="w")

    student_cols = ("stdID", "firstName", "lastName", "faculty", "major")
    student_tree = ttk.Treeview(
        fm,
        columns=student_cols,
        show="headings",
        height=6
    )

    headers = ["รหัสนักศึกษา", "ชื่อ", "นามสกุล", "คณะ", "สาขา"]
    widths = [110, 120, 140, 220, 220]

    for c, h, w in zip(student_cols, headers, widths):
        student_tree.heading(c, text=h)
        student_tree.column(c, width=w, anchor=W)

    student_tree.grid(row=2, column=0, sticky="nsew", pady=(5, 10))
    scroll_std = ttk.Scrollbar(fm, orient="vertical", command=student_tree.yview)
    student_tree.configure(yscrollcommand=scroll_std.set)
    scroll_std.grid(row=2, column=1, sticky="ns", pady=(5, 10))

    # ------------------ Profile Box ------------------
    profile_box = LabelFrame(
        fm,
        text="ข้อมูลนักศึกษา",
        font=("Kanit", 14, "bold"),
        bg=cl_white
    )
    profile_box.grid(row=3, column=0, sticky="ew", pady=(0, 10))

    profile_box.grid_columnconfigure(1, weight=1)

    v_profile = {
        "stdID": StringVar(),
        "name": StringVar(),
        "faculty": StringVar(),
        "major": StringVar(),
        "email": StringVar(),
        "tel": StringVar(),
    }

    def add_profile_row(r, label, var):
        Label(profile_box, text=label, bg=cl_white, font=font_h5)\
            .grid(row=r, column=0, sticky="w", padx=10, pady=2)
        Label(profile_box, textvariable=var, bg=cl_white, font=font_h5)\
            .grid(row=r, column=1, sticky="w", padx=10, pady=2)

    add_profile_row(0, "รหัส:", v_profile["stdID"])
    add_profile_row(1, "ชื่อ:", v_profile["name"])
    add_profile_row(2, "คณะ:", v_profile["faculty"])
    add_profile_row(3, "สาขา:", v_profile["major"])
    add_profile_row(4, "อีเมล:", v_profile["email"])
    add_profile_row(5, "โทร:", v_profile["tel"])

    # ------------------ Book Select + Buttons ------------------
    action_box = Frame(fm, bg=cl_white)
    action_box.grid(row=4, column=0, sticky="ew", pady=(0, 10))

    Label(
        action_box,
        text="เลือกหนังสือเพื่อยืม:",
        bg=cl_white,
        font=font_h5
    ).pack(side=LEFT, padx=(0, 5))

    v_book = StringVar()
    book_combo = ttk.Combobox(
        action_box,
        textvariable=v_book,
        width=50,
        state="readonly"
    )
    book_combo.pack(side=LEFT, padx=5)

    # ปุ่ม ยืม / คืน / ลบ
    btn_borrow = Button(
        action_box,
        text="ยืมหนังสือ",
        bg=cl_red,
        fg="white",
        font=font_h5
    )
    btn_borrow.pack(side=LEFT, padx=8)

    btn_return = Button(
        action_box,
        text="คืนหนังสือ",
        bg="grey",
        fg="white",
        font=font_h5
    )
    btn_return.pack(side=LEFT, padx=5)

    btn_delete = Button(
        action_box,
        text="ลบรายการ",
        bg="black",
        fg="white",
        font=font_h5
    )
    btn_delete.pack(side=LEFT, padx=5)




    # ------------------ History Table ------------------
    his_frame = LabelFrame(
        fm,
        text="ประวัติการยืมของนักศึกษาคนนี้",
        font=("Kanit", 14, "bold"),
        bg=cl_white
    )
    his_frame.grid(row=5, column=0, sticky="nsew")

    his_cols = ("brwID", "bookID", "title", "borrowDate",
                "dueDate", "returnDate", "status", "fine")
    his_table = ttk.Treeview(his_frame, columns=his_cols, show="headings")

    his_headers = [
        "Borrow ID", "Book ID", "ชื่อหนังสือ",
        "วันที่ยืม", "วันกำหนดคืน", "วันที่คืน",
        "สถานะ", "ค่าปรับ"
    ]
    his_widths = [80, 80, 260, 100, 100, 100, 110, 80]

    for c, h, w in zip(his_cols, his_headers, his_widths):
        his_table.heading(c, text=h)
        his_table.column(c, width=w, anchor=W)

    his_table.pack(fill="both", expand=True)
    scroll_his = ttk.Scrollbar(his_frame, orient="vertical", command=his_table.yview)
    his_table.configure(yscrollcommand=scroll_his.set)
    scroll_his.pack(side=RIGHT, fill=Y)

    # ----------------------------------------------------------------
    #                    HELPER FUNCTIONS (inner)
    # ----------------------------------------------------------------
    def generate_new_borrow_id(cur):
        """
        gen รหัสยืม BRW001, BRW002, ...
        """
        cur.execute("""
            SELECT brwID
            FROM borrowings
            ORDER BY CAST(SUBSTR(brwID, 4) AS INTEGER) DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        if row and row[0]:
            last_num = int(row[0][3:])
            return f"BRW{last_num+1:03d}"
        return "BRW001"

    def load_students(keyword=""):
        student_tree.delete(*student_tree.get_children())
        conn, cur = db_connection()

        if keyword:
            kw = f"%{keyword}%"
            cur.execute("""
                SELECT stdID, stdFirstName, stdLastName, faculty, major
                FROM student
                WHERE stdID LIKE ?
                   OR stdFirstName LIKE ?
                   OR stdLastName LIKE ?
                ORDER BY stdID
            """, (kw, kw, kw))
        else:
            cur.execute("""
                SELECT stdID, stdFirstName, stdLastName, faculty, major
                FROM student
                ORDER BY stdID
            """)
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            student_tree.insert("", "end", values=r)

    def load_profile(std_row):
        """
        std_row: (stdID, firstName, lastName, faculty, major)
        ดึง email, tel เพิ่ม แล้วโหลด history + books
        """
        stdID = std_row[0]
        conn, cur = db_connection()
        cur.execute("""
            SELECT stdID, stdFirstName, stdLastName,
                   faculty, major, email, tel
            FROM student
            WHERE stdID = ?
        """, (stdID,))
        s = cur.fetchone()
        conn.close()

        if not s:
            return

        v_profile["stdID"].set(s[0])
        v_profile["name"].set(s[1] + " " + s[2])
        v_profile["faculty"].set(s[3])
        v_profile["major"].set(s[4])
        v_profile["email"].set(s[5] or "")
        v_profile["tel"].set(s[6] or "")

        load_history(stdID)
        load_books()

    def load_history(stdID):
        his_table.delete(*his_table.get_children())
        conn, cur = db_connection()
        cur.execute("""
            SELECT b.brwID,
                   b.bookID,
                   k.title,
                   b.borrowDate,
                   b.dueDate,
                   IFNULL(b.returnDate, '-'),
                   b.status,
                   IFNULL(b.fineAmount, 0)
            FROM borrowings b
            JOIN books k ON b.bookID = k.bookID
            WHERE b.stdID = ?
            ORDER BY b.brwID DESC
        """, (stdID,))
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            his_table.insert("", "end", values=r)

    def load_books():
        """
        โหลดเฉพาะหนังสือที่ยัง Available > 0
        """
        conn, cur = db_connection()
        cur.execute("""
            SELECT bookID, title
            FROM books
            WHERE availableCopies > 0
            ORDER BY CAST(SUBSTR(bookID, 2) AS INTEGER)
        """)
        rows = cur.fetchall()
        conn.close()

        display = [f"{r[0]} - {r[1]}" for r in rows]
        book_combo["values"] = display
        if display:
            book_combo.current(0)
        else:
            v_book.set("")

    def borrow_book():
        stdID = v_profile["stdID"].get()
        if not stdID:
            messagebox.showwarning("Borrow", "กรุณาเลือกนักศึกษาก่อน")
            return

        if not v_book.get():
            messagebox.showwarning("Borrow", "กรุณาเลือกหนังสือที่จะยืม")
            return

        book_id = v_book.get().split(" - ")[0]

        conn, cur = db_connection()

        # จำกัดจำนวนเล่มที่ยืมค้าง (เช่น 3 เล่ม)
        cur.execute("""
            SELECT COUNT(*)
            FROM borrowings
            WHERE stdID = ?
              AND status = 'Borrowed'
              AND (returnDate IS NULL OR returnDate = '')
        """, (stdID,))
        cnt = cur.fetchone()[0]
        if cnt >= 3:
            conn.close()
            messagebox.showwarning(
                "Borrow",
                "นักศึกษาคนนี้มียืมค้างครบจำนวนที่กำหนดแล้ว (3 เล่ม)"
            )
            return

        # เช็ค stock หนังสือ
        cur.execute("SELECT availableCopies FROM books WHERE bookID = ?", (book_id,))
        row = cur.fetchone()
        if (not row) or row[0] <= 0:
            conn.close()
            messagebox.showwarning("Borrow", "หนังสือเล่มนี้ไม่พร้อมให้ยืมแล้ว")
            return

        # สร้างรหัสยืมใหม่
        brw_id = generate_new_borrow_id(cur)
        today = date.today()
        due = today + timedelta(days=14)

        cur.execute("""
            INSERT INTO borrowings
                (brwID, stdID, bookID, borrowDate, dueDate, status, fineAmount,userID)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            brw_id,
            stdID,
            book_id,
            today.isoformat(),
            due.isoformat(),
            "Borrowed",
            0,
            user[0] 
        ))

        cur.execute("""
            UPDATE books
            SET availableCopies = availableCopies - 1
            WHERE bookID = ?
        """, (book_id,))

        conn.commit()
        conn.close()

        load_history(stdID)
        load_books()
        messagebox.showinfo("Borrow", "ทำรายการยืมหนังสือเรียบร้อยแล้ว")

    def return_book():
        sel = his_table.selection()
        if not sel:
            messagebox.showwarning("Return", "กรุณาเลือกรายการที่จะคืนจากตารางประวัติ")
            return

        vals = his_table.item(sel[0], "values")
        brw_id, book_id, title, brw_date, due_date, return_date, status, fine_now = vals

        if status.startswith("Returned"):
            messagebox.showinfo("Return", "รายการนี้คืนไปแล้ว")
            return

        today = date.today()

        # คำนวณค่าปรับ
        try:
            d_due = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            d_due = today

        if today > d_due:
            days_late = (today - d_due).days
            fine_amount = days_late * FINE_PER_DAY
            new_status = "Returned (Late)"
        else:
            fine_amount = 0
            new_status = "Returned"

        conn, cur = db_connection()
        cur.execute("""
            UPDATE borrowings
            SET returnDate = ?,
                status = ?,
                fineAmount = ?
            WHERE brwID = ?
        """, (today.isoformat(), new_status, fine_amount, brw_id))

        cur.execute("""
            UPDATE books
            SET availableCopies = availableCopies + 1
            WHERE bookID = ?
        """, (book_id,))
        conn.commit()
        conn.close()

        stdID = v_profile["stdID"].get()
        if stdID:
            load_history(stdID)
        load_books()

        msg = f"คืนหนังสือเรียบร้อยแล้ว"
        if fine_amount > 0:
            msg += f"\nค่าปรับ {fine_amount} บาท"
        messagebox.showinfo("Return", msg)

    def delete_borrow():
        sel = his_table.selection()
        if not sel:
            messagebox.showwarning("Delete", "กรุณาเลือกรายการที่จะลบจากตารางประวัติ")
            return

        vals = his_table.item(sel[0], "values")
        brw_id, book_id, title, brw_date, due_date, return_date, status, fine_now = vals

        if not messagebox.askyesno("Delete", f"ต้องการลบรายการยืม {brw_id} ใช่หรือไม่?"):
            return

        conn, cur = db_connection()

        # ถ้ายังอยู่สถานะ Borrowed ให้คืน stock ด้วย
        if status == "Borrowed":
            cur.execute("""
                UPDATE books
                SET availableCopies = availableCopies + 1
                WHERE bookID = ?
            """, (book_id,))

        cur.execute("DELETE FROM borrowings WHERE brwID = ?", (brw_id,))
        conn.commit()
        conn.close()

        stdID = v_profile["stdID"].get()
        if stdID:
            load_history(stdID)
        load_books()

        messagebox.showinfo("Delete", "ลบรายการยืมเรียบร้อยแล้ว")



        def save_edit():
            new_status = v_new_status.get()
            new_return = v_new_return.get().strip()

            conn, cur = db_connection()
            cur.execute("""
                UPDATE borrowings 
                SET status=?, returnDate=?
                WHERE brwID=?
            """, (new_status, new_return, brw_id))

            conn.commit()
            conn.close()

            stdID = v_profile["stdID"].get()
            load_history(stdID)

            messagebox.showinfo("Edit", "อัปเดตข้อมูลเรียบร้อยแล้ว")
            win.destroy()

        Button(
            win,
            text="บันทึกการแก้ไข",
            bg="blue",
            fg="white",
            font=("Kanit", 12),
            command=save_edit
        ).pack(pady=15)




    def on_select_student(event):
        sel = student_tree.selection()
        if not sel:
            return
        vals = student_tree.item(sel[0], "values")
        load_profile(vals)

    # ผูก event / ปุ่มกับฟังก์ชัน
    student_tree.bind("<<TreeviewSelect>>", on_select_student)
    btn_borrow.configure(command=borrow_book)
    btn_return.configure(command=return_book)
    btn_delete.configure(command=delete_borrow)
    

    # โหลดข้อมูลเริ่มต้น
    load_students()
    load_books()

def history(user):
    clear_main_frame()
    bar_home(user)

    fm = Frame(fm_main, bg=cl_white, padx=20, pady=20)
    fm.grid(row=0, column=0, sticky="nsew")
    fm_main.grid_rowconfigure(0, weight=1)
    fm_main.grid_columnconfigure(0, weight=1)

    fm.grid_rowconfigure(2, weight=1)  # ให้ตารางขยายเต็มจอ
    fm.grid_columnconfigure(0, weight=1)

    Label(
        fm, text="History (All Status)",
        font=("Kanit", 22, "bold"),
        bg=cl_white
    ).grid(row=0, column=0, sticky="w", pady=(0, 10))

    # ------------------- Search + Filter -------------------
    search_frame = Frame(fm, bg=cl_white)
    search_frame.grid(row=1, column=0, sticky="w")

    Label(search_frame, text="ค้นหา:", bg=cl_white, font=font_h5)\
        .pack(side=LEFT)

    # Dropdown filter
    status_var = StringVar()
    status_filter = ttk.Combobox(search_frame,
                                 textvariable=status_var,
                                 width=18,
                                 state="readonly")
    status_filter['values'] = [
        "All Status", "Borrowing", "Returned", "Returned (Late)"
    ]
    status_filter.current(0)
    status_filter.pack(side=LEFT, padx=10)

    v_search = StringVar()
    ent = Entry(search_frame, textvariable=v_search,
                width=40, bg=cl_white_gray)
    ent.pack(side=LEFT, padx=8)

    # ปุ่มค้นหา
    Button(
        search_frame, text="ค้นหา",
        bg=cl_red, fg="white", font=font_h5,
        command=lambda: load_history(v_search.get().strip(),
                                     status_var.get())
    ).pack(side=LEFT)

    # ------------------- Table -------------------
    cols = (
        "brwID", "stdID", "name",
        "bookID", "title",
        "borrowDate", "dueDate", "returnDate",
        "fine"
    )

    table = ttk.Treeview(fm, columns=cols, show="headings")
    headers = [
        "Borrow ID", "Student ID", "Name",
        "Book ID", "Title",
        "Borrow Date", "Due Date", "Return Date",
        "Fine"
    ]
    widths = [80, 100, 160, 80, 260, 100, 100, 100, 80]

    for c, h, w in zip(cols, headers, widths):
        table.heading(c, text=h)
        table.column(c, width=w, anchor=W)

    table.grid(row=2, column=0, sticky="nsew", padx=5, pady=10)
    scroll = ttk.Scrollbar(fm, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)
    scroll.grid(row=2, column=1, sticky="ns", pady=10)

    # =====================================================
    #              LOAD HISTORY FUNCTION (INSIDE)
    # =====================================================
    def load_history(keyword="", status="All Status"):
        table.delete(*table.get_children())

        conn, cur = db_connection()

        # ------------------- FILTER STATUS -------------------
        if status == "Borrowing":
            status_condition = " AND b.status = 'Borrowed' "
        elif status == "Returned":
            status_condition = " AND b.status = 'Returned' "
        elif status == "Returned (Late)":
            status_condition = " AND b.status = 'Returned (Late)' "
        else:
            status_condition = ""   # All Status

        # ------------------- SQL QUERY -------------------
        sql = f"""
            SELECT  b.brwID,
                    b.stdID,
                    s.stdFirstName || ' ' || s.stdLastName AS fullName,
                    b.bookID,
                    k.title,
                    b.borrowDate,
                    b.dueDate,
                    b.returnDate,
                    IFNULL(b.fineAmount, 0)
            FROM borrowings b
            JOIN student s ON s.stdID = b.stdID
            JOIN books k   ON k.bookID = b.bookID
            WHERE (
                    b.brwID LIKE ?
                 OR b.stdID LIKE ?
                 OR s.stdFirstName LIKE ?
                 OR s.stdLastName LIKE ?
                 OR k.title LIKE ?
            )
            {status_condition}
            ORDER BY b.borrowDate DESC
        """

        key = f"%{keyword}%"
        cur.execute(sql, (key, key, key, key, key))
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            table.insert("", "end", values=r)

    # โหลดข้อมูลครั้งแรก
    load_history("")





#login page   
def login():
    
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white, padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg=cl_white)
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    mid = Frame(fm,bg=cl_white)
    mid.rowconfigure((0,1),weight=1)
    mid.columnconfigure((0,1),weight=1)
    mid.grid(row=1,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg=cl_white)
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure(0,weight=1)
    bot.grid(row=2,columnspan=2,sticky=NSEW)
    
    #global veriable
    global username_login_entry, password_login_entry
    username_info = StringVar()
    password_info = StringVar()
    
    #set scale of component
    
    # - component inside -
    #menubar
    bar_login()

    # top frame 
    Label(top,image=logo_img,bg=cl_white).grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="username : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    username_login_entry = Entry(mid,bg=cl_white_gray, textvariable=username_info)
    username_login_entry.grid(row=0,column=1,sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)
    
    Label(mid,text="password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    password_login_entry = Entry(mid,bg=cl_white_gray,show='*', textvariable=password_info)
    password_login_entry.grid(row=1, column=1, sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)

    # bot frame 
    button_login = Button(bot,text="login",bg=cl_red,fg=cl_white,font=font_h3_bold, command=lambda: login_click(username_info.get(),password_info.get()))
    button_login.grid(row=0,column=0, ipadx=50, ipady=5) 

# ...existing code...
# ...existing code...
def dashboard(user):
    """
    Dashboard สรุปการยืมหนังสือสำหรับบรรณารักษ์
    ใช้ตาราง: borrowings, books, category, student, user
    """
    # พยายาม import matplotlib ถ้าไม่มีให้ข้ามกราฟไป
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib
        import matplotlib.pyplot as plt
        # ฟอนต์ไทย (Windows มี Tahoma อยู่แล้ว)
        matplotlib.rcParams['font.family'] = 'Tahoma'
    except Exception:
        FigureCanvasTkAgg = None
        plt = None

    # ล้างหน้าจอเก่าออกจาก fm_main
    for w in fm_main.winfo_children():
        w.destroy()

    # เฟรมหลักของหน้า dashboard
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=0)  # title
    fm.grid_rowconfigure(1, weight=0)  # KPI cards
    fm.grid_rowconfigure(2, weight=1)  # content (กราฟ + รายการ)
    fm.grid_columnconfigure(0, weight=1)

    # เมนูด้านบน
    bar_home(user)
    
    # ฟอนต์ที่ใช้เฉพาะในหน้านี้
    card_title_font = ("Tahoma", 11, "bold")     # หัวข้อการ์ด / หัวข้อ box
    card_value_font = ("Tahoma", 16, "bold")     # ตัวเลขใหญ่
    card_sub_font   = ("Tahoma", 9)              # คำอธิบายย่อย

    # หัวข้อใหญ่
    Label(
        fm,
        text="Dashboard",
        bg=cl_white,
        fg="black",
        font=font_h3_bold
    ).grid(row=0, column=0, sticky=W, padx=spacing_comp, pady=(8, 0))

    #  ฟังก์ชันดึงข้อมูลจาก DB 
    def safe_query(sql, params=()):
        try:
            conn_q, cur_q = db_connection()
            cur_q.execute(sql, params)
            rows = cur_q.fetchall()
            conn_q.close()
            return rows
        except Exception as e:
            print("DB query error:", e, "| SQL:", sql)
            return []


    #   ดึงสถิติจากฐานข้อมูล

    # 1) หมวดหมู่ที่ถูกยืมเยอะที่สุด
    top_cat_name = "-"
    top_cat_total = 0
    r = safe_query("""
        SELECT c.ctgName, COUNT(*) AS total
        FROM borrowings b
        JOIN books bk ON b.bookID = bk.bookID
        JOIN category c ON bk.ctgID = c.ctgID
        GROUP BY c.ctgID, c.ctgName
        ORDER BY total DESC
        LIMIT 1;
    """)
    if r:
        top_cat_name, top_cat_total = r[0]

    # 2) จำนวนคนที่เคยยืม
    r = safe_query("SELECT COUNT(DISTINCT stdID) FROM borrowings;")
    borrower_count = r[0][0] if r and r[0][0] is not None else 0

    # 3) จำนวนครั้งที่ยืมทั้งหมด
    r = safe_query("SELECT COUNT(*) FROM borrowings;")
    total_borrow_count = r[0][0] if r and r[0][0] is not None else 0

    # 4) ยอดยืมเดือนปัจจุบัน
    r = safe_query("""
        SELECT COUNT(*)
        FROM borrowings
        WHERE strftime('%Y-%m', borrowDate) = strftime('%Y-%m', 'now');
    """)
    borrow_this_month = r[0][0] if r and r[0][0] is not None else 0

    # 5) จำนวนหนังสือทั้งหมด
    r = safe_query("SELECT COUNT(*) FROM books;")
    total_books = r[0][0] if r and r[0][0] is not None else 0

    # 6) จำนวนหมวดหมู่
    r = safe_query("SELECT COUNT(*) FROM category;")
    total_categories = r[0][0] if r and r[0][0] is not None else 0

    # 7) จำนวนนักศึกษา
    r = safe_query("SELECT COUNT(*) FROM student;")
    total_students = r[0][0] if r and r[0][0] is not None else 0


    # ยอดยืมรายเดือน (ไว้ทำกราฟ)
    monthly_rows = safe_query("""
        SELECT strftime('%Y-%m', borrowDate) AS mon,
               COUNT(*) AS total
        FROM borrowings
        GROUP BY mon
        ORDER BY mon;
    """)
    monthly_rows = [row for row in monthly_rows if row[0] is not None]

    # Top 5 หนังสือที่ถูกยืมมากที่สุด
    top5_books = safe_query("""
        SELECT bk.title, COUNT(*) AS total
        FROM borrowings b
        JOIN books bk ON b.bookID = bk.bookID
        GROUP BY bk.bookID, bk.title
        ORDER BY total DESC
        LIMIT 5;
    """)

    # จำนวนหนังสือในแต่ละหมวดหมู่
    category_book_counts = safe_query("""
        SELECT c.ctgName, COUNT(b.bookID) AS total
        FROM category c
        LEFT JOIN books b ON c.ctgID = b.ctgID
        GROUP BY c.ctgID, c.ctgName
        ORDER BY total DESC;
    """)

    #   แถวการ์ด KPI ด้านบน (2 แถว × 4 ใบ)
    
    kpi = Frame(fm, bg=cl_white)
    kpi.grid(row=1, column=0, sticky=EW,
             padx=spacing_comp, pady=(spacing_comp, 0))
    for c in range(4):
        kpi.columnconfigure(c, weight=1)

    def kpi_card(parent, row, col, title, value, subtitle=""):
        box = Frame(parent, bg=cl_white, bd=1, relief=SOLID, padx=14, pady=10)
    
        # ถ้าเป็นคอลัมน์แรก (ซ้ายสุด) ไม่ต้องมี padding ด้านซ้าย
        # เพื่อให้ขอบซ้ายของการ์ดตรงกับกราฟด้านล่าง
        if col == 0:
            box.grid(row=row, column=col, padx=(0, 8), pady=6, sticky="nsew")
        else:
            box.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
    
        Label(
            box,
            text=title,
            bg=cl_white,
            fg="black",
            font=card_title_font
        ).pack(anchor=W)
    
        Label(
            box,
            text=str(value),
            bg=cl_white,
            fg="black",
            font=card_value_font
        ).pack(anchor=W, pady=(2, 0))
    
        if subtitle:
            Label(
                box,
                text=subtitle,
                bg=cl_white,
                fg=cl_gray,
                font=card_sub_font
            ).pack(anchor=W, pady=(2, 0))

    # แถวที่ 1
    kpi_card(
        kpi, 0, 0,
        "หมวดหมู่ที่ยืมเยอะที่สุด",
        top_cat_name,
        f"{top_cat_total} ครั้ง"
    )
    kpi_card(
        kpi, 0, 1,
        "จำนวนผู้ยืม",
        borrower_count,
        "คนที่เคยยืมหนังสือ"
    )
    kpi_card(
        kpi, 0, 2,
        "จำนวนครั้งที่ยืมทั้งหมด",
        total_borrow_count,
        "ตั้งแต่เริ่มใช้ระบบ"
    )
    kpi_card(
        kpi, 0, 3,
        "ยอดยืมเดือนนี้",
        borrow_this_month,
        "ครั้งในเดือนปัจจุบัน"
    )

    # แถวที่ 2
    kpi_card(
        kpi, 1, 0,
        "จำนวนหนังสือทั้งหมด",
        total_books,
        "เล่มในระบบ"
    )
    kpi_card(
        kpi, 1, 1,
        "จำนวนหมวดหมู่",
        total_categories,
        "หมวดหมู่"
    )
    kpi_card(
        kpi, 1, 2,
        "จำนวนนักศึกษา",
        total_students,
        "คนในฐานข้อมูล"
    )
      
    #   พื้นที่หลักด้านล่าง (กราฟ + รายการ)

    content = Frame(fm, bg=cl_white)
    content.grid(row=2, column=0, sticky=NSEW,
                 padx=spacing_comp, pady=spacing_comp)
    content.columnconfigure(0, weight=3)  # ซ้าย
    content.columnconfigure(1, weight=2)  # ขวา
    content.rowconfigure(0, weight=1)

    # ด้านซ้าย : กราฟ + Top 5 
    left = Frame(content, bg=cl_white)
    left.grid(row=0, column=0, sticky=NSEW, padx=(0, 8))
    left.rowconfigure(0, weight=2)  # กราฟ
    left.rowconfigure(1, weight=0)  # Top 5
    left.columnconfigure(0, weight=1)

    # กราฟ
    chart_card = Frame(left, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    chart_card.grid(row=0, column=0, sticky=NSEW)
    Label(
        chart_card,
        text="ยอดยืมรายเดือน (3 เดือนล่าสุด)",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    # เดือนที่เป็นภาษาไทย
    thai_months = {
        "01": "ม.ค.", "02": "ก.พ.", "03": "มี.ค.", "04": "เม.ย.",
        "05": "พ.ค.", "06": "มิ.ย.", "07": "ก.ค.", "08": "ส.ค.",
        "09": "ก.ย.", "10": "ต.ค.", "11": "พ.ย.", "12": "ธ.ค."
    }

    if monthly_rows and plt and FigureCanvasTkAgg:
        # เอาแค่ 3 เดือนล่าสุด
        monthly_rows_sorted = sorted(monthly_rows, key=lambda r: r[0])
        last_rows = monthly_rows_sorted[-3:]

        month_labels = []
        totals = []
        for ym, total in last_rows:
            year, mon = ym.split("-")
            label_th = f"{thai_months.get(mon, mon)} {year}"
            month_labels.append(label_th)
            totals.append(total)

        x = list(range(len(month_labels)))

        fig, ax = plt.subplots(figsize=(5.5, 2.4))

        # ----- แท่ง (bar) ด้านหลัง -----
        bar_width = 0.6
        ax.bar(
            x,
            totals,
            width=bar_width,
            color="#e1efff",          
            edgecolor="#c0d4f5",
            linewidth=1
        )

        
        ax.plot(
            x,
            totals,
            color="#ff6b6b",          
            marker="o",
            markersize=5,
            linewidth=2
        )

        # เส้นgridแกน Y ช่องๆ
        ax.grid(True, axis="y", linestyle="--", alpha=0.3)

        #ปิดขอบบนขวา
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.set_xticks(x)
        ax.set_xticklabels(month_labels, rotation=45)
        ax.set_xlabel("เดือน")
        ax.set_ylabel("จำนวนครั้งที่ยืม")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    else:
        Label(chart_card, text="No monthly data",
              bg=cl_white, fg="black").pack(anchor=W, pady=8)

    # Top 5 หนังสือ
    top_box = Frame(left, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    top_box.grid(row=1, column=0, sticky=EW, pady=(8, 0))
    Label(
        top_box,
        text="Top 5 หนังสือที่ถูกยืมมากที่สุด",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    if top5_books:
        for title, total in top5_books:
            Label(
                top_box,
                text=f"{title} — {total} ครั้ง",
                bg=cl_white,
                anchor="w",
                font=card_sub_font
            ).pack(fill="x")
    else:
        Label(top_box, text="No data", bg=cl_white,
              font=card_sub_font).pack(anchor=W, pady=4)

    #  ด้านขวา  จำนวนหนังสือในแต่ละหมวด 
    right = Frame(content, bg=cl_white)
    right.grid(row=0, column=1, sticky=NSEW, padx=(8, 0))
    right.rowconfigure(0, weight=0)
    right.columnconfigure(0, weight=1)

    category_card = Frame(right, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    category_card.grid(row=0, column=0, sticky=NSEW)
    Label(
        category_card,
        text="จำนวนหนังสือในแต่ละหมวดหมู่",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    if category_book_counts:
        for name, total in category_book_counts:
            Label(
                category_card,
                text=f"{name} — {total} เล่ม",
                bg=cl_white,
                anchor="w",
                font=card_sub_font
            ).pack(fill="x")
    else:
        Label(
            category_card,
            text="No category data",
            bg=cl_white,
            font=card_sub_font
        ).pack(anchor=W, pady=4)

def clear_main_frame():
    """ล้าง widget ทั้งหมดใน fm_main ก่อนเปลี่ยนหน้า"""
    for w in fm_main.winfo_children():
        w.destroy()

# ================== BOOKS MODULE (Category + Shelves + Books Page) ==================

def get_categories():
    """
    ดึง ctgID, ctgName จากตาราง category
    ใช้ตอนเปิดฟอร์มหนังสือ
    """
    cursor.execute("SELECT ctgID, ctgName FROM category ORDER BY ctgID")
    return cursor.fetchall()      # [(ctgID, ctgName), ...]

def get_shelves():
    """
    ดึง shelfID, section, floor, aisle จากตาราง shelves
    ใช้ตอนเปิดฟอร์มหนังสือ
    """
    cursor.execute("SELECT shelfID, section, floor, aisle FROM shelves ORDER BY shelfID")
    return cursor.fetchall()     

def generate_new_book_id():
    """
    gen bookID ใหม่แบบ B0001, B0002, ...
    ดูจากค่าที่มากที่สุดที่ขึ้นต้นด้วย 'B'
    """
    cursor.execute("""
        SELECT bookID
        FROM books
        WHERE bookID LIKE 'B%'
        ORDER BY CAST(SUBSTR(bookID, 2) AS INTEGER) DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row and row[0]:
        last_num = int(row[0][1:])  
        new_num = last_num + 1
    else:
        new_num = 1

    return f"B{new_num:04d}"        

""" ============= FRONT END : BOOKS PAGE ============= """

def books(user):
    """
    หน้าจอจัดการหนังสือทั้งหมด (ค้นหา / เพิ่ม / แก้ไข / ลบ)
    """
    clear_main_frame()
    fm = Frame(fm_main, bg=cl_white, padx=20, pady=20)
    fm.grid(row=0, column=0, sticky="nsew")

    fm.grid_rowconfigure(0, weight=0) 
    fm.grid_rowconfigure(1, weight=1) 
    fm.grid_rowconfigure(2, weight=0) 
    fm.grid_columnconfigure(0, weight=1)

    bar_home(user)

    # ---------- Top: Title + Search ----------
    top = Frame(fm, bg=cl_white)
    top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    Label(top, text="Books", font=font_h3_bold, bg=cl_white)\
        .pack(side=LEFT, padx=(0, 20))

    Label(top, text="ค้นหาจาก:", bg=cl_white).pack(side=LEFT, padx=(0, 5))

    book_search_options = {
        "ID": "b.bookID",
        "Title": "b.title",
        "Author": "b.author",
        "ISBN": "b.ISBN",
        "Status": "b.bookStatus",
        "Category": "c.ctgName",
        "ShelfID": "b.shelfID"
    }
    book_search_cb = ttk.Combobox(
        top,
        values=list(book_search_options.keys()),
        state="readonly",
        width=10
    )
    book_search_cb.current(1)  # default = Title
    book_search_cb.pack(side=LEFT, padx=5)

    search_var = StringVar()
    Entry(top, textvariable=search_var, width=30)\
        .pack(side=LEFT, padx=5)

    Button(top, text="Search", bg="#2196F3", fg="white",
           command=lambda: refresh_books())\
        .pack(side=LEFT, padx=5)
    Button(top, text="Reset",
           command=lambda: [search_var.set(""), refresh_books(reset=True)],
           bg="gray", fg="white")\
        .pack(side=LEFT, padx=5)

    # ---------- Table ----------
    columns = (
        "bookID", "title", "author", "ISBN",
        "totalCopies", "availableCopies",
        "bookStatus", "category", "shelfID"
    )
    tree = ttk.Treeview(fm, columns=columns, show="headings")
    headers = ["ID", "Title", "Author", "ISBN",
               "Total", "Available", "Status",
               "Category", "ShelfID"]
    widths = [70, 220, 180, 130, 60, 80, 100, 160, 80]

    for c, h, w in zip(columns, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w, anchor=W)

    tree.grid(row=1, column=0, sticky="nsew")
    scroll = ttk.Scrollbar(fm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=1, column=1, sticky="ns")

    # ใช้ BACK END ดึงข้อมูล + ใส่ในตาราง
    def refresh_books(reset=False):
        col = None
        kw = None
        if not reset:
            txt = search_var.get().strip()
            if txt != "":
                display = book_search_cb.get()
                col = book_search_options[display]
                kw = txt
        rows = be_get_books(col, kw)   # <-- เรียก BACK END
        tree.delete(*tree.get_children())
        for r in rows:
            tree.insert("", END, values=r)

    # ---------- Popup Add/Edit ----------
    def open_book_form(mode="add"):
        selected_values = None
        if mode == "edit":
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Books", "Please select a book.")
                return
            selected_values = tree.item(sel[0], "values")

        popup = Toplevel(root)
        popup.title("Add Book" if mode == "add" else "Edit Book")
        popup.geometry("520x540")
        popup.transient(root)
        popup.grab_set()

        frm = Frame(popup, bg=cl_white, padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        # ตัวแปร
        title_var = StringVar()
        author_var = StringVar()
        isbn_var = StringVar()
        pub_var = StringVar()
        year_var = StringVar()
        total_var = StringVar()
        avail_var = StringVar()

        status_options = be_get_book_status_options()
        status_var = StringVar(value="available")

        ctg_list = be_get_categories_for_book()   
        shelf_list = be_get_shelves_for_book()     
        ctg_display = [f"{c[0]} - {c[1]}" for c in ctg_list]
        shelf_display = [f"{s[0]} - {s[1]}" for s in shelf_list]
        ctg_var = StringVar()
        shelf_var = StringVar()

        edit_book_id = None

        # ====== โหมด EDIT: ดึงค่าจากแถวที่เลือก ======
        if mode == "edit":
            v = selected_values
            edit_book_id = v[0]
            title_var.set(v[1])
            author_var.set(v[2])
            isbn_var.set(v[3])
            total_var.set(v[4])
            avail_var.set(v[5])

            current_status = v[6] or "available"
            if current_status not in status_options:
                status_options.append(current_status)
            status_var.set(current_status)

            for c in ctg_list:
                if c[1] == v[7]:
                    ctg_var.set(f"{c[0]} - {c[1]}")
                    break

            for s in shelf_list:
                if s[0] == v[8]:
                    shelf_var.set(f"{s[0]} - {s[1]}")
                    break

            pub, year = be_get_book_extra(edit_book_id)
            pub_var.set(pub or "")
            year_var.set(year or "")

        def row_input(label, var, r):
            Label(frm, text=label, bg=cl_white, anchor="e", width=14)\
                .grid(row=r, column=0, pady=3, padx=5, sticky="e")
            Entry(frm, textvariable=var, width=28)\
                .grid(row=r, column=1, pady=3, padx=5, sticky="w")

        row_input("Title *", title_var, 0)
        row_input("Author", author_var, 1)
        row_input("ISBN", isbn_var, 2)
        row_input("Publisher", pub_var, 3)
        row_input("Pub. Year", year_var, 4)
        row_input("Total Copies", total_var, 5)
        row_input("Available Copies", avail_var, 6)

        Label(frm, text="Status", bg=cl_white, anchor="e", width=14)\
            .grid(row=7, column=0, pady=3, padx=5, sticky="e")
        status_cb = ttk.Combobox(
            frm, textvariable=status_var,
            values=status_options, state="readonly", width=26
        )
        status_cb.grid(row=7, column=1, pady=3, padx=5, sticky="w")

        Label(frm, text="Category", bg=cl_white, anchor="e", width=14)\
            .grid(row=8, column=0, pady=3, padx=5, sticky="e")
        ttk.Combobox(
            frm, textvariable=ctg_var,
            values=ctg_display, state="readonly", width=26
        ).grid(row=8, column=1, pady=3, padx=5, sticky="w")
        
        Label(frm, text="Shelf", bg=cl_white, anchor="e", width=14)\
            .grid(row=9, column=0, pady=3, padx=5, sticky="e")
        ttk.Combobox(
            frm, textvariable=shelf_var,
            values=shelf_display, state="readonly", width=26
        ).grid(row=9, column=1, pady=3, padx=5, sticky="w")

        # ---------- save_book ----------
        def save_book():
            title_txt = title_var.get().strip()
            if title_txt == "":
                messagebox.showwarning("Books", "Please enter title.")
                return

            author_txt = author_var.get().strip()
            isbn_txt = isbn_var.get().strip()
            publisher_txt = pub_var.get().strip()
            pubyear_txt = year_var.get().strip()
            status_txt = status_var.get().strip() or "available"

            def to_int(txt, default=0):
                txt = txt.strip()
                if txt == "":
                    return default
                try:
                    return int(txt)
                except ValueError:
                    return None

            total_copies = to_int(total_var.get(), 0)
            avail_copies = to_int(avail_var.get(), 0)

            if total_copies is None or avail_copies is None:
                messagebox.showerror("Books", "Total/Available must be numbers.")
                return

            if avail_var.get().strip() == "":
                avail_copies = total_copies

            ctg_id = None
            shelf_id = None
            if ctg_var.get():
                ctg_id = ctg_var.get().split(" - ")[0]
            if shelf_var.get():
                shelf_id = shelf_var.get().split(" - ")[0]

            if mode == "add":
                be_insert_book(
                    user_id=user[0],
                    ctg_id=ctg_id,
                    shelf_id=shelf_id,
                    isbn=isbn_txt,
                    title=title_txt,
                    author=author_txt,
                    publisher=publisher_txt,
                    pub_year=pubyear_txt,
                    total=total_copies,
                    avail=avail_copies,
                    status=status_txt
                )
            else:
                be_update_book(
                    book_id=edit_book_id,
                    ctg_id=ctg_id,
                    shelf_id=shelf_id,
                    isbn=isbn_txt,
                    title=title_txt,
                    author=author_txt,
                    publisher=publisher_txt,
                    pub_year=pubyear_txt,
                    total=total_copies,
                    avail=avail_copies,
                    status=status_txt
                )

            refresh_books(reset=True)
            popup.destroy()

        Button(frm, text="Save", command=save_book,
               bg=cl_red, fg="white", font=font_h3_bold)\
            .grid(row=10, column=0, columnspan=2,
                  pady=15, ipadx=40, ipady=3)

    # ---------- Bottom buttons ----------
    bottom = Frame(fm, bg=cl_white)
    bottom.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    Button(bottom, text="Add Book",
           command=lambda: open_book_form("add"),
           bg="#2ecc71", fg="white", width=12)\
        .pack(side=LEFT, padx=5)

    Button(bottom, text="Edit Book",
           command=lambda: open_book_form("edit"),
           bg="#f39c12", fg="white", width=12)\
        .pack(side=LEFT, padx=5)

    def delete_book():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Books", "Please select a book.")
            return
        v = tree.item(sel[0], "values")
        bid, title_txt = v[0], v[1]
        if not messagebox.askyesno("Books", f"Delete book '{title_txt}' ?"):
            return
        be_delete_book(bid)
        refresh_books(reset=True)

    Button(bottom, text="Delete Book",
           command=delete_book,
           bg="#e74c3c", fg="white", width=12)\
        .pack(side=LEFT, padx=5)

    # โหลดข้อมูลครั้งแรก
    refresh_books(reset=True)

""" ============= FRONT END : CATEGORY PAGE ============= """

def catagory(user):
    clear_main_frame()
    fm = Frame(fm_main, bg=cl_white, padx=20, pady=20)
    fm.grid(row=0, column=0, sticky="nsew")

    fm.grid_rowconfigure(0, weight=0)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_rowconfigure(2, weight=0)
    fm.grid_columnconfigure(0, weight=1)

    bar_home(user)

    top = Frame(fm, bg=cl_white)
    top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    Label(top, text="Category", bg=cl_white, font=font_h3_bold)\
        .pack(side=LEFT, padx=(0, 20))

    Label(top, text="ค้นหาจาก:", bg=cl_white).pack(side=LEFT, padx=(0, 5))

    cat_search_options = {
        "Category ID": "ctgID",
        "Category Name": "ctgName"
    }
    cat_search_cb = ttk.Combobox(
        top,
        values=list(cat_search_options.keys()),
        state="readonly",
        width=15
    )
    cat_search_cb.current(0)
    cat_search_cb.pack(side=LEFT, padx=5)

    search_var = StringVar()
    Entry(top, textvariable=search_var, width=25)\
        .pack(side=LEFT, padx=5)

    Button(top, text="Search",
           command=lambda: refresh_cat(), bg="#2196F3", fg="white")\
        .pack(side=LEFT, padx=5)
    Button(top, text="Reset",
           command=lambda: [search_var.set(""), refresh_cat(reset=True)],
           bg="gray", fg="white")\
        .pack(side=LEFT, padx=5)

    columns = ("ctgID", "ctgName")
    tree = ttk.Treeview(fm, columns=columns, show="headings")
    tree.heading("ctgID", text="Category ID")
    tree.heading("ctgName", text="Category Name")
    tree.column("ctgID", width=100, anchor=W)
    tree.column("ctgName", width=260, anchor=W)
    tree.grid(row=1, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(fm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=1, column=1, sticky="ns")

    def refresh_cat(reset=False):
        col = None
        kw = None
        if not reset:
            txt = search_var.get().strip()
            if txt != "":
                display = cat_search_cb.get()
                col = cat_search_options[display]
                kw = txt
        rows = be_get_categories(col, kw)
        tree.delete(*tree.get_children())
        for r in rows:
            tree.insert("", END, values=r)

    def open_cat_form(mode="add"):
        popup = Toplevel(root)
        popup.title("Add Category" if mode == "add" else "Edit Category")
        popup.geometry("360x200")
        popup.transient(root)
        popup.grab_set()

        frm = Frame(popup, bg=cl_white, padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        id_var = StringVar()
        name_var = StringVar()

        if mode == "edit":
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Category", "Please select a row.")
                popup.destroy()
                return
            v = tree.item(sel[0], "values")
            id_var.set(v[0])
            name_var.set(v[1])

        Label(frm, text="ID", bg=cl_white, width=10, anchor="e")\
            .grid(row=0, column=0, padx=5, pady=5)
        ent_id = Entry(frm, textvariable=id_var, width=20)
        ent_id.grid(row=0, column=1, padx=5, pady=5)

        Label(frm, text="Name", bg=cl_white, width=10, anchor="e")\
            .grid(row=1, column=0, padx=5, pady=5)
        Entry(frm, textvariable=name_var, width=20)\
            .grid(row=1, column=1, padx=5, pady=5)

        if mode == "edit":
            ent_id.config(state="readonly")

        def save():
            if id_var.get().strip() == "" or name_var.get().strip() == "":
                messagebox.showwarning("Category", "Please fill all fields.")
                return
            if mode == "add":
                be_insert_category(id_var.get().strip(), name_var.get().strip())
            else:
                be_update_category(id_var.get().strip(), name_var.get().strip())
            refresh_cat(reset=True)
            popup.destroy()

        Button(frm, text="Save", command=save,
               bg=cl_red, fg="white", font=font_h3_bold)\
            .grid(row=2, column=0, columnspan=2,
                  pady=15, ipadx=30, ipady=3)

    bottom = Frame(fm, bg=cl_white)
    bottom.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    Button(bottom, text="Add", command=lambda: open_cat_form("add"),
           bg="#2ecc71", fg="white", width=10)\
        .pack(side=LEFT, padx=5)
    Button(bottom, text="Edit", command=lambda: open_cat_form("edit"),
           bg="#f39c12", fg="white", width=10)\
        .pack(side=LEFT, padx=5)

    def delete_cat():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Category", "Please select a row.")
            return
        v = tree.item(sel[0], "values")
        cid = v[0]
        if not messagebox.askyesno("Category", f"Delete category {cid}?"):
            return
        be_delete_category(cid)
        refresh_cat(reset=True)

    Button(bottom, text="Delete", command=delete_cat,
           bg="#e74c3c", fg="white", width=10)\
        .pack(side=LEFT, padx=5)

    refresh_cat(reset=True)

""" ============= FRONT END : SHELVES PAGE ============= """

def shelves(user):
    clear_main_frame()
    fm = Frame(fm_main, bg=cl_white, padx=20, pady=20)
    fm.grid(row=0, column=0, sticky="nsew")

    fm.grid_rowconfigure(0, weight=0)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_rowconfigure(2, weight=0)
    fm.grid_columnconfigure(0, weight=1)

    bar_home(user)

    top = Frame(fm, bg=cl_white)
    top.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    Label(top, text="Shelves", bg=cl_white, font=font_h3_bold)\
        .pack(side=LEFT, padx=(0, 20))

    Label(top, text="ค้นหาจาก:", bg=cl_white).pack(side=LEFT, padx=(0, 5))

    shelf_search_options = {
        "Shelf ID": "shelfID",
        "Section": "section",
        "Floor": "floor",
        "Aisle": "aisle"
    }
    shelf_search_cb = ttk.Combobox(
        top,
        values=list(shelf_search_options.keys()),
        state="readonly",
        width=12
    )
    shelf_search_cb.current(0)
    shelf_search_cb.pack(side=LEFT, padx=5)

    search_var = StringVar()
    Entry(top, textvariable=search_var, width=25)\
        .pack(side=LEFT, padx=5)

    Button(top, text="Search",
           command=lambda: refresh_shelves(), bg="#2196F3", fg="white")\
        .pack(side=LEFT, padx=5)
    Button(top, text="Reset",
           command=lambda: [search_var.set(""), refresh_shelves(reset=True)],
           bg="gray", fg="white")\
        .pack(side=LEFT, padx=5)

    columns = ("shelfID", "section", "floor", "aisle")
    tree = ttk.Treeview(fm, columns=columns, show="headings")
    headers = ["Shelf ID", "Section", "Floor", "Aisle"]
    widths = [80, 180, 80, 80]

    for c, h, w in zip(columns, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w, anchor=W)

    tree.grid(row=1, column=0, sticky="nsew")
    scroll = ttk.Scrollbar(fm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=1, column=1, sticky="ns")

    def refresh_shelves(reset=False):
        col = None
        kw = None
        if not reset:
            txt = search_var.get().strip()
            if txt != "":
                display = shelf_search_cb.get()
                col = shelf_search_options[display]
                kw = txt
        rows = be_get_shelves(col, kw)
        tree.delete(*tree.get_children())
        for r in rows:
            tree.insert("", END, values=r)

    def open_shelf_form(mode="add"):
        popup = Toplevel(root)
        popup.title("Add Shelf" if mode == "add" else "Edit Shelf")
        popup.geometry("380x230")
        popup.transient(root)
        popup.grab_set()

        frm = Frame(popup, bg=cl_white, padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        shelfID_var = StringVar()
        section_var = StringVar()
        floor_var = StringVar()
        aisle_var = StringVar()

        if mode == "edit":
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Shelves", "Please select a row.")
                popup.destroy()
                return
            v = tree.item(sel[0], "values")
            shelfID_var.set(v[0])
            section_var.set(v[1])
            floor_var.set(v[2])
            aisle_var.set(v[3])

        def row_input(label, var, r, readonly=False):
            Label(frm, text=label, bg=cl_white, width=10, anchor="e")\
                .grid(row=r, column=0, padx=5, pady=4, sticky="e")
            state = "readonly" if readonly else "normal"
            ent = Entry(frm, textvariable=var, width=20, state=state)
            ent.grid(row=r, column=1, padx=5, pady=4, sticky="w")
            return ent

        row_input("Shelf ID", shelfID_var, 0, readonly=(mode == "edit"))
        row_input("Section", section_var, 1)
        row_input("Floor", floor_var, 2)
        row_input("Aisle", aisle_var, 3)

        def save():
            if shelfID_var.get().strip() == "" or section_var.get().strip() == "":
                messagebox.showwarning("Shelves", "Please fill ShelfID & Section.")
                return

            if mode == "add":
                be_insert_shelf(
                    shelfID_var.get().strip(),
                    section_var.get().strip(),
                    floor_var.get().strip(),
                    aisle_var.get().strip()
                )
            else:
                be_update_shelf(
                    shelfID_var.get().strip(),
                    section_var.get().strip(),
                    floor_var.get().strip(),
                    aisle_var.get().strip()
                )
            refresh_shelves(reset=True)
            popup.destroy()

        Button(frm, text="Save", command=save,
               bg=cl_red, fg="white", font=font_h3_bold)\
            .grid(row=4, column=0, columnspan=2,
                  pady=12, ipadx=30, ipady=3)

    bottom = Frame(fm, bg=cl_white)
    bottom.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    Button(bottom, text="Add", command=lambda: open_shelf_form("add"),
           bg="#2ecc71", fg="white", width=10)\
        .pack(side=LEFT, padx=5)
    Button(bottom, text="Edit", command=lambda: open_shelf_form("edit"),
           bg="#f39c12", fg="white", width=10)\
        .pack(side=LEFT, padx=5)

    def delete_shelf():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Shelves", "Please select a row.")
            return
        v = tree.item(sel[0], "values")
        sid = v[0]
        if not messagebox.askyesno("Shelves", f"Delete shelf {sid}?"):
            return
        be_delete_shelf(sid)
        refresh_shelves(reset=True)

    Button(bottom, text="Delete", command=delete_shelf,
           bg="#e74c3c", fg="white", width=10)\
        .pack(side=LEFT, padx=5)

    refresh_shelves(reset=True)



def profileUser(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_rowconfigure(2, weight=0)
    fm.grid_columnconfigure(0, weight=1)
    
    bar_home(user)

    current_id = user[0]

    v_username = StringVar(value=user[1])
    v_password = StringVar(value=user[2])
    v_firstname = StringVar(value=user[3])
    v_lastname = StringVar(value=user[4])
    v_email = StringVar(value=user[5])
    v_tel = StringVar(value=user[6]) 
    v_role = StringVar(value=user[7])

    def save_profile():
        try:
            conn, cursor = db_connection()
            sql = """
                UPDATE user 
                SET username=?, password=?, firstName=?, lastName=?, email=?, tel=?
                WHERE userID=?
            """
            params = (
                v_username.get(),
                v_password.get(),
                v_firstname.get().strip(), # strip() เพื่อลบช่องว่างท้ายคำถ้ามี
                v_lastname.get().strip(),
                v_email.get(),
                v_tel.get(),
                current_id # ใช้ ID เดิมเป็นตัวอ้างอิง (WHERE)
            )
            
            cursor.execute(sql, params)
            conn.commit()
            
            messagebox.showinfo("Success", "บันทึกข้อมูลเรียบร้อยแล้ว!")
            
            # (Optional) ถ้าอยากให้หน้าจอรีเฟรชข้อมูลใหม่ทันที อาจต้องมีการเรียก query ข้อมูลใหม่อีกรอบ
            # หรือส่งค่าใหม่กลับไปที่ฟังก์ชัน profileUser(new_data_tuple)
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

    def cancel_edit():
        # คืนค่าในช่องกรอก ให้กลับไปเป็นค่าเริ่มต้นจากตัวแปร user
        v_username.set(user[1])
        v_password.set(user[2])
        v_firstname.set(user[3])
        v_lastname.set(user[4])
        v_email.set(user[5])
        v_tel.set(user[6])
        # (ไม่ต้องแจ้งเตือนก็ได้ หรือจะแจ้งก็ได้ครับ)
        # messagebox.showinfo("Cancelled", "คืนค่าข้อมูลเดิมเรียบร้อยแล้ว")

    # --- สร้าง Layout ---
    content_box = Frame(fm, bg=cl_white, padx=20, pady=20)
    content_box.grid(row=1, column=0)

    Label(content_box, text="Edit Profile", font=('Arial', 24, 'bold'), bg=cl_white, fg="#333333").pack(pady=(0, 20))

    # Helper Function สร้างช่องกรอก
    def create_input(label_text, text_var, is_password=False, is_readonly=False):
        row_frame = Frame(content_box, bg=cl_white)
        row_frame.pack(fill='x', pady=5)
        
        Label(row_frame, text=label_text, font=('Arial', 12, 'bold'), width=12, anchor='w', bg=cl_white).pack(side=LEFT)
        
        if is_readonly:
            # ถ้าแก้ไขไม่ได้ ให้ใช้ Entry แต่ disable ไว้ หรือใช้ Label เหมือนเดิมก็ได้
            ent = Entry(row_frame, textvariable=text_var, font=('Arial', 12), state='disabled', disabledbackground="#f0f0f0", disabledforeground="#555")
        else:
            # ถ้าแก้ไขได้
            show_char = '*' if is_password else None
            ent = Entry(row_frame, textvariable=text_var, font=('Arial', 12), show=show_char, bg="#f9f9f9", bd=1, relief=SOLID)
            
        ent.pack(side=LEFT, fill='x', expand=True, ipady=3)

    # แสดงผลช่องต่างๆ
    create_input("User ID :", StringVar(value=current_id), is_readonly=True) # แก้ไม่ได้
    create_input("Role :", v_role, is_readonly=True)    # แก้ไม่ได้ (ปกติ User ไม่ควรแก้ Role เองได้)
    
    Frame(content_box, height=2, bd=1, relief=SUNKEN).pack(fill='x', pady=10) # เส้นคั่น

    create_input("Username :", v_username)
    create_input("Password :", v_password, is_password=False) # ใส่ True ถ้าอยากให้เป็น ****
    create_input("First Name :", v_firstname)
    create_input("Last Name :", v_lastname)
    create_input("Email :", v_email)
    create_input("Tel :", v_tel)

    btn_frame = Frame(content_box, bg=cl_white)
    btn_frame.pack(pady=20)

    # ปุ่ม Save (สีเขียว)
    btn_save = Button(content_box, text="Save", command=save_profile, 
                  font=('Arial', 12, 'bold'), bg="#2ecc71", fg="white", 
                  cursor="hand2", padx=20, pady=5, bd=0)
    btn_save.pack(pady=(20, 5)) # เพิ่มระยะห่างด้านบน 20px, ด้านล่าง 5px

    # ปุ่ม Cancel (สีแดง)
    btn_cancel = Button(content_box, text="Cancel", command=cancel_edit, 
                    font=('Arial', 12), bg="#e74c3c", fg="white", 
                    cursor="hand2", padx=15, pady=5, bd=0)
    btn_cancel.pack(pady=(5, 0)) # เพิ่มระยะห่างด้านบน 5px, ด้านล่าง 0px

def userManagement(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)
    # ==========================================
    # 1. ส่วนค้นหา (Search & Filter)
    # ==========================================
    search_frame = Frame(fm, bg='white')
    search_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    Label(search_frame, text="ค้นหาจาก:", bg='white').pack(side=LEFT, padx=5)

    # ตัวเลือกคอลัมน์ที่จะค้นหา (Map ชื่อที่โชว์ -> ชื่อใน DB)
    search_options = {
        "Username": "username",
        "First Name": "firstName",
        "Last Name": "lastName",
        "Role": "role"
    }
    
    combo_search = ttk.Combobox(search_frame, values=list(search_options.keys()), state="readonly", width=15)
    combo_search.current(0) # เลือกค่าแรกเป็น Default
    combo_search.pack(side=LEFT, padx=5)

    entry_search = Entry(search_frame, width=20)
    entry_search.pack(side=LEFT, padx=5)

    def search_data():
        selected_display = combo_search.get()
        col_name = search_options[selected_display] # แปลงเป็นชื่อ Column ใน DB
        keyword = entry_search.get()

        # Query ข้อมูลตามเงื่อนไข
        sql = f"SELECT * FROM user WHERE {col_name} LIKE ?"
        cursor.execute(sql, ('%' + keyword + '%',))
        rows = cursor.fetchall()
        update_table(rows)

    btn_search = Button(search_frame, text="ค้นหา", command=search_data, bg='#2196F3', fg='white')
    btn_search.pack(side=LEFT, padx=5)

    btn_reset = Button(search_frame, text="ล้างค่า", command=lambda: load_all_data(), bg='gray', fg='white')
    btn_reset.pack(side=LEFT, padx=5)

    # ==========================================
    # 2. ส่วนตาราง (Treeview)
    # ==========================================
    columns = ('userID', 'username', 'password', 'firstName', 'lastName', 'email', 'tel', 'role')
    tree = ttk.Treeview(fm, columns=columns, show='headings', height=10)
    
    # กำหนดหัวตาราง (Config เหมือนเดิมของคุณ)
    headers = ['User ID', 'Username', 'Password', 'First Name', 'Last Name', 'Email', 'Tel', 'Role']
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)
        tree.column(col, width=100) # ปรับ width ตามชอบ

    tree.grid(row=1, column=0, sticky='nsew', padx=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(fm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')

    # ฟังก์ชันอัปเดตข้อมูลในตาราง
    def update_table(rows):
        tree.delete(*tree.get_children()) # ลบข้อมูลเก่าในตารางออกให้หมด
        for row in rows:
            tree.insert('', 'end', values=row)

    # ฟังก์ชันโหลดข้อมูลทั้งหมด (ตอนเปิดครั้งแรก)
    def load_all_data():
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        update_table(rows)
        entry_search.delete(0, END) # ล้างช่องค้นหา

    load_all_data() # เรียกทำงานทันที

    # ==========================================
    # 3. ส่วนปุ่ม Action (Add, Edit, Delete)
    # ==========================================
    btn_frame = Frame(fm, bg='white')
    btn_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

    def get_next_id():
        try:
            # เลือกค่า userID ที่มากที่สุดในตาราง
            cursor.execute("SELECT MAX(userID) FROM user")
            result = cursor.fetchone()[0]
            
            # ถ้าไม่มีข้อมูลเลย (result เป็น None) ให้เริ่มที่ 1
            if result is None:
                return 1
            else:
                # ถ้ามีข้อมูล ให้เอาค่ามากที่สุด + 1
                return int(result) + 1
        except Exception as e:
            print(e)
            return 1

    # --- ฟังก์ชันสำหรับปุ่มต่างๆ ---
    
    def open_popup(mode, data=None):
        # สร้างหน้าต่างเด้งขึ้นมา (Toplevel)
        popup = Toplevel(root)
        popup.title(f"{mode} User")
        popup.geometry("400x450")
        
        vars_dict = {}
        # เรียงลำดับ field ใหม่ เอา Role มาไว้ใกล้ๆ ID จะได้เลือกก่อนได้
        fields = ['userID', 'role', 'username', 'password', 'firstName', 'lastName', 'email', 'tel']
        
        # ฟังก์ชันอัปเดต ID เมื่อมีการเลือก Role (ใช้เฉพาะตอน Add)
        def update_id_on_role_select(event):
            if mode == "Add":
                selected_role = vars_dict['role'].get()
                if selected_role:
                    # เรียกฟังก์ชัน generate_user_id ที่มีอยู่แล้วด้านล่างไฟล์
                    new_id = generate_user_id(selected_role)
                    
                    # อัปเดตช่อง userID
                    entry_id = vars_dict['userID']
                    entry_id.config(state='normal') # ปลดล็อกก่อนแก้
                    entry_id.delete(0, END)
                    entry_id.insert(0, new_id)
                    entry_id.config(state='readonly') # ล็อกกลับ

        for i, field in enumerate(fields):
            Label(popup, text=field).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            # --- กรณีเป็น Role ให้สร้างเป็น Dropdown ---
            if field == 'role':
                entry = ttk.Combobox(popup, values=["librarian", "admin"], state="readonly")
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                # ผูก Event: เมื่อเลือกค่า ให้ไปเรียกฟังก์ชัน update_id_on_role_select
                entry.bind("<<ComboboxSelected>>", update_id_on_role_select)
            
            # --- กรณีอื่นสร้างเป็นช่องกรอกปกติ ---
            else:
                entry = Entry(popup)
                entry.grid(row=i, column=1, padx=10, pady=5)

            vars_dict[field] = entry    

            # --- จัดการค่าเริ่มต้น (Add/Edit) ---
            
            # กรณี Edit: ใส่ค่าเดิมลงไป
            if mode == "Edit" and data:
                # ต้อง map index ของ data ให้ตรงกับชื่อ field เพราะ data เรียงตาม DB
                # DB: userID(0), username(1), password(2), firstName(3), lastName(4), email(5), tel(6), role(7)
                db_map = {
                    'userID': 0, 'username': 1, 'password': 2, 'firstName': 3, 
                    'lastName': 4, 'email': 5, 'tel': 6, 'role': 7
                }
                val = data[db_map[field]]
                
                if field == 'role':
                    entry.set(val) # Combobox ใช้ set
                else:
                    entry.insert(0, val)
                
                if field == 'userID':     
                    entry.config(state='readonly') # ห้ามแก้ ID

            # กรณี Add:
            if mode == "Add" and field == "userID":
                entry.insert(0, "Select Role First...") # บอกให้เลือก Role ก่อน
                entry.config(state='readonly')

        def save_data():
            # อ่านค่าจากช่องต่าง ๆ
            username = vars_dict['username'].get().strip()
            password = vars_dict['password'].get().strip()
            firstName = vars_dict['firstName'].get().strip()
            lastName = vars_dict['lastName'].get().strip()
            email = vars_dict['email'].get().strip()
            tel = vars_dict['tel'].get().strip()
            role = vars_dict['role'].get().strip()

            if role not in ("librarian", "admin"):
                messagebox.showerror("Error", "Role ต้องเป็น librarian หรือ admin เท่านั้น")
                return

            def save_data():
                # อ่านค่าจากช่องต่าง ๆ
                username = vars_dict['username'].get().strip()
                password = vars_dict['password'].get().strip()
                firstName = vars_dict['firstName'].get().strip()
                lastName = vars_dict['lastName'].get().strip()
                email = vars_dict['email'].get().strip()
                tel = vars_dict['tel'].get().strip()
                role = vars_dict['role'].get().strip() # ไม่ต้อง lower() เพราะ dropdown บังคับค่าแล้ว

                if not role:
                    messagebox.showerror("Error", "กรุณาเลือก Role")
                    return

                if mode == "Add":
                    try:
                        # ดึง ID ที่โชว์อยู่ในช่อง (ซึ่งเจนมาแล้วตอนเลือก Role)
                        final_id = vars_dict['userID'].get()
                        
                        # ป้องกันกรณี User ยังไม่เลือก Role แล้วกด Save
                        if not final_id or "Select" in final_id:
                            messagebox.showerror("Error", "กรุณาเลือก Role เพื่อสร้าง User ID")
                            return

                        sql = """INSERT INTO user(userID, username, password, firstName, lastName, email, tel, role)
                                VALUES (?,?,?,?,?,?,?,?)"""

                        params = (final_id, username, password, firstName, lastName, email, tel, role)

                        cursor.execute(sql, params)
                        conn.commit()
                        messagebox.showinfo("Success", f"เพิ่มผู้ใช้สำเร็จ\nUser ID = {final_id}")
                        popup.destroy()
                        load_all_data()

                    except Exception as e:
                        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

                elif mode == "Edit":
                    try:
                        user_id = vars_dict['userID'].get() # ดึงจากช่อง Entry โดยตรง

                        sql = """
                            UPDATE user
                            SET username=?, password=?, firstName=?, lastName=?,
                                email=?, tel=?, role=?
                            WHERE userID=?
                        """
                        cursor.execute(sql, (
                            username, password, firstName, lastName,
                            email, tel, role, user_id
                        ))
                        conn.commit()
                        messagebox.showinfo("Success", "แก้ไขข้อมูลสำเร็จ")
                        popup.destroy()
                        load_all_data()
                    except Exception as e:
                        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

            Button(popup, text="Save", command=save_data,
                bg='green', fg='white').grid(row=len(fields), column=1, pady=20)

    def add_user():
        open_popup("Add")

    def edit_user():
        selected = tree.selection() # ดูว่า user เลือกแถวไหน
        if not selected:
            messagebox.showwarning("Warning", "กรุณาเลือกรายการที่จะแก้ไข")
            return
        item = tree.item(selected)
        data = item['values'] # ได้ข้อมูลเป็น list
        open_popup("Edit", data)

    def delete_user():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "กรุณาเลือกรายการที่จะลบ")
            return
        
        confirm = messagebox.askyesno("Confirm", "ต้องการลบข้อมูลนี้ใช่หรือไม่?")
        if confirm:
            item = tree.item(selected)
            user_id = item['values'][0] # สมมติว่า ID อยู่คอลัมน์แรก
            cursor.execute("DELETE FROM user WHERE userID = ?", (user_id,))
            conn.commit()
            load_all_data() # รีเฟรชตาราง

    # วางปุ่ม
    Button(btn_frame, text="เพิ่มข้อมูล (Add)", command=add_user, bg='green', fg='white', width=15).pack(side=LEFT, padx=5)
    Button(btn_frame, text="แก้ไข (Edit)", command=edit_user, bg='orange', fg='white', width=15).pack(side=LEFT, padx=5)
    Button(btn_frame, text="ลบ (Delete)", command=delete_user, bg='red', fg='white', width=15).pack(side=LEFT, padx=5)
    
# ================== BOOKS / CATEGORY / SHELVES ==================

def be_generate_new_book_id():
    """
    gen bookID ใหม่ในรูป B0001, B0002, ...
    ใช้ cursor, conn global เดิม
    """
    cursor.execute("""
        SELECT bookID
        FROM books
        WHERE bookID LIKE 'B%'
        ORDER BY CAST(SUBSTR(bookID, 2) AS INTEGER) DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row and row[0]:
        last_num = int(row[0][1:])
        new_num = last_num + 1
    else:
        new_num = 1
    return f"B{new_num:04d}"

def be_list_books(search_text=None):
    sql = """
        SELECT b.bookID,
               b.title,
               b.author,
               b.ISBN,
               b.totalCopies,
               b.availableCopies,
               b.bookStatus,
               c.ctgName,
               b.shelfID
        FROM books b
        LEFT JOIN category c ON b.ctgID = c.ctgID
    """
    params = ()
    if search_text:
        like = f"%{search_text}%"
        sql += " WHERE b.title LIKE ? OR b.author LIKE ? OR b.ISBN LIKE ?"
        params = (like, like, like)
    sql += " ORDER BY b.bookID"

    cursor.execute(sql, params)
    return cursor.fetchall()

def be_get_book_status_options():
    cursor.execute("""
        SELECT DISTINCT bookStatus
        FROM books
        WHERE bookStatus IS NOT NULL AND TRIM(bookStatus) <> ''
    """)
    db_statuses = [row[0] for row in cursor.fetchall()]
    default_statuses = ["available", "unavailable", "maintenance"]
    # รวม list แล้วลบตัวซ้ำ
    return list(dict.fromkeys(default_statuses + db_statuses))

def be_get_categories():
    cursor.execute("SELECT ctgID, ctgName FROM category ORDER BY ctgID")
    return cursor.fetchall()

def be_get_shelves():
    cursor.execute(
        "SELECT shelfID, section, floor, aisle FROM shelves ORDER BY shelfID"
    )
    return cursor.fetchall()

def be_get_book_extra(book_id):
    cursor.execute(
        "SELECT publisher, pubYear FROM books WHERE bookID = ?",
        (book_id,)
    )
    return cursor.fetchone()

def be_insert_book(
    book_id, ctg_id, shelf_id, isbn, title, author,
    publisher, pubyear, total_copies, avail_copies,
    status, create_by
):
    cursor.execute("""
        INSERT INTO books (
            bookID,
            ctgID,
            shelfID,
            ISBN,
            title,
            author,
            publisher,
            pubYear,
            totalCopies,
            availableCopies,
            bookStatus,
            createBy
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        book_id,
        ctg_id,
        shelf_id,
        isbn,
        title,
        author,
        publisher,
        pubyear,
        total_copies,
        avail_copies,
        status,
        create_by
    ))
    conn.commit()

def be_update_book(
    book_id, ctg_id, shelf_id, isbn, title, author,
    publisher, pubyear, total_copies, avail_copies,
    status
):
    cursor.execute("""
        UPDATE books
        SET ctgID = ?,
            shelfID = ?,
            ISBN = ?,
            title = ?,
            author = ?,
            publisher = ?,
            pubYear = ?,
            totalCopies = ?,
            availableCopies = ?,
            bookStatus = ?
        WHERE bookID = ?
    """, (
        ctg_id,
        shelf_id,
        isbn,
        title,
        author,
        publisher,
        pubyear,
        total_copies,
        avail_copies,
        status,
        book_id
    ))
    conn.commit()

def be_delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE bookID = ?", (book_id,))
    conn.commit()

# ---------- CATEGORY BACKEND ----------

def be_list_categories(search_text=None):
    sql = "SELECT ctgID, ctgName FROM category"
    params = ()
    if search_text:
        like = f"%{search_text}%"
        sql += " WHERE ctgID LIKE ? OR ctgName LIKE ?"
        params = (like, like)
    sql += " ORDER BY ctgID"
    cursor.execute(sql, params)
    return cursor.fetchall()

def be_insert_category(ctg_id, ctg_name):
    cursor.execute(
        "INSERT INTO category(ctgID, ctgName) VALUES(?,?)",
        (ctg_id, ctg_name)
    )
    conn.commit()

def be_update_category(ctg_id, ctg_name):
    cursor.execute(
        "UPDATE category SET ctgName=? WHERE ctgID=?",
        (ctg_name, ctg_id)
    )
    conn.commit()

def be_delete_category(ctg_id):
    cursor.execute("DELETE FROM category WHERE ctgID=?", (ctg_id,))
    conn.commit()

def borrow_page(user):
    clear_main_frame()

    fm = Frame(main_frame, bg="white")
    fm.grid(row=0, column=0, sticky="nsew")

    # Layout 3 แถว
    fm.grid_rowconfigure(0, weight=0)  # student table
    fm.grid_rowconfigure(1, weight=0)  # student detail
    fm.grid_rowconfigure(2, weight=1)  # borrow history + borrow form
    fm.grid_columnconfigure(0, weight=1)

    Label(fm, text="Borrowing System", font=("Kanit", 18, "bold"), bg="white").grid(
        row=0, column=0, pady=(10,5)
    )


# ---------- SHELVES BACKEND ----------

def be_list_shelves(search_text=None):
    sql = "SELECT shelfID, section, floor, aisle FROM shelves"
    params = ()
    if search_text:
        like = f"%{search_text}%"
        sql += " WHERE shelfID LIKE ? OR section LIKE ?"
        params = (like, like)
    sql += " ORDER BY shelfID"
    cursor.execute(sql, params)
    return cursor.fetchall()


def be_insert_shelf(shelf_id, section, floor, aisle):
    cursor.execute(
        "INSERT INTO shelves(shelfID, section, floor, aisle) VALUES(?,?,?,?)",
        (shelf_id, section, floor, aisle)
    )
    conn.commit()


def be_update_shelf(shelf_id, section, floor, aisle):
    cursor.execute(
        "UPDATE shelves SET section=?, floor=?, aisle=? WHERE shelfID=?",
        (section, floor, aisle, shelf_id)
    )
    conn.commit()


def be_delete_shelf(shelf_id):
    cursor.execute("DELETE FROM shelves WHERE shelfID=?", (shelf_id,))
    conn.commit()   

def order(user,order=None):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure((0), weight=1)
    fm.grid_rowconfigure(1, weight=10)
    
    # variable
    global  tree_order
    search_var = StringVar()
    # find product
    if order is None:
        order = retrieve_order(user[0])
    # table product
    columns = ("id", "quantity", "total price")
    tree_order = Treeview(fm, columns=columns, show="headings")
    
    # frame inside
    #menubar
    bar_home(user)
    
    #head name page
    Label(fm,text="Order",bg=cl_white,fg='black',font=font_h3_bold).grid(row=0,column=0,sticky=W,padx=spacing_comp)
    
    #search frame
    search_home_entry = Entry(fm,bg=cl_white,fg='black',font=font_h5,textvariable=search_var)
    search_home_entry.grid(row=0,column=1, ipadx=long_entry,ipady=high_entry ,padx=spacing_comp, sticky=E) #Spy Gb
    search_button = Button(fm,image=search_icon,command=lambda: search_order(search_var.get(), user))
    search_button.grid(row=0, column=1,padx=spacing_comp, sticky=E)
    
    # กำหนดหัวตาราง
    for col in columns:
        tree_order.heading(col, text=col)
        tree_order.column(col, width=50, anchor=W)
    
    # เพิ่มข้อมูล
    for row in order:
        tree_order.insert("", END, value=row)
    
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="info", command=lambda: info_order_page(tree_order))
    context_menu.add_command(label="delete", command=lambda: delete_order(tree_order))
    
    #ผูกการคลิกขวากับ show_context_menu
    tree_order.bind("<Button-3>", lambda event: show_context_menu(event, tree_order, context_menu))
    # # แสดง Treeview
    tree_order.grid(row=1, columnspan=3, padx=spacing_comp, sticky=NSEW)
       
def stock(user,product=None):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure((0), weight=1)
    fm.grid_rowconfigure(1, weight=10)
    
    # variable
    global  tree_stock
    search_var = StringVar()
    # find product
    if product is None:
        product = retrieve_product(user[0])
    # table product
    columns = ("id", "name", "price", "amount")
    tree_stock = Treeview(fm, columns=columns, show="headings")
    
    # frame inside
    #menubar
    bar_home(user)
    
    #head name page
    Label(fm,text="Stock",bg=cl_white,fg='black',font=font_h3_bold).grid(row=0,column=0,sticky=W,padx=spacing_comp)
    
    #search frame
    search_home_entry = Entry(fm,bg=cl_white,fg='black',font=font_h5,textvariable=search_var)
    search_home_entry.grid(row=0,column=1, ipadx=long_entry,ipady=high_entry ,padx=spacing_comp, sticky=E) #Spy Gb
    search_button = Button(fm,image=search_icon,command=lambda: search_products(search_var.get(), user))
    search_button.grid(row=0, column=1,padx=spacing_comp, sticky=E)
    
    # add product
    add_button = Button(fm,image=add_item_icon, text="add product",fg=cl_black,font=font_h5,compound=LEFT,padx=10, pady=5, bg=cl_white_gray,command=lambda: add_product_page(user))
    add_button.grid(row=0, column=2,padx=spacing_comp, sticky=E)
    

    # กำหนดหัวตาราง
    for col in columns:
        tree_stock.heading(col, text=col)
        tree_stock.column(col, width=50, anchor=W)
    
    # เพิ่มข้อมูล
    for row in product:
        tree_stock.insert("", END, value=row)
    
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="edit", command=lambda: edit_product_page(tree_stock,user))
    context_menu.add_command(label="delete", command=lambda: delete_product(tree_stock))
    
    #ผูกการคลิกขวากับ show_context_menu
    tree_stock.bind("<Button-3>", lambda event: show_context_menu(event, tree_stock, context_menu))
    # # แสดง Treeview
    tree_stock.grid(row=1, columnspan=3, padx=spacing_comp, sticky=NSEW)
    
def profile(user):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white, padx=295, pady=104)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg=cl_white)
    top.rowconfigure((0,1,2),weight=1)
    top.columnconfigure(0,weight=1)
    top.columnconfigure(1,weight=2)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg=cl_white)
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure((0,1),weight=1)
    bot.grid(row=1,columnspan=2,sticky=NSEW)
    
    #global veriable
    global name_profile_entry, username_profile_entry
    username = StringVar(value=user[1])
    password = StringVar(value=user[2])
    name = StringVar(value=user[3])
    user_id = user[0]
    
    #set scale of component
    
    
    # - component inside -
    #menubar
    bar_home(user)
    
    # top frame 
    Label(top,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_profile_entry = Entry(top,bg=cl_white_gray, textvariable = name)
    name_profile_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="username : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    username_profile_entry = Entry(top,bg=cl_white_gray, textvariable = username)
    username_profile_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    password_profile_label = Label(top,bg=cl_white_gray, textvariable = password, anchor=W,)
    password_profile_label.grid(row=2,column=1,sticky='w',ipadx=145 , ipady=high_entry ,padx=spacing_comp)
    
    # bot frame 
    update_btn = Button(bot,text="update profile",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: update_profile(name.get(), username.get(), user_id))
    update_btn.grid(row=0,column=0, ipadx=50, ipady=5, padx=10)
    change_password_btn = Button(bot,text="change password",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: change_password_page(user))
    change_password_btn.grid(row=0,column=1, ipadx=50, ipady=5, padx=10)

""" POP UP """
def change_password_page(user):
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Change Password")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #global veriable
    global change_password_entry, change_confirm_password_entry
    new_password = StringVar()
    confirm_password = StringVar()
    user_id = user[0]    
    # - component inside -
    
    Label(popup,text="new password : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    change_password_entry = Entry(popup,bg=cl_white_gray, textvariable = new_password)
    change_password_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="confirm password : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    change_confirm_password_entry = Entry(popup,bg=cl_white_gray, textvariable = confirm_password)
    change_confirm_password_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    change_password_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: change_password(new_password.get(),confirm_password.get(),user_id))
    change_password_btn.grid(row=2,columnspan=2, ipadx=50, ipady=5, padx=10)
    
def edit_product_page(tree,user):
    selected = tree.selection()
    item = tree.item(selected, "values")
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Edit Product")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2,3), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global name_edit_product_entry, price_edit_product_entry, amount_edit_product_entry
    name_product = StringVar(value=item[1])
    price_product = StringVar(value=item[2])
    amount_product = StringVar(value=item[3])    
    
    # - component inside -
    Label(popup,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = name_product)
    name_edit_product_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="price : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    price_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = price_product)
    price_edit_product_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="amount : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    amount_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = amount_product)
    amount_edit_product_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    edit_product_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: edit_product(name_product.get(),price_product.get(),amount_product.get(),item[0],user))
    edit_product_btn.grid(row=3,columnspan=2, ipadx=50, ipady=5, padx=10)

def add_product_page(user):
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Add Product")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2,3), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global name_add_product_entry, price_add_product_entry, amount_add_product_entry
    name_product = StringVar()
    price_product = StringVar()
    amount_product = StringVar()
    
    # - component inside -
    Label(popup,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = name_product)
    name_add_product_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="price : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    price_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = price_product)
    price_add_product_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="amount : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    amount_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = amount_product)
    amount_add_product_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    add_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: add_product(name_product.get(),price_product.get(),amount_product.get(),user))
    add_btn.grid(row=3,columnspan=2, ipadx=50, ipady=5, padx=10)

def info_order_page(tree):
    selected = tree.selection()
    item = tree.item(selected, "values")
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("info order")
    popup.geometry("500x500")
    popup.grid_rowconfigure((0), weight=4)
    popup.grid_rowconfigure((1,2), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global tree_order_info
    
    order_item = retrieve_order_item(item[0])
    for row in order_item:
        value = row[2]  # ดึง column index ที่ 2
        product = retrieve_product_order(value)
        
    print(product)
    columns = ("name", "amount", "price","total price")
    tree_order_info = Treeview(popup, columns=columns, show="headings")
    # - component inside -
    for col in columns:
        tree_order_info.heading(col, text=col)
        tree_order_info.column(col, width=20, anchor=W)
    
    for row in order_item:
        value = row[2]  # ดึง column index ที่ 2
        product = retrieve_product_order(value)
        
        row_data = (
            product[1],
            row[3],
            product[2],
            row[4]
        )
        tree_order_info.insert("", END, value=row_data)
    
    tree_order_info.grid(row=0, columnspan=2, padx=spacing_comp,pady=spacing_comp, sticky=NSEW)
    
    
    Label(popup,text=f"Total Amount : {item[1]}",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,columnspan=2,sticky='w', padx=spacing_comp)
    Label(popup,text=f"Total Price : {item[2]}",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,columnspan=2,sticky='w', padx=spacing_comp)
    
    
""" BACK END """
def login_click(username,password) :
    # Is username blank?
    if username == "" :
        messagebox.showwarning("Admin:","Please enter username")
        username_login_entry.focus_force()
    else :
        if password == "" :
            # check username exists on database.
            messagebox.showwarning("Admin:","Please enter password")
            password_login_entry.focus_force()
        else :
            # check username and password 
            sql = "select * from user where username = ? and password = ? "
            cursor.execute(sql,[username, password])
            user = cursor.fetchone()
            if user :
                messagebox.showinfo("Admin:","Login Successfully")
                print(user)

                dashboard(user)   # <-- ส่ง user เข้าฟังก์ชัน

            else :
                messagebox.showwarning("Admin:","Username not found\n Please register before Login")
                password_login_entry.select_range(0,END)
                password_login_entry.focus_force()

def check_user(username):
    sql = "select * from user where username = ?"
    cursor.execute(sql, [username])
    profile = cursor.fetchone()    
    return profile

def update_profile(name, username, user_id):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name")
        name_profile_entry.focus_force() 
        return
    if username == "" :
        messagebox.showwarning("Admin:","Please enter username")
        username_profile_entry.focus_force()  
        return

    sql = "select * from user where userID = ?"
    cursor.execute(sql,[user_id])
    old_username = cursor.fetchone()

    sql = "select * from user where username = ?"
    cursor.execute(sql,[username])
    new_username = cursor.fetchone()

    if new_username:
        if new_username == old_username:
            sql = 'update user set firstName = ?, username = ? where userID = ?'
            cursor.execute(sql, (name, username, user_id))
        else:
            messagebox.showwarning("Admin:","The username already exists in the system. Please enter a new username")
            username_profile_entry.focus_force()
            return
    else:
        sql = 'update user set firstName = ?, username = ? where userID = ?'
        cursor.execute(sql, (name, username, user_id))

    conn.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Update Profile", "Updated profile successfully.")
        user = retrieve_user(user_id)
        profile(user)
    else:
        messagebox.showwarning("Update Profile", "No data changes.")


def retrieve_user_management():
    sql = "select * from user "
    cursor.execute(sql)
    tableUser = cursor.fetchall()
    return tableUser


def retrieve_user(user_id):
    sql = """
        SELECT userID, username, password, firstName, lastName, email, tel, role
        FROM user
        WHERE userID = ?
    """
    cursor.execute(sql, (user_id,))
    return cursor.fetchone()

def retrieve_product(user_id):
    sql = "select * from products where user_id = ?"
    cursor.execute(sql, [user_id])
    product = cursor.fetchall()
    
    return product
def retrieve_product_order(product_id):
    sql = "select * from products where product_id = ?"
    cursor.execute(sql, [product_id])
    product = cursor.fetchone()
   
    return product
def retrieve_order(user_id):
    sql = "select * from orders where userID = ?"
    cursor.execute(sql, [user_id])
    order = cursor.fetchall()
    
    return order
def retrieve_order_item(order_id):
    sql = "select * from order_items where order_id = ?"
    cursor.execute(sql, [order_id])
    order = cursor.fetchall()
    
    return order

def change_password(new_password, confirm_password, user_id):
    if new_password == "":
        messagebox.showwarning("Admin:", "Please enter new password")
        change_password_entry.focus_force()
        return

    if confirm_password == "":
        messagebox.showwarning("Admin:", "Please enter confirm password")
        change_confirm_password_entry.focus_force()
        return

    if new_password != confirm_password:
        messagebox.showwarning(
            "Admin:",
            "Your new password and confirmation do not match. Kindly confirm your password again"
        )
        change_confirm_password_entry.focus_force()
        return

    sql = "UPDATE user SET password = ? WHERE userID = ?"
    cursor.execute(sql, (new_password, user_id))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Update Profile", "Updated new password successfully.")
        user = retrieve_user(user_id)
    else:
        messagebox.showwarning("Update Profile", "No data changes.")
          
def show_context_menu(event, tree, context_menu):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)
        
def delete_product(tree):
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        confirm = messagebox.askyesno("Delete", f"ต้องการลบ: {item[1]} หรือไม่?")
        if confirm:
            conn, cursor = db_connection()
            cursor.execute("DELETE FROM products WHERE product_id=?", (item[0],))
            conn.commit()
            conn.close()
            tree.delete(selected)
            messagebox.showinfo("Delete", "ลบข้อมูลสำเร็จแล้ว!")
            
def edit_product(name,price_txt,amount_txt,product_id,user):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name product")
        name_edit_product_entry.focus_force()  
    else :
        if price_txt == "" :
            messagebox.showwarning("Admin:","Please enter price product")
            price_edit_product_entry.focus_force() 
        else :
            try :
                price = int(price_txt)
            except ValueError:
                messagebox.showerror("Admin:", "Price must be an integer number")
                price_edit_product_entry.focus_force()
                return
            
            if amount_txt == "" :
                messagebox.showwarning("Admin:","Please enter amount product")    
                amount_edit_product_entry.focus_force() 
            else :
                try :
                    amount = int(amount_txt)
                except ValueError:
                    messagebox.showerror("Admin:","Amount must be an integer product")
                    amount_edit_product_entry.focus_force()
                    return
                sql = 'update products set name = ? , price = ?, stock_quantity = ? where product_id = ?'
                cursor.execute(sql, (name, price, amount, product_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Edit Product", "Edit product successfully.")
                    stock(user)
                else:
                    messagebox.showwarning("Edit Product", "No data changes.")
                    name_edit_product_entry.focus_force() 
def add_product(name,price_txt,amount_txt,user):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name product") 
        name_add_product_entry.focus_force() 
    else :
        if price_txt == "" :
            messagebox.showwarning("Admin:","Please enter price product")
            price_add_product_entry.focus_force() 
        else :
            try :
                price = int(price_txt)
            except ValueError:
                messagebox.showerror("Admin:", "Price must be an integer number")
                price_add_product_entry.focus_force()
                return
            if amount_txt == "" :
                messagebox.showwarning("Admin:","Please enter amount product")
                amount_add_product_entry.focus_force()     
            else :
                try :
                    amount = int(amount_txt)
                except ValueError:
                    messagebox.showerror("Admin:","Amount must be an integer product")
                    amount_add_product_entry.focus_force()
                    return
                sql = "insert into products (name, price, stock_quantity, user_id) values ( ?, ?, ?, ?)"
                cursor.execute(sql, (name, price, amount, user[0]))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Add Product", "Add product successfully.")
                    stock(user)
                else:
                    messagebox.showwarning("Add Product", "No data changes.")
                    name_add_product_entry.focus_force() 

def search_products(search_text, user):
    # ล้างข้อมูลเก่าใน treeview
    search = f'%{search_text}%'
    
    for item in tree_stock.get_children():
        tree_stock.delete(item)
        
    # ถ้าไม่ได้กรอกอะไร ให้ดึงทั้งหมด
    if search_text == "":
        sql = "SELECT product_id, name, price, stock_quantity FROM products WHERE user_id = ?"
        cursor.execute(sql, (user[0],))
    else :
        sql = """
        SELECT product_id, name, price, stock_quantity
        FROM products
        WHERE user_id = ?
        AND (
            product_id LIKE ?
            OR name LIKE ?
            OR price LIKE ?
            OR stock_quantity LIKE ?
            )
            """
        cursor.execute(sql, (user[0], search, search, search, search))
    
    results = cursor.fetchall()
    for row in results:
        tree_stock.insert("", END, values=row)

def delete_order(tree):
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        confirm = messagebox.askyesno("Delete", f"ต้องการคำสั่งซื้อ: {item[1]} หรือไม่ ?")
        if confirm:
            conn, cursor = db_connection()
            order_id = item[0]

            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))

            cursor.execute("""
                DELETE FROM orders
                WHERE order_id NOT IN (
                    SELECT DISTINCT order_id FROM order_items
                )
            """)
            conn.commit()
            conn.close()

            tree.delete(selected)
            messagebox.showinfo("Delete", "ลบคำสั่งซื้อเรียบร้อยแล้ว!")

def search_order(search_text, user):
    # ล้างข้อมูลเก่าใน treeview
    search = f'%{search_text}%'
    
    for item in tree_order.get_children():
        tree_order.delete(item)
        
    # ถ้าไม่ได้กรอกอะไร ให้ดึงทั้งหมด
    if search_text == "":
        sql = "SELECT order_id, quantity , total_price FROM orders WHERE user_id = ?"
        cursor.execute(sql, (user[0],))
    else :
        sql = """
        SELECT order_id, quantity , total_price
        FROM orders
        WHERE user_id = ?
        AND (
            order_id LIKE ?
            )
            """
        cursor.execute(sql, (user[0], search))
    
    results = cursor.fetchall()
    for row in results:
        tree_order.insert("", END, values=row)    
""" ==================== BACK END : BOOKS / CATEGORY / SHELVES ==================== """

# ---------- BOOKS BACK END ----------

def be_get_books(filter_col=None, keyword=None):
    sql = """
        SELECT b.bookID,
               b.title,
               b.author,
               b.ISBN,
               b.totalCopies,
               b.availableCopies,
               b.bookStatus,
               c.ctgName,
               b.shelfID
        FROM books b
        LEFT JOIN category c ON b.ctgID = c.ctgID
    """
    params = []
    if filter_col and keyword:
        sql += f" WHERE {filter_col} LIKE ?"
        params.append(f"%{keyword}%")

    sql += " ORDER BY b.bookID"
    cursor.execute(sql, params)
    return cursor.fetchall()

def be_get_book_status_options():
    cursor.execute("""
        SELECT DISTINCT bookStatus
        FROM books
        WHERE bookStatus IS NOT NULL AND TRIM(bookStatus) <> ''
    """)
    db_statuses = [row[0] for row in cursor.fetchall()]
    default_statuses = ["available", "unavailable", "maintenance"]
    # ลบซ้ำ
    return list(dict.fromkeys(default_statuses + db_statuses))

def be_get_categories_for_book():
    cursor.execute("SELECT ctgID, ctgName FROM category ORDER BY ctgID")
    return cursor.fetchall() 


def be_get_shelves_for_book():
    cursor.execute("SELECT shelfID, section, floor, aisle FROM shelves ORDER BY shelfID")
    return cursor.fetchall() 


def be_get_book_extra(book_id):
    cursor.execute(
        "SELECT publisher, pubYear FROM books WHERE bookID = ?",
        (book_id,)
    )
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    return None, None

def be_generate_new_book_id():
    cursor.execute("""
        SELECT bookID
        FROM books
        WHERE bookID LIKE 'B%'
        ORDER BY CAST(SUBSTR(bookID, 2) AS INTEGER) DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row and row[0]:
        last_num = int(row[0][1:])
        new_num = last_num + 1
    else:
        new_num = 1
    return f"B{new_num:04d}"

def be_insert_book(user_id, ctg_id, shelf_id,
                   isbn, title, author, publisher,
                   pub_year, total, avail, status):
    book_id = be_generate_new_book_id()
    cursor.execute("""
        INSERT INTO books (
            bookID,
            ctgID,
            shelfID,
            ISBN,
            title,
            author,
            publisher,
            pubYear,
            totalCopies,
            availableCopies,
            bookStatus,
            createBy
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        book_id,
        ctg_id,
        shelf_id,
        isbn,
        title,
        author,
        publisher,
        pub_year,
        total,
        avail,
        status,
        user_id
    ))
    conn.commit()

def be_update_book(book_id, ctg_id, shelf_id,
                   isbn, title, author, publisher,
                   pub_year, total, avail, status):
    cursor.execute("""
        UPDATE books
        SET ctgID = ?,
            shelfID = ?,
            ISBN = ?,
            title = ?,
            author = ?,
            publisher = ?,
            pubYear = ?,
            totalCopies = ?,
            availableCopies = ?,
            bookStatus = ?
        WHERE bookID = ?
    """, (
        ctg_id,
        shelf_id,
        isbn,
        title,
        author,
        publisher,
        pub_year,
        total,
        avail,
        status,
        book_id
    ))
    conn.commit()


def be_delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE bookID=?", (book_id,))
    conn.commit()

# ---------- CATEGORY BACK END ----------

def be_get_categories(filter_col=None, keyword=None):
    sql = "SELECT ctgID, ctgName FROM category"
    params = []
    if filter_col and keyword:
        sql += f" WHERE {filter_col} LIKE ?"
        params.append(f"%{keyword}%")
    sql += " ORDER BY ctgID"
    cursor.execute(sql, params)
    return cursor.fetchall()


def be_insert_category(ctg_id, ctg_name):
    cursor.execute(
        "INSERT INTO category(ctgID, ctgName) VALUES(?,?)",
        (ctg_id, ctg_name)
    )
    conn.commit()


def be_update_category(ctg_id, ctg_name):
    cursor.execute(
        "UPDATE category SET ctgName=? WHERE ctgID=?",
        (ctg_name, ctg_id)
    )
    conn.commit()


def be_delete_category(ctg_id):
    cursor.execute("DELETE FROM category WHERE ctgID=?", (ctg_id,))
    conn.commit()

# ---------- SHELVES BACK END ----------

def be_get_shelves(filter_col=None, keyword=None):
    sql = "SELECT shelfID, section, floor, aisle FROM shelves"
    params = []
    if filter_col and keyword:
        sql += f" WHERE {filter_col} LIKE ?"
        params.append(f"%{keyword}%")
    sql += " ORDER BY shelfID"
    cursor.execute(sql, params)
    return cursor.fetchall()

def be_insert_shelf(shelf_id, section, floor, aisle):
    cursor.execute(
        "INSERT INTO shelves(shelfID, section, floor, aisle) VALUES(?,?,?,?)",
        (shelf_id, section, floor, aisle)
    )
    conn.commit()


def be_update_shelf(shelf_id, section, floor, aisle):
    cursor.execute(
        "UPDATE shelves SET section=?, floor=?, aisle=? WHERE shelfID=?",
        (section, floor, aisle, shelf_id)
    )
    conn.commit()

def be_delete_shelf(shelf_id):
    cursor.execute("DELETE FROM shelves WHERE shelfID=?", (shelf_id,))
    conn.commit()
# ===========================
#      BACK-END USER
# ===========================
def generate_user_id(role):
    """
    รูปแบบ: 25 + roleCode(01/02) + running 3 หลัก
    25 = ปี
    role:
        librarian -> 01
        admin -> 02
    """
    year_prefix = "25"
    if role == "librarian":
        role_code = "01"
    elif role == "admin":
        role_code = "02"
    else:
        role_code = "99"

    prefix = year_prefix + role_code 
    cursor.execute("""
        SELECT userID
        FROM user
        WHERE userID LIKE ?
        ORDER BY CAST(SUBSTR(userID, 5) AS INTEGER) DESC
        LIMIT 1
    """, (prefix + "%",))

    row = cursor.fetchone()

    if row:
        last_run = int(str(row[0])[4:]) 
    else:
        last_run = 0

    new_run = last_run + 1
    return f"{prefix}{new_run:03d}"

# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
root = create_window()
fm_main = create_layout(root)
conn, cursor = db_connection()

# โหลดรูป
logo_img = PhotoImage(file="img/logo_full.png").subsample(4, 4)
add_cart_icon = PhotoImage(file="img/add_cart.png")
add_item_icon = PhotoImage(file="img/add_item.png")
delete_icon = PhotoImage(file="img/delete.png")
edit_icon = PhotoImage(file="img/edit.png")
search_icon = PhotoImage(file="img/search.png")

# ถ้าอยากให้ล็อกอินหน้าแรก ให้เรียก login()
login()

# ถ้าอยากเทสต์เข้าเป็นแอดมินตรง ๆ ค่อยใช้โค้ดนี้ทีหลัง
# sql = "select * from user where userID = 2501001"
# cursor.execute(sql)
# user = cursor.fetchone()
# dashboard(user)

root.mainloop()
conn.close()

