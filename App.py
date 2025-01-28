import customtkinter as ctk
from SETTINGS import *
from UTILS import *
from DATAFRAME import *
from DataBaseManager import DataBaseManager as DBM
from PIL import  Image
from GRAPH import DonutGraph
from GRAPH import BarGraph


class App (ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=WHITE)
        self.geometry("1280x720")
        self.resizable(False,False)
        
        self.dbManager = DBM()
        
        
        #layout configuration
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1,weight=40)
        self.rowconfigure(2, weight=40)
        
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)
        
        TopFrame(parent=self, width=self.winfo_width(), height=60)
        self.MonthlyCat = MonthlyCategories(parent=self, dbmanager=self.dbManager)
        
        #print(self.winfo_screenheight())
        MonthlyAverage(parent=self, dbmanager=self.dbManager)
        Extra(parent=self)
        self.settingsTab = SettingsTab(parent=self, width=443, height=700-48, dbmanager=self.dbManager, monthlyCategories=self.MonthlyCat)
        
        self.bind("<Button>", func=lambda event: self.closeSettings(event))
        
        self.bind_widget_events(frame=self.settingsTab)
        
        #transparentFrame = ctk.CTkFrame(self,bg_color="transparent")
        #transparentFrame.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth =0.5, relheight =0.5)
       
        self.mainloop()
    
    def closeSettings (self, event):
        if not self.settingsTab.mouse_in_frame():
            self.settingsTab.animateBackwards()
    
    def bind_widget_events(self, frame):
        """Bind Enter and Leave events for the specified frame and its children."""
        # Bind the events to the parent frame
        frame.bind("<Enter>", frame.onEnter)
        frame.bind("<Leave>", frame.onLeave)

        # Ensure child widgets propagate events to the parent frame
        for child in frame.winfo_children():
            child.bind("<Enter>", frame.onEnter)
            child.bind("<Leave>", frame.onLeave)
      
class TopFrame(ctk.CTkFrame):
    def __init__(self, parent, width, height):
        super().__init__(master=parent, fg_color=PRIMARY_RED, width=width, height=height, corner_radius=0)
        
        
        #titleText
        titleFont = ctk.CTkFont(family=FONT, weight="bold", size=TITLE_FONT_SIZE)
        
        titleText = ctk.CTkLabel(master=self, text="Expense Tracker", font=titleFont, text_color=TERTIARY_RED)
        
        titleText.pack(fill = "both", side = "left", expand = True, padx =10,pady =10)
        
        self.grid(row = 0, column = 0, columnspan = 3, sticky = "nsew")
        
