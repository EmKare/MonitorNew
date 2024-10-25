from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Checkbutton, BooleanVar, \
    Scrollbar, Frame, RIGHT, LEFT, BOTH, Y, Listbox, END, scrolledtext, INSERT, Text, CENTER
from PIL import Image, ImageTk, ImageGrab
from lorem_text import lorem
import phonefiles as files

from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from parkingLots import _parkingLots
import openrouteservice as ors
from itertools import islice
from datetime import datetime
from geopy import distance
from time import time
import win32api

class EditCanvas(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        __screen_width = win32api.GetSystemMetrics(0)
        __screen_height = win32api.GetSystemMetrics(1)
        self.width, self.height = int(__screen_width/3.84), int(__screen_height/1.152) 
        self.geometry(f'{self.width}x{self.height}+980+10')
        self.resizable(False, False)
        
        self.labelFrame = LabelFrame(self, width = self.width-10, height = self.height-10)
        self.labelFrame.place(x = 5, y = 5)
        
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        self.demoEmail = 'user@mail.com'
        self.name = "Kareem"
        self.inbox = []
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
        
    def run(self):
        self.dummyMails3()
        self.dummyMails2()
        self.dummyMails1()
        self.mail()
        self.mainloop()
        
    def mail(self):
        self.count = 1
        self.mainCanvas.config(bg = "azure")
        
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 30, text = 'MAILBOX', font = ('bold', 30), anchor = "center", tags = 'text')
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 60, text = f'{self.demoEmail}', font = ('bold', 18), anchor = "center", tags = 'text',fill = "gray31")
        
        Button(self.mainCanvas, text = 'BACK', relief = "flat", font = ('bold', 15), fg = "blue2", activeforeground = "blue2", bg = "light cyan", activebackground = "light cyan", command = self.destroy).place(x = 10, y  = 10)
            
        if len(self.inbox) == 0:
            amnt = "mail"
        else:
            amnt = "mails"
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 85, text = f'{len(self.inbox)} {amnt} in Inbox', font = ('bold', 14), anchor = "center", tags = 'text',fill = "gray50")
        
        self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")   
        
        self.mailBoxCanvas = Canvas(self.mainCanvas, bd = 0, highlightthickness  =2, relief = 'ridge', highlightbackground = "black", bg = "light cyan")
        self.gotMail()
        
    def gotMail(self):
        stop = 0
        
        self.mailBoxCanvas.place(x = 2, y = 100, width = self.mainCanvas.winfo_reqwidth() - 6 , height = self.mainCanvas.winfo_reqheight() - 103,)
        
        self.mailScroll()
        while stop < (len(self.inbox) + 8):
            if stop <= len(self.inbox) - 1: #
                popupMail_width = int(self.mainCanvas.winfo_reqwidth() - 12)
                popupMail_height = int(((self.mainCanvas.winfo_reqheight() / 8) * 7) - 7)
                email_thumbnail = self.inbox[stop].setMailCanvas(self.frame, self.mainCanvas.winfo_reqwidth() - 21, popupMail_width, popupMail_height, (len(self.inbox) - 1) - stop)                
                email_thumbnail.grid(row = stop, column = 0,)
            else:
                pass
                email_thumbnail = Canvas(self.frame, height = 80, width = self.mainCanvas.winfo_reqwidth() - 21, bd = 1, highlightbackground = "gray87",  relief = "flat",)
                email_thumbnail.grid(row = stop, column = 0,)
                email_thumbnail.create_text(int((self.mainCanvas.winfo_reqwidth() - 14) / 2), 40, text = "-", font = ('bold', 30), justify = "left", fill = "gray58")
                if stop % 3 == 0:
                    email_thumbnail.configure(bg = 'papaya whip',)
                elif stop % 3 == 1:
                    email_thumbnail.configure(bg = 'PaleTurquoise2',)
                else:
                    email_thumbnail.configure(bg = 'azure3',)
            stop += 1
    
    def createDummyImages(self):
        image = Image.open(files.dummy_entrance_image)
        nextimg = image.resize((350, 300), Image.Resampling.LANCZOS)
        self.dummyEntImage = ImageTk.PhotoImage(nextimg)
        image = Image.open(files.dummy_exit_image)
        nextimg = image.resize((350, 300), Image.Resampling.LANCZOS)
        self.dummyExtImage = ImageTk.PhotoImage(nextimg)
    
    #this function is used to check if 'self.gotMail()' works properly
    #function is called 14 lines up, and can be commented/uncommented if necessary
    def dummyMails1(self):
        self.createDummyImages()
        mail = FMPSpot_Mail("First Parking Lot", 100, "A4", "Entrance Map", 1, datetime.now(), self.demoEmail, self.dummyEntImage, parentCanvas=self.mainCanvas,)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("First Parking Lot", 100, "A4", "Exit Map", 2, datetime.now(), self.demoEmail, self.dummyExtImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Second Parking Lot", 200, "A4", "Entrance Map", 1, datetime.now(), self.demoEmail, self.dummyEntImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Second Parking Lot", 200, "A4", "Exit Map", 2, datetime.now(), self.demoEmail, self.dummyExtImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Third Parking Lot", 300, "A4", "Entrance Map", 1, datetime.now(), self.demoEmail, self.dummyEntImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Third Parking Lot", 300, "A4", "Exit Map", 2, datetime.now(), self.demoEmail, self.dummyExtImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Intersection of Maxfield Avenue \n& Hagley Park Road", 400, "A4", "Entrance Map", 1, datetime.now(), self.demoEmail, self.dummyEntImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Intersection of Maxfield Avenue \n& Hagley Park Road", 400, "A4", "Exit Map", 2, datetime.now(), self.demoEmail, self.dummyExtImage, parentCanvas=self.mainCanvas)
        self.inbox.append(mail)
        
    def dummyMails2(self):
        mail = FMPLot_Mail("First Parking Lot", 400, datetime.now(), self.demoEmail, parentCanvas=self.mainCanvas, url="www.google.first")
        self.inbox.append(mail)
        mail = FMPLot_Mail("Second Parking Lot", 300, datetime.now(), self.demoEmail, parentCanvas=self.mainCanvas, url="www.google.second")
        self.inbox.append(mail)
        mail = FMPLot_Mail("Intersection of Maxfield Avenue &\n Hagley Park Road", 200, datetime.now(), self.demoEmail, parentCanvas=self.mainCanvas, url="www.google.com")
        self.inbox.append(mail)
    
    def dummyMails3(self):
        mail = Bank_Statement(datetime.now(), self.name, self.demoEmail, 300, parentCanvas=self.mainCanvas,)
        self.inbox.append(mail)
        mail = Bank_Statement(datetime.now(), self.name, self.demoEmail, 500, parentCanvas=self.mainCanvas, )
        self.inbox.append(mail)
        mail = Bank_Statement(datetime.now(), self.name, self.demoEmail, 100.50, parentCanvas=self.mainCanvas,)
        self.inbox.append(mail) 
        
    def mailScroll(self):
        self.main = Canvas(self.mailBoxCanvas, bd = 0, highlightthickness = 0, width = int(self.mainCanvas.winfo_reqwidth() / 4) + 3, height = self.mainCanvas.winfo_reqheight() - 103,)# width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 106,)
        self.main.place(x = 2, y = 2)
        #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
        self.canvas = Canvas(self.main, borderwidth=0, width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 106,)# width = self.mainCanvas.winfo_reqwidth() - 12, height = self.mainCanvas.winfo_reqheight() - 111,)
        ##create a new 'frame' canvas in the 'canvas' canvas, preset with the width and height of 'mainCanvas'
        self.frame = Canvas(self.canvas, width = self.mainCanvas.winfo_reqwidth(), height = self.mainCanvas.winfo_reqheight() - 10)
        #'vsb' is a Scrollbar event, and it is placed on self
        self.listboxScrollbar = Scrollbar(self.mainCanvas, orient="vertical", command=self.canvas.yview)
        #sets a yscrollcommand for the 'canvas' widget
        self.canvas.configure(yscrollcommand=self.listboxScrollbar.set)
        #places the scrollbar off screen
        self.listboxScrollbar.place(x = self.mainCanvas.winfo_reqwidth()+30, y = 0)
        #packs the 'camvas' widet into the 'main' widget
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")
        #binds 2 functions to the canvas, and 1 to the frame
        self.frame.bind("<Configure>", self.__on_NewFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self.__new_on_mousewheel)

    def __on_NewFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #this function configues the 'canvas' canvas scroll type
    def __new_on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
        try:
            self.mailBoxCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass

