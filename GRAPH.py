import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from SETTINGS import *
import customtkinter as ctk


class BarGraph(ctk.CTkFrame):
    def __init__(self,data, parent):
        super().__init__(master=parent)
        
        xVal = list(data.keys())
        yVal = list(data.values())
        
        self.fig = Figure(figsize=(6,2.75), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_facecolor(LIGHT_GRAY)
        self.fig.patch.set_facecolor(LIGHT_GRAY)

        rect = self.ax.bar(xVal,yVal, width=0.5, color = PRIMARY_RED)

        for p in self.ax.patches:

            self.ax.annotate(text=round(p.get_height(),1),
                xy=(p.get_x()+p.get_width()/2., p.get_height()),
                ha='center',
                va='center',
                xytext=(0, 10),
                textcoords='offset points')
        
        #plt.xticks(positions, xVal)
        
        # fig.set_figwidth(6)
        # fig.set_figheight(2)
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(True)
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill="both")
        
        self.canvas.draw()
        
        self.pack(expand=True, fill="both", padx = 10, pady = 20, side = "top")
        
    def updateGraph(self,data):
        
        xVal = list(data.keys())
        yVal = list(data.values())
        
        self.ax.clear()
     
        self.ax.bar(xVal, yVal, width=0.5, color=PRIMARY_RED)

        self.ax.set_facecolor(LIGHT_GRAY)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(True)
        
        for p in self.ax.patches:

            self.ax.annotate(text=round(p.get_height(),1),
                xy=(p.get_x()+p.get_width()/2., p.get_height()),
                ha='center',
                va='center',
                xytext=(0, 10),
                textcoords='offset points')
        
        self.canvas.draw()
        
        
  
        
class DonutGraph(ctk.CTkFrame):
    def __init__(self, data,backgroundCol, parent, colors=None, explodeAmount=0):
        super().__init__(master=parent, bg_color=backgroundCol,fg_color=LIGHT_GRAY)
        
        self.radius : float = 1.25 #start using type declaration for practice
        
        self.colors = colors
        self.explodeAmount = explodeAmount
        self.backgroundCol = backgroundCol
        
        if all(val == 0 for val in data):
            data = [1,1,1,1,1]
        
        if colors == None:
            colors = ["red" for x in range(len(data))]
        
        self.fig = Figure(figsize=(2.7, 2.7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        if backgroundCol:
            self.fig.patch.set_facecolor(backgroundCol)  # Set figure background
            self.ax.set_facecolor(backgroundCol) 
        
        self.ax.pie(x=data, colors=colors, radius=self.radius, explode=[explodeAmount for x in range(len(data))])
    
        circle = plt.Circle((0,0), self.radius/2, fc = backgroundCol)
        
        self.ax.add_artist(circle)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="x", expand=True)
        
        self.canvas.draw()
        
        self.pack()
    
    def UpdateGraph (self,data):
        
        if all(val == 0 for val in data):
            data = [1,1,1,1,1]
        
        self.ax.clear()

        self.ax.pie(x=data, colors=self.colors, radius=self.radius, explode=[self.explodeAmount for x in range(len(data))])
    
        circle = plt.Circle((0,0), self.radius/2, fc = self.backgroundCol)
        
        self.ax.add_artist(circle)

        
        self.fig.patch.set_facecolor(self.backgroundCol)  # Set figure background
        self.ax.set_facecolor(self.backgroundCol) 
        
        self.canvas.draw()
