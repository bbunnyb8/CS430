from tkinter import *
import sqlite3
from tkinter import messagebox, Menu
from tkinter.ttk import Treeview
from connect import *
from config import *

""" FRONT END """
def create_window():
    root = Tk()
    root.title("POS : Be Lune")
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
        
# Register page
def register():
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white, padx=295, pady=104)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,2), weight=1)
    fm.grid_rowconfigure(1, weight=4)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg=cl_white)
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    mid = Frame(fm,bg=cl_white)
    mid.rowconfigure((0,1,2,3),weight=1)
    mid.columnconfigure(0,weight=1)
    mid.columnconfigure(1,weight=3)
    mid.grid(row=1,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg=cl_white)
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
    
    
    # - component inside -
    #menubar
    bar_login()
    
    # top frame 
    Label(top,image=logo_img,bg=cl_white).grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_register_entry = Entry(mid,bg=cl_white_gray, textvariable = name_regis)
    name_register_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="username : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    username_register_entry = Entry(mid,bg=cl_white_gray, textvariable = username_regis)
    username_register_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    password_register_entry= Entry(mid,bg=cl_white_gray,show='*', textvariable = password_regis)
    password_register_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(mid,text="confirm password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=3,column=0,sticky='e')
    confirm_password_register_entry = Entry(mid,bg=cl_white_gray,show='*', textvariable = confirm_password_regis)
    confirm_password_register_entry.grid(row=3,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)

    # bot frame 
    button_register = Button(bot,text="register",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: register_click(name_regis.get(), username_regis.get(), password_regis.get(), confirm_password_regis.get()))
    button_register.grid(row=0,column=0, ipadx=50, ipady=5)

def home(user):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=4)
    fm.grid_columnconfigure(0, weight=4)
    fm.grid_columnconfigure(1, weight=3)
    
    """
    layout ส่วนแสดงสินค้า มี 2 ส่วน ส่วนแรกเป็นชื่อหน้าต่างที่กำลังทำงานอยู่ และปุ่มค้นหา 
    ส่วนที่สอง เป็นตารางแสดงรายการสินค้า
    """
    fm_show_product = Frame(fm, bg=cl_white)
    fm_show_product.grid(row=0, column=0, sticky=NSEW)
    fm_show_product.grid_rowconfigure(0, weight=1)
    fm_show_product.grid_rowconfigure(1, weight=10)
    fm_show_product.grid_columnconfigure((0,1), weight=1)
    
    #layout รายการที่เลือก
    fm_select_product = Frame(fm, bg="red")
    fm_select_product.grid(row=0, column=1, sticky=NSEW)
    
    #veriable
     
    # name_regis = StringVar()
    # username_regis = StringVar()
    # password_regis = StringVar()
    # confirm_password_regis = StringVar()
    
    #set scale of component
    columns = ("id", "name", "price", "amount")
    
    # frame inside
    #menubar
    bar_home(user)
    
    #head name page
    Label(fm_show_product,text="Home",bg=cl_white,fg='black',font=font_h3_bold).grid(row=0,column=0,sticky=W,padx=spacing_comp)
    
    #search frame
    search_home_entry = Entry(fm_show_product,bg=cl_white,fg='black',font=font_h5)
    search_home_entry.grid(row=0,column=1, ipadx=long_entry,ipady=high_entry ,padx=spacing_comp, sticky=E) #Spy Gb
    search_button = Button(fm_show_product,image=search_icon)
    search_button.grid(row=0, column=1,padx=spacing_comp, sticky=E)
    
    product = retrieve_product(user[0])

    # table product
    tree = Treeview(fm_show_product, columns=columns, show="headings")

    # กำหนดหัวตาราง
    for col in columns:
        tree.heading(col, text=col)
    # กำหนดความกว้างคอลัมน์
    for col in columns:
        tree.column(col, width=50, anchor=W)
    # เพิ่มข้อมูล
    for row in product:
        tree.insert("", END, value=row)
    
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="add cart")
    #ผูกการคลิกขวากับ show_context_menu
    tree.bind("<Button-3>", lambda event: show_context_menu(event, tree, context_menu))
    # # แสดง Treeview
    tree.grid(row=1, columnspan=2, padx=spacing_comp, sticky=NSEW)
    

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
        tree_order.heading(col, text=col)
        tree_order.column(col, width=50, anchor=W)
    
    # เพิ่มข้อมูล
    for row in order:
        tree_order.insert("", END, value=row)
    
    # context_menu = Menu(root, tearoff=0)
    # context_menu.add_command(label="edit", command=lambda: edit_product_page(tree_order))
    # context_menu.add_command(label="delete", command=lambda: delete_product(tree_order))
    
    #ผูกการคลิกขวากับ show_context_menu
    # tree_order.bind("<Button-3>", lambda event: show_context_menu(event, tree_order, context_menu))
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
    context_menu.add_command(label="edit", command=lambda: edit_product_page(tree_stock))
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
    
def edit_product_page(tree):
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
                        user = retrieve_user(user_id)
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
                    user = retrieve_user(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")               
def retrieve_user(user_id):
    sql = "select * from users where user_id = ?"
    cursor.execute(sql, [user_id])
    user = cursor.fetchone()
    conn.close
    return user
def retrieve_product(user_id):
    sql = "select * from products where user_id = ?"
    cursor.execute(sql, [user_id])
    product = cursor.fetchall()
    conn.close
    return product
def retrieve_order(user_id):
    sql = "select * from orders where user_id = ?"
    cursor.execute(sql, [user_id])
    order = cursor.fetchall()
    conn.close
    return order

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
                    user = retrieve_user(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")
            else :
                messagebox.showwarning("Admin:","Your new password and confirmation do not match. Kindly confirm your password again")
                change_confirm_password_entry.focus_force() 
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
        
# --------------------------------------------------------------------------------------------------------
root = create_window()
fm_main = create_layout(root)
conn,cursor = db_connection()

# - Spy -


# - img -
logo_img = PhotoImage(file="img/logo_full.png").subsample(4,4)
add_cart_icon = PhotoImage(file="img/add_cart.png")
add_item_icon = PhotoImage(file="img/add_item.png")
delete_icon = PhotoImage(file="img/delete.png")
edit_icon = PhotoImage(file="img/edit.png")
search_icon = PhotoImage(file="img/search.png")


# admin run
sql = "select * from users where user_id = 1"
cursor.execute(sql)
user = cursor.fetchone()   


# - RUN -

stock(user)

root.mainloop()