class FMPSpot_Mail:
    def __init__(self, lot_name:str, distance:float, spot:str, header:str, type:int, time:datetime, email:str, image = None, parentCanvas:Canvas = None, url:str = ""):
        self.lot_name = lot_name
        self.distance = distance
        self.spot = spot
        self.header = header
        self.type = type
        self.time = time
        self.email = email
        self.image = image
        self.parentCanvas = parentCanvas
        self.url = url

    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i = None,):       
        c = Canvas(canvas, height = 80, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "F", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "Find Me Parking", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"{self.header} from Find Me Parking", font = ('bold', 12),)
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[Find Me Parking] Your parking spot at {self.lot_name} is...", font = ('bold', 10), )
        
        logo.place(x = 7, y = 7, width = 70, height = 70,)
        time.place(x = 325, y = 5)
        header.place(x = 80, y = 5)
        middle.place(x = 80, y = 36)
        footcontainer.place(x = 80, y = 60, width = 285)
        
        logo.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        time.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        header.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        middle.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footcontainer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        c.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        
        if i % 3 == 0:
            logo.configure(bg = 'azure3')
            time.config(bg = 'papaya whip',)
            header.config(bg = 'papaya whip',)
            middle.config(bg = 'papaya whip',)
            footer.config(bg = 'papaya whip',)
            c.configure(bg = 'papaya whip',)
        elif i % 3 == 1:
            logo.config(bg = 'papaya whip',)
            time.configure(bg = 'PaleTurquoise2',)
            header.config(bg = 'PaleTurquoise2',)
            middle.configure(bg = 'PaleTurquoise2',)
            footer.configure(bg = 'PaleTurquoise2',)
            c.configure(bg = 'PaleTurquoise2',)
        else:
            logo.configure(bg = 'PaleTurquoise2',)
            time.config(bg = 'azure3',)
            header.config(bg = 'azure3',)
            middle.configure(bg = 'azure3')
            footer.configure(bg = 'azure3')
            c.configure(bg = 'azure3')        
        return c

    def clickedmail(self, popupMail_width, popupMail_height, i = None):
        if i is not None:
            if self.type == 1: #Entrance Map
                txt1 = 'Please follow this guide map to get to'
                txt2 = f'{self.spot} quickly and safely'
            elif self.type == 2:
                txt1 = 'Please follow this guide map to get from'
                txt2 = f'{self.spot} to the Exit quickly and safely' 
            bg = "honeydew4"
            top_fg = "black"
            outline = "black"
            mini_txt = "gray90"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 290, y = 10)
            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"Find Me Parking: {self.header}", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "F", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)
            Label(popupMail, text = "Find Me Parking", font = ('bold',12), fg = mini_txt, bg = bg).place(x = 65, y = 43)
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 250, y = 56)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 71)
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = "gray85", tags="rectangle")
            #self, lot_name, distance, spot, header, type, time, image
            popupMail.create_text(int(popupMail_width / 2), 145, text = f'{self.lot_name}', font = ('bold', 17), fill = 'green')
            popupMail.create_text(int(popupMail_width / 2), 193, text = f'{self.header}', font = ('bold', 15), fill = 'blue')
            popupMail.create_text(int(popupMail_width / 2), 225, text = f'Your parking spot is at {self.spot}', font = ('bold', 15))
            image_label = Label(popupMail, bg = bg, image = self.image)
            image_label.place(x = int(popupMail_width / 2) - int(image_label.winfo_reqwidth() / 2), y = 250)
            popupMail.create_text(int(popupMail_width / 2), 680, text = f'You are {self.distance:.2f}km away', font = ('bold', 12))  
            popupMail.create_text(int(popupMail_width / 2), 700, text = txt1, font = ('bold', 12))
            popupMail.create_text(int(popupMail_width / 2), 720, text = txt2, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 745, text = 'Not satisfied with this spot?', font = ('bold', 9))
            popupMail.create_text(int(popupMail_width / 2), 762, text = 'You can change it in the Find Me Parking App', font = ('bold', 9))
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)

    def openURL(self):
        print(self.url)

