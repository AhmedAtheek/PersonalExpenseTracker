import customtkinter as ctk
from SETTINGS import *
import datetime
from datetime import datetime
from datetime import date, timedelta
from DataBaseManager import DataBaseManager as DBM
import sqlite3
import csv
from App import MonthlyCategories
import tkcalendar as tkc
from PIL import  Image
from collections import deque
from tkinter.filedialog import asksaveasfilename as askSave


database = "expenses.db"

class ExpenseEntry(ctk.CTkFrame):
    def __init__(self, parent, dbmanager : DBM, monthlyCategories : MonthlyCategories):
        super().__init__(master=parent, fg_color= TERTIARY_RED, width=380,height=700-53,corner_radius=0)
        
        """
            Entry Manager

            All settings in the infoframe
        
        """
        
        self.dbManager : DBM = dbmanager
        
        #TITLE
        titleFrame = ctk.CTkFrame(self,fg_color=PRIMARY_RED, width=379, height=70, corner_radius=0)
        titleFont = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight="bold")
        title =ctk.CTkLabel(titleFrame, text="Expense Entry", font=titleFont)
        
        infoFrame = ctk.CTkFrame(self, fg_color=TERTIARY_RED, width=379, height=470, corner_radius=0)
        infoFrame.pack_propagate(False)
        
        Infoframe(parent=infoFrame, dbmanager=self.dbManager, monthlyCategories=monthlyCategories)
        
        #configure
        
        self.columnconfigure(0,weight=1) #column
        
        self.rowconfigure(0, weight=1) #row
        self.rowconfigure(1, weight=50)
        
        #packing
        titleFrame.grid(row =0, column = 0,sticky = "new")
        title.pack(expand = "True", fill = "both", padx =5, pady= 5)
        infoFrame.grid(row = 1,column = 0 ,sticky = "nsew")
    

class ExpenseHistory(ctk.CTkFrame):
    def __init__(self, parent, dbManager : DBM, monthlyCategories : MonthlyCategories):
        super().__init__(master=parent, fg_color= TERTIARY_RED, width=380,height=700-53)
        
        self.dbManager : DBM = dbManager
        self.monthlyCategories = monthlyCategories
        
        self.dateFormat : str = "%m/%d/%Y"
        
        titleFrame   = ctk.CTkFrame(self,fg_color=PRIMARY_RED, width=379, height=70, corner_radius=0)
        titleFont = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight="bold")
        title =ctk.CTkLabel(titleFrame, text="History", font=titleFont)
        
        infoFrame = ctk.CTkFrame(self, fg_color=TERTIARY_RED, width=379, height=470, corner_radius=0)
        infoFrame.grid_propagate(False)

        
        infoFrame.grid_columnconfigure((0,1,2,3,4), weight=1)
        infoFrame.rowconfigure(0, weight=1)
        infoFrame.rowconfigure(1, weight=5)
        
        
        
        dateFont = ctk.CTkFont(family=FONT,size=MEDIUM_SIZE,weight="bold")

        startDateLabel = ctk.CTkLabel(master=infoFrame, text="Start: ", text_color=BLACK,font=dateFont)
        self.startDate = tkc.DateEntry(master=infoFrame, width = 15, fg_color = TERTIARY_RED)
        self.startDateStr = ctk.StringVar(value=self.startDate.get_date().strftime(self.dateFormat))
        
        self.startDate.bind("<<DateEntrySelected>>", lambda _ : self.updateDates(dateEntry=self.startDate,dateVar=self.startDateStr))
        
        endDateLabel = ctk.CTkLabel(master=infoFrame, text="End: ", text_color=BLACK,font=dateFont)
        self.endDate = tkc.DateEntry(master=infoFrame, width = 15, fg_color = TERTIARY_RED)
        self.endDateStr = ctk.StringVar(value=self.endDate.get_date().strftime(self.dateFormat))
        
        self.endDate.bind("<<DateEntrySelected>>", lambda _ : self.updateDates(dateEntry=self.endDate,dateVar=self.endDateStr))
        
        undoImage = Image.open(UNDO_IMAGE_PATH)
        undoImage = ctk.CTkImage(dark_image=undoImage, size=(25,25))
                
        undoButton = ctk.CTkButton(master=infoFrame, 
                                   width=25,height=20, 
                                   command=lambda :self.undoCall(), 
                                   text="", corner_radius=5,
                                   hover_color=TERTIARY_RED,
                                   fg_color=TERTIARY_RED,
                                   image=undoImage
                                   )
                
        #configure
        self.columnconfigure(0,weight=1) #column
        
        self.rowconfigure(0, weight=1) #row
        self.rowconfigure(1, weight=60)
        
        #packing
        startDateLabel.grid(row= 0, column = 0, sticky= "w", padx = 10)
        self.startDate.grid(row=0, column = 1, sticky= "w")
        
        endDateLabel.grid(row = 0, column = 2, sticky= "w")
        self.endDate.grid(row=0, column = 3, sticky= "w")
        
        self.scrollableFrame = ScrollableFrame(infoFrame, self.startDateStr.get(), self.endDateStr.get(), dbManager=self.dbManager, monthlyCategories=monthlyCategories)
        
        titleFrame.grid(row =0, column = 0,sticky = "new")
        title.pack(expand = "True", fill = "both", padx =5, pady= 5)
        
        undoButton.grid(row = 0, column = 4, sticky = "w")
        
        infoFrame.grid(row = 1,column = 0 ,sticky = "nsew")     
        
    def updateDates(self, dateVar : ctk.StringVar, dateEntry : tkc.DateEntry):
        dateVar.set(dateEntry.get_date().strftime(self.dateFormat))
        
        self.scrollableFrame.UpdateExpenseHistory(startdate=self.startDateStr.get(), enddate=self.endDateStr.get())
        
        
    def undoCall(self):
        
        data = self.scrollableFrame.buffer.getCurrentState()
        
        print(data)
        
        if self.scrollableFrame.buffer.getCurrentState() == None:
            pass
        else:

            self.dbManager.addExpense("INSERT INTO expenses VALUES ('{}','{}','{}','{}','{}')"
                                        .format(data[0], data[2], data[1], data[3], data[4]))

            self.monthlyCategories.callUpdate() 
            self.scrollableFrame.buffer.undo()
    
        self.scrollableFrame.UpdateExpenseHistory(startdate=self.startDateStr.get(), enddate=self.endDateStr.get())
        
        
       
