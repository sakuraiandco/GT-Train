from tkinter import *
import urllib.request
import base64
from tkinter import messagebox
import datetime
import pymysql

class GUI:

    def __init__(self,rootWin):
        #creates window
        self.rootWin = rootWin
        self.rootWin.title('Login')

        #Username label
        Label(self.rootWin,text='Username:').grid(row=2,column=0,sticky=E)

        #makes variable of username input
        self.usv = StringVar()
        self.uEntry = Entry(self.rootWin,textvariable=self.usv,width=30)
        self.uEntry.grid(row=2,column=1,padx=5)

        #Password label
        Label(self.rootWin,text="Password:").grid(row=3,column=0,sticky=E)

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

        Label(self.rootWin,image=self.image).grid(row=0,column=0,columnspan=2,padx=5,pady=5)
        
        #Login label
        Label(self.rootWin,text="Login",font=("Calibri",15,"bold"),fg="gold").grid(row=1,column=0,columnspan=2)

        #creates button frame
        self.frame = Frame(self.rootWin)
        self.frame.grid(row=4,column=1,padx=2,sticky=E)

        #creates Register button
        Button(self.frame,text="Register",command=self.toRegister).pack(side=RIGHT,padx=2,pady=5)

        #creates Login button
        login = Button(self.frame,text="Login",command=self.toLogin)
        login.pack(side=RIGHT,padx=2,pady=5)

        self.chosenTrains = []
        self.departDates = []
        self.departures = []
        self.arrivals = []
        self.classes = []
        self.prices = []
        self.allBags = []
        self.passengers = []

    def connect(self):
        db = pymysql.connect(host="academic-mysql.cc.gatech.edu",
                             user="cs4400_Team_62",
                             passwd="ZocPpqSS",
                             db="cs4400_Team_62")
        return(db)

        
    def toLogin(self):
        db = self.connect()
        cursor = db.cursor()
        username = self.uEntry.get()
        password = self.pEntry.get()

        #check that fields are filled
        if username == "":
            r = messagebox.showerror("Error!","Please enter a username.")
        elif password == "":
            r = messagebox.showerror("Error!","Please enter a password.")
        else:
            #check if username/password combination is a user
            sql = "SELECT * FROM User WHERE Username='"+username+"' AND Password='"+password+"'"
            cursor.execute(sql)
            results = cursor.fetchall()

            #check if user is a customer or manager
            if len(results) > 0:
                sql2 = "SELECT * FROM Customer WHERE Username='"+username+"'"
                cursor.execute(sql2)
                results2 = cursor.fetchall()
                if len(results2) > 0:
                    self.chooseCFunc()
                else:
                    self.chooseMFunc()
            else:
                r = messagebox.showerror("Error!","This is an invalid username/password combination.")

        cursor.close()
        db.commit()
        db.close()


###### REGISTER #######

    def toRegister(self):
        self.rootWin2 = Toplevel()
        self.rootWin.withdraw()
        self.rootWin2.title("Register")

        Label(self.rootWin2,image=self.image).grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)
        Label(self.rootWin2,text="New User Registration",font=("Calibri",15,"bold"),fg="gold").grid(row=1,column=0,columnspan=2,pady=5)
        Label(self.rootWin2,text="Username:").grid(row=2,column=0,sticky=E)

        self.usv = StringVar()
        self.uEntry = Entry(self.rootWin2,textvariable=self.usv,width=30)
        self.uEntry.grid(row=2,column=1,padx=5)

        Label(self.rootWin2,text="Email Address:").grid(row=3,column=0,sticky=E)

        self.esv = StringVar()
        self.eE = Entry(self.rootWin2,textvariable=self.esv,width=30)
        self.eE.grid(row=3,column=1,padx=5)

        Label(self.rootWin2,text="Password:").grid(row=4,column=0,sticky=E)

        self.psv = StringVar()
        self.pE = Entry(self.rootWin2,textvariable=self.psv,width=30)
        self.pE.grid(row=4,column=1,padx=5)

        Label(self.rootWin2,text="Confirm Password:").grid(row=5,column=0,sticky=E)

        self.cpsv = StringVar()
        self.cpE = Entry(self.rootWin2,textvariable=self.cpsv,width=30)
        self.cpE.grid(row=5,column=1,padx=5)

        Button(self.rootWin2,text="Back",command=self.backLogin).grid(row=6,column=0,padx=5,pady=5,sticky=W)
        Button(self.rootWin2,text="Create",command=self.checkReg).grid(row=6,column=1,padx=5,pady=5,sticky=E)

    def backLogin(self):
        self.rootWin2.withdraw()
        self.rootWin.deiconify()

    def checkReg(self):
        db = self.connect()
        cursor = db.cursor()

        username = self.uEntry.get()
        email = self.eE.get()
        password = self.pE.get()
        confirm = self.cpE.get()
        
        #check that all fields are filled
        if username == "" or email == "" or password == "" or confirm == "":
            r = messagebox.showerror("Error!","One or more fields has been left blank.")
        else:
            #check for username in database
            sql = "SELECT * FROM User WHERE Username='"+username+"'"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) > 0:
                r = messagebox.showerror("Error!","The entered username is unavailable.")
            else:
                #check if password and confirm password match
                if password != confirm:
                    r = messagebox.showerror("Error!","The entered passwords do not match.")
                else:
                    #check for email in database since needs to be unique
                    sql2 = "SELECT * FROM Customer WHERE Email='"+email+"'"
                    cursor.execute(sql2)
                    results2 = cursor.fetchall()
                    if len(results2) > 0:
                        r = messagebox.showerror("Error!","An invalid email address has been entered.")
                    else:
                        #input new customer info in database
                        sql3 = "INSERT INTO User VALUES ('"+username+"','"+password+"')"
                        sql4 = "INSERT INTO Customer VALUES ((SELECT Username FROM User WHERE Username = "+username+"),0,"+email+")"
                        cursor.execute(sql3)
                        cursor.execute(sql4)
                        cursor.close()
                        db.commit()
                        db.close()
                        self.chooseCFunc()


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
        
        make = Button(self.rootWinCF,text="Make a new reservation",fg="blue",command=self.searchTrain)
        make.grid(row=3,column=0,columnspan=2,pady=5)

        update = Button(self.rootWinCF,text="Update a reservation",fg="blue",command=self.updateReservation)
        update.grid(row=4,column=0,columnspan=2,pady=5)

        cancel = Button(self.rootWinCF,text="Cancel a reservation",fg="blue",command=self.cancelReservation)
        cancel.grid(row=5,column=0,columnspan=2,pady=5)

        giveR = Button(self.rootWinCF,text="Give review",fg="blue",command=self.giveReview)
        giveR.grid(row=6,column=0,columnspan=2,pady=5)

        viewR = Button(self.rootWinCF,text="View review",fg="blue",command=self.viewReview)
        viewR.grid(row=7,column=0,columnspan=2,pady=5)

        school = Button(self.rootWinCF,text="Add school information (student discount)",fg="blue",command=self.addSchool)
        school.grid(row=8,column=0,columnspan=2,pady=5)

        logout = Button(self.rootWinCF,text="Log out",command=self.logoutCF)
        logout.grid(row=9,column=1,padx=5,pady=5,sticky=E)

    def logoutCF(self):
        self.rootWinCF.withdraw()
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

        search = Button(self.rootWin5,text="Search",command=self.trainSchedule)
        search.grid(row=3,column=0,columnspan=2,pady=10)

    def trainSchedule(self):
        tNum = self.tNE.get()
        if tNum == "":
            r = messagebox.showerror("Error!","Please enter a train number.")

        else:
            db = self.connect()
            cursor = db.cursor()

            #fetching train schedule
            sql = "SELECT TrainRoute.TrainNumber,Stop.StationName,Stop.ArrivalTime,Stop.DepartureTime FROM TrainRoute JOIN Stop ON TrainRoute.TrainNumber = Stop.TrainNumber AND Stop.TrainNumber = "+tNum+" ORDER BY Stop.ArrivalTime"
            cursor.execute(sql)
            results = cursor.fetchall()
            trainID,stations,aTimes,dTimes = zip(*results)
            stations = list(stations)
            aTimes = list(aTimes)
            dTimes = list(dTimes)
            
            if len(results) == 0:
               r = messagebox.showerror("Error!","This is an invalid train number.")
            else:
                self.rootWinSched = Toplevel()
                self.rootWinSched.title("View Train Schedule")
                self.rootWin5.withdraw()

                v = Label(self.rootWinSched,text="View Train Schedule",font=("Calibri",15,"bold"),fg="gold")
                v.grid(row=1,column=0,columnspan=2,pady=5)

                #table of train schedule
                frame = Frame(self.rootWinSched)
                frame.grid(row=2,column=0,columnspan=2,padx=5,pady=5)

                Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame,text="Arrival Time",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame,text="Departure Time",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame,text="Station",bg="gold",width=15).grid(row=0,column=3,sticky=W)

                Label(frame,text=tNum).grid(row=1,column=0,sticky=W)

                for i in range(1,len(aTimes)):
                    Label(frame,text=aTimes[i]).grid(row=i+1,column=1,sticky=W)
                for i in range(0,len(dTimes)-1):
                    Label(frame,text=dTimes[i]).grid(row=i+1,column=2,sticky=W)
                for i in range(0,len(stations)):
                    Label(frame,text=stations[i]).grid(row=i+1,column=3,sticky=W)
                
                back = Button(self.rootWinSched,text="Back",command=self.backViewTrain)
                back.grid(row=3,column=0,padx=10,pady=15)
            
            cursor.close()
            db.commit()
            db.close()

    def backViewTrain(self):
        self.rootWinSched.withdraw()
        self.rootWin5.deiconify()

