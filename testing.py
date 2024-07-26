import tkinter as tk
from random import choice
from files import rel_path
from PIL import ImageTk, Image
from getParkingLot import ParkingLotInfo, GetLot

class Scrollable(tk.Canvas):

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width,)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.place(x=0,y=0)#pack()#(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Canvas.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "pages")

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

root = tk.Tk()
width, height = 400, 600
root.geometry(f"{width}x{height}+100+10")
root.resizable(False,False)

#header = tk.Frame(root)
body = tk.Canvas(root)#,width=width,height=height)
#footer = tk.Frame(root)
#header.pack()
body.place(x=0,y=0,width=width,height=600)
#footer.pack()

#tk.Label(header, text="The header").pack()
#tk.Label(footer, text="The Footer",bg="red").pack()

images = []
g = GetLot()
for lotname in g.listOfFolders:
    s = []
    s.append(lotname)
    i = ImageTk.PhotoImage(Image.open(f"{rel_path}{lotname}/{lotname}_logo.png").resize((100,100), Image.Resampling.LANCZOS))
    s.append(i)
    images.append(s)

scrollable_body = Scrollable(body)
colours = ["lightblue","lightgreen","yellow","orange"]

for item in images:
    c = tk.Canvas(scrollable_body,height=body.winfo_reqheight(), bg=choice(colours))    
    c.create_text(int(c.winfo_reqwidth()/2), 30, text = f"{item[0]}", font = ('bold', 20), anchor = "center", tags = 'text')
    l = tk.Label(c, bg = choice(colours), image=item[1],width = int(c.winfo_reqwidth()/2), height = int(c.winfo_reqheight()/2) )
    l.place(x = int(c.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 60, )
    b = tk.Button(c, text=f"click me!")
    b.place(x = int(c.winfo_reqwidth()/2) - int(b.winfo_reqwidth()/2), y = 230)
    c.pack(fill="both", expand=True)

scrollable_body.update()

root.mainloop()