class TrackerFrame(ctk.CTkFrame):
    def __init__(self, parent, ):
        super().__init__(master=parent, fg_color= TERTIARY_RED, width=380,height=700-53)
        
        titleFrame = ctk.CTkFrame(self,fg_color=PRIMARY_RED, width=379, height=70, corner_radius=0)
        titleFont = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight="bold")
        title =ctk.CTkLabel(titleFrame, text="Transfer", font=titleFont)
        
        infoFrame = ctk.CTkFrame(self, fg_color=TERTIARY_RED, width=379, height=470, corner_radius=0)
        
        self.columnconfigure(0,weight=1) #column
        
        self.rowconfigure(0, weight=1) #row
        self.rowconfigure(1, weight=2)
        
        
        
        #packing
        titleFrame.grid(row =0, column = 0,sticky = "new")
        title.pack(expand = "True", fill = "both", padx =5, pady= 5)
        infoFrame.grid(row = 1,column = 0 ,sticky = "nsew")
               
class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, dbManager :DBM ):
        super().__init__(master=parent, fg_color= TERTIARY_RED, width=380,height=700-53)
        
        
        self.dbManager =dbManager
        
        titleFrame = ctk.CTkFrame(self,fg_color=PRIMARY_RED, width=379, height=70, corner_radius=0)
        titleFont = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight="bold")
        title =ctk.CTkLabel(titleFrame, text="Settings", font=titleFont)
        
        infoFrame = ctk.CTkFrame(self, fg_color=TERTIARY_RED, width=379, height=470, corner_radius=0)
        infoFrame.pack_propagate(False)
        
        ExportCsv(infoFrame, self.dbManager)
        
        self.columnconfigure(0,weight=1) #column
        
        self.rowconfigure(0, weight=1) #row
        self.rowconfigure(1, weight=10)
        
        #packing
        titleFrame.grid(row =0, column = 0,sticky = "new")
        title.pack(expand = "True", fill = "both", padx =5, pady= 5)
        infoFrame.grid(row = 1,column = 0 ,sticky = "nsew")

