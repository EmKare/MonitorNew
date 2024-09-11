from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Scrollbar, Frame, RIGHT, LEFT, BOTH, Y
from Parking import ParkingLot
from getParkingLot import ParkingLotInfo, GetLot
from PIL import ImageTk, Image
import files
from random import choice
import asyncio

class FindMeParkingApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width, self.height = 400, 750 
        self.geometry(f'{self.width}x{self.height}+10+10')
        #self.resizable(False, False)
        self.title("Find Me Parking App")
        self.count, self.unbindEvent, self.loader = 1, 0, 0
        #self.parkingLots = GetLot()
        
        self.newsize = (350, 300)
        self.labelFrame = LabelFrame(self, width = self.width-10, height = self.height-10)
        self.labelFrame.place(x = 5, y = 5)
        
        self.containerFrame = Frame(self.labelFrame, highlightthickness = 0, bd = 2,  relief = "flat", border=0, bg="blue")
        self.containerFrame.place(x = 0, y = 0, width = self.width - 15, height = self.height - 15,)
        
        #frame for main window
        mainFrame = Frame(self.containerFrame, highlightthickness = 0, bd = 0, relief = "flat", bg="red", width = self.width - 10, height = self.height - 10,)
        mainFrame.pack(side="top", fill="both", expand=True)
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)
        
        self.Screens = {}
        
        for classes in (homePage, appPage, mailBox):
            theframe = classes(parent = mainFrame, master = self,)
            self.Screens[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
        
        #self.getSpots()
        #self.homePage()        
        
        self.show_frame(homePage)
        self.mainloop()
    
    def show_frame(self, anotherClass,):
        frame = self.Screens[anotherClass]
        try:
            anotherClass.start()
        except Exception:
            pass
        frame.tkraise()
        
class homePage(Frame):
    def __init__(self, parent, master,):
        Frame.__init__(self, parent)
        self.master = master
        self.width, self.height = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.mainCanvas = Canvas(self, width = self.width, height = self.height - 10, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)      
        self.addImageToHome()
        
    def addImageToHome(self):        
        self.im = Image.open(files.app_screen)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.mainCanvas.create_image(0, 0, image = self.tk_im, anchor = NW, tags = "Im")
        self.mainCanvas.bind("<ButtonPress-1>", self.checkClick)
        #self.mainCanvas.unbind("<ButtonPress-3>")
        self.mainCanvas.create_rectangle(10, 10, 107, 107, outline = "black", width = 2, tags="rectangle")
        self.mainCanvas.create_rectangle(2, self.height - 80, self.width - 9, self.height - 9, outline = "red", width = 1, tags="rectangle")
        self.mainCanvas.create_rectangle(98, 216, 195, 313, outline = "purple", width = 2, tags="rectangle")
        
    def checkClick(self,event):
        if self.master.unbindEvent == 0:                   
            if 98 < event.x < 195  and 220 < event.y < 313:
                self.master.unbindEvent = 1
                self.master.loader = 1
                self.master.show_frame(appPage)
            elif 10 < event.x < 107  and 10 < event.y < 107:
                self.master.unbindEvent = 1 
                self.master.show_frame(mailBox)
                            
"""                
    def backtoHome(self, event):
        if self.unbindEvent == 1:            
            if 2 < event.x < 670 and 380 < event.y < 731:
                self.unbindEvent = 0
                self.mainCanvas.unbind("<ButtonPress-3>")
                self.mainCanvas.destroy()
                try:
                    self.getReadingButton.destroy()
                except Exception:
                    pass
                self.homePage()                  
"""

class appPage(Frame):
    def __init__(self, parent, master,):
        Frame.__init__(self, parent)
        self.master = master
        self.width, self.height = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.mainCanvas = Canvas(self, width = self.width, height = self.height - 10, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        #self.start()
    
    #async def waiting(self):
    #    task = asyncio.create_task(other())
    #    pass
                                    
    def start(self):
        self.count = 1        
        #self.mainCanvas.unbind("<ButtonPress-1>")
        self.mainCanvas.bind("<ButtonPress-1>", self.backtoHome)
        self.mainCanvas.create_text(200, 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
        

        self.mainCanvas.after(300, self.addImages)        
        
    def addImages(self):
        from time import sleep
        if self.count <= 12:      
            try:
                self.canvas.delete("Im")
            except Exception:
                pass
            self.im = Image.open(files.loading_gif+f'{self.count}.png')
            self.tk_im = ImageTk.PhotoImage(self.im)
            self.mainCanvas.create_image(100, 320, image = self.tk_im, anchor = NW, tags = "Im")                
            self.count += 1
            self.mainCanvas.after(300, self.addImages)
        else:
            sleep(0.5)
            self.createMainButton()
    
    def backtoHome(self, event):
        if self.master.unbindEvent == 1:            
            if 2 < event.x < 670 and 380 < event.y < 731:
                self.master.unbindEvent = 0
                self.master.show_frame(homePage)
                #self.mainCanvas.unbind("<ButtonPress-3>")
                #self.mainCanvas.destroy()
                #self.homePage()
    """    
    def setProgressBar(self):
        self.main.destroy()
        self.mainCanvas.delete("text")
        self.mainCanvas.create_text(int((self.width - 20) / 2), 440, text = 'Finding You A Spot', font = ('bold', 12), anchor = "center", tags = 'text')
        self.p = ttk.Progressbar(self.mainCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100)
        self.p['value'] = 0
        self.p.place(x = int((self.width - 20) / 2), y = 400, anchor = "center",)
        self.route = 1
        self.after(1000, self.loading)
    
    def loading(self):
        if self.p['value'] <= 100:
            self.p['value'] += 20
        if self.p['value'] > 100:
            if self.route == 1:
                self.mainCanvas.delete("text")
                self.p.destroy()
                self.displayParkingSpotInformation()
            if self.route == 2:
                self.mainCanvas.delete("text")
                self.p.destroy()
                self.checkAvailability()
        else:
            self.p.after(1000, self.loading)
            
    def displayParkingSpotInformation(self):
        self.mainCanvas.create_text(int((self.width - 20) / 2), 70, text = f'{self.activeLot.ParkingLot_name}', font = ('bold', 20), anchor = "center", tags = 'text')
        self.mainCanvas.create_text(int((self.width - 20) / 2), 110, text = f'Your parking spot is at {self.mySpot[0]}', font = ('bold', 20), anchor = "center", tags = 'text')
        self.imageLabel = Label(self.mainCanvas,width=355, height=305)
        self.imageLabel.place(x = 12, y = 150)
        self.imageLabel.config(image=self.EntranceMap)
        self.mainCanvas.create_text(int((self.width - 20) / 2), 530, text = f' Please follow this guide map\nto get to {self.mySpot[1]} quickly and safely', font = ('bold', 12), anchor = "center", tags = 'text')
    """    
    
    def createMainButton(self):
        image = Image.open(files.no_user)
        image = image.resize((50,50), Image.Resampling.LANCZOS)
        self.userLabel_image = ImageTk.PhotoImage(image)
        self.userLabelButton = Button(self.mainCanvas, bg = "white",image = self.userLabel_image, highlightthickness=0, relief="flat", borderwidth=0, command = lambda : self.noUserButtonClick())
        self.userLabelButton.place(x = self.mainCanvas.winfo_reqwidth() - self.userLabelButton.winfo_reqwidth() - 15, y = 4,)
        self.getReadingButton = Button(self.mainCanvas, bg = "lightgreen", fg = "white", command = lambda: self.getLotsLoading(), highlightthickness=0, relief="flat", borderwidth=0, text = "Find Me Parking", font = ('bold', 20),)# activebackground = "lightgreen", activeforeground = "white")
        self.getReadingButton.config(width = 20, height = 2)
        self.getReadingButton.place(x = int((self.width) / 2) - int(self.getReadingButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2)-10)
        
    def noUserButtonClick(self):
        self.userLabelButton.config(command = lambda : self.closenoUserPopupLabel())
        self.noUserPopupLabel = Canvas(self.mainCanvas,)# font = ('bold', 10), text = )
        self.noUserPopupLabel.create_text(65,20,font = ('bold', 10), text = "Log In or Sign Up\nfor added features",)
        self.noUserPopupLabel.place(x = int(self.mainCanvas.winfo_reqwidth() /2), y = 20, width = 130, height = 65)
        self.noUserPopupLabelButton = Button(self.noUserPopupLabel, bg = "lightgreen", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "Get More", fg = "gray", activebackground="lightgreen", activeforeground="gray")
        self.noUserPopupLabelButton.place(x = 35, y = 40, width = 60)
    
    def closenoUserPopupLabel(self):
        self.userLabelButton.config(command = lambda : self.noUserButtonClick())
        self.noUserPopupLabel.destroy()
        
    def getLotsLoading(self):
        self.getReadingButton.destroy()
        self.userLabelButton.config(command = lambda : self.noUserButtonClick())
        try:
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
        """
        self.mainCanvas.delete("text")
        self.mainCanvas.create_text(int((self.width - 20) / 2), 440, text = 'Loading Parking Lot Database', font = ('bold', 12), anchor = "center", tags = 'text')
        self.p = ttk.Progressbar(self.mainCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100)
        self.p['value'] = 0
        self.p.place(x = int((self.width - 20) / 2), y = 400, anchor = "center",)
        self.route = 2
        self.after(1000, self.loading)
        
    def checker(self):
        if self.__checking == 0:
            self.__checking = 1
            self.showGivenSpot()
        
    def checkAvailability(self):
        try:
            self.mainCanvas.delete("text")
        except Exception:
            pass
        
        self.setScroll()        
         
    def setScroll(self):
        self.main = Canvas(self.mainCanvas, background="#ffffff")
        self.main.pack(side="left", fill="both", expand=True)
        
        self.canvas = Canvas(self.main, borderwidth=0, background="#ffffff",width=self.mainCanvas.winfo_reqwidth(),height=self.mainCanvas.winfo_reqheight())
        
        self.frame = Canvas(self.canvas, background="#ffffff",width=self.mainCanvas.winfo_reqwidth(), height=self.mainCanvas.winfo_reqheight())
        
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.place(x = self.mainCanvas.winfo_reqwidth()+30, y = 0)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.populate()

    def populate(self):
        self.lots = []
        
        for lotname in self.parkingLots.listOfFolders:
            lot = ParkingLotInfo(files.rel_path, lotname)
            self.lots.append(lot)
        
        colours = ["lightblue","lightgreen","yellow","orange"]

        for lot in self.lots:            
            c = Canvas(self.frame, bg=choice(colours), width=self.mainCanvas.winfo_reqwidth() - 10, height=self.mainCanvas.winfo_reqheight() - 5, )    
            c.create_text(int(c.winfo_reqwidth()/2), 80, text = f"{lot.ParkingLot_name}", font = ('bold', 20), anchor = "center", tags = 'text')
            l = Label(c, bg = choice(colours), image=lot.image)
            l.place(x = int(c.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 150, )
            c.create_text(int((self.width - 20) / 2), 510, text = f'It currently has {lot.ParkingLot_amountAvailable} available parking spots.', font = ('bold', 13), anchor = "center", tags = 'text')            
            b = self.setButton(c, choice(colours), lot)
            b.place(x = int(c.winfo_reqwidth()/2) - int(b.winfo_reqwidth()/2), y = 570,) 
            c.pack(fill="both", expand=True, )
        
    def setButton(self,c, choice, lot):
        return Button(c, text="Reserve", font = ('bold',20), command = lambda : self.setParkingLot(lot), width = 10, height = 2, highlightthickness = 0, relief = "flat", borderwidth = 0, bg = choice, fg = "black")

    def setParkingLot(self, lot):
        self.userLabelButton.config(command = lambda : self.noUserButtonClick())
        try:
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
        self.activeLot = lot
        self.checker()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def showGivenSpot(self):
        self.mySpot = choice(self.activeLot.ParkingLot_availableSpots) #['B10', 'A', 6]
        print(self.mySpot)
        self.setProgressBar()
        self.getMapImages()        
    
    def getMapImages(self):               
        index = ""
        if self.mySpot[2] < 10:
            index = f'0{self.mySpot[2]}'
        else:
            index = self.mySpot[2]
            
        entrance = ParkingLot(self.activeLot.ParkingLot_mapcontents, self.activeLot.ParkingLot_sides, "E", index, 1, self.mySpot[0], f"{self.activeLot.path}{self.mySpot[0]}_entrance.png", self.activeLot.ParkingLot_number)
        self.EntranceMap =  ImageTk.PhotoImage(entrance.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        
        exit = ParkingLot(self.activeLot.ParkingLot_mapcontents, self.activeLot.ParkingLot_sides, index, "X", 0, self.mySpot[0],  f"{self.activeLot.path}{self.mySpot[0]}_exit.png", self.activeLot.ParkingLot_number)
        self.ExitMap =  ImageTk.PhotoImage(exit.output_image().resize(self.newsize, Image.Resampling.LANCZOS))

                
    def getSpots(self):
        import re
        with open(files.spot_names) as f:
            for line in f:
                word = line.rstrip().split('#')
                spots = []
                pos = re.sub(r"[\([{})\]]", "", word[0])
                res = tuple(map(int, pos.split(', ')))
                spots.append(res) #position
                spots.append(word[2].strip()) #name
                spots.append(word[3].strip()) #status
                spots.append(int(word[1].strip())) #index
                self.__getLotSpotsStatuses.append(spots)
    """

class mailBox(Frame):
    def __init__(self, parent, master,):
        Frame.__init__(self, parent)
        self.master = master
        self.master = master
        self.width, self.height = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.mainCanvas = Canvas(self, width = self.width, height = self.height - 10, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        self.mail()
    
    def mail(self):
        self.count = 1
        #self.mainCanvas.unbind("<ButtonPress-1>")
        #self.mainCanvas.bind("<ButtonPress-3>", self.backtoHome)  
        self.mainCanvas.create_text(200, 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')

FindMeParkingApp()