####### MAKE A NEW RESERVATION ########

    ### search trains that fit criteria ###

    def searchTrain(self):
        self.rootWinSearch = Toplevel()
        self.rootWinSearch.title("Make a Reservation")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinSearch,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        s = Label(self.rootWinSearch,text="Search Train",font=("Calibri",15,"bold"),fg="gold")
        s.grid(row=1,column=0,columnspan=2,pady=5)

        tNum = Label(self.rootWinSearch,text="Departs From")
        tNum.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        db = self.connect()
        cursor = db.cursor()

        #populate with possible starting cities
        sql = "SELECT DISTINCT Location FROM Station"
        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
            
        cities = []
        for each in results:
            for one in each:
                cities.append(one)

        self.departsFrom = StringVar()
        pulldownD = OptionMenu(self.rootWinSearch,self.departsFrom,*cities)
        pulldownD.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        r = Label(self.rootWinSearch,text="Arrives At")
        r.grid(row=3,column=0,padx=5,pady=5,sticky=W)

        self.arrivesAt = StringVar()
        pulldownA = OptionMenu(self.rootWinSearch,self.arrivesAt,*cities)
        pulldownA.grid(row=3,column=1,padx=5,pady=5,sticky=W)

        c = Label(self.rootWinSearch,text="Departure Date")
        c.grid(row=4,column=0,padx=5,pady=5,sticky=W)

        self.departDatesv = StringVar()
        self.departDateE = Entry(self.rootWinSearch,textvariable=self.departDatesv,width=20)
        self.departDateE.grid(row=4,column=1,padx=5,pady=5,sticky=W)

        e = Label(self.rootWinSearch,text="Enter date in format YYYY-MM-DD",font=("Calibri",8))
        e.grid(row=5,column=0,columnspan=2,padx=5,sticky=W)

        submit = Button(self.rootWinSearch,text="Find Trains",command=self.selectDepart)
        submit.grid(row=6,column=1,padx=10,pady=15,sticky=E)

    # of available trains, select which to buy ticket from
    
    def selectDepart(self):
        departsFrom = self.departsFrom.get()
        arrivesAt = self.arrivesAt.get()
        departDate = self.departDateE.get()
        
        if departsFrom == "":
            r = messagebox.showerror("Error!","Please select a departure city.")
        elif arrivesAt == "":
            r = messagebox.showerror("Error!","Please select an arrival location.")
        elif departDate == "":
            r = messagebox.showerror("Error!","Please enter a departure date.")
        elif departsFrom == arrivesAt:
            r = messagebox.showerror("Error!","Please select different departure and arrival locations.")
        elif departDate[4] != "-" or departDate[7] != "-":
            r = messagebox.showerror("Error!","Please enter the departure date in the correct format.")
        else:
            departDate = datetime.datetime.strptime(departDate,'%Y-%m-%d').date()
            today = datetime.date.today()

            if departDate <= today:
                r = messagebox.showerror("Error!","Please enter the departure date after today.")
            else:           
                self.rootWinSelectD = Toplevel()
                self.rootWinSelectD.title("Make a Reservation")
                self.rootWinSearch.withdraw()

                v = Label(self.rootWinSelectD,text="Select Departure",font=("Calibri",15,"bold"),fg="gold")
                v.grid(row=0,column=0,columnspan=2,pady=5)

                db = self.connect()
                cursor = db.cursor()

                sql = "SELECT DISTINCT TrainNumber FROM Reserves WHERE DepartsFrom = '"+departsFrom+"' AND ArrivesAt = '"+arrivesAt+"'"
                cursor.execute(sql)
                results = cursor.fetchall()

                if len(results) == 0:
                    r = messagebox.showerror("Error!","There is not train route from the selected departure location to the selected arrival location.")
                else:
                    results3 = []
                    for each in results:
                        results3.append(each[0])

                    allResults = []
                    for each in results3:
                        sql2 = "SELECT TrainNumber,1stClassPrice,2ndClassPrice FROM TrainRoute WHERE TrainNumber = "+str(each)
                        cursor.execute(sql2)
                        results2 = cursor.fetchall()
                        allResults.append(results2)

                trains = []
                for i in range(0,len(allResults)):
                    for j in range(0,len(allResults[i])):
                        trains.append(allResults[i][j])

                trainNums = []
                class1 = []
                class2 = []
                for each in trains:
                    trainNums.append(each[0])
                    class1.append(each[1])
                    class2.append(each[2])

                frame = Frame(self.rootWinSelectD)
                frame.grid(row=1,column=0,columnspan=2,padx=5,pady=5)

                Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame,text="Time Duration",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame,text="1st Class Price",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame,text="2nd Class Price",bg="gold").grid(row=0,column=3,sticky=W)

                self.trainRowCol = StringVar()
                for i in range(0,len(trainNums)):
                    Label(frame,text=trainNums[i]).grid(row=i+1,column=0)
                for i in range(0,len(class1)):
                    Radiobutton(frame,text="%.2f"%class1[i],value=str(i+1)+str(1),variable=self.trainRowCol).grid(row=i+1,column=2,sticky=W)
                for i in range(0,len(class2)):
                    Radiobutton(frame,text="%.2f"%class2[i],value=str(i+1)+str(2),variable=self.trainRowCol).grid(row=i+1,column=3,sticky=W)

                back = Button(self.rootWinSelectD,text="Back",command=self.backToSearch)
                back.grid(row=2,column=0,padx=10,pady=15)

                search = Button(self.rootWinSelectD,text="Next",command=self.travelInfo)
                search.grid(row=2,column=1,padx=10,pady=15,sticky=E)

                cursor.close()
                db.commit()
                db.close()
                
    def backToSearch(self):
        self.rootWinSelectD.withdraw()
        self.rootWinSearch.deiconify()

    ### add number of baggages and passenger name ###

    def travelInfo(self):
        self.rootWinTravel = Toplevel()
        self.rootWinTravel.title("Make a reservation")
        self.rootWinSelectD.withdraw()

        v = Label(self.rootWinTravel,text="Travel Extras & Passenger Info",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)
        
        n = Label(self.rootWinTravel,text="Number of Baggage")
        n.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.numBag = IntVar()
        pulldownB = OptionMenu(self.rootWinTravel,self.numBag,0,1,2,3,4)
        pulldownB.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        small = Label(self.rootWinTravel,text="Every passenger can bring up to 4 baggage. 2 free of charge, 2 for $30 per bag",font=("Calibri",8))
        small.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        c = Label(self.rootWinTravel,text="Passenger Name")
        c.grid(row=4,column=0,padx=5,pady=5,sticky=W)

        self.passName = StringVar()
        self.passNameE = Entry(self.rootWinTravel,textvariable=self.passName,width=30)
        self.passNameE.grid(row=4,column=1,padx=5,pady=5,sticky=W)

        back = Button(self.rootWinTravel,text="Back",command=self.backToSelect)
        back.grid(row=5,column=0,padx=10,pady=15)

        search = Button(self.rootWinTravel,text="Next",command=self.reserveInfo)
        search.grid(row=5,column=1,padx=10,pady=15,sticky=E)

    def backToSelect(self):
        self.rootWinTravel.withdraw()
        self.rootWinSelectD.deiconify()

    ### shows reservation info and total calculated cost ###

    def reserveInfo(self):
        username = self.uEntry.get()
        numBag = self.numBag.get()
        departsFrom = self.departsFrom.get()
        arrivesAt = self.arrivesAt.get()
        departDate = self.departDateE.get()
        trainRowCol = self.trainRowCol.get()
        passenger = self.passName.get()

        trainRow = trainRowCol[:1]
        classNum = trainRowCol[1:]
        
        db = self.connect()
        cursor = db.cursor()

        sql3 = "SELECT TrainRoute.TrainNumber, TrainRoute.1stClassPrice, TrainRoute.2ndClassPrice FROM TrainRoute JOIN Stop ON TrainRoute.TrainNumber = Stop.TrainNumber JOIN Station ON Stop.StationName = Station.Name AND Station.Location = '"+departsFrom+"'"
        cursor.execute(sql3)
        results3 = cursor.fetchall()

        #identifies chosen trainNum, price, and class
        trains,class1,class2 = zip(*results3)
        trains = list(trains)
        class1 = list(class1)
        class2 = list(class2)
        pickTrain = []
        pickTrain.append(trains)
        pickTrain.append(class1)
        pickTrain.append(class2)
        trainNum = pickTrain[0][int(trainRow)-1]
        price = pickTrain[int(classNum)][int(trainRow)-1]

        #adds to list used to make reservation table
        self.chosenTrains.append(trainNum)
        self.departDates.append(departDate)
        self.departures.append(departsFrom)
        self.arrivals.append(arrivesAt)
        self.classes.append(classNum)
        self.prices.append(price)
        self.allBags.append(numBag)
        self.passengers.append(passenger)
        
        self.rootWinRes = Toplevel()
        self.rootWinRes.title("Make a reservation")
        self.rootWinTravel.withdraw()

        v = Label(self.rootWinRes,text="Make Reservation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=0,column=0,columnspan=3,pady=5)

        cs = Label(self.rootWinRes,text="Currently Selected")
        cs.grid(row=1,column=0,padx=5,sticky=W)

        # table with reservation informaation
        self.frame = Frame(self.rootWinRes)
        self.frame.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

        Label(self.frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
        Label(self.frame,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
        Label(self.frame,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
        Label(self.frame,text="Departs From",bg="gold",width=15).grid(row=0,column=3)
        Label(self.frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=4)
        Label(self.frame,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
        Label(self.frame,text="Price",bg="gold",width=10).grid(row=0,column=6,sticky=W)
        Label(self.frame,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
        Label(self.frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)
        Label(self.frame,text="Remove",bg="gold").grid(row=0,column=9,sticky=W)

        #makes list of info to insert reservation
        self.reservations = []
        for i in range(0,len(self.chosenTrains)):
            reservation = [self.classes[i],self.departDates[i],self.passengers[i],self.allBags[i],self.departures[i],self.arrivals[i],self.chosenTrains[i]]
            self.reservations.append(reservation)

        for i in range(0,len(self.chosenTrains)):
            Label(self.frame,text=self.chosenTrains[i]).grid(row=i+1,column=0,sticky=W)
        for i in range(0,len(self.departDates)):
            Label(self.frame,text=self.departDates[i]).grid(row=i+1,column=1,sticky=W)
        #for i in range(0,len(chosenTrains)):
         #   Label(self.frame,text=chosenTrains[i]).grid(row=i+1,column=2,sticky=W)
        for i in range(0,len(self.departures)):
            Label(self.frame,text=self.departures[i]).grid(row=i+1,column=3,sticky=W)
        for i in range(0,len(self.arrivals)):
            Label(self.frame,text=self.arrivals[i]).grid(row=i+1,column=4,sticky=W)
        for i in range(0,len(self.classes)):
            Label(self.frame,text=self.classes[i]).grid(row=i+1,column=5)
        for i in range(0,len(self.prices)):
            Label(self.frame,text="%.2f"%self.prices[i]).grid(row=i+1,column=6)
        for i in range(0,len(self.allBags)):
            Label(self.frame,text=self.allBags[i]).grid(row=i+1,column=7)
        for i in range(0,len(self.passengers)):
            Label(self.frame,text=self.passengers[i]).grid(row=i+1,column=8,sticky=W)

        self.removeRow = IntVar()
        for i in range(0,len(self.reservations)):
            Radiobutton(self.frame,value=i,variable=self.removeRow).grid(row=i+1,column=9)
        Button(self.rootWinRes,text="Remove",command=self.removeTrain).grid(row=3,column=2,padx=5,sticky=E)

        sql = "SELECT isStudent FROM Customer WHERE Username='"+username+"'"
        cursor.execute(sql)
        results = cursor.fetchall()

        if results[0][0] == True:
            sd = Label(self.rootWinRes,text="Student Discount Applied")
            sd.grid(row=3,column=0,padx=5,pady=5,sticky=W)

            discount = 0.8
        else:
            discount = 1.0

        tc = Label(self.rootWinRes,text="Total Cost")
        tc.grid(row=4,column=0,padx=5,sticky=W)

        totalPrice = sum(self.prices)

        bagPrices = []
        for each in self.allBags:
            if each > 2:
                bagPrices.append((each-2)*30)
            else:
                bagPrices.append(0)
        bagPrice = sum(bagPrices)
    
        totalCost = (totalPrice + bagPrice)*discount
        
        self.costSV = StringVar()
        self.costSV.set("%.2f"%totalCost)
        self.costE = Entry(self.rootWinRes,textvariable=self.costSV,width=25)
        self.costE.grid(row=4,column=1,columnspan=2,padx=5,sticky=W)

        uc = Label(self.rootWinRes,text="Use Card")
        uc.grid(row=5,column=0,padx=5,sticky=W)

        db = self.connect()
        cursor = db.cursor()

        sql2 = "SELECT CardNumber FROM PaymentInfo WHERE Username = '"+username+"'"
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        
        cursor.close()
        db.commit()
        db.close()

        cards = list(results2)
        self.chosenCard = StringVar()
        pulldownC = OptionMenu(self.rootWinRes,self.chosenCard,*cards)
        pulldownC.grid(row=5,column=1,pady=5,sticky=W)

        ac = Button(self.rootWinRes,text="Add Card",fg="blue",command=self.payInfo)
        ac.grid(row=5,column=2,padx=5,pady=5,sticky=W)

        ca = Button(self.rootWinRes,text="Continue adding a train",fg="blue",command=self.moreTrains)
        ca.grid(row=6,column=0,padx=5,pady=5,sticky=W)

        back = Button(self.rootWinRes,text="Back",command=self.backToTravel)
        back.grid(row=7,column=0,padx=10,pady=15,sticky=W)

        submit = Button(self.rootWinRes,text="Submit",command=self.submitRes)
        submit.grid(row=7,column=2,padx=10,pady=15,sticky=E)

    def removeTrain(self):
        username = self.uEntry.get()
        removeRow = self.removeRow.get()
        self.reservations.remove(self.reservations[removeRow])
        self.chosenTrains.remove(self.chosenTrains[removeRow])
        self.departDates.remove(self.departDates[removeRow])
        self.departures.remove(self.departures[removeRow])
        self.arrivals.remove(self.arrivals[removeRow])
        self.classes.remove(self.classes[removeRow])
        self.prices.remove(self.prices[removeRow])
        self.allBags.remove(self.allBags[removeRow])
        self.passengers.remove(self.passengers[removeRow])

        self.frame.grid_forget()

        self.frame = Frame(self.rootWinRes)
        self.frame.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

        Label(self.frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
        Label(self.frame,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
        Label(self.frame,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
        Label(self.frame,text="Departs From",bg="gold",width=15).grid(row=0,column=3)
        Label(self.frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=4)
        Label(self.frame,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
        Label(self.frame,text="Price",bg="gold",width=10).grid(row=0,column=6,sticky=W)
        Label(self.frame,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
        Label(self.frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)
        Label(self.frame,text="Remove",bg="gold").grid(row=0,column=9,sticky=W)

        for i in range(0,len(self.chosenTrains)):
            Label(self.frame,text=self.chosenTrains[i]).grid(row=i+1,column=0,sticky=W)
        for i in range(0,len(self.departDates)):
            Label(self.frame,text=self.departDates[i]).grid(row=i+1,column=1,sticky=W)
        #for i in range(0,len(chosenTrains)):
         #   Label(self.frame,text=chosenTrains[i]).grid(row=i+1,column=2,sticky=W)
        for i in range(0,len(self.departures)):
            Label(self.frame,text=self.departures[i]).grid(row=i+1,column=3,sticky=W)
        for i in range(0,len(self.arrivals)):
            Label(self.frame,text=self.arrivals[i]).grid(row=i+1,column=4,sticky=W)
        for i in range(0,len(self.classes)):
            Label(self.frame,text=self.classes[i]).grid(row=i+1,column=5)
        for i in range(0,len(self.prices)):
            Label(self.frame,text="%.2f"%self.prices[i]).grid(row=i+1,column=6)
        for i in range(0,len(self.allBags)):
            Label(self.frame,text=self.allBags[i]).grid(row=i+1,column=7)
        for i in range(0,len(self.passengers)):
            Label(self.frame,text=self.passengers[i]).grid(row=i+1,column=8,sticky=W)

        self.removeRow = IntVar()
        for i in range(0,len(self.reservations)):
            Radiobutton(self.frame,value=i,variable=self.removeRow).grid(row=i+1,column=9)
        Button(self.rootWinRes,text="Remove",command=self.removeTrain).grid(row=3,column=2,padx=5,sticky=E)

        db = self.connect()
        cursor = db.cursor()
        
        sql = "SELECT isStudent FROM Customer WHERE Username='"+username+"'"
        cursor.execute(sql)
        results = cursor.fetchall()

        if results[0][0] == True:
            discount = 0.8
        else:
            discount = 1.0

        totalPrice = sum(self.prices)

        bagPrices = []
        for each in self.allBags:
            if each > 2:
                bagPrices.append((each-2)*30)
            else:
                bagPrices.append(0)
        bagPrice = sum(bagPrices)
    
        totalCost = (totalPrice + bagPrice)*discount
        
        self.costSV.set("%.2f"%totalCost)

        cursor.close()
        db.commit()
        db.close()

    def moreTrains(self):
        self.rootWinRes.withdraw()
        self.searchTrain()

    def backToTravel(self):
        self.rootWinRes.withdraw()
        self.rootWinTravel.deiconify()

    def submitRes(self):
        ## add all info to database ##

        card = self.chosenCard.get()
        card = card[2:len(card)-3]
        username = self.uEntry.get()
        totalCost = self.costSV.get()
        totalCost = totalCost[:len(totalCost)-3]

        if card == "":
            r = messagebox.showerror("Error!","Please select a payment method.")
        else:
            db = self.connect()
            cursor = db.cursor()

            sql = "INSERT INTO Reservation(ReservationID,isCancelled,CardNumber,Username,TotalCost) VALUES(NULL,0,"+card+",(SELECT Username FROM User WHERE Username = '"+username+"'),"+totalCost+")"
            cursor.execute(sql)

            sql2 = "SELECT ReservationID FROM Reservation WHERE Username = '"+username+"' GROUP BY `ReservationID` DESC"
            cursor.execute(sql2)
            results = cursor.fetchall()
            self.resID = results[0][0]
	
            for each in self.reservations:
                sql = "INSERT INTO Reserves VALUES ((SELECT ReservationID FROM Reservation WHERE ReservationID = "+str(self.resID)+"),"+str(each[6])+","+str(each[0])+",'"+str(each[1])+"','"+str(each[2])+"',"+str(each[3])+",'"+str(each[4])+"','"+str(each[5])+"')"
                cursor.execute(sql)

            cursor.close()
            db.commit()
            db.close()

            self.confirmScreen()

    def confirmScreen(self):
        self.rootWinCon = Toplevel()
        self.rootWinCon.title("Make a reservation")
        self.rootWinRes.withdraw()

        v = Label(self.rootWinCon,text="Confirmation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        r = Label(self.rootWinCon,text="Reservation ID")
        r.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.resIDsv = StringVar()
        self.resIDsv.set(self.resID)
        self.resIDE = Entry(self.rootWinCon,textvariable=self.resIDsv,width=10)
        self.resIDE.grid(row=2,column=1,padx=5,pady=5)

        small = Label(self.rootWinCon,text="Thank you for your purchase! Please save reservation ID for your records.",font=("Calibri",8))
        small.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        back = Button(self.rootWinCon,text="Back to Choose Functionality",command=self.backConfirm)
        back.grid(row=4,column=0,columnspan=2,padx=10,pady=15)

    def backConfirm(self):
        self.rootWinCon.withdraw()
        self.rootWinCF.deiconify()

    ## payment info ##

    def payInfo(self):
        username = self.uEntry.get()
        
        self.rootWinPay = Toplevel()
        self.rootWinPay.title("Payment Information")
        self.rootWinRes.withdraw()

        v = Label(self.rootWinPay,text="Payment Information",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=0,column=0,columnspan=4,pady=5)

        ## ADD CARD ##
        
        ac = Label(self.rootWinPay,text="Add Card",font=("Calibri",12,"bold"))
        ac.grid(row=1,column=0,padx=5,pady=10,sticky=W)

        n = Label(self.rootWinPay,text="Name on Card")
        n.grid(row=2,column=0,padx=5,sticky=W)

        self.nameCsv = StringVar()
        self.nameCE = Entry(self.rootWinPay,textvariable=self.nameCsv,width=20)
        self.nameCE.grid(row=2,column=1,padx=5,sticky=W)

        cn = Label(self.rootWinPay,text="Card Number")
        cn.grid(row=3,column=0,padx=5,sticky=W)

        self.cardNumsv = StringVar()
        self.cardNumE = Entry(self.rootWinPay,textvariable=self.cardNumsv,width=20)
        self.cardNumE.grid(row=3,column=1,padx=5,sticky=W)

        cv = Label(self.rootWinPay,text="CVV")
        cv.grid(row=4,column=0,padx=5,sticky=W)

        self.cvvSV = StringVar()
        self.cvvE = Entry(self.rootWinPay,textvariable=self.cvvSV,width=5)
        self.cvvE.grid(row=4,column=1,padx=5,sticky=W)

        ex = Label(self.rootWinPay,text="Expiration Date")
        ex.grid(row=5,column=0,padx=5,sticky=W)

        self.exDatesv = StringVar()
        self.exDateE = Entry(self.rootWinPay,textvariable=self.exDatesv,width=10)
        self.exDateE.grid(row=5,column=1,padx=5,sticky=W)

        e = Label(self.rootWinPay,text="Enter date in format YYYY-MM-DD",font=("Calibri",8))
        e.grid(row=6,column=0,columnspan=2,padx=5,sticky=W)

        submit1 = Button(self.rootWinPay,text="Submit",command=self.addCard)
        submit1.grid(row=7,column=0,columnspan=2,pady=15)

        ## DELETE CARD ##

        dc = Label(self.rootWinPay,text="Delete Card",font=("Calibri",12,"bold"))
        dc.grid(row=1,column=2,padx=30,pady=10,sticky=W)

        cn2 = Label(self.rootWinPay,text="Card Number")
        cn2.grid(row=2,column=2,padx=30,sticky=W)

        db = self.connect()
        cursor = db.cursor()

        sql = "SELECT CardNumber FROM PaymentInfo WHERE Username = '"+username+"'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        cursor.close()
        db.commit()
        db.close()

        cards = list(results)
        self.delCard = StringVar()
        pulldownDC = OptionMenu(self.rootWinPay,self.delCard,*cards)
        pulldownDC.grid(row=2,column=3,padx=15,pady=5,sticky=W)

        submit2 = Button(self.rootWinPay,text="Submit",command=self.deleteCard)
        submit2.grid(row=7,column=2,columnspan=2,pady=15)

    def addCard(self):
        name = self.nameCE.get()
        card = self.cardNumE.get()
        cvv = self.cvvE.get()
        exDate = self.exDateE.get()
        username = self.uEntry.get()

        if exDate[4] != "-" or exDate[7] != "-":
            r = messagebox.showerror("Error!","Please enter a expiration date in the correct formatting.")
        else:
            exDate = datetime.datetime.strptime(exDate,'%Y-%m-%d').date()
            today = datetime.date.today()

            if exDate <= today:
                r = messagebox.showerror("Error!","Please enter a expiration date later than today.")
            else:    
                db = self.connect()
                cursor = db.cursor()

                sql = "INSERT INTO PaymentInfo VALUES ("+card+","+cvv+",'"+str(exDate)+"','"+name+"', (SELECT Username FROM User WHERE Username='"+username+"'))"
                cursor.execute(sql)

                self.rootWinPay.withdraw()
                self.rootWinRes.deiconify()

                sql2 = "SELECT CardNumber FROM PaymentInfo WHERE Username = '"+username+"'"
                cursor.execute(sql2)
                results2 = cursor.fetchall()
                
                cursor.close()
                db.commit()
                db.close()

                cards = list(results2)
                self.chosenCard = StringVar()
                pulldownC = OptionMenu(self.rootWinRes,self.chosenCard,*cards)
                pulldownC.grid(row=5,column=1,pady=5,sticky=W)

    def deleteCard(self):

        db = self.connect()
        cursor = db.cursor()

        card = self.delCard.get()

        sql3 = "SELECT Reservation.ReservationID,Reservation.CardNumber,Reserves.DepartureDate FROM Reservation JOIN Reserves ON Reserves.ReservationID = Reservation.ReservationID 	WHERE Reservation.CardNumber = "+card+" AND Reserves.DepartureDate > CURDATE()"
        cursor.execute(sql3)
        results = cursor.fetchall()

        if len(results) > 0:
            r = messagebox.showerror("Error!","The selected card is being used in a current transaction. This card cannot be deleted.")
        else:
            sql = "DELETE FROM PaymentInfo WHERE CardNumber = "+card
            cursor.execute(sql)

            self.rootWinPay.withdraw()
            self.rootWinRes.deiconify()

            sql2 = "SELECT CardNumber FROM PaymentInfo WHERE Username = '"+username+"'"
            cursor.execute(sql2)
            results2 = cursor.fetchall()
            
            cursor.close()
            db.commit()
            db.close()

            cards = list(results2)
            self.chosenCard = StringVar()
            pulldownC = OptionMenu(self.rootWinRes,self.chosenCard,*cards)
            pulldownC.grid(row=5,column=1,pady=5,sticky=W)
            

####### UPDATE RESERVATION #######

    def updateReservation(self):
        self.rootWinUR = Toplevel()
        self.rootWinUR.title("Update Reservation")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinUR,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinUR,text="Update Reservation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        rNum = Label(self.rootWinUR,text="Reservation ID")
        rNum.grid(row=2,column=0,padx=5,pady=5)

        self.urIDsv = StringVar()
        self.urIDE = Entry(self.rootWinUR,textvariable=self.urIDsv,width=15)
        self.urIDE.grid(row=2,column=1,padx=5,pady=5)

        back = Button(self.rootWinUR,text="Back",command=self.backUpdate)
        back.grid(row=3,column=0,padx=10,pady=15,sticky=W)

        search = Button(self.rootWinUR,text="Search",command=self.searchUpdate)
        search.grid(row=3,column=1,padx=10,pady=15,sticky=E)

    def backUpdate(self):
        self.rootWinCF.deiconify()
        self.rootWinUR.withdraw()

    def searchUpdate(self):
        username = self.uEntry.get()
        urID = self.urIDE.get()
        db = self.connect()
        cursor = db.cursor()
        
        if urID == "":
            r = messagebox.showerror("Error!","Please enter a reservation ID.")

        else:
            #check for reservation ID in database and that it has not already been cancelled
            sql = "SELECT ReservationID,isCancelled,Username FROM Reservation WHERE ReservationID ="+urID+" AND Username='"+username+"'"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                r = messagebox.showerror("Error!","There is no reservation with this ID number.")
            elif results[0][1] == True:
                r = messagebox.showerror("Error!","This reservation has already been cancelled.")

            else:
                self.rootWinU = Toplevel()
                self.rootWinU.title("Update Reservation")
                self.rootWinUR.withdraw()

                v = Label(self.rootWinU,text="Update Reservation",font=("Calibri",15,"bold"),fg="gold")
                v.grid(row=1,column=0,columnspan=2,pady=5)

                sql2 = "SELECT Reserves.TrainNumber,Reserves.DepartureDate,Reserves.DepartsFrom,Reserves.ArrivesAt,Reserves.Class,Reserves.NumberBaggage,Reserves.PassengerName,TrainRoute.1stClassPrice,TrainRoute.2ndClassPrice FROM Reserves JOIN TrainRoute ON Reserves.TrainNumber = TrainRoute.TrainNumber WHERE ReservationID = "+urID

                cursor.execute(sql2)
                results2 = cursor.fetchall()

                cursor.close()
                db.commit()
                db.close()
                
                tNum,departDate,depart,arrive,classNum,bag,passenger,class1,class2 = zip(*results2)
                tNum = list(tNum)
                departDate = list(departDate)
                depart = list(depart)
                arrive = list(arrive)
                classNum = list(classNum)
                bag = list(bag)
                passenger = list(passenger)
                class1 = list(class1)
                class2 = list(class2)

                tPrices = []
                for i in range(0,len(tNum)):
                    tPrices.append([tNum[i],class1[i],class2[i]])

                #list of reservation by row
                self.reservations = []
                for i in range(0,len(tNum)):
                    reservation = [tNum[i],departDate[i],depart[i],arrive[i],classNum[i],tPrices[i][classNum[i]],bag[i],passenger[i]]
                    self.reservations.append(reservation)


                #table of current reservatons
                frame = Frame(self.rootWinU)
                frame.grid(row=2,column=0,columnspan=2,padx=5,pady=5)

                Label(frame,text="Select",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame,text="Departure Date",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame,text="Time (Duration)",bg="gold").grid(row=0,column=3,sticky=W)
                Label(frame,text="Departs From",bg="gold",width=15).grid(row=0,column=4,sticky=W)
                Label(frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=5,sticky=W)
                Label(frame,text="Class",bg="gold").grid(row=0,column=6,sticky=W)
                Label(frame,text="Price",bg="gold",width=10).grid(row=0,column=7,sticky=W)
                Label(frame,text="# of Baggage",bg="gold").grid(row=0,column=8,sticky=W)
                Label(frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=9,sticky=W)

                self.selectR = IntVar()
                for i in range(0,len(tNum)):
                    Radiobutton(frame,value=i,variable=self.selectR).grid(row=i+1,column=0)
                for i in range(0,len(tNum)):
                    Label(frame,text=tNum[i]).grid(row=i+1,column=1)
                for i in range(0,len(departDate)):
                    Label(frame,text=departDate[i]).grid(row=i+1,column=2)
                #for all time duration
                for i in range(0,len(depart)):
                    Label(frame,text=depart[i]).grid(row=i+1,column=4,sticky=W)
                for i in range(0,len(arrive)):
                    Label(frame,text=arrive[i]).grid(row=i+1,column=5,sticky=W)
                for i in range(0,len(classNum)):
                    Label(frame,text=classNum[i]).grid(row=i+1,column=6)
                for i in range(0,len(tPrices)):
                    Label(frame,text="%.2f"%tPrices[i][classNum[i]]).grid(row=i+1,column=7)
                for i in range(0,len(bag)):
                    Label(frame,text=bag[i]).grid(row=i+1,column=8)
                for i in range(0,len(passenger)):
                    Label(frame,text=passenger[i]).grid(row=i+1,column=9,sticky=W)

                #navigation buttons
                
                back = Button(self.rootWinU,text="Back",command=self.back2)
                back.grid(row=6,column=0,padx=10,pady=15,sticky=W)

                nextB = Button(self.rootWinU,text="Next",command=self.makeUpdates)
                nextB.grid(row=6,column=1,padx=10,pady=15,sticky=E)

    def back2(self):
        self.rootWinU.withdraw()
        self.rootWinUR.deiconify()

    def makeUpdates(self):
        self.rootWinMU = Toplevel()
        self.rootWinMU.title("Update Reservation")
        self.rootWinU.withdraw()

        v = Label(self.rootWinMU,text="Update Reservation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=0,column=0,columnspan=3,pady=5)

        Label(self.rootWinMU,text="Current Train Ticket").grid(row=1,column=0,pady=5,sticky=W)

        frame = Frame(self.rootWinMU)
        frame.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

        #column names
        Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
        Label(frame,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
        Label(frame,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
        Label(frame,text="Departs From",bg="gold",width=15).grid(row=0,column=3,sticky=W)
        Label(frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=4,sticky=W)
        Label(frame,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
        Label(frame,text="Price",bg="gold").grid(row=0,column=6,sticky=W)
        Label(frame,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
        Label(frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)

        #reservation info
        which = self.selectR.get()
        for i in range(0,len(self.reservations[which])):
            Label(frame,text=self.reservations[which][i]).grid(row=1,column=i)
        #####columns are slightly off until add time duration
        
        Label(self.rootWinMU,text="New Departure Date").grid(row=3,column=0,pady=5,sticky=W)

        self.nDD = StringVar()
        self.nDDE = Entry(self.rootWinMU,textvariable=self.nDD,width=15)
        self.nDDE.grid(row=3,column=1,padx=10)

        e = Label(self.rootWinMU,text="Enter date in format YYYY-MM-DD",font=("Calibri",8))
        e.grid(row=4,column=0,columnspan=2,sticky=W)

        s = Button(self.rootWinMU,text="Search availability",command=self.searchAvailable)
        s.grid(row=3,column=2,padx=10)
        
        back = Button(self.rootWinMU,text="Back",command=self.back3)
        back.grid(row=9,column=0,padx=10,pady=15,sticky=W)

    def back3(self):
        self.rootWinMU.withdraw()
        self.rootWinU.deiconify()

    def searchAvailable(self):
        newDate = self.nDD.get()

        if newDate[4] != "-" or newDate[7] != "-":
            r = messagebox.showerror("Error!","Please enter a new departure date in the correct formatting.")
        else:
            newDate = datetime.datetime.strptime(newDate,'%Y-%m-%d').date()
            today = datetime.date.today()

            tdelta = newDate - today
            
            if tdelta.days < 1:
                r = messagebox.showerror("Error!","Departure dates cannot be changed within one day of departure.")
            else:
                self.rootWinMU.withdraw()
                self.rootWinMU = Toplevel()
                self.rootWinMU.title("Update Reservation")
                self.rootWinU.withdraw()

                v = Label(self.rootWinMU,text="Update Reservation",font=("Calibri",15,"bold"),fg="gold")
                v.grid(row=0,column=0,columnspan=3,pady=5)

                Label(self.rootWinMU,text="Current Train Ticket").grid(row=1,column=0,pady=5,sticky=W)

                frame = Frame(self.rootWinMU)
                frame.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

                #column names
                Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame,text="Departs From",bg="gold",width=15).grid(row=0,column=3,sticky=W)
                Label(frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=4,sticky=W)
                Label(frame,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
                Label(frame,text="Price",bg="gold").grid(row=0,column=6,sticky=W)
                Label(frame,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
                Label(frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)

                #reservation info
                which = self.selectR.get()
                for i in range(0,len(self.reservations[which])):
                    Label(frame,text=self.reservations[which][i]).grid(row=1,column=i)
                #####columns are slightly off until add time duration
                
                Label(self.rootWinMU,text="New Departure Date").grid(row=3,column=0,pady=5,sticky=W)

                self.nDDE = Entry(self.rootWinMU,textvariable=self.nDD,width=15)
                self.nDDE.grid(row=3,column=1,padx=10)

                e = Label(self.rootWinMU,text="Enter date in format YYYY-MM-DD",font=("Calibri",8))
                e.grid(row=4,column=0,columnspan=2,sticky=W)

                s = Button(self.rootWinMU,text="Search availability",command=self.searchAvailable)
                s.grid(row=3,column=2,padx=10)
                
                Label(self.rootWinMU,text="Updated Train Ticket").grid(row=5,column=0,pady=5,sticky=W)
                #table with updated train tickets

                frame2 = Frame(self.rootWinMU)
                frame2.grid(row=6,column=0,columnspan=3,padx=5,pady=5)

                #column names
                Label(frame2,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame2,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame2,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame2,text="Departs From",bg="gold",width=15).grid(row=0,column=3,sticky=W)
                Label(frame2,text="Arrives At",bg="gold",width=15).grid(row=0,column=4,sticky=W)
                Label(frame2,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
                Label(frame2,text="Price",bg="gold").grid(row=0,column=6,sticky=W)
                Label(frame2,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
                Label(frame2,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)

                #reservation info
                which = self.selectR.get()
                self.reservations[which][1] = self.nDDE.get()
                for i in range(0,len(self.reservations[which])):
                    Label(frame2,text=self.reservations[which][i]).grid(row=1,column=i)
                
                Label(self.rootWinMU,text="Change Fee").grid(row=7,column=0,pady=5,sticky=W)

                self.cFee = IntVar()
                self.cFee.set(50)
                self.cFeeE = Entry(self.rootWinMU,textvariable=self.cFee,width=15)
                self.cFeeE.grid(row=7,column=1,padx=10)

                Label(self.rootWinMU,text="Updated Total Cost").grid(row=8,column=0,pady=5,sticky=W)

                urID = self.urIDE.get()
                
                db = self.connect()
                cursor = db.cursor()
                sql = "SELECT TotalCost FROM Reservation WHERE ReservationID="+urID
                cursor.execute(sql)
                results = cursor.fetchall()
                results = list(results)
                oldCost = results[0][0]

                self.newCost = StringVar()
                self.newCost.set("%.2f"%(50 + oldCost))
                self.newCostE = Entry(self.rootWinMU,textvariable=self.newCost,width=15)
                self.newCostE.grid(row=8,column=1,padx=10)

                back = Button(self.rootWinMU,text="Back",command=self.back3)
                back.grid(row=9,column=0,padx=10,pady=15,sticky=W)

                submit = Button(self.rootWinMU,text="Submit",command=self.submitUpdates)
                submit.grid(row=9,column=1,padx=10,pady=15,sticky=E)

                cursor.close()
                db.commit()
                db.close()

    def submitUpdates(self):
        rID = self.urIDE.get()
        newDate = self.nDDE.get()
        newCost = self.newCost.get()
        
        db = self.connect()
        cursor = db.cursor()

        sql = "UPDATE Reserves SET DepartureDate = "+newDate+" WHERE ReservationID = "+rID
        sql2 = "UPDATE Reservation SET TotalCost = "+newCost+" WHERE ReservationID = "+rID
        cursor.execute(sql)
        cursor.execute(sql2)

        cursor.close()
        db.commit()
        db.close()

        self.rootWinMU.withdraw()
        self.rootWinCF.deiconify()
        

####### CANCEL RESERVATION ######

    def cancelReservation(self):
        self.rootWinCR = Toplevel()
        self.rootWinCR.title("Cancel Reservation")
        self.rootWinCF.withdraw()

        pic = Label(self.rootWinCR,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinCR,text="Cancel Reservation",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=3,pady=5)

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
        self.rootWinCR.withdraw()
        self.rootWinCF.deiconify()

    def cancel(self):
        rID = self.rIDE.get()
        username = self.uEntry.get()
        db = self.connect()
        cursor = db.cursor()
        
        if rID == "":
            r = messagebox.showerror("Error!","Please enter a reservation ID.")

        else:
            #check for reservation ID in database and that it has not already been cancelled
            sql = "SELECT ReservationID, isCancelled FROM Reservation WHERE ReservationID ="+rID+" AND Username='"+username+"'"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                r = messagebox.showerror("Error!","There is no reservation with this ID number.")
            elif results[0][1] == True:
                r = messagebox.showerror("Error!","This reservation has already been cancelled.")
            else:

                self.rootWinC = Toplevel()
                self.rootWinC.title("Cancel Reservation")
                self.rootWinCR.withdraw()

                v = Label(self.rootWinC,text="Cancel Reservation",font=("Calibri",15,"bold"),fg="gold")
                v.grid(row=1,column=0,columnspan=2,pady=5)

                sql2 = "SELECT Reserves.TrainNumber,Reserves.DepartureDate,Reserves.DepartsFrom,Reserves.ArrivesAt,Reserves.Class,Reserves.NumberBaggage,Reserves.PassengerName,TrainRoute.1stClassPrice,TrainRoute.2ndClassPrice FROM Reserves JOIN TrainRoute ON Reserves.TrainNumber = TrainRoute.TrainNumber WHERE ReservationID = "+rID

                cursor.execute(sql2)
                results2 = cursor.fetchall()
               
                tNum,departDate,depart,arrive,classNum,bag,passenger,class1,class2 = zip(*results2)
                tNum = list(tNum)
                departDate = list(departDate)
                depart = list(depart)
                arrive = list(arrive)
                classNum = list(classNum)
                bag = list(bag)
                passenger = list(passenger)
                class1 = list(class1)
                class2 = list(class2)

                tPrices = []
                for i in range(0,len(tNum)):
                    tPrices.append([tNum[i],class1[i],class2[i]])

                #list of reservation by row
                self.reservations = []
                for i in range(0,len(tNum)):
                    reservation = [tNum[i],departDate[i],depart[i],arrive[i],classNum[i],tPrices[i][classNum[i]],bag[i],passenger[i]]
                    self.reservations.append(reservation)

                #table of current reservatons
                frame = Frame(self.rootWinC)
                frame.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

                Label(frame,text="Train (Train Number)",bg="gold").grid(row=0,column=0,sticky=W)
                Label(frame,text="Departure Date",bg="gold").grid(row=0,column=1,sticky=W)
                Label(frame,text="Time (Duration)",bg="gold").grid(row=0,column=2,sticky=W)
                Label(frame,text="Departs From",bg="gold",width=15).grid(row=0,column=3,sticky=W)
                Label(frame,text="Arrives At",bg="gold",width=15).grid(row=0,column=4,sticky=W)
                Label(frame,text="Class",bg="gold").grid(row=0,column=5,sticky=W)
                Label(frame,text="Price",bg="gold",width=10).grid(row=0,column=6,sticky=W)
                Label(frame,text="# of Baggage",bg="gold").grid(row=0,column=7,sticky=W)
                Label(frame,text="Passenger Name",bg="gold",width=15).grid(row=0,column=8,sticky=W)

                for i in range(0,len(tNum)):
                    Label(frame,text=tNum[i]).grid(row=i+1,column=0)
                for i in range(0,len(departDate)):
                    Label(frame,text=departDate[i]).grid(row=i+1,column=1)
                #for all time duration
                for i in range(0,len(depart)):
                    Label(frame,text=depart[i]).grid(row=i+1,column=3,sticky=W)
                for i in range(0,len(arrive)):
                    Label(frame,text=arrive[i]).grid(row=i+1,column=4,sticky=W)
                for i in range(0,len(classNum)):
                    Label(frame,text=classNum[i]).grid(row=i+1,column=5)
                for i in range(0,len(tPrices)):
                    Label(frame,text="%.2f"%tPrices[i][classNum[i]]).grid(row=i+1,column=6)
                for i in range(0,len(bag)):
                    Label(frame,text=bag[i]).grid(row=i+1,column=7)
                for i in range(0,len(passenger)):
                    Label(frame,text=passenger[i]).grid(row=i+1,column=8,sticky=W)
                    
            #total cost of reservation

                sql3 = "SELECT TotalCost FROM Reservation WHERE ReservationID = "+rID
                cursor.execute(sql3)
                results3 = cursor.fetchall()
                cost = results3[0][0]
                
                c = Label(self.rootWinC,text="Total Cost of Reservation")
                c.grid(row=3,column=0,padx=5,pady=5,sticky=W)

                self.costRiv = IntVar()
                self.costRiv.set(cost)
                self.costRE = Entry(self.rootWinC,textvariable=self.costRiv,width=15)
                self.costRE.grid(row=3,column=1,padx=5,pady=5,sticky=W)
                
            #date of cancellation
                
                d = Label(self.rootWinC,text="Date of Cancellation")
                d.grid(row=4,column=0,padx=5,pady=5,sticky=W)

                self.datesv = StringVar()
                self.datesv.set(datetime.date.today())
                self.dateE = Entry(self.rootWinC,textvariable=self.datesv,width=15)
                self.dateE.grid(row=4,column=1,padx=5,pady=5,sticky=W)

            #amount to be refunded

                amount = Label(self.rootWinC,text="Amount to be Refunded")
                amount.grid(row=5,column=0,padx=5,pady=5,sticky=W)
                
                orderDate = departDate.copy()
                orderDate.sort()
                earliest = orderDate[0]
                today = datetime.date.today()

                self.tdelta = earliest - today
            
                if self.tdelta.days < 1:
                    percent = 0
                elif self.tdelta.days >= 1 and self.tdelta.days <=7:
                    percent = 0.5
                else:
                    percent = 0.8

                refund = (cost*percent)-50
                if refund < 0:
                    refund = 0

                self.newCost = cost - refund
                
                self.rfiv = IntVar()
                self.rfiv.set(refund)
                self.rfE = Entry(self.rootWinC,textvariable=self.rfiv,width=15)
                self.rfE.grid(row=5,column=1,padx=5,pady=5,sticky=W)

            #navigation buttons
                
                back = Button(self.rootWinC,text="Back",command=self.backToID)
                back.grid(row=6,column=0,padx=10,pady=15,sticky=W)

                search = Button(self.rootWinC,text="Submit",command=self.submitCancel)
                search.grid(row=6,column=2,padx=10,pady=15,sticky=E)

                cursor.close()
                db.commit()
                db.close()

    def backToID(self):
        self.rootWinC.withdraw()
        self.rootWinCR.deiconify()
    
    def submitCancel(self):
        if self.tdelta.days < 1:
            r = messagebox.showerror("Error!","Reservations cannot be cancelled within one day of earliest departure.")
        else:
            resID = self.rIDE.get()
            db = self.connect()
            cursor = db.cursor()
            
            self.newCost = str(self.newCost)
            newCost = self.newCost[:len(self.newCost)-2]

            sql = "UPDATE Reservation SET isCancelled = True, TotalCost="+newCost+" WHERE Reservation.ReservationID = "+resID
            cursor.execute(sql)

            cursor.close()
            db.commit()
            db.close()

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
        username = self.uEntry.get()
        trainNum = self.tNRE.get()
        rating = self.rating.get()
        comment = self.comE.get()

        db = self.connect()
        cursor = db.cursor()
        
        if trainNum == "":
            r = messagebox.showerror("Error!","Please enter a train number.")
        elif rating == "":
            r = messagebox.showerror("Error!","Please select a rating.")
        #check if train number is not available in database
        else:
            sql = "SELECT TrainNumber FROM TrainRoute WHERE TrainNumber ="+trainNum
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                r = messagebox.showerror("Error!","This train number is unavailable.")
            #add rating to database
            else:
                if rating == "Very Good":
                    rating = 5
                elif rating == "Good":
                    rating = 4
                elif rating == "Neutral":
                    rating = 3
                elif rating == "Bad":
                    rating = 2
                else:
                    rating = 1
                if comment == "":
                    comment = "NULL"
                else:
                    comment = "'"+comment+"'"
                sql2 = "INSERT INTO Review (ReviewNumber,Comment,Rating,TrainNumber,Username) VALUES (NULL,"+comment+","+str(rating)+","+trainNum+",'"+username+"')"
                cursor.execute(sql2)
                
            cursor.close()
            db.commit()
            db.close()
            self.rootWinGR.withdraw()
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
        self.rootWinVR.withdraw()
        self.rootWinCF.deiconify()

    def reviewTable(self):
        tNum = self.tNVRE.get()
        self.rootWinRT = Toplevel()
        self.rootWinRT.title("View Review")
        self.rootWinVR.withdraw()

        pic = Label(self.rootWinRT,image=self.image)
        pic.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        v = Label(self.rootWinRT,text="View Review",font=("Calibri",15,"bold"),fg="gold")
        v.grid(row=1,column=0,columnspan=2,pady=5)

        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT Review.Comment, Review.Rating FROM Review WHERE Review.TrainNumber = "+tNum
        cursor.execute(sql)
        results = cursor.fetchall()
        
        cursor.close()
        db.commit()
        db.close()

        comments,ratings = zip(*results)
        comments = list(comments)
        ratings = list(ratings)

        for each in ratings:
            if each == 5:
                each = "Very Good"
            elif each == 4:
                each = "Good"
            elif each == 3:
                each = "Neutral"
            elif each == 2:
                each = "Bad"
            else:
                each = "Very Bad"

        frame = Frame(self.rootWinRT)
        frame.grid(row=2,column=0,padx=5,pady=5)

        Label(frame,text="Rating",bg="gold").grid(row=0,column=0,sticky=W)
        Label(frame,text="Comment",bg="gold",width=20).grid(row=0,column=1,sticky=W)

        for i in range(0,len(ratings)):
            Label(frame,text=ratings[i]).grid(row=i+1,column=0)
        for i in range(0,len(comments)):
            Label(frame,text=comments[i]).grid(row=i+1,column=1,sticky=W)

        back = Button(self.rootWinRT,text="Back to Choose Functionality",command=self.backReviewTable)
        back.grid(row=3,column=0,columnspan=2,padx=10,pady=15)

    def backReviewTable(self):
        self.rootWinRT.withdraw()
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

        small = Label(self.rootWin4,text="Your school email address must end with .edu",font=("Calibri",8))
        small.grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        back = Button(self.rootWin4,text="Back",command=self.backSchool)
        back.grid(row=4,column=0,padx=10,pady=15,sticky=W)

        submit = Button(self.rootWin4,text="Submit",command=self.submitSchool)
        submit.grid(row=4,column=1,padx=10,pady=15,sticky=E)

    def backSchool(self):
        self.rootWin4.withdraw()
        self.rootWinCF.deiconify()

    def submitSchool(self):
        username = self.uEntry.get()
        schoolEmail = self.seE.get()
        
        if schoolEmail.endswith(".edu") == True:
            db = self.connect()
            cursor = db.cursor()

            sql = "UPDATE Customer SET isStudent = TRUE WHERE  Username = '"+username+"'"
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()
            
            self.rootWin4.withdraw()
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

        rev = Button(self.rootWinMF,text="View revenue report",fg="blue",command=self.viewRevenue)
        rev.grid(row=2,column=0,columnspan=2,pady=5)
        
        route = Button(self.rootWinMF,text="View popular route report",fg="blue",command=self.viewPopular)
        route.grid(row=3,column=0,columnspan=2,pady=5)

        logout = Button(self.rootWinMF,text="Log out",command=self.logoutMF)
        logout.grid(row=4,column=1,padx=5,pady=10,sticky=E)

    def logoutMF(self):
        self.rootWinMF.withdraw()
        self.rootWin.deiconify()
    
        
######## VIEW REVENUE REPORT ########

    def viewRevenue(self):
        self.rootWinRev = Toplevel()
        self.rootWinRev.title("Manager")
        self.rootWinMF.withdraw()

        c = Label(self.rootWinRev,text="View Revenue Report",font=("Calibri",15,"bold"),fg="gold")
        c.grid(row=1,column=0,columnspan=2,padx=10,pady=5)

        db = self.connect()
        cursor = db.cursor()

        sql = "SELECT MONTH(Reserves.DepartureDate) AS Month, SUM(Reservation.TotalCost) as Revenue FROM Reservation JOIN Reserves ON Reservation.ReservationID = Reserves.ReservationID GROUP BY MONTH(Reserves.DepartureDate) LIMIT 3"
        cursor.execute(sql)
        results = cursor.fetchall()

        months,revenue = zip(*results)
        months = list(months)
        revenue = list(revenue)

        frame = Frame(self.rootWinRev)
        frame.grid(row=2,column=0,padx=5,pady=5)
        
        Label(frame,text="Month",bg="gold",width=10).grid(row=0,column=0)
        Label(frame,text="Revenue",bg="gold",width=10).grid(row=0,column=1,sticky=W)
        
        possible = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        for i in range(0,len(months)):
            months[i] = possible[months[i]-1]
            Label(frame,text=months[i]).grid(row=i+1,column=0,sticky=W)
        for i in range(0,len(revenue)):
            Label(frame,text="%.2f"%revenue[i]).grid(row=i+1,column=1,sticky=W)

        b = Button(self.rootWinRev,text="Back",command=self.backRMgr)
        b.grid(row=3,column=0,padx=10,pady=15)

    def backRMgr(self):
        self.rootWinRev.withdraw()
        self.rootWinMF.deiconify()

######## VIEW POPULAR ROUTE REPORT ########

    def viewPopular(self):
        self.rootWinPop = Toplevel()
        self.rootWinPop.title("Manager")
        self.rootWinMF.withdraw()

        c = Label(self.rootWinPop,text="View Popular Route Report",font=("Calibri",15,"bold"),fg="gold")
        c.grid(row=0,column=0,columnspan=2,pady=5)

        frame = Frame(self.rootWinPop)
        frame.grid(row=1,column=0,padx=5,pady=5)
            
        Label(frame,text="Month",bg="gold",width=10).grid(row=0,column=0,sticky=W)
        Label(frame,text="Train Number",bg="gold",width=10).grid(row=0,column=1,sticky=W)
        Label(frame,text="# of Reservations",bg="gold",width=10).grid(row=0,column=2,sticky=W)
            
        today = datetime.date.today()
        if today.month != 1:
            month3 = datetime.date(today.year,today.month-1,today.day).month
        else:
            month3 = datetime.date(today.year-1,12,today.day).month
            
        if today.month == 2:
            month2 = datetime.date(today.year-1,12,today.day).month
        elif today.month == 1:
            month2 = datetime.date(today.year-1,11,today.day).month
        else:
            month2 = datetime.date(today.year,today.month-2,today.day).month
            
        if today.month == 3:
            month1 = datetime.date(today.year-1,12,today.day).month
        if today.month == 2:
            month1 = datetime.date(today.year-1,11,today.day).month
        if today.month == 1:
            month1 = datetime.date(today.year-1,10,today.day).month
        else:
            month1 = datetime.date(today.year,today.month-3,today.day).month

        db = self.connect()
        cursor = db.cursor()

        months = [month1,month2,month3]

        #month 1
        sql = "SELECT MONTH(Reserves.DepartureDate) AS Month, Reserves.TrainNumber AS TrainNumber, COUNT(Reserves.TrainNumber) AS ReserveNum FROM Reservation JOIN Reserves ON Reservation.ReservationID = Reserves.ReservationID WHERE MONTH(Reserves.DepartureDate) = "+str(months[0])+" GROUP BY Reserves.TrainNumber HAVING COUNT(Reserves.TrainNumber) > 0 ORDER BY ReserveNum DESC LIMIT 3"
        cursor.execute(sql)
        results = cursor.fetchall()
        trains = []
        for j in results:
            trains.append(list(j))

        mons = []
        trainNums = []
        resNums = []
        for each in trains:
            mons.append(each[0])
            trainNums.append(each[1])
            resNums.append(each[2])

        possible = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        mons[0] = possible[months[0]-1]
        Label(frame,text=mons[0],width=10).grid(row=1,column=0)
        for j in range(0,len(trainNums)):
            Label(frame,text=trainNums[j],width=10).grid(row=j+1,column=1)
        for j in range(0,len(resNums)):
            Label(frame,text=resNums[j],width=10).grid(row=j+1,column=2)

        #month 2
        sql2 = "SELECT MONTH(Reserves.DepartureDate) AS Month, Reserves.TrainNumber AS TrainNumber, COUNT(Reserves.TrainNumber) AS ReserveNum FROM Reservation JOIN Reserves ON Reservation.ReservationID = Reserves.ReservationID WHERE MONTH(Reserves.DepartureDate) = "+str(months[1])+" GROUP BY Reserves.TrainNumber HAVING COUNT(Reserves.TrainNumber) > 0 ORDER BY ReserveNum DESC LIMIT 3"
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        trains2 = []
        for j in results2:
            trains2.append(list(j))

        mons2 = []
        trainNums2 = []
        resNums2 = []
        for each in trains2:
            mons2.append(each[0])
            trainNums2.append(each[1])
            resNums2.append(each[2])

        frame2 = Frame(self.rootWinPop)
        frame2.grid(row=2,column=0,padx=5,pady=5)
        
        mons2[0] = possible[months[1]-1]
        Label(frame2,text=mons2[0],width=10).grid(row=1,column=0)
        for j in range(0,len(trainNums2)):
            Label(frame2,text=trainNums2[j],width=10).grid(row=j+1,column=1)
        for j in range(0,len(resNums2)):
            Label(frame2,text=resNums2[j],width=10).grid(row=j+1,column=2)

        #month 3
        sql3 = "SELECT MONTH(Reserves.DepartureDate) AS Month, Reserves.TrainNumber AS TrainNumber, COUNT(Reserves.TrainNumber) AS ReserveNum FROM Reservation JOIN Reserves ON Reservation.ReservationID = Reserves.ReservationID WHERE MONTH(Reserves.DepartureDate) = "+str(months[2])+" GROUP BY Reserves.TrainNumber HAVING COUNT(Reserves.TrainNumber) > 0 ORDER BY ReserveNum DESC LIMIT 3"
        cursor.execute(sql3)
        results3 = cursor.fetchall()
        trains3 = []
        for j in results3:
            trains3.append(list(j))

        mons3 = []
        trainNums3 = []
        resNums3 = []
        for each in trains3:
            mons3.append(each[0])
            trainNums3.append(each[1])
            resNums3.append(each[2])

        frame3 = Frame(self.rootWinPop)
        frame3.grid(row=3,column=0,padx=5,pady=5)
        
        mons3[0] = possible[months[2]-1]
        Label(frame3,text=mons3[0],width=10).grid(row=1,column=0)
        for j in range(0,len(trainNums3)):
            Label(frame3,text=trainNums3[j],width=10).grid(row=j+1,column=1)
        for j in range(0,len(resNums3)):
            Label(frame3,text=resNums3[j],width=10).grid(row=j+1,column=2)

        b = Button(self.rootWinPop,text="Back",command=self.backPMgr)
        b.grid(row=4,column=0,padx=10,pady=15)

    def backPMgr(self):
        self.rootWinPop.withdraw()
        self.rootWinMF.deiconify()

     
win = Tk()
app = GUI(win)
win.mainloop()
