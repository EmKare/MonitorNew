from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Scrollbar, Frame, RIGHT, LEFT, BOTH, Y, Listbox, END
from PIL import Image, ImageTk

class EditCanvas(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width, self.height = 400, 750 
        self.geometry(f'{self.width}x{self.height}+10+10')
        self.resizable(False, False)
        
        self.labelFrame = LabelFrame(self, width = self.width-10, height = self.height-10)
        self.labelFrame.place(x = 5, y = 5)
        
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        
        self.shapes = []  # to hold the newly created image
        
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
        self.decorate()
        self.create_rectangle(2,2, 382, 731, fill='snow', alpha=.6)
        self.mainloop()
        
    def decorate(self):
        self.mainCanvas.create_polygon([4, 4, (self.width - 20)/2, self.height-20, 4, self.height-20], fill='light sea green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), self.height-20 ,(self.width - 20)/2 , self.height-20], fill='spring green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) * 2, (self.width - 20), self.height-20], fill='medium spring green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), (self.height - 20) / 3, (self.width - 20), ((self.height - 20) / 3) * 2], fill='aquamarine', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) / 2, (self.width - 20), (self.height - 20) / 3], fill='SpringGreen2', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2, (self.width - 20), ((self.height - 20) / 3) / 2], fill='PaleGreen1', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2], fill='azure', tags="shapes")
        self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="shapes")
    
    def create_rectangle(self,x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.shapes.append(ImageTk.PhotoImage(image))
            self.mainCanvas.create_image(x1, y1, image=self.shapes[-1], anchor='nw')
        self.mainCanvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        
EditCanvas()

"""
        
        from tkinter import *

tk = Tk()
tk.geometry("600x600")

canvas = Canvas(tk)

def triangle(x, y, w, h):
    points = [x,y, x+(w/2),y+h, x+w,y, x,y]
    
    canvas.create_polygon(points)

    canvas.pack(fill=BOTH, expand=True)

triangle(300, 300, 50, 50)

tk.mainloop()

        """