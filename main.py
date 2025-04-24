from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview

""" FRONT END """
def create_window():
    root = Tk()
    root.title("POS : Be Lune")
    root.geometry("1194x834")
    root.configure(bg="white")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    return root
def create_layout(root):
    fm_main = Frame(root,bg="white",padx=24,pady=24)
    fm_main.grid_rowconfigure(0, weight=1)
    fm_main.grid_columnconfigure(0, weight=1)
    fm_main.grid(row=0, column=0, sticky=NSEW)
    return fm_main

#Menu Bar
def bar_login():
    menu_bar = Menu(root, tearoff=0)
    menu_bar.add_command(label='Be Lune') 
    menu_bar.add_command(label='login', command=login) 
    menu_bar.add_command(label='register', command=register)
    menu_bar.add_command(label='exit', command=lambda: exit(0))  
    root.configure(menu=menu_bar)

def bar_home(user):
    menu_bar = Menu(root, tearoff=0)
    menu_bar.add_command(label='Be Lune') 
    menu_bar.add_command(label='home', command=lambda: home(user)) 
    menu_bar.add_command(label='order', command=lambda: order(user))
    menu_bar.add_command(label='stock', command=lambda: stock(user))
    menu_bar.add_command(label='profile', command=lambda: profile(user))
    menu_bar.add_command(label='log out', command=login) 
    root.configure(menu=menu_bar)

#login page   
def login():
    
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg='white')
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    mid = Frame(fm,bg='white')
    mid.rowconfigure((0,1),weight=1)
    mid.columnconfigure((0,1),weight=1)
    mid.grid(row=1,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg='white')
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure(0,weight=1)
    bot.grid(row=2,columnspan=2,sticky=NSEW)
    
    #global veriable
    global username_login_entry, password_login_entry
    username_info = StringVar()
    password_info = StringVar()
    
    #set scale of component
    long_entry = 80
    high_entry = 4
    spacing_comp = 10
    # - component inside -
    #menubar
    bar_login()

    # top frame 
    Label(top,image=logo,bg='white').grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="username : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    username_login_entry = Entry(mid,bg='#F3F3F3', textvariable=username_info)
    username_login_entry.grid(row=0,column=1,sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)
    
    Label(mid,text="password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    password_login_entry = Entry(mid,bg='#F3F3F3',show='*', textvariable=password_info)
    password_login_entry.grid(row=1, column=1, sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)

    # bot frame 
    Button(bot,text="login",bg='#B12937',fg='white',font=("Inter", 16, "bold"), command=lambda:login_click(username_info.get(),password_info.get())).grid(row=0,column=0, ipadx=50, ipady=5)
        
# Register page
def register():
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=104)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,2), weight=1)
    fm.grid_rowconfigure(1, weight=4)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg='white')
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    mid = Frame(fm,bg='white')
    mid.rowconfigure((0,1,2,3),weight=1)
    mid.columnconfigure(0,weight=1)
    mid.columnconfigure(1,weight=3)
    mid.grid(row=1,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg='white')
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure(0,weight=1)
    bot.grid(row=2,columnspan=2,sticky=NSEW)
    
    #global veriable
    global name_register_entry, username_register_entry, password_register_entry, confirm_password_register_entry
    
    name_regis = StringVar()
    username_regis = StringVar()
    password_regis = StringVar()
    confirm_password_regis = StringVar()
    
    #set scale of component
    long_entry = 80
    high_entry = 4
    spacing_comp = 10
    
    # - component inside -
    #menubar
    bar_login()
    
    # top frame 
    Label(top,image=logo,bg='white').grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="name : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    name_register_entry = Entry(mid,bg='#F3F3F3', textvariable = name_regis)
    name_register_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="username : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    username_register_entry = Entry(mid,bg='#F3F3F3', textvariable = username_regis)
    username_register_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=2,column=0,sticky='e')
    password_register_entry= Entry(mid,bg='#F3F3F3',show='*', textvariable = password_regis)
    password_register_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="confirm password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=3,column=0,sticky='e')
    confirm_password_register_entry = Entry(mid,bg='#F3F3F3',show='*', textvariable = confirm_password_regis)
    confirm_password_register_entry.grid(row=3,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)

    # bot frame 
    Button(bot,text="register",bg='#B12937',fg='white',font=("Inter", 16, "bold"),command=lambda:  register_click(name_regis.get(), username_regis.get(), password_regis.get(), confirm_password_regis.get())).grid(row=0,column=0, ipadx=50, ipady=5)

