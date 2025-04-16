from tkinter import *

def create_window():
    root = Tk()
    root.title("POS : Be Lune")
    root.geometry("1194x834")
    root.configure(bg="white")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    return root
def create_layout(root):
    fm_main = Frame(root)
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
    # menu_bar.add_command(label='Menu', command=create_menu) 
    # menu_bar.add_command(label='Checkout', command=create_checkout)
    menu_bar.add_command(label='logout', command=login) 
    
    root.configure(menu=menu_bar)
    
#login page   
def login():
    bar_login()
    
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    
    userinfo = StringVar()
    pwdinfo = StringVar()
    
    Label(fm,image=logo,bg='white').grid(row=0,columnspan=2,sticky='ews')
    
    Label(fm,text="username : ",bg='white',fg='#858585').grid(row=1,column=0,sticky='e')
    Entry(fm,bg='#F3F3F3',width=40,textvariable=userinfo).grid(row=1,column=1,sticky='w',ipady=4)
    
    Label(fm,text="password  : ",bg='white',fg='#858585').grid(row=1,column=0,sticky='es')
    Entry(fm,bg='#F3F3F3',width=40,show='*',textvariable=pwdinfo).grid(row=1,column=1,sticky='ws',ipady=4)

    Button(fm,text="Login",width=20,height=2,bg='#B12937',fg='white').grid(row=2,columnspan=2)
        
        
        

#register page
def register():
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2,3,4), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    
    userinfo = StringVar()
    pwdinfo = StringVar()
    
    Label(fm,image=logo,bg='white').grid(row=0,columnspan=2,sticky='ews')
    
    Label(fm,text="username : ",bg='white',fg='#858585').grid(row=1,column=0,sticky='e')
    Entry(fm,bg='#F3F3F3',width=40,textvariable=userinfo).grid(row=1,column=1,sticky='w',ipady=4)
    
    Label(fm,text="password  : ",bg='white',fg='#858585').grid(row=2,column=0,sticky='e')
    Entry(fm,bg='#F3F3F3',width=40,show='*',textvariable=pwdinfo).grid(row=2,column=1,sticky='w',ipady=4)
    
    Label(fm,text="confirm password  : ",bg='white',fg='#858585').grid(row=3,column=0,sticky='e')
    Entry(fm,bg='#F3F3F3',width=40,show='*',textvariable=pwdinfo).grid(row=3,column=1,sticky='w',ipady=4)

    Button(fm,text="Register",width=20,height=2,bg='#B12937',fg='white').grid(row=4,columnspan=2)

def home():
    bar_home()
    fm = Frame(fm_main, bg='white', padx=20, pady=10)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure(0, weight=1)
    
        




# -------------------------------------------------------------------------
root = create_window()
fm_main = create_layout(root)

#img
logo = PhotoImage(file="img/logo.png").subsample(5,5)

#spy


# RUN
login()

root.mainloop()