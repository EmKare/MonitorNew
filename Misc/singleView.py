from tkinter import Tk, Label, Canvas, mainloop
from tkinter.ttk import Combobox
from tkinter import ttk as ttk

class SingleView(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        
        self.__window_bredth, self.__window_length = 1045,670
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+100+50")
        self.config(bg = "pink")
        self.resizable(False, False)
        
        self.canvasWidth, self.canvasHeight = 850, 559
        self.singleViewLabel = Label(self, text = "Single View", font = ('calibri', 25), justify = "center", bg = "pink")
        self.singleViewLabel.place(x = self.__midpointAcross - (self.singleViewLabel.winfo_reqwidth() / 2), y = 5)
        self.chooseFeedLabel = Label(self, text = "Please Choose a Feed: ", font = ('calibri', 13), justify = "center", bg = "pink")
        self.chooseFeedLabel.place(x = self.__midpointAcross - (self.singleViewLabel.winfo_reqwidth()) - (self.chooseFeedLabel.winfo_reqwidth()), y = 56)
        self.canvas_ComboBox = Combobox(self, width = 40, font = ('bold', 10),values=["A","B","C","D","E"])
        self.canvas_ComboBox.place(x = self.__midpointAcross - (self.canvas_ComboBox.winfo_reqwidth() / 2), y = 60)        
        self.canvas_main = Canvas(self, width = self.canvasWidth, height = self.canvasHeight, bg = "blue", border = 4,  bd = 4,  )
        self.canvas_main.place(x = self.__midpointAcross - (self.canvas_main.winfo_reqwidth() / 2), y = 90)
        
        mainloop()

SingleView()
        