def home(user):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    
    #menubar
    bar_home(user)
    
    # submit_button = Button(top, text='Submit', command=print_answers) 
    # submit_button.grid(row=0, column=2, sticky=EW)
    # tree = Treeview(top, columns=("Name", "Age", "Country"), show="headings")

    # # กำหนดหัวตาราง
    # tree.heading("Name", text="ชื่อ")
    # tree.heading("Age", text="อายุ")
    # tree.heading("Country", text="ประเทศ")

    # # กำหนดความกว้างคอลัมน์
    # tree.column("Name", width=120)
    # tree.column("Age", width=60, anchor=CENTER)
    # tree.column("Country", width=100)

    # # เพิ่มข้อมูล
    # tree.insert("", END, values=("Alice", 25, "USA"))
    # tree.insert("", END, values=("Bob", 30, "Thailand"))
    # tree.insert("", END, values=("Charlie", 28, "Japan"))

    # # แสดง Treeview
    # tree.grid(row=1, column=0, columnspan=3, sticky=NSEW)
    

    
def order(user):
     # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    
    #menubar
    bar_home(user)
       
def stock(user):
     # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    
    #menubar
    bar_home(user)
    
def profile(user):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg='white', padx=295, pady=104)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg='white')
    top.rowconfigure((0,1,2),weight=1)
    top.columnconfigure(0,weight=1)
    top.columnconfigure(1,weight=2)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg='white')
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
    long_entry = 80
    high_entry = 4
    spacing_comp = 10
    
    # - component inside -
    #menubar
    bar_home(user)
    
    # top frame 
    Label(top,text="name : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    name_profile_entry = Entry(top,bg='#F3F3F3', textvariable = name)
    name_profile_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="username : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    username_profile_entry = Entry(top,bg='#F3F3F3', textvariable = username)
    username_profile_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=2,column=0,sticky='e')
    password_profile_label = Label(top,bg='#F3F3F3', textvariable = password, anchor=W,)
    password_profile_label.grid(row=2,column=1,sticky='w',ipadx=145 , ipady=high_entry ,padx=spacing_comp)
    
    # bot frame 
    update_btn = Button(bot,text="update profile",bg='#B12937',fg='white',font=("Inter", 16, "bold"),command=lambda: update_profile(name.get(), username.get(), user_id))
    update_btn.grid(row=0,column=0, ipadx=50, ipady=5, padx=10)
    change_password_btn = Button(bot,text="change password",bg='#B12937',fg='white',font=("Inter", 16, "bold"),command=lambda: change_password_page(user))
    change_password_btn.grid(row=0,column=1, ipadx=50, ipady=5, padx=10)