class ExportCsv(ctk.CTkFrame):
    def __init__(self, parent, dbManger : DBM):
        super().__init__(master=parent, fg_color=SECONDARY_RED, height=50)
        #self.pack_propagate(False)
        #Button and Arrow
        #Button
        self.dbManager = dbManger
        self.isActive = False
        
        #Images
        Arrow = Image.open(ARROW_PATH)
        ArrowImage = ctk.CTkImage(dark_image=Arrow, size=(12, 12))
        
        selectionFont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE, weight="bold")
        csvExportDropdownButton = ctk.CTkButton(self, text="Export CSV", anchor="w", command=lambda : self.csvDropdown(), height=25,
                                                fg_color=SECONDARY_RED, 
                                                corner_radius=5,
                                                text_color=WHITE,
                                                font=selectionFont,
                                                hover_color= SECONDARY_RED, image=ArrowImage)
        
        csvExportDropdownButton.pack(fill = "both", expand = True, padx = 10, pady= 5)
        
        #Settings csv
        self.csvSettingsFrame = ctk.CTkFrame(self, height=150, fg_color=SECONDARY_RED, corner_radius=10 )
        self.csvSettingsFrame.pack_propagate(False)
        
        titleFont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE, weight="bold")
        #Title Label 
        exportMonthlyTitle = ctk.CTkLabel(self.csvSettingsFrame, text="Export Monthly Income Statement :", font=titleFont, text_color=BLACK)
        
        selectionFrame = ctk.CTkFrame(self.csvSettingsFrame, fg_color=SECONDARY_RED)
        monthTitle = ctk.CTkLabel(selectionFrame, text="Month:", font=titleFont, text_color=BLACK)
        yearTitle = ctk.CTkLabel(selectionFrame, text="Year:", font=titleFont, text_color=BLACK)
        
        
        
        # selection Settings
        self.months = ["Jan" ,"Feb","Mar","Apr","May","Jun","Jul","Aug","Sep" ,"Oct" ,"Nov" ,"Dec"]
        
        
        availableYears = self.dbManager.getExpense(""" SELECT DISTINCT SUBSTR(DATE, 7, 4) AS year FROM {}  """.format(self.dbManager.dbName[:-3]))
        self.monthstr = ctk.StringVar(value=self.months[datetime.now().month-1])
        monthsDropdown = ctk.CTkComboBox(selectionFrame,
                                     values=self.months,height=22,
                                     width=100, 
                                     command=lambda _: print(_), 
                                     variable=self.monthstr,
                                     fg_color=TERTIARY_RED,button_color=PRIMARY_RED, 
                                     text_color=BLACK, border_color=PRIMARY_RED, 
                                     button_hover_color=GRAY,
                                     dropdown_fg_color=SECONDARY_RED,
                                     dropdown_text_color=BLACK,
                                     dropdown_hover_color=TERTIARY_RED,
                                     font=selectionFont,
                                     dropdown_font=selectionFont,
                                     justify="center",
                                     corner_radius=10,
                                     )
        
        self.yearstr = ctk.StringVar(value=str(datetime.now().year))
        yearDropdown = ctk.CTkComboBox(selectionFrame,
                                        width=100,height=22,
                                     values=[year[0] for year in availableYears], 
                                     command=lambda _: print(_), 
                                     variable=self.yearstr,
                                     fg_color=TERTIARY_RED,button_color=PRIMARY_RED, 
                                     text_color=BLACK, border_color=PRIMARY_RED, 
                                     button_hover_color=GRAY,
                                     dropdown_fg_color=SECONDARY_RED,
                                     dropdown_text_color=BLACK,
                                     dropdown_hover_color=TERTIARY_RED,
                                     font=selectionFont,
                                     dropdown_font=selectionFont,
                                     justify="center",
                                     corner_radius=10,
                                     )
        
        exportButton = ctk.CTkButton(self.csvSettingsFrame, text="Export",command= lambda : self.exportCSV(self.monthstr.get(), self.yearstr.get()),
                                     fg_color=PRIMARY_RED, 
                                     corner_radius=5,
                                     text_color=WHITE,
                                     font=selectionFont,
                                     height= 20,
                                     hover_color= TERTIARY_RED)
        
        monthTitle.grid(row = 0, column = 0, padx = 10, sticky = "w")
        monthsDropdown.grid(row = 0, column = 1, padx = 5, sticky = "we")
        yearTitle.grid(row = 1, column = 0, padx = 10, sticky = "w")
        yearDropdown.grid(row = 1, column = 1, padx = 5, sticky = "we")
        
        exportMonthlyTitle.pack(padx = 20, pady = 20, fill = "x")  
        selectionFrame.pack(fill = "x")
        exportButton.pack(side = "left", fill = "x", padx =10)
        self.pack(fill = "x", padx = 10, pady =10)    
    
    def csvDropdown(self):
        if not self.isActive:
            self.isActive = True
            self.csvSettingsFrame.pack(fill = "x", )
        else:
            self.isActive = False
            self.csvSettingsFrame.pack_forget()
        
    def exportCSV(self, month : str, year : str):
        fileTypes = [("CSV", "*.csv"),("All Files", "*.*") ]
        
        monthStringNumber = str(self.months.index(month) + 1).zfill(2)
        
        data = self.dbManager.getExpense(f"SELECT * FROM {self.dbManager.dbName[:-3]} WHERE SUBSTR(DATE, 1, 2) = '{monthStringNumber}' AND SUBSTR(DATE, -4) = '{year}'")
        print(data)
        
        file = askSave(filetypes=fileTypes, defaultextension="*.csv", title="Save as CSV")
        try:
            with open(file=file, mode="w", newline="") as file:
                headers = ["Date", "ExpenseName", "Amount", "Type", "Currency"]

                writer = csv.writer(file)
                writer.writerow(headers)

                for row in data:
                    writer.writerow(row)
        except:
            pass
            
    def exportAll (self):
        pass
        
        
        
    
