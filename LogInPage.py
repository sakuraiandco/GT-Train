from tkinter import *
import urllib.request
import base64
from tkinter import messagebox

class GUI:

    def __init__(self,rootWin):
        #creates window
        self.rootWin = rootWin
        self.rootWin.title('Login')
        #self.rootWin.config(bg="grey")

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
        l = Label(self.rootWin,text="Login",font=("Calibri",15,"bold"),fg="gold")
        l.grid(row=1,column=0,columnspan=2)

        #creates button frame
        self.frame = Frame(self.rootWin)
        self.frame.grid(row=4,column=1,sticky=E)

        #creates Register button
        register = Button(self.frame,text="Register",command=self.toRegister)
        register.pack(side=RIGHT)

        #creates Login button
        login = Button(self.frame,text="Login",command=self.chooseFunc)#,command=self.toLogin)
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
##            self.chooseFunc
##        
##        except:
##            r = messagebox.showerror("Error!","An invalid username or password has been entered.")


###### REGISTER #######

    def toRegister(self):
        self.rootWin2 = Toplevel()
        self.rootWin.withdraw()
        self.rootWin2.title("Register")

        pic = Label(self.rootWin2,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        n = Label(self.rootWin2,text="New User Registration",font=("Calibri",15,"bold"),fg="gold")
        n.grid(row=1,column=0,columnspan=2)

        u = Label(self.rootWin2,text="Username:")
        u.grid(row=2,column=0,sticky=E)

        self.usv = StringVar()
        self.uE = Entry(self.rootWin2,textvariable=self.usv,width=30)
        self.uE.grid(row=2,column=1,padx=5)

        e = Label(self.rootWin2,text="Email Address:")
        e.grid(row=3,column=0,sticky=E)

        self.esv = StringVar()
        self.eE = Entry(self.rootWin2,textvariable=self.esv,width=30)
        self.eE.grid(row=3,column=1,padx=5)

        p = Label(self.rootWin2,text="Password:")
        p.grid(row=4,column=0,sticky=E)

        self.psv = StringVar()
        self.pE = Entry(self.rootWin2,textvariable=self.psv,width=30)
        self.pE.grid(row=4,column=1,padx=5)

        cp = Label(self.rootWin2,text="Confirm Password:")
        cp.grid(row=5,column=0,sticky=E)

        self.cpsv = StringVar()
        self.cpE = Entry(self.rootWin2,textvariable=self.cpsv,width=30)
        self.cpE.grid(row=5,column=1,padx=5)

        self.frame2 = Frame(self.rootWin2)
        self.frame2.grid(row=6,column=1,sticky=E)
        
        create = Button(self.frame2,text="Create",command=self.checkReg)
        create.pack()

    def checkReg(self):
##        self.connect()

        username = self.uE.get()
        email = self.eE.get()
        password = self.pE.get()
        confirm = self.cpE.get()
        if username == "" or email == "" or password == "" or confirm == "":
            r = messagebox.showerror("Error!","One or more fields has been left blank.")

##        check if username is avilable
##        else:
##            r = messagebox.showerror("Error!","The entered username is unavailable.")
##
        if password != confirm:
            r = messagebox.showerror("Error!","The entered passwords do not match.")
##
##        check if email address is valid and unique
##            self.next function
##        else:
##            r = messagebox.showerror("Error!","An invalid email address has been entered.")




###### CHOOSE FUNCTION SCREEN #######

    def chooseFunc(self):
        self.rootWin3 = Toplevel()
        self.rootWin3.title("Menu")
        try:
            self.rootWin2.withdraw()
        except:
            self.rootWin.withdraw()

        pic = Label(self.rootWin3,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        c = Label(self.rootWin3,text="Choose Functionality",font=("Calibri",15,"bold"),fg="gold")
        c.grid(row=1,column=0,columnspan=2,pady=5)

        view = Button(self.rootWin3,text="View Train Schedule",fg="blue",command=self.typeTrainNum)
        view.grid(row=2,column=0,columnspan=2,pady=5)
        
        make = Button(self.rootWin3,text="Make a new reservation",fg="blue")
        make.grid(row=3,column=0,columnspan=2,pady=5)

        update = Button(self.rootWin3,text="Update a reservation",fg="blue")
        update.grid(row=4,column=0,columnspan=2,pady=5)

        cancel = Button(self.rootWin3,text="Cancel a reservation",fg="blue")
        cancel.grid(row=5,column=0,columnspan=2,pady=5)

        review = Button(self.rootWin3,text="Give review",fg="blue")
        review.grid(row=6,column=0,columnspan=2,pady=5)

        school = Button(self.rootWin3,text="Add school information (student discount)",fg="blue",command=self.addSchool)
        school.grid(row=7,column=0,columnspan=2,pady=5)

        logout = Button(self.rootWin3,text="Log out",command=self.logout)
        logout.grid(row=8,column=1,padx=5,pady=5,sticky=E)

    def logout(self):
        self.rootWin3.withdraw()
        self.rootWin.deiconify()



##### ADD SCHOOL INFO#######

    def addSchool(self):
        self.rootWin4 = Toplevel()
        self.rootWin4.title("Add School Information")
        self.rootWin3.withdraw()

        pic = Label(self.rootWin4,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        a = Label(self.rootWin4,text="Add School Info",font=("Calibri",15,"bold"),fg="gold")
        a.grid(row=1,column=0,columnspan=2,pady=5)

        school = Label(self.rootWin4,text="School Email Address:")
        school.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.sesv = StringVar()
        self.seE = Entry(self.rootWin4,textvariable=self.sesv,width=30)
        self.seE.grid(row=2,column=1,padx=5,pady=5)

        small = Label(self.rootWin4,text="Your school email address ends with .edu",font=("Calibri",8))
        small.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        back = Button(self.rootWin4,text="Back",command=self.backSchool)
        back.grid(row=4,column=0,padx=10,pady=15,sticky=W)

        submit = Button(self.rootWin4,text="Submit",command=self.submitSchool)
        submit.grid(row=4,column=1,padx=10,pady=15,sticky=E)

    def backSchool(self):
        self.rootWin4.withdraw()
        self.rootWin3.deiconify()

    def submitSchool(self):
        schoolEmail = self.seE.get()
        
        if schoolEmail.endswith(".edu") == True:
            print("True")
            #add student to customer in database
            self.rootWin4.withdraw()
            self.rootWin3.deiconify()
        else:
            r = messagebox.showerror("Error!","This is not a valid school email address.")



###### VIEW TRAIN SCHEDULE ########

    def typeTrainNum(self):
        self.rootWin5 = Toplevel()
        self.rootWin5.title("View Train Schedule")
        self.rootWin3.withdraw()

        pic = Label(self.rootWin5,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWin5,text="View Train Schedule",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        tNum = Label(self.rootWin5,text="Train Number:")
        tNum.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.tNsv = StringVar()
        self.tNE = Entry(self.rootWin5,textvariable=self.tNsv,width=20)
        self.tNE.grid(row=2,column=1,padx=5,pady=5)

        search = Button(self.rootWin5,text="Search")
        search.grid(row=3,column=0,columnspan=2,pady=10)

        
win = Tk()
app = GUI(win)
win.mainloop()