class MonthlyCategories(ctk.CTkFrame):
    def __init__(self,parent,dbmanager : DBM):
        super().__init__(master=parent, fg_color=LIGHT_GRAY, corner_radius=20,)
        
        self.dbManager = dbmanager
        
        #selectionFrame
        selectionFont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE, weight="bold")
        selectionFrame = ctk.CTkFrame(self,fg_color=LIGHT_GRAY)
        monthLabel = ctk.CTkLabel(text="Month:", master=selectionFrame,font=selectionFont,text_color=BLACK)
        yearLabel = ctk.CTkLabel(text="Year:", master=selectionFrame,font=selectionFont,text_color=BLACK)
        
        selectionFrame.columnconfigure((0,1), weight=1)
        selectionFrame.columnconfigure(2, weight=2)
        selectionFrame.columnconfigure((3,4), weight=1)
        
        months = ["Jan" ,"Feb","Mar","Apr","May","Jun","Jul","Aug","Sep" ,"Oct" ,"Nov" ,"Dec"]
        
        availableYears = self.dbManager.getExpense(""" SELECT DISTINCT SUBSTR(DATE, 7, 4) AS year FROM {}  """.format(self.dbManager.dbName[:-3]))
        # self.dbManager.dbName[:-2]
        print()
        
        self.monthstr = ctk.StringVar(value=months[datetime.now().month-1])
        monthsDropdown = ctk.CTkComboBox(selectionFrame,
                                     values=months,
                                     width=100, 
                                     command=lambda _: self.callUpdate(), 
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
        self.yearDropdown = ctk.CTkComboBox(selectionFrame,
                                        width=100,
                                     values=[year[0] for year in availableYears], 
                                     command=lambda _: self.callUpdate(), 
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
        
        monthLabel.grid(column = 0, row = 0, sticky = "w", padx=10)
        monthsDropdown.grid(column= 1, row = 0, sticky ="w")
        yearLabel.grid(column= 3, row = 0, sticky ="w")
        self.yearDropdown.grid(column= 4, row = 0, sticky ="w")
        
        
        
        #TITLE FRAME
        titleFrame = ctk.CTkFrame(self, fg_color=SECONDARY_RED, height=50, width=600, corner_radius=15)
        
        #Title
        title_font = ctk.CTkFont(FONT, size=CATEGORY_FONT_SIZE, weight="bold")
        title = ctk.CTkLabel(titleFrame, text_color=TERTIARY_RED, font=title_font, text="Monthly Categories")
        
        #Total Frame
        totalFont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE, weight="bold")
        
        totalFrame = ctk.CTkFrame(master=self, fg_color=LIGHT_GRAY)
        totalTitle = ctk.CTkLabel(master=totalFrame, text="Total:", text_color=BLACK, font=totalFont)
        
        self.totalNum = ctk.DoubleVar(value=0)
        totalLabel = ctk.CTkLabel(master=totalFrame, text="0", text_color=GRAY, textvariable=self.totalNum, font=totalFont)

        totalTitle.pack(side = "left", padx = 25)
        totalLabel.pack(side = "left", padx = 5)
        self.UpdateTotal()

        #packing
        self.grid(row = 1, column = 0,rowspan = 2,  sticky = "nsew", padx = 25, pady =25)
        
        titleFrame.pack(fill = "x", padx =10, pady =10)
        title.pack(expand = True,padx =10, pady =10)
        
        Labels  : list[str]     =   ["Food",  "General",  "Groceries", "Transport", "Utililty"]
        colors  : list[object]  =   [PRIMARY_RED,DONUTCOL_3,SECONDARY_RED,DONUTCOL,DONUTCOL_2]
        
        selectionFrame.pack(fill = "x")
        
        self.donut = DonutGraph(data=[1,1,1,1,1],
                   colors=colors, 
                   parent=self,backgroundCol=LIGHT_GRAY,
                   )
        
        self.labelList = []
        
        #Total Frame
        totalFrame.pack( fill = "x")
        
        for i in range(len(Labels)):
            self.labelList.append(ColorLabels(self, infoColor=colors[i], txt=Labels[i], amount=20))
            
        self.callUpdate()
    
    def UpdateTotal (self):
        currentMonth = datetime.now().month
        currentMonth = f'{currentMonth:02d}'
        currentYr = f'{datetime.now().year}'
        
        Total = self.dbManager.getExpense(f"""
                                        SELECT SUM(AMOUNT)
                                        FROM expenses
                                        WHERE substr(DATE, 1, 2) = '{currentMonth}'  
                                        AND substr(DATE, 7, 4) = '{currentYr}'       
                                    """)
        if Total[0][0] == None:
            self.totalNum.set(value=0)
        else:
            
            self.totalNum.set(value=Total[0][0])
    
        
    def getMonthlyCatergories(self, year, month):
        
        categories = {
            "Food" : 0 ,
            "Groceries": 0, 
            "General" : 0,
            "Transport" : 0,
            "Utililty" : 0,
        }   
      
        mappings = {
            "FOOD" : "Food",
            "GENERAL" : "General",
            "GROCERIES" : "Groceries",
            "TRANSPORT" : "Transport",
            "UTILITIES" : "Utililty"
        }
      
        months = { "Jan" : "01",
                   "Feb" : "02",
                   "Mar" : "03",
                   "Apr" : "04",
                   "May" : "05",
                   "Jun" : "06",
                   "Jul" : "07",
                   "Aug" : "08",
                   "Sep" : "09",
                   "Oct" : "10",
                   "Nov" : "11",
                   "Dec" : "12"}
        
        
        
        rows = self.dbManager.getExpense(f"""
        SELECT 
        SUBSTR(DATE, 1, 2) AS month,
        TYPE,
        SUM(AMOUNT) AS total
        FROM expenses
        WHERE SUBSTR(DATE, -4) = '{year}' 
        AND SUBSTR(DATE, 1, 2) = '{months[month]}'
        GROUP BY month, TYPE
        ORDER BY month ASC, TYPE ASC
        """)
        
        for date, category, amount in rows:
            if category in mappings:
                categories[mappings[category]] = amount
        
        return categories
        
    def callUpdate(self):
        
        data = self.getMonthlyCatergories(year=int(self.yearstr.get()), month=self.monthstr.get())
        
        self.donut.UpdateGraph(list(data.values()))
        print(data)
        
        for i in range(len(data)):
            self.labelList[i].updateLabels(round(list(data.values())[i],2), list(data.keys())[i])
                
        availableYears = self.dbManager.getExpense(""" SELECT DISTINCT SUBSTR(DATE, 7, 4) AS year FROM {}  """.format(self.dbManager.dbName[:-3]))
        self.yearDropdown.configure(values=[year[0] for year in availableYears])     
    
        self.UpdateTotal()

    
class ColorLabels (ctk.CTkFrame):
        def __init__(self, parent, infoColor : str, txt : str, amount):
            super().__init__(master=parent, fg_color=LIGHT_GRAY, height=0)
            
            self.txt = txt
            self.amount = amount
            
            textFont = ctk.CTkFont(family=FONT, size=MEDIUM_SIZE, weight="bold")
            
            colorFrame = ctk.CTkFrame(self,fg_color=infoColor, width=25,height=20, corner_radius=8)
            
            self.label = ctk.CTkLabel(self,text=self.txt, text_color=BLACK, font=textFont, height=500)
            
            self.amountLabel = ctk.CTkLabel(self, text=self.amount, font=textFont,text_color=BLACK)
            
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0, weight=1)        
            self.columnconfigure(1, weight=5)        

            colorFrame.grid(row = 0,column = 0, sticky = "w", padx = 20)
            self.label.place(relx = 0.15, rely = 0.5, anchor = "w",)
            self.amountLabel.place(relx = 0.8, rely = 0.5, anchor = "w",)
            
            self.pack(fill = "x",pady=12)
    
        def updateLabels(self, amount, labelTitle):
            self.amountLabel.configure(text = amount)
            self.label.configure(text = labelTitle)
        