class Infoframe(ctk.CTkFrame):

    def __init__(self, parent, dbmanager : DBM, monthlyCategories : MonthlyCategories):
        super().__init__(master=parent, fg_color=SECONDARY_RED, corner_radius=20, width=310, height=600, )
        
        """
            Holds all the widgets for the entry
        
        """
        
        self.dbManager : DBM = dbmanager
        self.monthlyCategories = monthlyCategories
        
        dateFormat : str = "%m/%d/%Y"
        self.expenseTypes : list[str] = ["GROCERIES", "UTILITIES", "FOOD", "GENERAL", "TRANSPORT"]
        self.currencyTypes : list[str] = ["MYR", "USD", "MVR"]
        
        spacing1 = ctk.CTkLabel(self, text="")
        spacing2 = ctk.CTkLabel(self, text="")
        
        #dateFrame
        dateFrame = ctk.CTkFrame(self, fg_color=TERTIARY_RED, corner_radius=10, width=130, height=40)
        
        
        dateFont = ctk.CTkFont(family=FONT, weight="bold", size=CATEGORY_FONT_SIZE)
        
        calendar = tkc.DateEntry(master=dateFrame, width = 10, fg_color = TERTIARY_RED)
        self.datestr = ctk.StringVar(value=calendar.get_date().strftime(dateFormat))
        
        date = ctk.CTkLabel(master=dateFrame, 
                            text=f'{calendar.get_date().strftime(dateFormat)}', 
                            text_color=BLACK,font=dateFont,textvariable=self.datestr)
        
        
        
        LabelFont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE, weight="bold")
        nameLabel = ctk.CTkLabel(self, text="Name: ", font=LabelFont, text_color=BLACK, )
        
        entryFont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE, weight="bold")

        self.expenseName = ctk.StringVar()
        expenseNameEntry = ctk.CTkEntry(master=self, fg_color=TERTIARY_RED, text_color=BLACK, border_width=0, font=entryFont, textvariable=self.expenseName)
        expenseNameEntry.bind(sequence="<Return>", command=lambda event: print(self.expenseName.get())) #need to change
    
        self.expenseAmount = ctk.StringVar()
        amountLabel = ctk.CTkLabel(self, text="Amount: ", font=LabelFont, text_color=BLACK)
        expenseAmountEntry = ctk.CTkEntry(master=self, fg_color=TERTIARY_RED, text_color=BLACK, 
                                          border_width=0, font=entryFont, textvariable=self.expenseAmount)
        
        
        self.currency = ctk.StringVar(value=self.currencyTypes[0])
        currencyDropdown = ctk.CTkComboBox(self,values=self.currencyTypes,
                                            width=300,
                                            fg_color=TERTIARY_RED,button_color=PRIMARY_RED, 
                                            text_color=BLACK, border_color=PRIMARY_RED, 
                                            button_hover_color=SECONDARY_RED,
                                            dropdown_fg_color=TERTIARY_RED,
                                            dropdown_text_color=BLACK,
                                            dropdown_hover_color=SECONDARY_RED,
                                            font=entryFont,
                                            dropdown_font=entryFont,
                                            justify="center",
                                            corner_radius=10,
                                            variable=self.currency,
                                            command=lambda event : print(self.currency.get())
                                            )
        self.expenseType = ctk.StringVar(value=self.expenseTypes[0])
        expenseTypeDropdown = ctk.CTkComboBox(self, values=self.expenseTypes,
                                              width=300,                                  
                                              fg_color=TERTIARY_RED,button_color=PRIMARY_RED, 
                                              text_color=BLACK, border_color=PRIMARY_RED, 
                                              button_hover_color=SECONDARY_RED,
                                              dropdown_fg_color=TERTIARY_RED,
                                              dropdown_text_color=BLACK,
                                              dropdown_hover_color=SECONDARY_RED,
                                              font=entryFont,
                                              dropdown_font=entryFont,
                                              justify="center",
                                              corner_radius=10,
                                              variable=self.expenseType,
                                              command=lambda event : print(self.expenseType.get())
                                              )
        
        submitButton = ctk.CTkButton(self, text='SUBMIT', command=lambda: self.submitData(), 
                                     fg_color=PRIMARY_RED, 
                                     corner_radius=15,
                                     text_color=WHITE,
                                     font=LabelFont,
                                     height= 40,
                                     hover_color= TERTIARY_RED)
 
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        self.rowconfigure(0, weight=1)
        
        self.rowconfigure(1, weight=2)
        
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
    
        self.rowconfigure(6, weight=3)
    
        self.rowconfigure(7, weight=1)
        
        spacing1.grid(row = 1, column = 0, columnspan =2, sticky = "nsew", pady = 10)
        spacing2.grid(row = 6, column = 0, columnspan =2, sticky = "nsew", pady = 10)
        
        dateFrame.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew", padx =60, pady = 10)
        date.pack(padx =30, pady= 5)
        
        calendar.pack(pady = 5, padx = 10, expand = True)
        
        expenseNameEntry.grid(row= 2, column = 1, padx =10, pady = 5,sticky ="we")
        nameLabel.grid(row = 2, column =0, padx =10, pady = 5, sticky ="w")
        
        expenseAmountEntry.grid(row= 3, column = 1, padx =10, pady = 5,sticky ="we")
        amountLabel.grid(row = 3, column =0, padx =10, pady = 5,sticky ="w")
        
        currencyDropdown.grid(row = 4, column = 0, columnspan = 2, padx =10, pady = 5)
        expenseTypeDropdown.grid(row = 5, column = 0, columnspan = 2,padx =10, pady = 5)
        
        submitButton.grid(row = 7, column = 0, columnspan = 2, sticky ="nsew", padx =20, pady =20)
        
        calendar.bind("<<DateEntrySelected>>", lambda _ : self.datestr.set(calendar.get_date().strftime(dateFormat)))
        
        # self.place(relx =0.5, rely =0.5, anchor = "center",)
        self.pack_propagate(False)
        self.pack(fill = "both", expand = True, padx= 30, pady =30)
       
        
        
    def submitData(self):
        
        def resetValues():
            self.expenseName.set(value="")
            self.expenseAmount.set(value="")
            self.expenseType.set(value=self.expenseTypes[0])
            self.currency.set(value=self.currencyTypes[0])
        
        def handleResult(isConfirm : bool):
            if isConfirm:
                expenseName = self.expenseName.get()
                expenseAmount = float(self.expenseAmount.get())
                expenseType = self.expenseType.get()
                expenseCurrency = self.currency.get()
                
                date = self.datestr.get()

                self.dbManager.addExpense("INSERT INTO expenses VALUES ('{}','{}','{}','{}','{}')"
                          .format(date, expenseName, expenseAmount, expenseType, expenseCurrency))
                
                resetValues()
                self.monthlyCategories.callUpdate()
                
                #Update The Graphs, The total Expenditure
                    
                    
                
            else:
                resetValues()
        

        
        expenseName = self.expenseName.get().strip()  # Strip whitespace from name
        try:
            if not expenseName:
                raise ValueError("Name cannot be empty")
            expenseAmount = float(self.expenseAmount.get())  # Try converting to float
            confiramtionDialogue(mainwindow=self, callbackFunc=handleResult)
        except ValueError as e:
            ErrorMessage(parent=self, text=f"CANNOT SUBMIT:\n -{e}")
            resetValues()

                
                
        
        # if expenseName == "":
        #     ErrorMessage(parent=self, text="-CANNOT SUBMIT BLANK VALUES\n -ENSURE THE AMOUNT IS A NUMBER")
        #     resetValues()
        #     print(expenseAmount)
        # else:
        #     confiramtionDialogue(mainwindow=self, callbackFunc=handleResult)
        
