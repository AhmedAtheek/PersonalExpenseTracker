import customtkinter as CTk
import tkinter as tk  # PEP8: `import *` is not preferred
#import keyboard

class MainWindow():

    def __init__(self) -> None:
        self.layout_0 = tk.Tk()

        self.layout_1 = tk.Frame(self.layout_0)
        self.layout_1.grid()

        self.display_0_var = tk.StringVar()

        self.display_0 = CTk.CTkEntry(master=self.layout_1, font=('Arial', 50), 
                                      textvariable=self.display_0_var, width=294, 
                                      justify='right', corner_radius=0, border_width=0, state='readonly')
        
        self.display_0.grid(column=0, row=0)

        self.button = CTk.CTkButton(master=self.layout_0, command=self.input)
        self.button.place(x=10, y=100)

        #keyboard.on_press_key('0', self.input_key)        # <-- old version doesn't run animation
        #keyboard.on_press_key('0', self.button._clicked)  # <-- runs animation and `self.input()`
        self.layout_0.bind("0", self.button._clicked)      # <-- runs animation and `self.input()`

        self.layout_0.mainloop()
    

    def input(self):
        current = self.display_0.get()
        new = current + '0'
        self.display_0_var.set(new)
        #...

    #def input_key(self, events):
    #    #self.input()
    #    self.button._clicked()
        

MainWindow()