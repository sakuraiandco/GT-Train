from tkinter import *
import urllib.request
import base64
from tkinter import messagebox
import datetime

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
        login = Button(self.frame,text="Login",command=self.chooseCFunc)#,command=self.toLogin)
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
##        if customer:
##            self.chooseCFunc
##        if manager:
#            self.chooseMFunc
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




###### CHOOSE CUSTOMER FUNCTION SCREEN #######

    def chooseCFunc(self):
        self.rootWinCF = Toplevel()
        self.rootWinCF.title("Menu")
        try:
            self.rootWin2.withdraw()
        except:
            self.rootWin.withdraw()

        pic = Label(self.rootWinCF,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        c = Label(self.rootWinCF,text="Choose Functionality",font=("Calibri",15,"bold"),fg="gold")
        c.grid(row=1,column=0,columnspan=2,pady=5)

        view = Button(self.rootWinCF,text="View Train Schedule",fg="blue",command=self.typeTrainNum)
        view.grid(row=2,column=0,columnspan=2,pady=5)
        
        make = Button(self.rootWinCF,text="Make a new reservation",fg="blue")
        make.grid(row=3,column=0,columnspan=2,pady=5)

        update = Button(self.rootWinCF,text="Update a reservation",fg="blue")
        update.grid(row=4,column=0,columnspan=2,pady=5)

        cancel = Button(self.rootWinCF,text="Cancel a reservation",fg="blue",command=self.cancelReservation)
        cancel.grid(row=5,column=0,columnspan=2,pady=5)

        giveR = Button(self.rootWinCF,text="Give review",fg="blue",command=self.giveReview)
        giveR.grid(row=6,column=0,columnspan=2,pady=5)

        viewR = Button(self.rootWinCF,text="View review",fg="blue",command=self.viewReview)
        viewR.grid(row=7,column=0,columnspan=2,pady=5)

        school = Button(self.rootWinCF,text="Add school information (student discount)",fg="blue",command=self.addSchool)
        school.grid(row=8,column=0,columnspan=2,pady=5)

        logout = Button(self.rootWinCF,text="Log out",command=self.logout)
        logout.grid(row=9,column=1,padx=5,pady=5,sticky=E)

    def logout(self):
        try:
            self.rootWinCF.destroy()
        except:
            self.rootWinMF.destroy()
        self.rootWin.deiconify()


###### VIEW TRAIN SCHEDULE ########

    def typeTrainNum(self):
        self.rootWin5 = Toplevel()
        self.rootWin5.title("View Train Schedule")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWin5,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWin5,text="View Train Schedule",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        tNum = Label(self.rootWin5,text="Train Number:")
        tNum.grid(row=2,column=0,padx=5,pady=5)

        self.tNsv = StringVar()
        self.tNE = Entry(self.rootWin5,textvariable=self.tNsv,width=20)
        self.tNE.grid(row=2,column=1,padx=5,pady=5)

        search = Button(self.rootWin5,text="Search")
        search.grid(row=3,column=0,columnspan=2,pady=10)

####### CANCEL RESERVATION ######

    def cancelReservation(self):
        self.rootWinCR = Toplevel()
        self.rootWinCR.title("Cancel Reservation")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinCR,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinCR,text="Cancel Reservation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        rNum = Label(self.rootWinCR,text="Reservation ID")
        rNum.grid(row=2,column=0,padx=5,pady=5)

        self.rIDsv = StringVar()
        self.rIDE = Entry(self.rootWinCR,textvariable=self.rIDsv,width=15)
        self.rIDE.grid(row=2,column=1,padx=5,pady=5)

        back = Button(self.rootWinCR,text="Back",command=self.backCancel)
        back.grid(row=3,column=0,padx=10,pady=15,sticky=W)

        search = Button(self.rootWinCR,text="Search",command=self.cancel)
        search.grid(row=3,column=1,padx=10,pady=15,sticky=E)

    def backCancel(self):
        self.rootWinCR.destroy()
        self.rootWinCF.deiconify()

    def cancel(self):
        rID = self.rIDE.get()
        if rID == "":
            r = messagebox.showerror("Error!","Please enter a reservation ID.")

        else:
        #check for reservation ID in database and that it has not already been cancelled

            self.rootWinC = Toplevel()
            self.rootWinC.title("Cancel Reservation")
            self.rootWinCR.withdraw()

            pic = Label(self.rootWinC,image=self.image)
            pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

            v = Label(self.rootWinC,text="Cancel Reservation",font=("Calibri",15,"bold"),fg="gold")
            v.grid(row=1,column=0,columnspan=2,pady=5)

        ## table with reservations listed ##

        #total cost of reservation

            c = Label(self.rootWinC,text="Total Cost of Reservation")
            c.grid(row=3,column=0,padx=5,pady=5,sticky=W)

            #cost = (from database)
            self.costRiv = IntVar()
            #self.costRsv.set(cost)
            self.costRE = Entry(self.rootWinC,textvariable=self.costRiv,width=15)
            self.costRE.grid(row=3,column=1,padx=5,pady=5)
            
        #date of cancellation
            
            d = Label(self.rootWinC,text="Date of Cancellation")
            d.grid(row=4,column=0,padx=5,pady=5,sticky=W)

            self.datesv = StringVar()
            self.datesv.set(datetime.date.today())
            self.dateE = Entry(self.rootWinC,textvariable=self.datesv,width=15)
            self.dateE.grid(row=4,column=1,padx=5,pady=5)

        #amount to be refunded
            
            amount = Label(self.rootWinC,text="Amount to be Refunded")
            amount.grid(row=5,column=0,padx=5,pady=5,sticky=W)

            #refund = (from database)
            self.rfiv = IntVar()
            #self.rfiv.set(refund)
            self.rfE = Entry(self.rootWinC,textvariable=self.rfiv,width=15)
            self.rfE.grid(row=5,column=1,padx=5,pady=5)

        #navigation buttons
            
            back = Button(self.rootWinC,text="Back",command=self.backCancel)
            back.grid(row=6,column=0,padx=10,pady=15,sticky=W)

            search = Button(self.rootWinC,text="Submit",command=self.cancel)
            search.grid(row=6,column=1,padx=10,pady=15,sticky=E)

####### GIVE REVIEW ########

    def giveReview(self):
        self.rootWinGR = Toplevel()
        self.rootWinGR.title("Give Review")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinGR,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        g = Label(self.rootWinGR,text="Give Review",font=("Calibri",15,"bold"),fg="gold")
        g.grid(row=1,column=0,columnspan=2,pady=5)

        tNum = Label(self.rootWinGR,text="Train Number")
        tNum.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.tNRsv = StringVar()
        self.tNRE = Entry(self.rootWinGR,textvariable=self.tNRsv,width=30)
        self.tNRE.grid(row=2,column=1,padx=5,pady=5)        

        r = Label(self.rootWinGR,text="Rating")
        r.grid(row=3,column=0,padx=5,pady=5,sticky=W)
    
        self.rating = StringVar()
        self.rating.set("Good")
        pulldown = OptionMenu(self.rootWinGR,self.rating,"Very Good","Good","Neutral","Bad","Very Bad")
        pulldown.grid(row=3,column=1,padx=5,pady=5,sticky=W)
        
        c = Label(self.rootWinGR,text="Comment")
        c.grid(row=4,column=0,padx=5,pady=5,sticky=W)

        self.comsv = StringVar()
        self.comE = Entry(self.rootWinGR,textvariable=self.comsv,width=30)
        self.comE.grid(row=4,column=1,padx=5,pady=5)

        submit = Button(self.rootWinGR,text="Submit",command=self.submitReview)
        submit.grid(row=5,column=1,padx=10,pady=15,sticky=E)

    def submitReview(self):
        trainNum = self.tNRE.get()
        rating = self.rating.get()
        
        if trainNum == "":
            r = messagebox.showerror("Error!","Please enter a train number.")

        #check if train number is not available in database
            #r = messagebox.showerror("Error!","This train number is unavailable.")
            
        else:
            #assign review to train number
            self.rootWinGR.destroy()
            self.rootWinCF.deiconify()
        

####### VIEW REVIEW ##########

    def viewReview(self):
        self.rootWinVR = Toplevel()
        self.rootWinVR.title("View Review")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinVR,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinVR,text="View Review",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        tNum = Label(self.rootWinVR,text="Train Number:")
        tNum.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.tNVRsv = StringVar()
        self.tNVRE = Entry(self.rootWinVR,textvariable=self.tNVRsv,width=20)
        self.tNVRE.grid(row=2,column=1,padx=5,pady=5)

        back = Button(self.rootWinVR,text="Back",command=self.backReview)
        back.grid(row=3,column=0,padx=10,pady=15,sticky=W)

        find = Button(self.rootWinVR,text="Next",command=self.reviewTable)
        find.grid(row=3,column=1,padx=10,pady=15,sticky=E)

    def backReview(self):
        self.rootWinVR.destroy()
        self.rootWinCF.deiconify()

    def reviewTable(self):
        self.rootWinRT = Toplevel()
        self.rootWinRT.title("View Review")
        self.rootWinVR.withdraw()

        pic = Label(self.rootWinRT,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinRT,text="View Review",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        back = Button(self.rootWinRT,text="Back to Choose Functionality",command=self.backReviewTable)
        back.grid(row=3,column=0,columnspan=2,padx=10,pady=15)

    def backReviewTable(self):
        self.rootWinRT.destroy()
        self.rootWinCF.deiconify()


##### ADD SCHOOL INFO #######

    def addSchool(self):
        self.rootWin4 = Toplevel()
        self.rootWin4.title("Add School Information")
        self.rootWinCF.withdraw()

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
        self.rootWin4.destroy()
        self.rootWinCF.deiconify()

    def submitSchool(self):
        schoolEmail = self.seE.get()
        
        if schoolEmail.endswith(".edu") == True:
            print("True")
            #add student to customer in database
            self.rootWin4.destroy()
            self.rootWinCF.deiconify()
        else:
            r = messagebox.showerror("Error!","This is not a valid school email address.")


####### CHOOSE MANAGER FUNCTION SCREEN ########

    def chooseMFunc(self):
        self.rootWinMF = Toplevel()
        self.rootWinMF.title("Menu")
        self.rootWin.withdraw()

        pic = Label(self.rootWinMF,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        c = Label(self.rootWinMF,text="Choose Functionality",font=("Calibri",15,"bold"),fg="gold")
        c.grid(row=1,column=0,columnspan=2,pady=5)

        rev = Button(self.rootWinMF,text="View revenue report",fg="blue",command=self.typeTrainNum)
        rev.grid(row=2,column=0,columnspan=2,pady=5)
        
        route = Button(self.rootWinMF,text="View popular route report",fg="blue")
        route.grid(row=3,column=0,columnspan=2,pady=5)

        logout = Button(self.rootWinMF,text="Log out",command=self.logout)
        logout.grid(row=4,column=1,padx=5,pady=10,sticky=E)

        
win = Tk()
app = GUI(win)
win.mainloop()