class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, startdate, enddate, dbManager : DBM, monthlyCategories : MonthlyCategories):
        super().__init__(master=parent, scrollbar_button_color=SECONDARY_RED, 
                                                 fg_color=TERTIARY_RED,
                                                 scrollbar_button_hover_color= GRAY,)
        
        self.dbManager : DBM = dbManager 
        self.monthlyCategories = monthlyCategories
        
        self.startDate : str  = startdate
        self.endDate : str = enddate
        
        self.UpdateExpenseHistory(self.startDate, self.endDate)

        self.buffer = UndoBuffer(None, maxlength=10)
        
        self.grid(row = 1, column =0, sticky = "nsew",padx =2, pady= 2, columnspan = 5)
        

    def UpdateExpenseHistory(self, startdate, enddate):
        
        datelist : list[str] =[]
        
        startdate : str = datetime.strptime(startdate, '%m/%d/%Y')
        enddate : str = datetime.strptime(enddate, '%m/%d/%Y')
        
        delta = enddate-startdate
        
        if delta < timedelta(0):
            ErrorMessage(self,"ENTER AN APPROPRIATE DATE RANGE")
        else:
            
            for widgets in self.winfo_children():
                widgets.destroy()
            
            for i in range(delta.days + 1):
                day = startdate + timedelta(days=i)
                datelist.append(day.strftime('%m/%d/%Y'))

            for i in range(len(datelist)):
                
                # c.execute("SELECT * FROM expenses WHERE DATE = '{}'".format(datelist[i]))
                # expenseList = c.fetchall()
                
                expenseList = self.dbManager.getExpense("SELECT * FROM expenses WHERE DATE = '{}'".format(datelist[i]))
                
                for i in range(len(expenseList)):
                    ExpenseHistoryDisplays(self,date=expenseList[i][0], 
                                           expensename=expenseList[i][1], 
                                           amount=expenseList[i][2], 
                                           type=expenseList[i][3],
                                           currency=expenseList[i][4],parentclass=self, monthlyCategories=self.monthlyCategories, dbManager=self.dbManager)
                
            self.monthlyCategories.callUpdate()        
           
    
