from tkinter import *

# front-end
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

def bar_home():
    menu_bar = Menu(root, tearoff=0)
    menu_bar.add_command(label='Be Lune') 
    menu_bar.add_command(label='home', command=home) 
    menu_bar.add_command(label='order', command=order)
    menu_bar.add_command(label='stock', command=stock)
    menu_bar.add_command(label='profile', command=profile)
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
    
    # - object inside -
    #menubar
    bar_login()
    
    """ ยังไม่ได้มีการผูก spy และฟังก์ชั่นตรวจสอบเข้าสู่ระบบ """
    
    # top frame 
    Label(top,image=logo,bg='white').grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="username : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35).grid(row=0,column=1,sticky='w',ipady=4,padx=10)
    
    Label(mid,text="password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35,show='*').grid(row=1,column=1,sticky='w',ipady=4,padx=10)

    # bot frame 
    Button(bot,text="login",width=12,height=2,bg='#B12937',fg='white',font=("Inter", 16, "bold")).grid(row=0,column=0)
        
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
    
    # - object inside -
    #menubar
    bar_login()
    
    """ ยังไม่ได้มีการผูก spy และฟังก์ชั่นลงทะเบียน """
    
    # top frame 
    Label(top,image=logo,bg='white').grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="name : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=0,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35).grid(row=0,column=1,sticky='w',ipady=4,padx=10)
    
    Label(mid,text="username : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=1,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35).grid(row=1,column=1,sticky='w',ipady=4,padx=10)
    
    Label(mid,text="password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=2,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35,show='*').grid(row=2,column=1,sticky='w',ipady=4,padx=10)
    
    Label(mid,text="confirm password  : ",bg='white',fg='#858585',font=("Inter", 12)).grid(row=3,column=0,sticky='e')
    Entry(mid,bg='#F3F3F3',width=35,show='*').grid(row=3,column=1,sticky='w',ipady=4,padx=10)

    # bot frame 
    Button(bot,text="register",width=12,height=2,bg='#B12937',fg='white',font=("Inter", 16, "bold")).grid(row=0,column=0)

def home():
    bar_home()
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure(0, weight=1)
def order():
    bar_home()
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure(0, weight=1)    
def stock():
    bar_home()
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure(0, weight=1)
def profile():
    bar_home()
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure(0, weight=1)
# back-end




# --------------------------------------------------------------------------------------------------------
# main

root = create_window()
fm_main = create_layout(root)

# - img -
logo = PhotoImage(file="img/logo_full.png").subsample(4,4)

# - Spy -


# - RUN -

home()

root.mainloop()