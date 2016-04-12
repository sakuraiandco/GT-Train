from tkinter import *
import urllib.request
import base64
from tkinter import messagebox

class GUI:

    def __init__(self,rootWin):
        #creates window
        self.rootWin = rootWin
        self.rootWin.title('Login')

        #Username label
        u = Label(self.rootWin,text='Username:')
        u.grid(row=2,column=0,sticky=E)

        #makes variable of username input
        self.usv = StringVar()
        self.uEntry = Entry(self.rootWin,textvariable=self.usv,width=30)
        self.uEntry.grid(row=2,column=1,padx=5)

        #Password label
        p = Label(self.rootWin,text="Password:")
        p.grid(row=3,column=0,sticky=E)

        #makes variable of password input
        self.psv = StringVar()
        self.pEntry = Entry(self.rootWin,textvariable=self.psv,width=30)
        self.pEntry.grid(row=3,column=1,padx=5)

        #add GT logo
        self.response = urllib.request.urlopen("http://www.cc.gatech.edu/classes/AY2015/cs2316_fall/codesamples/techlogo.gif")
        self.html = self.response.read()
        self.response.close()

        b64_data = base64.encodebytes(self.html)
        self.image = PhotoImage(data=b64_data)

        pic = Label(self.rootWin,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5)
        
        #Login label
        l = Label(self.rootWin,text="Login",font=("Calibri",15))
        l.grid(row=1,column=0,columnspan=2)

        #creates button frame
        self.frame = Frame(self.rootWin)
        self.frame.grid(row=4,column=1,sticky=E)

        #creates Register button
        register = Button(self.frame,text="Register",command=self.toRegister)
        register.pack(side=RIGHT)

        #creates Login button
        login = Button(self.frame,text="Login")#,command=self.toLogin)
        login.pack(side=RIGHT)

##    def connect(self):
##        db = pymysql.connect(host="academic-mysql.cc.gatech.edu",
##                             user="yposhedly3",
##                             passwd="A8KvQybO",
##                             db="cs2316db")
##        return(db)

        
##    def toLogin(self):
##        self.connect()
##
##        try:
##            check login info
##            self.next function
##        
##        except:
##            r = messagebox.showerror("Error!","An invalid username or password has been entered.")

    def toRegister(self):
        self.rootWin2 = Toplevel()
        self.rootWin.withdraw()
        self.rootWin2.title("Register")

        pic2 = Label(self.rootWin2,image=self.image)
        pic2.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        u = Label(self.rootWin2,text="Username:")
        u.grid(row=1,column=0,sticky=E)

        self.usv = StringVar()
        self.uE = Entry(self.rootWin2,textvariable=self.usv,width=30)
        self.uE.grid(row=1,column=1,padx=5)

        e = Label(self.rootWin2,text="Email Address:")
        e.grid(row=2,column=0,sticky=E)

        self.esv = StringVar()
        self.eE = Entry(self.rootWin2,textvariable=self.esv,width=30)
        self.eE.grid(row=2,column=1,padx=5)

        p = Label(self.rootWin2,text="Password:")
        p.grid(row=3,column=0,sticky=E)

        self.psv = StringVar()
        self.pE = Entry(self.rootWin2,textvariable=self.psv,width=30)
        self.pE.grid(row=3,column=1,padx=5)

        cp = Label(self.rootWin2,text="Confirm Password:")
        cp.grid(row=4,column=0,sticky=E)

        self.cpsv = StringVar()
        self.cpE = Entry(self.rootWin2,textvariable=self.cpsv,width=30)
        self.cpE.grid(row=4,column=1,padx=5)

        self.frame2 = Frame(self.rootWin2)
        self.frame2.grid(row=5,column=1,sticky=E)
        
        register = Button(self.frame2,text="Create")#,command=self.toRegister)
        register.pack()

##    def toRegister(self):
##        self.connect()
##
##        try:
##            check if username is avilable
##        except:
##            r = messagebox.showerror("Error!","The entered username is unavailable.")
##
##        try:
##            check if passwords are the same
##        except:
##            r = messagebox.showerror("Error!","The entered passwords do not match.")
##
##        try:
##            check if email address is valid
##            self.next function
##        except:
##            r = messagebox.showerror("Error!","An invalid email address has been entered.")



        
win = Tk()
app = GUI(win)
win.mainloop()