class ExpenseHistoryDisplays (ctk.CTkFrame):
    def __init__(self, parent,date, amount, expensename, type, currency, parentclass, monthlyCategories: MonthlyCategories, dbManager : DBM):
        super().__init__(master=parent, corner_radius=10, fg_color=WHITE, height=80)
        
        self.dbManager = dbManager
        
        self.date = date
        self.amount = amount
        self.expensename = expensename
        self.type = type
        self.currency = currency
        self.parentclass = parentclass
        
        self.monthlyCat = monthlyCategories
        
        #fonts
        labelSubfont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE,weight="bold")
        labelMainfont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE,weight="bold")
        
        #labels
        labelDateTitle = ctk.CTkLabel(master=self, text="Date:", text_color= BLACK, font=labelSubfont )
        labelTypeTitle = ctk.CTkLabel(master=self, text="Type:", text_color= BLACK, font=labelSubfont )
        labelExpenseDate = ctk.CTkLabel(master=self, text=date, text_color= GRAY, font=labelSubfont )
        labelExpenseType = ctk.CTkLabel(master=self, text=type, text_color= GRAY, font=labelSubfont )
        
        exitButton = ctk.CTkButton(master=self, text="x", width=5, height=2, fg_color=WHITE, 
                                   text_color=BLACK, 
                                   hover_color=WHITE, 
                                   command=self.removeDisplay,
                                   corner_radius=20)
        
        
        expenseNameLabel = ctk.CTkLabel(master=self, text=expensename, font=labelMainfont, text_color=BLACK)
        expenseAmountLabel = ctk.CTkLabel(master=self, text=f"{amount} {currency}", font=labelMainfont, text_color=BLACK)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        
        self.columnconfigure((0,1,2,3), weight=1)
       
        labelDateTitle.grid(column= 0, row = 0, pady =5, padx =2, sticky = "w")
        labelExpenseDate.grid(row= 0, column = 1, sticky = "w")
        
        labelTypeTitle.grid(row = 0, column = 2, padx =2,sticky ="w")
        labelExpenseType.grid(row = 0, column = 3,padx =5, sticky = "w")
        
        expenseNameLabel.grid(row = 1, column= 0, columnspan = 2,padx =10, pady= 5, sticky ="w")
        expenseAmountLabel.grid(row = 1, column= 2, padx = 10, sticky ="e",columnspan = 2)
        
        exitButton.place(relx = 1, rely = 0, anchor = "ne")
        exitButton.lift()
        
        
        self.pack(expand = True, fill = "both", pady = 5)
        
    def removeDisplay(self):
        
        def callback(bool):
            if bool:
                
                self.parentclass.buffer.AddState((self.date,self.amount,self.expensename,self.type,self.currency))
               
                self.dbManager.deleteExpense("DELETE FROM expenses WHERE DATE = '{}' AND amount = {}".format(self.date, self.amount))
                
                self.monthlyCat.callUpdate()
                self.pack_forget()
            else:
                pass
            
        confiramtionDialogue(self,callbackFunc=callback)
             
        