def change_password_page(user):
    
    popup = Toplevel(fm_main, bg='white')
    popup.title("Change Password")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #global veriable
    global change_password_entry, change_confirm_password_entry
    new_password = StringVar()
    confirm_password = StringVar()
    user_id = user[0]
    
    #set scale of component
    long_entry = 80
    high_entry = 4
    spacing_comp = 10
    
    # - component inside -
    
    Label(popup,text="new password : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    change_password_entry = Entry(popup,bg='#F3F3F3', textvariable = new_password)
    change_password_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="confirm password : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    change_confirm_password_entry = Entry(popup,bg='#F3F3F3', textvariable = confirm_password)
    change_confirm_password_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    change_password_btn = Button(popup,text="submit",bg='#B12937',fg='white',font=("Inter", 16, "bold"),command=lambda: change_password(new_password.get(),confirm_password.get(),user_id))
    change_password_btn.grid(row=2,columnspan=2, ipadx=50, ipady=5, padx=10)

""" BACK END """

def db_connection() :
    db_path = 'database/Be_Lune.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn,cursor

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
            sql = "select * from users where username = ? and password = ? "
            cursor.execute(sql,[username, password])   #case2
            user = cursor.fetchone()
            if user :
                messagebox.showinfo("Admin:","Login Successfully")
                print(user)
                home(user)
            else :
                messagebox.showwarning("Admin:","Username not found\n Please register before Login")
                password_login_entry.select_range(0,END)
                password_login_entry.focus_force()

def register_click(name, username, password, confirm_password) :
    if name == "" :
        messagebox.showwarning("Admin: ","Please enter name")
        name_register_entry.focus_force()
    elif username == "" :
        messagebox.showwarning("Admin: ","Please enter username")
        username_register_entry.focus_force()
    elif password == "" :
        messagebox.showwarning("Admin: ","Please enter password")
        password_register_entry.focus_force()    
    elif confirm_password == "" :
        messagebox.showwarning("Admin: ","Please enter confirm password")
        confirm_password_register_entry.focus_force()
    else : 
        result = check_user(username)

        if result :
            messagebox.showerror("Admin:","The username is already exists")
        else :
            if password == confirm_password: #verify a new password and confirm password are equal
                # เพิ่มข้อมูลลงในตาราง
                sql = ''' insert into users (username, password, name) values ( ?, ?, ?) '''
                cursor.execute(sql, [username, password, name])
                conn.commit()
                messagebox.showinfo("Admin:","Registration Successfully")  
                login()              
            else :  #verify a new pwd and confirm pwd are not equal
                messagebox.showwarning("Admin: ","Please make sure both password fields match exactly")

#ตรวจสอบว่ามีข้อมูล username นี้อยู่ในตารางมั้ย
def check_user(username):
    sql = "select * from users where username = ?"
    cursor.execute(sql, [username])
    profile = cursor.fetchone()    
    return profile

def update_profile(name, username, user_id):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name")
        name_profile_entry.focus_force() 
    else :
        if username == "" :
            messagebox.showwarning("Admin:","Please enter username")
            username_profile_entry.focus_force()  
        else :
            #เรียกหาข้อมูลเก่าของผู้ใช้งาน
            sql = "select * from users where user_id = ?"
            cursor.execute(sql,[user_id])
            old_username = cursor.fetchone()
            #ตรวจข้อมูลชื่อผู้ใช้ ใหม่ว่าเหมือนกับข้อมูลผู้ใช้คนอื่นมั้ย
            sql = "select * from users where username = ?"
            cursor.execute(sql,[username])
            new_username = cursor.fetchone()
            if new_username :
                #ตรวจสอบว่าซ้ำกันจริง โดยแบ่งเป็นซ้ำกันตัวอื่นหรีอซ้ำกับตัวมันเอง
                if new_username == old_username :   
                    #หากซ้ำกับตัวมันเอง ให้ทำการ update name ได้
                    sql = 'update users set name = ? where user_id = ?'
                    cursor.execute(sql, (name, user_id))
                    conn.commit()
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Update Profile", "Updated profile successfully.")
                        user = retrieve_profile(user_id)
                        profile(user)
                    else:
                        messagebox.showwarning("Update Profile", "No data changes.")
                else :
                    messagebox.showwarning("Admin:","The username already exists in the system. Please enter a new username")
                    username_profile_entry.focus_force() 
            else :
                #ทำการ update username และ name
                sql = 'update users set username = ?, name = ? where user_id = ?'
                cursor.execute(sql, (username, name, user_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Update Profile", "Updated profile successfully.")
                    user = retrieve_profile(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")
                    
def retrieve_profile(user_id):
    sql = "select * from users where user_id = ?"
    cursor.execute(sql, [user_id])
    user = cursor.fetchone()
    return user

def change_password(new_password, confirm_password, user_id):
    if new_password == "" :
        messagebox.showwarning("Admin:","Please enter new password")
        change_password_entry.focus_force() 
    else :
        if confirm_password == "" :
            messagebox.showwarning("Admin:","Please enter confirm password")
            change_confirm_password_entry.focus_force()  
        else :
            if new_password == confirm_password :
                sql = 'update users set password = ? where user_id = ?'
                cursor.execute(sql, (new_password, user_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Update Profile", "Updated new password successfully.")
                    user = retrieve_profile(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")
            else :
                messagebox.showwarning("Admin:","Your new password and confirmation do not match. Kindly confirm your password again")
                change_confirm_password_entry.focus_force() 

# --------------------------------------------------------------------------------------------------------
# global variable

root = create_window()
fm_main = create_layout(root)
conn,cursor = db_connection()

# - Spy -

# - img -
logo = PhotoImage(file="img/logo_full.png").subsample(4,4)


# admin run
sql = "select * from users where user_id = 1"
cursor.execute(sql)
user = cursor.fetchone()    


# - RUN -


profile(user)

root.mainloop()