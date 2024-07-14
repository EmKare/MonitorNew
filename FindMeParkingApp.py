from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW
from ParkingLot import ParkingLot
from PIL import ImageTk, Image
import files as files

class FindMeParkingApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width, self.height = 400, 750 
        self.geometry(f'{self.width}x{self.height}+10+10')
        self.resizable(False, False)
        self.title("Find Me Parking App")
        self.count, self.unbindEvent = 1, 0
        self.__checking, self.__readings = 0, 0
        
        self.newsize = (350, 300)
        self.labelFrame = LabelFrame(self, width = self.width-10, height = self.height-10)
        self.labelFrame.place(x = 5, y = 5)
        self.__getLotSpotsStatuses = []
        
        self.getSpots()
        self.homePage()        
                
        self.mainloop()
    
    def homePage(self):
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        self.im = Image.open(files.app_screen)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.mainCanvas.create_image(0, 0, image = self.tk_im, anchor = NW, tags = "Im")
        self.mainCanvas.bind("<ButtonPress-1>", self.checkClick)
        
    def checkClick(self,event): #98, 220, 195, 313
        if self.unbindEvent == 0:
            self.unbindEvent = 1
            if 98 < event.x < 195  and 220 < event.y < 313:
                self.mainCanvas.delete("Im")
                self.start()        
                            
    def start(self):
        try:
            self.canvas.delete("text")
        except Exception:
            pass
        self.count = 1
        self.mainCanvas.unbind("<ButtonPress-1>")   
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
            try:
                self.mainCanvas.delete("Im")
                self.mainCanvas.delete("text")
            except Exception:
                pass
            #self.createCanvas()
            self.mainCanvas.create_text(int((self.width - 20) / 2), int((self.height - 100) / 2), text = "Find Me Parking", font = ('bold', 20), anchor = "center", tags = 'text')      
            self.createMainButton()
    
    def setProgressBar(self):
        self.imageLabel.destroy()
        self.mainCanvas.delete("text")
        self.mainCanvas.create_text(int((self.width - 20) / 2), 440, text = 'Finding You A Spot', font = ('bold', 12), anchor = "center", tags = 'text')
        self.p = ttk.Progressbar(self.mainCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100)
        self.p['value'] = 0
        self.p.place(x = int((self.width - 20) / 2), y = 400, anchor = "center",)
        self.after(1000, self.loading)
    
    def loading(self):
        if self.p['value'] <= 100:
            self.p['value'] += 20
        if self.p['value'] > 100:
            self.mainCanvas.delete("text")
            self.p.destroy()
            self.displayParkingSpotInformation()
        else:
            self.p.after(1000, self.loading)
            
    def displayParkingSpotInformation(self):
        self.mainCanvas.create_text(int((self.width - 20) / 2), 80, text = f'Your parking spot is at {self.mySpot[1]}', font = ('bold', 20), anchor = "center", tags = 'text')
        self.imageLabel = Label(self.mainCanvas,width=355, height=305)
        self.imageLabel.place(x = 12, y = 150)
        self.imageLabel.config(image=self.EntranceMap)
        self.mainCanvas.create_text(int((self.width - 20) / 2), 530, text = f' Please follow this guide map\nto get to {self.mySpot[1]} quickly and safely', font = ('bold', 12), anchor = "center", tags = 'text')
        
    def createMainButton(self):
        self.getReadingButton = Button( bg = "white", command = lambda: self.checkAvailability(), highlightthickness=0, relief="flat", borderwidth=0,activebackground = "white",)#,width = 15, height = 3,) text = "Check Availablility", font = ('bold', 10),  fg = "black",
        self.getReadingButton.place(x = 120, y = 660, width = 150, height = 35)
        
    def checker(self):
        if self.__checking == 0:
            self.__checking = 1
            self.showGivenSpot()
            
    def getImage(self, imagename, addnewsize, newsize):
                 
        self.im = Image.open(imagename)        
        if addnewsize: 
            self.im = self.im.resize(newsize, Image.Resampling.LANCZOS)        
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.imageLabel.config(image=self.tk_im)
        
    def checkAvailability(self):
        try:
            self.mainCanvas.delete("text")
        except Exception:
            pass
        
        self.mainCanvas.create_text(int((self.width - 20) / 2), int((self.height - 610) / 2), text = "MegaMart Parking Lot", font = ('bold', 20), anchor = "center", tags = 'text')
        self.mainCanvas.create_text(int((self.width - 20) / 2), int((self.height - 545) / 2), text = "is 600 meters away", font = ('bold', 15), anchor = "center", tags = 'text')
        self.imageLabel = Label(self.mainCanvas,width=355, height=305)
        self.imageLabel.place(x = 12, y = 150)
        self.getImage(files.image_name, True, self.newsize)
        self.getReadings()
        self.mainCanvas.create_text(int((self.width - 20) / 2), 510, text = f'It currently has {self.__readings} available parking spots.', font = ('bold', 13), anchor = "center", tags = 'text')
        self.getReadingButton.config(text = "  Reserve a Spot   ", command = lambda: self.checker())
        
    def showGivenSpot(self):
        self.mySpot = self.__getParkingSpot()
        self.setProgressBar()
        self.getMapImages()        
    
    def getMapImages(self):        
        index = ""
        if self.mySpot[3] < 10:
            index = f'0{self.mySpot[3]}'
        else:
            index = self.mySpot[3]
        entrance = ParkingLot(files.folderpath+"ParkingLot1.txt", #text file
                                "E", #starting point
                                index, #goal
                                1, #type of map
                                self.mySpot[1], #name of the spot
                                files.folderpath+"Entrance.png" #name of the image
                                )#f"Entrance_{self.mySpot[1]}.png") #name of the image
        self.EntranceMap = ImageTk.PhotoImage(entrance.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        exit = ParkingLot(files.folderpath+"ParkingLot1.txt", index, "X", 0, self.mySpot[1], files.folderpath+"Exit.png")#f"Exit_{self.mySpot[1]}.png") f"Leaving {self.mySpot[1]}"
        self.ExitMap = ImageTk.PhotoImage(exit.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        self.getSpotImage()

    def __getParkingSpot(self):
        from random import choice
        availableSpots = []
        for spot in self.__getLotSpotsStatuses: 
            if spot[2] == "A":
                availableSpots.append(spot)
        return choice(availableSpots)

    def getReadings(self):
        with open(files.amount_available) as f:
            line = f.readline()
            if self.__readings is not int(line):
                self.__readings = int(line)
                
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
                
    def getSpotImage(self):
        im = Image.open(files.image_name)
        im1 = im.resize((550, 360), Image.Resampling.LANCZOS)
        x, y = self.mySpot[0]
        x = int(x * 0.97)        
        y = int(y * 0.96)
        return im1.crop((x, y, x + 53, y + 22))   

FindMeParkingApp()





#def createCanvas(self): 
    #self.mainCanvas.config(width = self.width - 30, bg = "white")
    #self.mainCanvas.create_rectangle(3, 3, 381, 732, outline = "black", width = 2)
    #self.mainCanvas.create_text(int((self.width - 20) / 2), int((self.height - 100) / 2), text = "Find Me Parking", font = ('bold', 20), anchor = "center", tags = 'text')
    #self.mainCanvas.place(x = 5, y = 5)