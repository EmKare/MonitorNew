from tkinter import Tk, Label, Canvas, mainloop
from tkinter.ttk import Combobox
from tkinter import ttk as ttk

class DoubleView(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        main_colour = "lightblue"
        self.__window_bredth, self.__window_length = 1045,670
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+100+50")
        self.config(bg = main_colour)
        self.resizable(False, False)

        self.canvasWidth, self.canvasHeight = 500, 328

        self.canvas_1_ComboBox = Combobox(self, width = 40, font = ('bold', 10),values=["A","B","C","D","E"])
        self.canvas_1_ComboBox.place(x = 105, y = 105) 
        
        self.canvas_2_ComboBox = Combobox(self, width = 40, font = ('bold', 10),values=["A","B","C","D","E"])
        self.canvas_2_ComboBox.place(x = self.canvasWidth +  140, y = 105)

        self.chooseFeedLabel = Label(self, text = "Please Choose a Feed", font = ('calibri', 15, 'bold'), justify = "center", bg = main_colour)
        self.chooseFeedLabel.place(x = self.__midpointAcross - (self.chooseFeedLabel.winfo_reqwidth() / 2), y = 100)
               
        self.canvas_1 = Canvas(self, width = self.canvasWidth, height = self.canvasHeight, bg = "blue", border = 4,  bd = 4,  )
        self.canvas_1.place(x = 10, y = self.__midpointDown - int(self.canvas_1.winfo_reqheight() / 2))
        
        self.canvas_2 = Canvas(self, width = self.canvasWidth, height = self.canvasHeight, bg = "orange", border = 4,  bd = 4,  )
        self.canvas_2.place(x = self.canvasWidth +  20, y = self.__midpointDown - int(self.canvas_2.winfo_reqheight() / 2))
        
        mainloop()

DoubleView()
        