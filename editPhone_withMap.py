from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Checkbutton, BooleanVar, \
    Scrollbar, Frame, RIGHT, LEFT, BOTH, Y, Listbox, END, scrolledtext, INSERT, Text, CENTER
from PIL import Image, ImageTk
from lorem_text import lorem
import files

from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from parkingLots import _parkingLots
import openrouteservice as ors
from itertools import islice
from geopy import distance
from time import time

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
        
        self.client = ors.Client(key = '5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')
        self.distanceService = Nominatim(user_agent = "geoapiExercises")
        
        self.shapes = []
        
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="main-rectangle")
        self.decorate()
        self.create_rectangle(2,2, 382, 731, fill='snow', alpha=.6, tags = "blur")
        self.termsAgreed, self.canvasCleared  = False, False
        self.termsAndConditions()
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
        self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")
    
    def create_rectangle(self,x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            tags = kwargs.pop('tags')
            fill = self.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.shapes.append(ImageTk.PhotoImage(image))
            self.mainCanvas.create_image(x1, y1, image=self.shapes[-1], anchor='nw', tags = tags)
        self.mainCanvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    
    def createUserButton(self):
        self.userLabelButton = Button(self.mainCanvas, bg = "white", highlightthickness=0, relief="flat", borderwidth=0, )
        image = Image.open(files.no_user)
        image = image.resize((50,50), Image.Resampling.LANCZOS)
        self.userLabel_image = ImageTk.PhotoImage(image)
        self.userLabelButton.config(image = self.userLabel_image, state = "normal")
        self.userLabelButton.place(x = self.mainCanvas.winfo_reqwidth() - self.userLabelButton.winfo_reqwidth() - 4, y = 4,)
    
    def createButtons(self):
        self.createUserButton()
        self.freeUseButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Find Close-By", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white", command = self.appMap)
        self.freeUseButton.config(width = 15, height = 2)
        self.freeUseButton.place(x = int((self.width) / 2) - int(self.freeUseButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) - 60)
        
        self.reserveSpotButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Reserve Parking", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white")
        self.reserveSpotButton.config(width = 15, height = 2)
        self.reserveSpotButton.place(x = int((self.width) / 2) - int(self.reserveSpotButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) + 60)
    
    def appMap(self):
        self.clearCanvasToLayMap()
        self.userLabelButton.destroy()
        self.freeUseButton.place_forget()
        self.reserveSpotButton.place_forget()
        self.map_widget = TkinterMapView(self.mainCanvas, width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 8, corner_radius = 2)
        self.map_widget.place(x = 4, y = 4)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22)
        self.map_widget.set_position(18.012265695689663, -76.79800557291115, marker = False)#set_position(17.9432311, -76.7466463, marker = False)
        
        if self.canvasCleared:
            self.createUserButton()
            self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")
        
    def clearCanvasToLayMap(self):
        self.mainCanvas.delete("shapes")
        self.mainCanvas.delete("group")
        self.canvasCleared = True

    def termsAndConditions(self):
        self.mainCanvas.create_text(50, 130, text = "->", activefill = "red", tags = "terms")
               
        self.termsAndConditionsBox = Text(self.mainCanvas, width = 32, height = 19, font = ("calibri", 12), relief = "flat", )
        self.termsAndConditionsBox.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight()) + 150)
        self.termsAndConditionsBox.insert(INSERT, "\n\n")
        self.termsAndConditionsBox.insert(INSERT, self.getText())
        
        self.headerLabel = Label(self.mainCanvas, text = "TERMS AND CONDITIONS", font = ("calibri", 14, 'underline'), bg = "#ffffff")
        self.headerLabel.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = 132, width = self.termsAndConditionsBox.winfo_reqwidth(), height = 30)
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight()) - int(self.headerLabel.winfo_reqheight()) + 158, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 243, 
        outline = "black", width = 2, tags = "terms")
        
        self.check_variable = BooleanVar()
        self.agree_disagree = Checkbutton(self.mainCanvas, text = "   I accept these Terms and Conditions  ", onvalue = 1, offvalue = 0, font = ('bold', 10), bg = "#ffffff", variable = self.check_variable, command = self.toggle_button_state, )
        self.agree_disagree.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 242,)        
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2,
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 244, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 214, 
        outline = "black", width = 2, tags = "terms")
        
        self.acceptTermsAndConditionButton = Button(self.mainCanvas, text = "continue", font = ('bold', 12), relief = "flat", state = "disabled", command = self.termsAndContidionsAgreed)
        self.acceptTermsAndConditionButton.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2, y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 213, width = int(self.termsAndConditionsBox.winfo_reqwidth() + 4))

    def termsAndContidionsAgreed(self):
        self.termsAgreed = True
        self.mainCanvas.delete("terms")
        self.mainCanvas.delete("blur")
        self.agree_disagree.destroy()
        self.headerLabel.destroy()
        self.termsAndConditionsBox.destroy()
        self.acceptTermsAndConditionButton.destroy()
        self.createButtons()
        
    def getText(self):
        text = lorem.words(15) + "\n\n" + lorem.paragraph()
        cap = 0
        while cap <= 12:
            text = f"{text}\n\n{cap+1})     {lorem.paragraph()}"
            cap += 1
        return text + "\n\nNB:     " + lorem.words(15)
    
    def toggle_button_state(self):
        if self.check_variable.get():
            self.acceptTermsAndConditionButton.config(state = "normal")
        else:
            self.acceptTermsAndConditionButton.config(state = "disabled")
        
EditCanvas()