class FMPLot_Mail:
    def __init__(self, lot_name:str, distance:float, time:datetime, email:str, parentCanvas:Canvas = None, url:str = ""):
        self.lot_name = lot_name
        self.distance = distance
        self.time = time
        self.email = email
        self.parentCanvas = parentCanvas
        self.url = url
        
    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i = None,):       
        c = Canvas(canvas, height = 80, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "F", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "Find Me Parking", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"to {self.lot_name}", font = ('bold', 12),)
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[Find Me Parking] Your parking lot choice is...    ", font = ('bold', 10), )
        
        logo.place(x = 7, y = 7, width = 70, height = 70,)
        time.place(x = 325, y = 5)
        header.place(x = 80, y = 5)
        middle.place(x = 80, y = 36)
        footcontainer.place(x = 80, y = 60, width = 285)
        
        logo.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        time.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        header.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        middle.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footcontainer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        c.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        
        if i % 3 == 0:
            logo.configure(bg = 'azure3')
            time.config(bg = 'papaya whip',)
            header.config(bg = 'papaya whip',)
            middle.config(bg = 'papaya whip',)
            footer.config(bg = 'papaya whip',)
            c.configure(bg = 'papaya whip',)
        elif i % 3 == 1:
            logo.config(bg = 'papaya whip',)
            time.configure(bg = 'PaleTurquoise2',)
            header.config(bg = 'PaleTurquoise2',)
            middle.configure(bg = 'PaleTurquoise2',)
            footer.configure(bg = 'PaleTurquoise2',)
            c.configure(bg = 'PaleTurquoise2',)
        else:
            logo.configure(bg = 'PaleTurquoise2',)
            time.config(bg = 'azure3',)
            header.config(bg = 'azure3',)
            middle.configure(bg = 'azure3')
            footer.configure(bg = 'azure3')
            c.configure(bg = 'azure3')        
        return c

    def clickedmail(self, popupMail_width, popupMail_height, i = None):
        if i is not None:
            txt1 = 'for directions to get to'
            txt2 = f'quickly and safely'
            
            bg = "honeydew4"
            top_fg = "black"
            outline = "black"
            mini_txt = "gray90"
            fill  = "gray85"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 290, y = 10)

            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"Find Me Parking", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "F", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)
            lotname = self.lot_name.replace('\n', '')
            Label(popupMail, text = f"to {lotname}", font = ('bold',12), fg = mini_txt, bg = bg, justify = "left", wraplength=200).place(x = 65, y = 40)
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 300, y = 56)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 81)
            
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = fill, tags="rectangle")
            
            popupMail.create_text(int(popupMail_width / 2), 163, text = 'Your parking lot choice is:', font = ('bold', 17))
            lot_lbl1 = Label(popupMail, text = f"{lotname}", font = ('bold',22), fg = "green", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            lot_lbl1.place(x = int(popupMail_width/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 200)
            popupMail.create_text(int(popupMail_width / 2), 380, text = f'You are {self.distance:.2f}km away', font = ('bold', 17))
            
            url = Button(popupMail, text = "click here", font = ('bold',15,'underline'), fg = "blue", bg = fill, justify = "center", relief='flat',highlightthickness=0, bd=0, borderwidth=0, activebackground = fill, activeforeground="blue", command=self.openURL)
            url.place(x = int(popupMail_width/2) - int(url.winfo_reqwidth()/2), y = 430)
            
            popupMail.create_text(int(popupMail_width / 2), 480, text = txt1, font = ('bold', 12))
            
            lot_lbl2 = Label(popupMail, text = f"{lotname}", font = ('bold',12), fg = "black", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            lot_lbl2.place(x = int(popupMail_width/2) - int(lot_lbl2.winfo_reqwidth()/2), y = 490)
            
            popupMail.create_text(int(popupMail_width / 2), 540, text = txt2, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 745, text = 'Not satisfied with this lot?', font = ('bold', 9))
            popupMail.create_text(int(popupMail_width / 2), 762, text = 'You can change it in the Find Me Parking App', font = ('bold', 9))
            
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)
            
    def openURL(self):
        print(self.url)

class Bank_Statement:
    def __init__(self, time:datetime, name:str, email:str, balance:float, parentCanvas:Canvas = None,):
        self.distance = distance
        self.time = time
        self.name = name
        self.email = email
        self.parentCanvas = parentCanvas
        self.balance = balance
        
    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i = None,):       
        c = Canvas(canvas, height = 80, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "B", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "YOUR BANK", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"{self.name} Account", font = ('bold', 12),)
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[YOUR BANK]  Your account balance is:...         ", font = ('bold', 10), )
        
        logo.place(x = 7, y = 7, width = 70, height = 70,)
        time.place(x = 325, y = 5)
        header.place(x = 80, y = 5)
        middle.place(x = 80, y = 36)
        footcontainer.place(x = 80, y = 60, width = 285)
        
        logo.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        time.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        header.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        middle.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footcontainer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        footer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        c.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a))
        
        if i % 3 == 0:
            logo.configure(bg = 'azure3')
            time.config(bg = 'papaya whip',)
            header.config(bg = 'papaya whip',)
            middle.config(bg = 'papaya whip',)
            footer.config(bg = 'papaya whip',)
            c.configure(bg = 'papaya whip',)
        elif i % 3 == 1:
            logo.config(bg = 'papaya whip',)
            time.configure(bg = 'PaleTurquoise2',)
            header.config(bg = 'PaleTurquoise2',)
            middle.configure(bg = 'PaleTurquoise2',)
            footer.configure(bg = 'PaleTurquoise2',)
            c.configure(bg = 'PaleTurquoise2',)
        else:
            logo.configure(bg = 'PaleTurquoise2',)
            time.config(bg = 'azure3',)
            header.config(bg = 'azure3',)
            middle.configure(bg = 'azure3')
            footer.configure(bg = 'azure3')
            c.configure(bg = 'azure3')        
        return c

    def clickedmail(self, popupMail_width, popupMail_height, i = None):
        if i is not None:
            txt1 = 'thanks for choosing'
            txt2 = f'[YOUR BANK]'
            
            bg = "honeydew4"
            top_fg = "black"
            outline = "black"
            mini_txt = "gray90"
            fill  = "gray85"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 290, y = 10)

            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"[YOUR BANK]", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "B", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)

            Label(popupMail, text = f"{self.name} Account Balance", font = ('bold',12), fg = mini_txt, bg = bg, justify = "left", wraplength=200).place(x = 65, y = 50)
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 300, y = 56)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 71)
            
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = fill, tags="rectangle")
            
            popupMail.create_text(int(popupMail_width / 2), 163, text = f'Hello {self.name}', font = ('bold', 17))
            popupMail.create_text(int(popupMail_width / 2), 200, text = 'Your account balance is:', font = ('bold', 17))
            balance_lbl = Label(popupMail, text = f"${self.balance:.2f}", font = ('bold',40), fg = "blue", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            balance_lbl.place(x = int(popupMail_width/2) - int(balance_lbl.winfo_reqwidth()/2), y = 300)
            
            popupMail.create_text(int(popupMail_width / 2), 480, text = txt1, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 500, text = txt2, font = ('bold', 12))
            
            #popupMail.create_text(int(popupMail_width / 2), 745, text = 'Not satisfied with this lot?', font = ('bold', 9))
            #popupMail.create_text(int(popupMail_width / 2), 762, text = 'You can change it in the Find Me Parking App', font = ('bold', 9))
            
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)
            
    def openURL(self):
        print(self.url)




if __name__ == "__main__":
    phone = EditCanvas()
    phone.run()
    
    """
        
    def save_canvas():
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        xx = x + canvas.winfo_width()
        yy = y + canvas.winfo_height()
        ImageGrab.grab(bbox=(x, y, xx, yy)).save("test.gif")
        
    root.after(1000, save_canvas)
        
        """