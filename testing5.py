import tkinter as tk
from random import choice
from files import rel_path
from PIL import ImageTk, Image
from getParkingLot import ParkingLotInfo, GetLot

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.main = tk.Frame(self, background="#ffffff")
        self.main.pack(side="left", fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.main, borderwidth=0, background="#ffffff")
        
        self.frame = tk.Canvas(self.canvas, background="#ffffff",width=parent.winfo_reqwidth())
        
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.pack(side="right", fill="y")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.populate()

    def populate(self):
        self.images = []
        g = GetLot()
        
        for lotname in g.listOfFolders:
            s = []
            s.append(lotname)
            i = ImageTk.PhotoImage(Image.open(f"{rel_path}{lotname}/{lotname}_logo.png").resize((100,100), Image.Resampling.LANCZOS))
            s.append(i)
            self.images.append(s)
        
        colours = ["lightblue","lightgreen","yellow","orange"]
        lot = []
        n = 0
        for item in self.images:
            getlot =[]
            getlot.append(n+1)
            getlot.append(item[0])
            lot.append(getlot)
            c = tk.Canvas(self.frame,height=self.frame.winfo_reqheight(), bg=choice(colours))    
            c.create_text(int(c.winfo_reqwidth()/2), 30, text = f"{item[0]}", font = ('bold', 20), anchor = "center", tags = 'text')
            l = tk.Label(c, bg = choice(colours), image=item[1],width = int(c.winfo_reqwidth()/2), height = int(c.winfo_reqheight()/2) )
            l.place(x = int(c.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 60, )
            b = tk.Button(c, text=f"{item[0]}", command = lambda : self.printInfo(rel_path,lot[n]))
            b.place(x = int(c.winfo_reqwidth()/2) - int(b.winfo_reqwidth()/2), y = 230)
            c.pack(fill="both", expand=True)
            n+=1

            
    def printInfo(self, rel_path, name):
        print(f"Path is '{rel_path}{name[0]}/' and name is {name[0]}")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root=tk.Tk()
    width, height = 400, 400
    root.geometry(f"{width}x{height}+100+10")
    root.resizable(False,False)
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()