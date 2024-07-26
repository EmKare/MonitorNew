from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Scrollbar, Frame, RIGHT, LEFT, BOTH, Y
from getParkingLot import ParkingLotInfo, GetLot
class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.main = Frame(self, background="#ffffff")
        self.main.pack(side="left", fill="both", expand=True)
        
        self.canvas = Canvas(self.main, borderwidth=0, background="#ffffff")
        
        self.frame = Canvas(self.canvas, background="red",width=300)
        
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.pack(side="right", fill="y")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.populate()

    def populate(self):
        from random import choice
        '''Put in some fake data'''
        colours = ["lightblue","lightgreen","yellow","orange"]
        for row in range(4):
            c = choice(colours)
            Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid", bg=c).grid(row=row, column=0)
            t="this is the second column for row %s" %row
            Label(self.frame, text=t, bg=c).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root=Tk()
    root.geometry("300x400+100+10")
    #root.resizable(False,False)
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()