class MonthlyAverage(ctk.CTkFrame):
    def __init__(self, parent, dbmanager : DBM):
        super().__init__(master=parent, fg_color=LIGHT_GRAY, corner_radius=20 )
        self.grid_propagate(False)
        
        self.dbManager = dbmanager
        
        availableYears = self.dbManager.getExpense(""" SELECT DISTINCT SUBSTR(DATE, 7, 4) AS year FROM {}  """.format(self.dbManager.dbName[:-3]))
        
        #TitleFrame 
        titleFrame = ctk.CTkFrame(self, fg_color=SECONDARY_RED,height=50,corner_radius=15)
        
        #Title
        title_font = ctk.CTkFont(FONT, size=CATEGORY_FONT_SIZE, weight="bold")
        title = ctk.CTkLabel(titleFrame, text_color=TERTIARY_RED, font=title_font, text="Monthly Average")
        
        yearSelectionFrame = ctk.CTkFrame(self, fg_color=LIGHT_GRAY)
        
        yearSelectionFrame.columnconfigure((0,1),weight=1)
        yearSelectionFrame.columnconfigure(2,weight=5)
        yearSelectionFrame.columnconfigure(3,weight=1)
        
        totalFont = ctk.CTkFont(family=FONT, size=SUB_CATEGORY_SIZE, weight="bold")
        
        #total
        totalLabel = ctk.CTkLabel(yearSelectionFrame, text="Total", text_color=BLACK,font=totalFont)
        monthTotal = ctk.CTkLabel(yearSelectionFrame,text="1600", text_color=GRAY,font=totalFont)
        
        
        
        self.yearstr = ctk.StringVar(value=str(datetime.now().year))
        self.yearselect = ctk.CTkComboBox(yearSelectionFrame,
                                     values=[year[0] for year in availableYears], 
                                     command=lambda _: self.updateGraph(self.bar), 
                                     variable=self.yearstr,
                                     fg_color=TERTIARY_RED,button_color=PRIMARY_RED, 
                                     text_color=BLACK, border_color=PRIMARY_RED, 
                                     button_hover_color=GRAY,
                                     dropdown_fg_color=SECONDARY_RED,
                                     dropdown_text_color=BLACK,
                                     dropdown_hover_color=TERTIARY_RED,
                                     font=totalFont,
                                     dropdown_font=totalFont,
                                     justify="center",
                                     corner_radius=10,
                                     )
        
        
        
        totalLabel.grid(row = 0,column = 0)
        monthTotal.grid(row = 0,column = 1, sticky = "w")
        self.yearselect.grid(row = 0,column = 3, pady = 2)
        
        
        titleFrame.pack(fill = "x", padx = 10, pady= 10)
        title.pack(expand = True,padx =10, pady =10)
        
        #totalLabel.pack(side = "left",padx =10)   
        #monthTotalAvailable.pack(side="left",padx =10)   
        #yearselect.pack(side = "right",padx =10) 
        yearSelectionFrame.pack(expand = True, fill = "x")
        
        #BarGraph(parent=self,xVal=month,Yval=averages)
        
        self.bar = BarGraph(data=self.calculateMonthlyAverage(self.yearstr.get()),parent=self)
        
        self.grid(row = 1, column = 1, sticky = "nswe", padx = 25, pady =15)
        
        
        #self.graph = BarGraph(positions=positions, xVal=month, Yval=averages, parent=self)    
    
    def calculateMonthlyAverage(self, year : int) -> dict[str,float]:
        
        months = {"01": "Jan",
                  "02": "Feb",
                  "03": "Mar",
                  "04": "Apr",
                  "05": "May",
                  "06": "Jun",
                  "07": "Jul",
                  "08": "Aug",
                  "09": "Sep",
                  "10": "Oct",
                  "11": "Nov",
                  "12": "Dec"}
        
        monthlyTotal = {f"{months[f'{month:02}']}": [] for month in range(1, 13)}
        
        rows = self.dbManager.getExpense("""SELECT SUBSTR(DATE, 1,2) AS month, SUM(AMOUNT) AS total FROM expenses WHERE SUBSTR(DATE, -4) = '{}' 
                  GROUP BY month ORDER BY month ASC""".format(f'{year}'))

        for row in rows:
            month = row[0]
            total = row[1]
            #print(month, total)
            if type(total) == list:
                monthlyTotal[months[month]] = 0
                
            monthlyTotal[months[month]] = total
        
        for key,value in monthlyTotal.items() :  
            if type(value) == list:
                monthlyTotal[key] = 0
                
        return monthlyTotal  
    
    def updateGraph(self, graph):
        
        monthlyAvg = self.calculateMonthlyAverage(self.yearstr.get())
        
        graph.updateGraph(monthlyAvg)
        
        availableYears = self.dbManager.getExpense(""" SELECT DISTINCT SUBSTR(DATE, 7, 4) AS year FROM {}  """.format(self.dbManager.dbName[:-3]))
        self.yearselect.configure(values=[year[0] for year in availableYears])           
        