class UndoBuffer (object):
    def __init__(self, value, maxlength = 10):
        self.maxlength = maxlength
        self.buffer = deque([value], maxlength)
        
    def getCurrentState(self): #return last
        return self.buffer[-1]
    
    def AddState(self, value): #add to last
        self.buffer.append(value)
    
    def undo(self):
        return self.buffer.pop()
    
    def getAll(self):
        return self.buffer
           

class ErrorMessage(ctk.CTkToplevel):
    def __init__(self, parent, text):
        super().__init__(master = parent,fg_color=TERTIARY_RED)
        self.title("WARNING")
        self.resizable(False,False)
        
        self.attributes("-alpha", 0)
        self.attributes("-toolwindow", True)
        
        textFont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE, weight="bold")
        
        self.label = ctk.CTkLabel(self, text=text, text_color=BLACK, font=textFont)
        self.label.pack(padx = 10, pady =20, expand = True, fill = "x")
        
        self.after(100, self.attributes, "-alpha", 1)
        
        self.grab_set()
        
class confiramtionDialogue(ctk.CTkToplevel):
    def __init__(self, mainwindow, callbackFunc):
        super().__init__(master = mainwindow, fg_color=TERTIARY_RED)
        
        self.title("CONFIRM")
        self.resizable(False,False)
        
        self.callback = callbackFunc
        
        self.attributes("-alpha", 0)
        self.attributes("-toolwindow", True)
        
        textFont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE, weight="bold")
        
        self.label = ctk.CTkLabel(self, text="CONFIRM", text_color=BLACK, font=textFont)
        
        self.yesButton = ctk.CTkButton(self,text="YES",fg_color=PRIMARY_RED, 
                                     corner_radius=15,
                                     text_color=WHITE,
                                     font=textFont,
                                     height= 40,
                                     hover_color= GRAY,command=lambda: self.handleButtonPress(True))
        
        self.noButton = ctk.CTkButton(self,text="NO",fg_color=PRIMARY_RED, 
                                     corner_radius=15,
                                     text_color=WHITE,
                                     font=textFont,
                                     height= 40,
                                     hover_color= GRAY, command=lambda: self.handleButtonPress(False))
        

        self.after(100, self.attributes, "-alpha", 1) #brings it forward
        
        self.label.pack(padx = 10, pady =20, expand = True, fill = "x")
        self.yesButton.pack(pady = 10, padx=10, side="left")
        self.noButton.pack(pady = 10, padx=10, side = "right")
        
        self.grab_set()
        
    def handleButtonPress(self, value):
        self.callback(value)
        self.destroy()
        