class Extra(ctk.CTkFrame):
    def __init__(self, parent):
        
        super().__init__(master=parent, fg_color=LIGHT_GRAY, corner_radius=20, )
        
        #TitleFrame 
        titleFrame = ctk.CTkFrame(self, fg_color=SECONDARY_RED,height=50,corner_radius=15)
        
        #Title
        title_font = ctk.CTkFont(FONT, size=CATEGORY_FONT_SIZE, weight="bold")
        title = ctk.CTkLabel(titleFrame, text_color=TERTIARY_RED, font=title_font, text="Extras")
        
        self.grid(row = 2, column = 1, sticky = "nswe",padx = 25, pady =15)
        titleFrame.pack(fill = "x", padx = 10, pady= 10)
        title.pack(expand = True,padx =10, pady =10)
        
class SettingsTab(ctk.CTkFrame):
    """
    
    Holds all the expense tab widgets [expense entry, history, transfer, settings]
    
    """
    
    def __init__(self, parent, width, height, dbmanager :DBM, monthlyCategories : MonthlyCategories):
        super().__init__(master=parent, fg_color=PRIMARY_RED,width=width, height=height, corner_radius=0,)
        
        self.dbmanager = dbmanager
        
        self.isactive = False
       
        self.expenseentryFrameBool = ctk.BooleanVar()
        self.expensedataFrameBool = ctk.BooleanVar()
        self.expensetransferFrameBool = ctk.BooleanVar()
        self.settingsFrameBool = ctk.BooleanVar()
        
        
        historyImage = Image.open(HISTORY_IMAGE_PATH)
        historyImage = ctk.CTkImage(dark_image=historyImage, size=(28, 28))
        
        EntryImage = Image.open(ENTRY_PATH)
        EntryImage = ctk.CTkImage(dark_image=EntryImage, size=(24, 24))
        
        transferImage = Image.open(TRANSFER_PATH)
        transferImage = ctk.CTkImage(dark_image=transferImage, size=(24, 24))
        
        settingsImage = Image.open(SETTINGS_IMAGE_PATH)
        settingsImage = ctk.CTkImage(dark_image=settingsImage, size=(32, 32))

        expenseHistoryButton = ctk.CTkButton(self, width=32, height=32, 
                                             text="", 
                                             fg_color=PRIMARY_RED, 
                                             hover_color=PRIMARY_RED,
                                             image=historyImage,
                                             command=lambda:self.frameState("HISTORY"))
        
        expenseEntryButton = ctk.CTkButton(self, width=32, height=32, 
                                           text="", fg_color=PRIMARY_RED, 
                                           hover_color=PRIMARY_RED, 
                                           image=EntryImage,
                                           command=lambda:self.frameState("ENTRY"))
        
        expenseTransferButton = ctk.CTkButton(self, width=32,height=32, 
                                              text="", 
                                              fg_color=PRIMARY_RED, 
                                              hover_color=PRIMARY_RED, 
                                              image=transferImage,
                                              command=lambda: self.frameState("TRANSFER"))
        
        settingsButton = ctk.CTkButton(self, width=32, height=32, 
                                       text="", 
                                       fg_color=PRIMARY_RED, 
                                       hover_color=PRIMARY_RED,
                                       command=lambda: self.frameState("SETTINGS"),
                                       image=settingsImage )
        
        expenseHistoryButton.bind("<Enter>", command=lambda event: historyImage.configure(size = (34,34)))
        expenseHistoryButton.bind("<Leave>", command=lambda event: historyImage.configure(size = (28, 28)))
        
        expenseEntryButton.bind("<Enter>", command=lambda event: EntryImage.configure(size = (32,32)))
        expenseEntryButton.bind("<Leave>", command=lambda event: EntryImage.configure(size = (24, 24)))
        
        expenseTransferButton.bind("<Enter>", command=lambda event: transferImage.configure(size = (32,32)))
        expenseTransferButton.bind("<Leave>", command=lambda event: transferImage.configure(size = (24, 24)))
        
        settingsButton.bind("<Enter>", command=lambda event: settingsImage.configure(size = (40,40)))
        settingsButton.bind("<Leave>", command=lambda event: settingsImage.configure(size = (32, 32)))
        
        self.frames = {
            
            "HISTORY" : ExpenseHistory(self, dbManager=self.dbmanager, monthlyCategories=monthlyCategories),
            "ENTRY" : ExpenseEntry(self, dbmanager= self.dbmanager, monthlyCategories=monthlyCategories),
            "TRANSFER" : TrackerFrame(self),
            "SETTINGS" : SettingsFrame(self, dbManager=self.dbmanager)
            
        }
        
        self.startpos = 0.95
        self.finalPos = 0.66
        self.width = abs(self.startpos- self.finalPos)
        
        self.pos = self.startpos
        self.instartPos = True
        
        self.current_frame = None
        #self.frameState("HISTORY")
        
        expenseHistoryButton.place(relx =0.07,rely = 0.1, anchor = "center")
        expenseEntryButton.place(relx =0.07,rely = 0.18, anchor = "center")
        expenseTransferButton.place(relx =0.07,rely = 0.26, anchor = "center")
        settingsButton.place(relx =0.07,rely = 0.92, anchor = "center")
        
       
   
        self.place(relx = self.startpos, rely = 1, anchor = "sw") #relHeight = 1)
    
    def onEnter(self, event):
        if not self.isactive:
            self.isactive = True
            
        #print("Mouse Entered the settings frame.")
                  
    def onLeave(self, event):
        if not self.mouse_in_frame():
            self.is_active = False
            #print("Mouse left the settings frame.")
    
    def mouse_in_frame(self):
        """Check if the mouse is within the settings frame hierarchy."""
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        widget = self.winfo_containing(x, y)
        current_widget = widget
        while current_widget:
            if current_widget == self:
                return True
            current_widget = current_widget.master
        return False

    def frameState(self, state):
        
        if self.current_frame:  
            self.current_frame.place_forget()
            
        self.current_frame = self.frames[state]
        self.current_frame.place(relx =0.15,rely= 0, anchor ="nw",relheight = 1)
    
        self.animateFrame()
        #for key,frame in self.state_mapping.items():
        #    frame.set(value=(state==key))
        #    print(frame.get())
        #        
            
    def animateFrame(self):
        #print(f"self.instartPos: {self.instartPos}")
        
        if self.instartPos:
            self.animateForward()

    def animateForward (self):
        if self.pos > self.finalPos:
            self.pos -= 0.008
            self.place(relx = self.pos, rely = 1, anchor = "sw")
            self.after(3, self.animateForward)
        else:
            self.instartPos = False
            
    def animateBackwards (self):
        if self.pos < self.startpos:
            self.pos += 0.008
            self.place(relx = self.pos, rely = 1, anchor = "sw")
            self.after(3, self.animateBackwards)
        else:
            self.instartPos = True



if __name__ == "__main__":
    App()
    
    
    