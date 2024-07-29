from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Scrollbar,\
Listbox, Label, Entry, Frame, font, NW, RIGHT, LEFT, BOTH, Y, END
from getParkingLot import GetLot, ParkingLotInfo
from random import choice, randint
from tkinter.ttk import Combobox
from time import strftime, sleep
from PIL import ImageTk, Image
from datetime import datetime
import phonefiles as files
import re

class FindMeParkingApp(Tk):
    #class contructor
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #set window width and height
        self.width, self.height = 400, 750
        #set window geometry, along with window placement
        self.geometry(f'{self.width}x{self.height}+1120+0')
        #window cannot be resized
        self.resizable(False, False)
        self.title("Find Me Parking App")
        self.count, self.unbindEvent = 1, 0
        self.__checking = 0
        self.userExists = False
        self.distanceAway = None
        
        self.homeScreen_bool = False
        self.apLoadingScreen_bool = False
        self.appMainScreen_bool = False        
        self.gettingLotsScreen_bool = False
        self.displayingLotsScreen_bool = False
        self.gettingSpotScreen_bool = False
        self.displayingSpotScreen_bool = False
        
        #User information: this could be placed in 
        #a 'User' class in the future
        self.gender = None
        self.fname, self.lname, self.email = "", "", ""
        self.phone, self.card = 0, 0,
        self.cvv, self.id = "", ""
        self.exp_month, self.exp_year = None, None
        self.username, self.password = "", ""
        #list with month numbers for card expiration date     
        self.months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        
        #global variables set for easy data access
        global gender
        gender = None 
        global fname
        fname = ""
        global lname
        lname = ""
        global email
        email = ""
        global phone
        phone = 0
        global card
        card = 0
        global cvv
        cvv = ""
        global month
        month = None
        global year
        year = None
        global id
        id = ""
        global username
        username = ""
        
        #demo email, to be removed
        self.demoEmail = 'user@mail.com'
        #how many unread mails are in the user inbox
        self.unreadMail = 0
        #user inbox
        self.inbox = []
        #to hold the newly created shape images
        self.shapes = []
        #boolean to check if a parking spot has been assigned to the user
        self.has_activeLot = False
        #UNSURE
        self.createUser = True
        #creates a an object of the 'GetLot' class
        self.parkingLots = GetLot()
        #size for parking lot company logo images 
        self.newsize = (350, 300)
        #frame that surrounds working area
        self.labelFrame = LabelFrame(self, width = self.width - 10, height = self.height - 10)
        self.labelFrame.place(x = 5, y = 5)
        #checks if user already exists
        self.userCheck()
        #calls 'homePage' function
        self.homePage()
        #calls the tkinter 'mainloop' function to start app
        self.mainloop()

    #this function checks if a user account exists
    def userCheck(self):
        try:
            with open(f"{files.user_profile}UserProfile1.txt","r") as file:
                lines = file.readlines()
                if len(lines) > 0:
                    self.username = lines[0].strip('\n')
                    self.password = lines[1].strip('\n')
                    self.gender = lines[2].strip('\n')
                    self.fname = lines[3].strip('\n')
                    self.lname = lines[4].strip('\n')
                    self.email = lines[5].strip('\n')
                    self.phone = int(lines[6].strip('\n'))
                    self.id = lines[7].strip('\n')
                    self.card = int(lines[8].strip('\n'))
                    self.cvv = lines[9].strip('\n')
                    self.exp_month = lines[10].strip('\n')
                    self.exp_year = lines[11].strip('\n')
                    self.userExists = True
                # else:
                    pass
        except:
            pass

    #this function sets a canvas window and a the homescreen image
    def homePage(self):
        self.create_mainCanvas()
        self.addImageToHome()
        
    #this methos creates a canvas called 'mainCanvas' and places it with the labelframe
    def create_mainCanvas(self):
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)

    #this method adds the phone screen image to 'mainCanvas', and binds a function to
    #'mainCanvas' while also unbinding a seperate function from it
    def addImageToHome(self):
        self.setActiveScreen(1)
        #uses PIL to open image
        image = Image.open(files.app_screen)
        #creates a image suitable for the tkinter library
        self.homeScreen_Image = ImageTk.PhotoImage(image)
        #adds image to 'mainCanvas'
        self.mainCanvas.create_image(0, 0, image = self.homeScreen_Image, anchor = NW, tags = "homeScreen")
        #binds function 'checkClick' to 'mainCanvas' when the left click is made
        self.mainCanvas.bind("<ButtonPress-1>", self.checkClick)
        #unbinds the double left click function from 'mainCanvas'
        self.mainCanvas.unbind("<Double-Button-1>")
        
        #uncomment to see rectanges drawn on the home screen
        #self.mainCanvas.create_rectangle(10, 10, 107, 107, outline = "black", width = 2, tags="rectangle")
        #self.mainCanvas.create_rectangle(2, self.height - 80, self.width - 20, self.height - 19, outline = "black", width = 1, tags="rectangle")
        #self.mainCanvas.create_rectangle(98, 216, 195, 313, outline = "black", width = 2, tags="rectangle")
        #(2,670,380,731)

    #this function checks where on 'mainCanvas' the mouse was clicked once (event)
    #and if the event happened in certain regions, certain specific actions
    #would take place
    #note: these events will only work on the home screen
    def checkClick(self,event):
        if self.unbindEvent == 0:
            #if the event occured on or around the app logo
            if 98 < event.x < 195  and 220 < event.y < 313:
                self.unbindEvent = 1
                self.mainCanvas.delete("homeScreen")
                self.start()
            #if the event occured on or around the mailbox logo
            elif 10 < event.x < 107  and 10 < event.y < 107:
                self.unbindEvent = 1 
                self.mainCanvas.delete("homeScreen")
                self.mail()

    #this function checks where on 'mainCanvas' the mouse was clicked twice (event)
    #and if the event happened in a certain region, certain specific action would take place
    #note: this event will not work on the home screen  
    def backtoHome(self, event):
        if self.unbindEvent == 1:
            #if the event occured at the bottom of 'mainCanvas'
            if 2 < event.x < 380 and 670 < event.y < 731:
                self.unbindEvent = 0
                self.createUser = True
                self.mainCanvas.destroy()
                try:
                    self.getReadingButton.destroy()
                except Exception:
                    pass
                self.homePage()

    #this function is the start to the app. here:
    #1. it binds a function 'mainCanvas' while also unbinding a seperate function from it.
    #2. if a parking spot has not already been assigned to the user, it creates a loading screen
    #3. if a parking spot has already been assigned to the user, it decorates 'mainCanvas,'
    #   then goes to display the assigned spot information
    def start(self):        
        #unbinds the single left click function from 'mainCanvas'
        self.mainCanvas.unbind("<ButtonPress-1>")
        #binds function 'backtoHome' to 'mainCanvas' when the left click is made twice
        self.mainCanvas.bind("<Double-Button-1>", self.backtoHome)
        if not self.has_activeLot:
            try:
                #deletes all elements from 'mainCanvas' with the "text" tag
                self.canvas.delete("text")
            except Exception:
                pass
            self.count = 1            
            #adds some text to 'mainCanvas', including the group name at the end of the window
            self.mainCanvas.create_text(200, 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
            self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
            self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group')
            #calls the after method for app loading screen
            self.setActiveScreen(2)
            self.mainCanvas.after(300, self.addImages)
        else:
            #decorates the canvas
            self.decorateCanvas(self.mainCanvas)
            #displays already assigned parking spot
            self.displayParkingSpotInformation()

    #this function is called to animate loading screen
    def create_Shape(self, image,):
        if image == 0:
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        if image == 1:
            self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 2:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20)/2, self.height-20, 4, self.height-20], fill='light sea green', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 3:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), self.height-20 ,(self.width - 20)/2 , self.height-20], fill='spring green', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 4:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) * 2, (self.width - 20), self.height-20], fill='medium spring green', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 5:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), (self.height - 20) / 3, (self.width - 20), ((self.height - 20) / 3) * 2], fill='aquamarine', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 6:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) / 2, (self.width - 20), (self.height - 20) / 3], fill='SpringGreen2', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 7:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2, (self.width - 20), ((self.height - 20) / 3) / 2], fill='PaleGreen1', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        elif image == 8:
            self.mainCanvas.create_polygon([4, 4, (self.width - 20), 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2], fill='azure', tags="shapes")
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
        else:
            self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="circle")
            
    #this function decorates the canvas parameter using different coloured triangles, and a circle,
    #and displays the group name at the end of the window
    def decorateCanvas(self, canvas):
        canvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")
        canvas.create_polygon([4, 4, (self.width - 20)/2, self.height-20, 4, self.height-20], fill='light sea green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), self.height-20 ,(self.width - 20)/2 , self.height-20], fill='spring green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) * 2, (self.width - 20), self.height-20], fill='medium spring green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), (self.height - 20) / 3, (self.width - 20), ((self.height - 20) / 3) * 2], fill='aquamarine', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) / 2, (self.width - 20), (self.height - 20) / 3], fill='SpringGreen2', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2, (self.width - 20), ((self.height - 20) / 3) / 2], fill='PaleGreen1', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2], fill='azure', tags="shapes")
        canvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="shapes")
        canvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group') 

    #this function displays images from a folder in sequence
    #to simulate a loading animation
    def addImages(self):
        #imports the sleep function from the 'time' library 
        if self.count <= 12:      
            try:
                #deletes all elements from 'mainCanvas' with the "loading_image" tag
                self.mainCanvas.delete("loading_image") 
            except Exception:
                pass
            try:
                #deletes all elements from 'mainCanvas' with the "loading_image" tag
                self.mainCanvas.delete('group')
            except Exception:
                pass
            try:
                #deletes all elements from 'mainCanvas' with the "loading_image" tag
                self.mainCanvas.delete('circle')
            except Exception:
                pass
            #--------
            self.create_Shape(self.count - 1)
            #-------------
            self.mainCanvas.create_text(200, 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
            self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group')
            #loads, creates and displays an image on 'mainCanvas'
            loading_image = Image.open(files.loading_gif+f'{self.count}.png')
            self.loading_image = ImageTk.PhotoImage(loading_image)
            
            self.mainCanvas.create_image(100, 320, image = self.loading_image, anchor = NW, tags = "loading_image")
            #increments the count             
            self.count += 1
            #function calls itself
            self.mainCanvas.after(300, self.addImages)
        else:
            #when the count is greater than 12, wait for 1/2 second
            sleep(0.5)
            #deletes all elements from 'mainCanvas' with the "loading_image" and "text' tags
            try:
                self.mainCanvas.delete("loading_image")
            except Exception:
                pass
            try:
                self.mainCanvas.delete("text")
            except Exception:
                pass
            #try:
            #    self.mainCanvas.delete("shapes")
            #except Exception:
            #    pass
                        
            #calls 'createMainButton' function
            self.createMainButton()                

    #this is 1 of 3 times the progress bar will be displayed in this app
    def setProgressBar(self):
        try:
            #destroys 'main' canvas
            self.main.destroy()
        except Exception:
            pass
        #deletes all elements from 'mainCanvas' with the "text' tag
        self.mainCanvas.delete("text")
        #creates some text
        self.mainCanvas.create_text(int((self.width - 20) / 2), 440, text = 'Finding You A Spot', font = ('bold', 12), anchor = "center", tags = 'text')
        #creates a Progressbar object from the ttk library, with specific parameters
        self.p = ttk.Progressbar(self.mainCanvas, orient="horizontal", length=200, mode="determinate", takefocus=True, maximum=100)
        self.p['value'] = 0
        self.p.place(x = int((self.width - 20) / 2), y = 400, anchor = "center",)
        #sets 1 to determine which route we will take after the Progressbar is finished
        self.route = 1
        #calls the after method for the Progressbar
        self.after(1000, self.loading)

    #this function displays the progress bar.
    #for all posibilities afterwards, the Progressbar is destroyed,
    #and all elements from 'mainCanvas' with the "text' tag is deleted.
    #if route is 1, already assigned spot information is displayed
    #if route is 2, the app checks makes a wide check, to see 
    #if there are any available parking spaces
    #if route is 3, the user image button is configured
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
            if self.route == 3:
                self.mainCanvas.delete("text")
                self.p.destroy()                
                self.userExists = True
                self.checkWhichScreenIWasOn()
        else:
            #function calls itself
            self.p.after(1000, self.loading)

    #this function displays the either already assigned parking spot,
    #or the recently generated parking spot
    #note: both buttons created call the same function
    def displayParkingSpotInformation(self):
        self.setActiveScreen(7)
        #this function is called to make 'mainCanvas' scrollable
        self.setScroll()
        if self.userExists:            
            text_1 = 'Not satisfied with this spot?'
            text_2 = 'Click below to change'
            btn_text = "Change Spot"
        else:            
            text_1 = 'To get live updates on parking changes'
            text_2 = 'and mail notification, plus other benefits,'
            btn_text = "Login/Signup here"

        #range is 2 seeing that there are ony 2 images to display
        for i in range(2):
            #creates a temporary canvas 's'
            global s
            s = Canvas(self.frame, bg="azure", width=self.mainCanvas.winfo_reqwidth() - 10, height=self.mainCanvas.winfo_reqheight() - 5, )
            #adds some default text to 's', with stored data
            s.create_text(int(s.winfo_reqwidth() / 2), 80, text = f'{self.activeLot.ParkingLot_name}', font = ('bold', 20), anchor = "center", tags = 'text')
            s.create_text(int(s.winfo_reqwidth() / 2), 160, text = f'Your parking spot is at {self.mySpot[0]}', font = ('bold', 20), anchor = "center", tags = 'text')
            global distances
            s.create_text(int(s.winfo_reqwidth() / 2), 520, text =  f'You are {self.distanceAway}m away', font = ('bold', 13), anchor = "center", tags = 'text')
            #for the 1st digit in the set range
            if i == 0:
                #adds some default text to 's', some with stored data
                s.create_text(int(s.winfo_reqwidth()/2), 120, text = f"Entrance Map", font = ('bold', 20), anchor = "center", tags = 'text')
                #creates and places a button 'back' within 's', to back to previous window
                back = Button(s, text = "BACK", font = ('bold',15), highlightthickness = 0, relief = "flat", borderwidth = 0, bg = "alice blue", fg = "black", justify = "center", command = lambda : self.goback(0))
                back.place(x = 10, y = 10, width = 90, height = 30,)
                #creates a temporary label 'l', and adds the map entrance image to it
                l = Label(s, bg = "PaleTurquoise2", image=self.EntranceMap)
                l.place(x = int(s.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 190, )
                s.create_text(int(s.winfo_reqwidth() / 2), 550, text =  'Please follow this guide map to get to', font = ('bold', 16), anchor = "center", tags = 'text')
                s.create_text(int(s.winfo_reqwidth() / 2), 580, text = f'{self.mySpot[0]} quickly and safely', font = ('bold', 16), anchor = "center", tags = 'text')
                #modified text
                s.create_text(int(s.winfo_reqwidth() / 2), 640, text = text_1, font = ('bold', 9), anchor = "center", tags = 'text')
                s.create_text(int(s.winfo_reqwidth() / 2), 657, text = text_2, font = ('bold', 9), anchor = "center", tags = 'text')                
                #creates a temporary button 'gb', which is also made global
                global gb
                gb = Button(s, text = btn_text, font = ('bold', 9), fg = "medium blue", bg = "azure", highlightthickness = 0, relief = "flat", justify = "center", activebackground = "azure", activeforeground = "medium blue",)
                if self.userExists:            
                    gb.config(command = lambda:  self.changeParkingSpot())
                else:            
                    gb.config(command = lambda: self.userAccount())
                gb.place(x = int(s.winfo_reqwidth() / 2) - 60, y = 665, width = 120)
                #temporary canvas 's' is packed into 'frame'
                s.pack(fill="both", expand=True, )
            #for the 1st digit in the set range
            elif i == 1:
                #adds some default text to 's', some with stored dat
                s.create_text(int(s.winfo_reqwidth()/2), 120, text = f"Exit Map", font = ('bold', 20), anchor = "center", tags = 'text')
                #creates and places a button 'back' within 's', to back to previous window
                back = Button(s, text = "BACK", font = ('bold',15), highlightthickness = 0, relief = "flat", borderwidth = 0, bg = "alice blue", fg = "black", justify = "center", command = lambda : self.goback(0))
                back.place(x = 10, y = 10, width = 90, height = 30,)
                #creates a temporary label 'l', and adds the map exit image to it
                l = Label(s, bg = "PaleTurquoise2", image=self.ExitMap)
                l.place(x = int(s.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 190, )
                s.create_text(int(s.winfo_reqwidth() / 2), 550, text =  'Please follow this guide map to get from', font = ('bold', 16), anchor = "center", tags = 'text')
                s.create_text(int(s.winfo_reqwidth() / 2), 580, text = f'{self.mySpot[0]} to the Exit quickly and safely', font = ('bold', 16), anchor = "center", tags = 'text')
                #modified text
                s.create_text(int(s.winfo_reqwidth() / 2), 640, text = text_1, font = ('bold', 9), anchor = "center", tags = 'text')
                s.create_text(int(s.winfo_reqwidth() / 2), 657, text = text_2, font = ('bold', 9), anchor = "center", tags = 'text')
                #creates a temporary button 'bg', which is also made global
                global bg
                bg = Button(s, text = btn_text, font = ('bold', 9), fg = "medium blue", bg = "azure", highlightthickness = 0, relief = "flat", justify = "center", activebackground = "azure", activeforeground = "medium blue",)
                if self.userExists:            
                    bg.config(command = lambda:  self.changeParkingSpot())
                else:            
                    bg.config(command = lambda: self.userAccount())
                bg.place(x = int(s.winfo_reqwidth() / 2) - 60, y = 665, width = 120)
                #temporary canvas 's' is packed into 'frame'
                s.pack(fill="both", expand=True, )
                
    def changeParkingSpot(self):
        #1st: it destroys a few displays that are either:
        #1. no longer needed
        #2. going to be recreated
        try:
            self.vsb.destroy()
        except Exception:
            pass
        try:
            self.frame.unbind("<Configure>")
            self.frame.destroy()
        except Exception:
            pass
        try:
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Double-Button-1>")
            self.canvas.destroy()
        except Exception:
            pass
        try:
            self.main.destroy()
        except Exception:
            pass
        self.has_activeLot = False
        self.__checking = 0
        self.getLotsLoading()

    #this function configues 'userLabelButton' if a user exists or not
    def setUserButtonIfUserExists(self):
        if self.userExists is False:
            #opens 'no user' image, resizes it, and recreates it
            image = Image.open(files.no_user)
            image = image.resize((50,50), Image.Resampling.LANCZOS)
            self.userLabel_image = ImageTk.PhotoImage(image)
            self.userLabelButton.config(command = lambda : self.noUserButtonClick(), image = self.userLabel_image, state = "normal")
        else: #self.userLabelButton.config( command = lambda : self.closeUserSettings(),)
            #opens 'cat' image, resizes it, and recreates it
            image = Image.open(files.cat)
            image = image.resize((50,50), Image.Resampling.LANCZOS)
            self.userLabel_image = ImageTk.PhotoImage(image)
            self.userLabelButton.config( command = lambda : self.UserSettings(), image = self.userLabel_image, state = "normal")
    
    #this function creates a profile button
    def create_userLabelButton(self):
        #the 'no user' or 'cat' image is added to this 'userLabelButton' button 
        self.userLabelButton = Button(self.mainCanvas, bg = "white", highlightthickness=0, relief="flat", borderwidth=0, )
        #reconfigures 'userLabelButton' if a user profile exists
        self.setUserButtonIfUserExists()
        #'userLabelButton' button is placed with 'mainCanvas'
        self.userLabelButton.place(x = self.mainCanvas.winfo_reqwidth() - self.userLabelButton.winfo_reqwidth() - 4, y = 4,)

    #this function creates 2 buttons for the app home screen
    def createMainButton(self):
        self.setActiveScreen(3)
        #'mainCanvas' is decorated
        self.decorateCanvas(self.mainCanvas)
        #create profile button
        self.create_userLabelButton()        
        #creates a main button to get and display available lots and spots
        self.getReadingButton = Button(self.mainCanvas, bg = "forest green", fg = "white", command = lambda: self.getLotsLoading(), highlightthickness=0, relief="flat", borderwidth=0, text = "Find Me Parking", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white")
        self.getReadingButton.config(width = 15, height = 2)
        self.getReadingButton.place(x = int((self.width) / 2) - int(self.getReadingButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) - 10)
        self.mainCanvas.bind("<Double-Button-1>", self.backtoHome)

    #this function is called when 'userLabelButton' is initially clicked
    def noUserButtonClick(self):
        #'userLabelButton' has its command changed to a new function
        self.userLabelButton.config(command = lambda : self.closenoUserPopupLabel())
        #creates a small canvas 'noUserPopupLabel, adds some text to it, and 
        #creates a button 'noUserPopupLabelButton' on it, with its own command
        self.noUserPopupLabel = Canvas(self.mainCanvas, bg = "spring green", highlightbackground="gray40")
        self.noUserPopupLabel.create_text(65,20,font = ('bold', 10), text = "Log In or Sign Up\nfor added features",)
        self.noUserPopupLabel.place(x = int(self.mainCanvas.winfo_reqwidth() /2), y = 20, width = 130, height = 65)
        self.noUserPopupLabelButton = Button(self.noUserPopupLabel, bg = "forest green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "Get More", fg = "gray16", activebackground="forest green", 
        activeforeground="gray16", command = lambda: self.userAccount())
        self.noUserPopupLabelButton.place(x = 35, y = 40, width = 60)
    
    #this function is called once 'userLabelButton' is clicked
    def closenoUserPopupLabel(self):
        #'userLabelButton' has its command changed to original function
        self.userLabelButton.config(command = lambda : self.noUserButtonClick())
        #'noUserPopupLabel' is destroyed
        self.noUserPopupLabel.destroy()

    #this function is called when 'noUserPopupLabelButton' is clicked
    def userAccount(self):
        if self.createUser is True:
            self.createUser = False
            global bg
            global gb
            try: #noUserPopupLabelButton
                #destroys 'noUserPopupLabel' canvas
                self.noUserPopupLabel.destroy()
            except Exception:
                pass
            try:
                #disables 'getReadingButton' button
                self.getReadingButton.config(state = "disabled")
            except Exception:
                pass
            try:
                #disables 'userLabelButton' button
                self.userLabelButton.config(state = "disabled")
            except Exception:
                pass
            try:
                self.frame.unbind("<Configure>")#, self.onFrameConfigure)
            except Exception:
                pass
            try:
                self.canvas.unbind_all("<MouseWheel>")#, self._on_mousewheel)
            except Exception:
                pass
            #creates a rectange image to blur out the background
            #note: this function uses '**kwargs'. all values that are not of type int
            #will be added to '**kwargs'; it act's like a tuple/set
            try:
                self.create_rectangle(self.mainCanvas,2,2, 382, 731, fill='snow', alpha=.6, tags = "blur")
            except Exception:
                pass
            global s
            try:
                self.create_rectangle(s,2,2, 382, 731, fill='snow', alpha=.6, tags = "blur")
            except Exception:
                pass
            #self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="blur",fill="snow")
            #calls 'LoginScreen' function
            self.LoginScreen()
            #self.RegistrationScreen1()
            #self.RegistrationScreen2()
            #self.RegistrationScreen3()
            #self.confirmRegistration()

    #this function creates a login screen above 'mainCanvas', by creating some text,
    #a few Entry and Button elements, and also a Label element.
    #It also binds a function to 'userAccountCanvas'
    def LoginScreen(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 5))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) ,  bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Login", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
        
        self.userAccountCanvas.create_text(100, 170, text = "Username", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.usernameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global username
        if len(username) != 0:
            self.usernameEntry.insert(0, username)
        self.usernameEntry.place(x = 20, y = 210, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.userAccountCanvas.create_text(100, 330, text = "Password", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.passwordEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center", show = "\u2022",)
        self.passwordEntry.place(x = 20, y = 370, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda : self.userLogin())
        self.login_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 70, y = 460, width = 140, height = 50)
    
        self.userAccountCanvas.create_text(120, 550, text = "Don't have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "login")
        
        self.register_Button = Button(self.userAccountCanvas, text = "Register", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.RegistrationScreen1())
        self.register_Button.place(x = 195, y = 540, width = 60, height = 25)
        
        self.usernameEntry.bind("<FocusIn>", self.clearLabel)
        self.passwordEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)
    
    #this function is called when a user is trying to log in 
    def userLogin(self):
        #if 'usernameEntry' is not blank 
        if len(self.usernameEntry.get()) != 0:
            #if 'passwordEntry' is not blank
            if len(self.passwordEntry.get()) != 0:
                #if the data in 'usernameEntry' is the same ss the user password
                if self.usernameEntry.get() == self.username:
                    #if the data in 'passwordEntry' is the same ss the user password
                    if self.passwordEntry.get() == self.password:
                        #Login is Successful
                        self.userExists = True
                    else:
                        #if username entered != self.username
                        self.empty_Label.config(text = "'Password' invalid", fg = "old lace", bg = "red2")
                else:
                    #if username entered != self.username
                    self.empty_Label.config(text = "'Username' invalid", fg = "old lace", bg = "red2")
            else:
                #if 'passwordEntry' is blank
                self.empty_Label.config(text = "'Password' is blank", fg = "old lace", bg = "red2")
        else:
            #if 'usernameEntry' is blank
            self.empty_Label.config(text = "'Username' is blank", fg = "old lace", bg = "red2")
        try:
            self.empty_Label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)
        except Exception:
            pass        
        self.login_confirm() 
    
    def login_confirm(self):
        self.mini_mainCanvas()
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 60, text = "Logging In", font = ('bold',30), tags = "text",)
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 200, text = "Login may take a couple seconds", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 215, text = "Please be patient", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.p = ttk.Progressbar(self.userAccountCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100,)
        self.p['value'] = 0
        self.p.place(x = int((self.userAccountCanvas.winfo_reqwidth()) / 2), y = 140, anchor = "center",)
        self.route = 3
        self.after(1000, self.loading)
        
    def checkWhichScreenIWasOn(self): #393
        try:
            self.getReadingButton.config(state = "normal", command = lambda: self.getLotsLoading())
        except Exception:
            pass
        try:
            self.setUserButtonIfUserExists()
        except Exception:
            pass
        try:
            self.userLabelButton.config(state = "normal")
        except Exception:
            pass
        try:
            self.frame.bind("<Configure>", self.onFrameConfigure)
        except Exception:
            pass
        try:            
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        except Exception:
            pass        
        #self.createUser = True
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        try:
            self.mainCanvas.delete("blur")
        except Exception:
            pass
        global s
        try:
            s.delete("blur")
        except Exception:
            pass
        if self.displayingSpotScreen_bool:
            self.start()       

    #this function resets the previously disabled buttons, and also resets their commands.
    #also, all 'User information' is reset to their original states. 
    #'userAccountCanvas' is also destroyed, and also the rectange image with the blur 
    def close_resetAll(self):
        try:
            self.getReadingButton.config(state = "normal", command = lambda: self.getLotsLoading())
        except Exception:
            pass
        try:
            self.userLabelButton.config(state = "normal", command = lambda : self.noUserButtonClick())
        except Exception:
            pass
        try:
            self.frame.bind("<Configure>", self.onFrameConfigure)
        except Exception:
            pass
        try:            
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        except Exception:
            pass
        self.userExists = False
        self.createUser = True
        #---------------------------------------------------
        self.gender = None
        self.fname, self.lname, self.email = "", "", ""
        self.phone, self.card = 0, 0, 
        self.cvv, self.id = "", ""
        self.exp_month, self.exp_year = None, None
        self.username, self.password = "", "" 
        #---------------------------------------------------
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        try:
            self.mainCanvas.delete("blur")
        except Exception:
            pass
        global s
        try:
            s.delete("blur")
        except Exception:
            pass

    #this function creates the 1st of 3 registration screens above 'mainCanvas'. It does
    #so by creating some text, a few Entry and Button elements, and also a Label element
    #and a Combobox element. It also binds a function to 'userAccountCanvas'
    def RegistrationScreen1(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 5))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
        
        self.userAccountCanvas.create_text(50, 150, text = "M/F", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")        
        
        self.gender_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.gender_Combo['values'] = ["M","F"]
        self.gender_Combo.config(font = "None 15 normal", )
        global gender
        if gender is not None:
            if gender == "M":
                self.gender_Combo.current(0)
            else:
                self.gender_Combo.current(1)
        self.gender_Combo.place(x = 20, y = 180, height = 40, width = 50)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))
        self.gender_Combo.bind("<<ComboboxSelected>>", self.setGender)
        
        self.userAccountCanvas.create_text(185, 150, text = "First Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.FnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global fname
        if len(fname) != 0:
            self.FnameEntry.insert(0, fname)
        self.FnameEntry.place(x = 100, y = 180, width = 200, height = 40)

        self.userAccountCanvas.create_text(100, 260, text = "Last Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.LnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global lname
        if len(lname) != 0:
            self.LnameEntry.insert(0, lname)
        self.LnameEntry.place(x = 20, y = 290, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.userAccountCanvas.create_text(125, 370, text = "Email Address", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.emailEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global email
        if len(email) != 0:
            self.emailEntry.insert(0, email)
        self.emailEntry.place(x = 20, y = 400, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Next", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda : self.checkBeforeContinueRegistering())
        self.register_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 70, y = 460, width = 140, height = 50)
        
        self.userAccountCanvas.create_text(110, 550, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "login")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 195, y = 540, width = 60, height = 25) 
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 585, text = "NB: Please fill all fields", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.FnameEntry.bind("<FocusIn>", self.clearLabel)
        self.LnameEntry.bind("<FocusIn>", self.clearLabel)
        self.emailEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)

    #this function clears the 'empty_Label' Label, once the user has selected a gender
    def clearLabel(self,event):
        if self.gender is not None:
            #'empty_Label': text is cleard, colours a reset to match 'userAccountCanvas'
            self.empty_Label.config(text = "", fg = "gray79", bg = "gray79")

    #this function is bound to the gender combobox. it assigns the user gender variable
    #to the value received from the gender combobox
    def setGender(self, event):
        self.gender = self.gender_Combo.get()
        self.clearLabel(event) 

    #this function checks if all the necessary parameters are met
    def checkBeforeContinueRegistering(self):
        #if the user gender variable is set
        if self.gender is not None:
            #the global gender is set to the user gender
            global gender 
            gender = self.gender
            #if the first name entry is not empty
            if len(self.FnameEntry.get()) != 0:
                #the user fname is set to the value in the first name entry
                #the global fname is set to the user fname
                self.fname = self.FnameEntry.get()
                global fname 
                fname = self.fname
                #if the last name entry is not empty
                if len(self.LnameEntry.get()) != 0:
                    #the user lname is set to the value in the last name entry
                    #the global lname is set to the user lname
                    self.lname = self.LnameEntry.get()
                    global lname 
                    lname = self.lname
                    #if the email entry is not empty
                    if len(self.emailEntry.get()) != 0:
                        #creates a regular expression to check validity of an email address
                        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                        #if the email address entered matches with the regular expression criteria
                        if(re.fullmatch(regex, self.emailEntry.get())):
                            #the user email is set to the value in the email entry
                            #the global email is set to the user email
                            self.email = self.emailEntry.get()
                            global email
                            email = self.email
                            #calls function for registration screen 2
                            self.RegistrationScreen2()
                        else:
                            #if the email address entered does not match with the regular expression criteria
                            self.empty_Label.config(text = "'Email Address' not valid", fg = "old lace", bg = "red2")    
                    else:
                        #if the email entry is empty
                        self.empty_Label.config(text = "'Email Address' is blank", fg = "old lace", bg = "red2")
                else:
                    #if the last name entry is empty
                    self.empty_Label.config(text = "'Last Name' is blank", fg = "old lace", bg = "red2")
            else:
                #if the first name entry is empty
                self.empty_Label.config(text = "'First Name' is blank", fg = "old lace", bg = "red2")
        else:
            #if the gender combobox was not selected
            self.empty_Label.config(text = "'Gender' is blank", fg = "old lace", bg = "red2")
        self.empty_Label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)

    #this function creates the 2nd of 3 registration screens above 'mainCanvas'. It does
    #so by creating some text, a few Entry, Button and Combobox elements, and also a Label
    #element. It also binds a function to 'userAccountCanvas'
    def RegistrationScreen2(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 5))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
                
        self.userAccountCanvas.create_text(130, 150, text = "Contact Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.phoneEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global phone
        if phone != 0:
            self.phoneEntry.insert(0, phone)
        self.phoneEntry.place(x = 20, y = 180, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)

        self.userAccountCanvas.create_text(110, 260, text = "Card Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cardEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global card
        if card != 0:
            self.cardEntry.insert(0, card)
        self.cardEntry.place(x = 20, y = 290, width = 210, height = 40)
        
        #self.cardType_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "red2" )
        #self.cardType_Label.place(x = 240, y = 290, width = 60, height = 40)
        
        self.userAccountCanvas.create_text(270, 260, text = "CVV", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cvvEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global cvv
        if cvv != 0:
            self.cvvEntry.insert(0, cvv)
        self.cvvEntry.place(x = 240, y = 290, width = 60, height = 40)
        
        self.userAccountCanvas.create_text(85, 375, text = "Expiry Date", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
        self.month_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.month_Combo['values'] = [x for x in self.months]
        self.month_Combo.config(font = "None 15 normal", )
        global month
        if month is not None:            
            self.month_Combo.current(month - 1)                
        self.month_Combo.place(x = 20, y = 400, height = 40, width = 70)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))
        self.month_Combo.bind("<<ComboboxSelected>>", self.setMonth)
        
        cur_year = int(strftime('%y'))
        self.year_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.year_Combo['values'] = [x for x in range(cur_year,100)]
        self.year_Combo.config(font = "None 15 normal", )
        global year
        if year is not None:
            pass           
            self.year_Combo.current(year - cur_year)  
        self.year_Combo.place(x = 90, y = 400, height = 40, width = 70)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))
        self.year_Combo.bind("<<ComboboxSelected>>", self.setYear)
        
        self.userAccountCanvas.create_text(230, 375, text = "Driver's ID", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
        self.idEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global id
        if len(id) != 0:
            self.idEntry.insert(0, id)
        self.idEntry.place(x = 170, y = 400, width = 130, height = 40)
        
        self.back_Button = Button(self.userAccountCanvas, text = "Back", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.setGlobals(1))
        self.back_Button.place(x = 20, y = 460, width = 130, height = 50)
        
        self.next_Button = Button(self.userAccountCanvas, text = "Next", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda:  self.checkBeforeFinishRegistering())
        self.next_Button.place(x = 170, y = 460, width = 130, height = 50)        
        
        self.userAccountCanvas.create_text(110, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 195, y = 535, width = 60, height = 25)
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 585, text = "NB: Please fill all fields", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.phoneEntry.bind("<FocusIn>", self.clearLabel)
        self.cardEntry.bind("<FocusIn>", self.clearLabel)
        self.cvvEntry.bind("<FocusIn>", self.clearLabel)
        self.idEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)

    #this function uses the global variables to populate the tkinter elements in the
    #previous or next registration screens. This is done so the user will not need
    #to retype all the information that had already typed out.
    #NOTE: the password fields will always need to be typed anew.
    def setGlobals(self, i):
        try:
            if len(self.phoneEntry.get()) != 0:
                global phone
                phone = self.phoneEntry.get()
        except Exception:
            pass
        try:
            if len(self.cardEntry.get()) != 0:
                global card
                card = self.cardEntry.get()
        except Exception:
            pass
        try:
            if len(self.cvvEntry.get()) != 0:
                global cvv
                cvv = self.cvvEntry.get()
        except Exception:
            pass
        try:
            if self.exp_month is not None:
                global month
                month = self.exp_month
        except Exception:
            pass
        try:
            if self.exp_year is not None:
                global year
                year = self.exp_year
        except Exception:
            pass
        try:
            if len(self.idEntry.get()) != 0:
                global id
                id = self.idEntry.get()
        except Exception:
            pass
        try:
            if len(self.RusernameEntry.get()) != 0:
                global username
                username = self.RusernameEntry.get()
        except Exception:
            pass
        if i == 1:
            #this function sets this 'i' parameter to 1 once we are on the 2nd 
            #registration page, and need to go back to the 1st registration page
            self.RegistrationScreen1()
        if i == 2:
            #this function sets this 'i' parameter to 2 once we are on the 3rd 
            #registration page, and need to go back to the 2nd registration page
            self.RegistrationScreen2()

    #this function sets the user expiration month variable. it is called when
    #the month combobox is interacted with.
    def setMonth(self,event):
        #this sets the expiration month user variable to 1 PLUS the index of 
        #the data received from the entry 
        self.exp_month = 1 + self.months.index(self.month_Combo.get())
        #calls 'clearLabel' to reset the 'empty_Label' label
        self.clearLabel(event)

    #this function sets the user expiration year variable. it is called when
    #the year combobox is interacted with.
    def setYear(self,event):
        #this converts the data received from the entry to an int,
        #then sets the expiration year user variable to that data
        self.exp_year = int(self.year_Combo.get())
        #calls 'clearLabel' to reset the 'empty_Label' label
        self.clearLabel(event)

    def checkBeforeFinishRegistering(self):
        if len(self.phoneEntry.get()) != 0:
            regex = r'^\d{1,4}\d{7}$'
            if(re.fullmatch(regex,self.phoneEntry.get())):
                self.phone = int(self.phoneEntry.get())
                global phone
                phone = self.phone
                if len(self.cardEntry.get()) != 0:
                    regex = r'^\d{15,16}$'
                    if(re.fullmatch(regex,self.cardEntry.get())):
                        self.card = int(self.cardEntry.get())
                        global card
                        card = self.card
                        if len(self.cvvEntry.get()) != 0:
                            regex = r'^\d{3,4}$'
                            if(re.fullmatch(regex,self.cvvEntry.get())):
                                self.cvv = str(self.cvvEntry.get())
                                global cvv
                                cvv = self.cvv
                                if self.exp_month is not None:
                                    if self.exp_year is not None:
                                        eyear = strftime('%y')
                                        emonth = strftime('%m')
                                        if (self.exp_month >= int(emonth) and self.exp_year >= int(eyear)) or (self.exp_month <= int(emonth) and self.exp_year > int(eyear)):
                                            global month
                                            global year 
                                            month = self.exp_month
                                            year = self.exp_year
                                            if len(self.idEntry.get()) != 0:
                                                regex = r'^\d{9}$'
                                                if(re.fullmatch(regex,self.idEntry.get())):
                                                    self.id = str(self.idEntry.get())
                                                    global id
                                                    id = self.id
                                                    self.RegistrationScreen3()
                                                else:
                                                    self.empty_Label.config(text = "'Driver's ID' not valid", fg = "old lace", bg = "red2")
                                            else:
                                                self.empty_Label.config(text = "'Driver's ID' is blank", fg = "old lace", bg = "red2")
                                        else:
                                            self.empty_Label.config(text = "'Expiry Date' not valid", fg = "old lace", bg = "red2")                             
                                    else:
                                        self.empty_Label.config(text = "'Expiry Date' not complete", fg = "old lace", bg = "red2")
                                else:
                                    self.empty_Label.config(text = "'Expiry Date' not complete", fg = "old lace", bg = "red2")
                            else:
                                self.empty_Label.config(text = "'CVV' is not valid", fg = "old lace", bg = "red2")
                        else:
                            self.empty_Label.config(text = "'CVV' is blank", fg = "old lace", bg = "red2")
                    else:
                        self.empty_Label.config(text = "'Card Number' is not valid", fg = "old lace", bg = "red2")
                else:
                    self.empty_Label.config(text = "'Card Number' is blank", fg = "old lace", bg = "red2")
            else:
                self.empty_Label.config(text = "'Contact Number' is not valid", fg = "old lace", bg = "red2")
        else:
            self.empty_Label.config(text = "'Contact Number' is blank", fg = "old lace", bg = "red2")
        self.empty_Label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)

    #this function creates the 3rd of 3 registration screens above 'mainCanvas'. It does
    #so by creating some text, a few Entry, and Button elements, and also a Label
    #element. It also binds a function to 'userAccountCanvas'
    def RegistrationScreen3(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 5))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) ,  bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
        
        self.userAccountCanvas.create_text(100, 170, text = "Username", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.RusernameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global username
        if len(username) != 0:
            self.RusernameEntry.insert(0, username)
        self.RusernameEntry.place(x = 20, y = 210, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.userAccountCanvas.create_text(100, 330, text = "Password", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.RpasswordEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center", )
        self.RpasswordEntry.place(x = 20, y = 370, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.back_Button = Button(self.userAccountCanvas, text = "Back", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.setGlobals(2))
        self.back_Button.place(x = 20, y = 460, width = 130, height = 50)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Register", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.completeRegistration())
        self.register_Button.place(x = 170, y = 460, width = 130, height = 50) 
        
        self.userAccountCanvas.create_text(110, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 195, y = 535, width = 60, height = 25)
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 585, text = "NB: Please fill all fields", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.RusernameEntry.bind("<FocusIn>", self.clearLabel)
        self.RpasswordEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)
        
    def completeRegistration(self):
        if len(self.RusernameEntry.get()) != 0:
            self.username = self.RusernameEntry.get()
            if len(self.RpasswordEntry.get()) != 0:
                if len(self.RpasswordEntry.get()) >= 8:
                    self.empty_Label.config(text = "", fg = "gray79", bg = "gray79")
                    self.password = self.RpasswordEntry.get()
                    global username
                    username = self.username
                    self.saveAccountInfo()
                else:
                    self.empty_Label.config(text = "'Password' too short", fg = "old lace", bg = "red2")
            else:
                self.empty_Label.config(text = "'Password' is blank", fg = "old lace", bg = "red2")
        else:
            self.empty_Label.config(text = "'Username' is blank", fg = "old lace", bg = "red2")
        self.empty_Label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)
        self.confirmRegistration()     

    #this function writes the 'User information' to a text file
    def saveAccountInfo(self):
        f = open(files.user_profile+"UserProfile.txt", "w")
        f.write(f"{self.username}\n")
        f.write(f"{self.password}\n")       
        f.write(f"{self.gender}\n")
        f.write(f"{self.fname}\n")
        f.write(f"{self.lname}\n")
        f.write(f"{self.email}\n")
        f.write(f"{self.phone}\n")
        f.write(f"{self.id}\n")
        f.write(f"{self.card}\n")
        f.write(f"{self.cvv}\n")            
        f.write(f"{self.exp_month}\n")
        f.write(f"{self.exp_year}")        
        f.close()

    #this is 1 of 3 times the progress bar will be displayed in this app
    #this function creates the mini 'saving data' above 'mainCanvas'.
    def mini_mainCanvas(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 2))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
    #this function creats and displays a small confirmation screen
    def confirmRegistration(self):
        self.mini_mainCanvas()
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 60, text = "Saving Data", font = ('bold',30), tags = "text",)
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 200, text = "Saving may take a couple seconds", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 215, text = "Please be patient", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.p = ttk.Progressbar(self.userAccountCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100,)
        self.p['value'] = 0
        self.p.place(x = int((self.userAccountCanvas.winfo_reqwidth()) / 2), y = 140, anchor = "center",)
        self.route = 3
        self.after(1000, self.loading)

    #this function changes the display image of the 'userLabelButton' button
    def changeImage_Login(self):
        try:
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
            
        image = Image.open(files.cat)
        image = image.resize((50,50), Image.Resampling.LANCZOS)
        self.userLabel_image = ImageTk.PhotoImage(image)
        
        self.getReadingButton.config(state = "normal", command = lambda: self.getLotsLoading())
        self.userLabelButton.config(state = "normal", command = lambda : self.UserSettings(), image = self.userLabel_image)
        self.createUser = True        
        self.userAccountCanvas.destroy()        
        self.mainCanvas.delete("blur")

    #this function is called when 'userLabelButton' is clicked an odd number of times
    #this function reconfigures the command for the 'userLabelButton' button.
    #it also creates a new popup window 'userPopupLabel,' which displays 
    #the user's name, email adress, and 3 buttons: profile, history, and logout
    def UserSettings(self):
        self.userLabelButton.config( command = lambda : self.closeUserSettings(),)
        self.userPopupLabel = Canvas(self.mainCanvas, bg = "spring green", highlightbackground="gray40")
        self.userPopupLabel.place(x = int(self.mainCanvas.winfo_reqwidth() /2), y = 20, width = 130, height = 140)
        self.userPopupLabel.create_text(65,20,font = ('bold', 10), text = f"Welcome {self.fname}", justify = "center", fill = "gray14")
        self.userPopupLabel.create_text(65,35,font = ('bold', 8), text = f"{self.email}", justify = "center", fill = "gray66")
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "previous bookings", fg = "gray16", activebackground="medium spring green", activeforeground="gray16",).place(x = 5, y = 45, height = 30, width = 120)
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "user profile", fg = "gray16", activebackground="medium spring green", activeforeground="gray16",).place(x = 5, y = 75, height = 30, width = 120)
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "log out", fg = "gray16", activebackground="medium spring green", activeforeground="gray16",).place(x = 5, y = 105, height = 30, width = 120)
        
    #this function is called when 'userLabelButton' is clicked an even number of times
    def closeUserSettings(self):
        #'userLabelButton' has its command changed to original function
        self.userLabelButton.config(command = lambda : self.UserSettings())
        #'noUserPopupLabel' is destroyed
        self.userPopupLabel.destroy()

    #this is 1 of 3 times the progress bar will be displayed in this app
    #this function shows a progress bar while setting up to display to
    #assigned parking spot, and entance/exit maps to the user
    def getLotsLoading(self):       
        try:
            self.userPopupLabel.destroy() 
        except Exception:
            pass
        try:
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
        if not self.has_activeLot:
            self.mainCanvas.destroy()
            self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
            self.mainCanvas.place(x = 0, y = 0)
            self.decorateCanvas(self.mainCanvas)
            self.create_userLabelButton()
            try:      
                self.getReadingButton.destroy()
            except Exception:
                pass
            try:
                self.setUserButtonIfUserExists()
            except Exception:
                pass
            try:
                self.noUserPopupLabel.destroy()
            except Exception:
                pass
            self.userLabelButton.config(state="disabled")
            self.mainCanvas.delete("text")
            self.mainCanvas.create_text(int((self.width - 20) / 2), 440, text = 'Loading Parking Lot Database', font = ('bold', 12), anchor = "center", tags = 'text')
            self.p = ttk.Progressbar(self.mainCanvas, orient="horizontal", length=200, mode="determinate",takefocus=True, maximum=100)
            self.p['value'] = 0
            self.p.place(x = int((self.width - 20) / 2), y = 400, anchor = "center",)
            self.setActiveScreen(4)
            self.route = 2
            self.after(1000, self.loading)
        else:
            #decorates the canvas
            self.decorateCanvas(self.mainCanvas)
            #displays already assigned parking spot
            self.displayParkingSpotInformation()

    #this funcion is a basic check and balance 
    def checker(self):
        if self.__checking == 0:
            self.__checking = 1
            #calls the 'showGivenSpot' function
            self.showGivenSpot()

    #this function is called after a loading screen after the user decides to search for a spot
    def checkAvailability(self):
        try:
            self.mainCanvas.delete("text")
        except Exception:
            pass
        self.setActiveScreen(5)
        #this function is called to prepare the widow for a scroll event
        self.setScroll()
        #after the scroll event is created, it is then populated with displays, and information
        self.populate()     

    #this function is called to create a scroll event within the app window 
    def setScroll(self):
        #1st: it destroys a few displays that are either:
        #1. no longer needed
        #2. going to be recreated
        try:
            self.vsb.destroy()
        except Exception:
            pass
        try:
            self.frame.unbind("<Configure>")
            self.frame.destroy()
        except Exception:
            pass
        try:
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Double-Button-1>")
            self.canvas.destroy()
        except Exception:
            pass
        try:
            self.main.destroy()
        except Exception:
            pass
        #create a new 'main' canvas and packs it in to 'mainCanvas'
        #this serves as a container for future widgets
        self.main = Canvas(self.mainCanvas,)
        self.main.pack(side="left", fill="both", expand=True)
        #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
        self.canvas = Canvas(self.main, borderwidth=0, width=self.mainCanvas.winfo_reqwidth() - 10, height=self.mainCanvas.winfo_reqheight() - 10)
        ##create a new 'frame' canvas in the 'canvas' canvas, preset with the width and height of 'mainCanvas'
        self.frame = Canvas(self.canvas, width = self.mainCanvas.winfo_reqwidth(), height = self.mainCanvas.winfo_reqheight() - 10)
        #self.decorateCanvas(self.frame)
        #'vsb' is a Scrollbar event, and it is placed on self
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        #sets a yscrollcommand for the 'canvas' widget
        self.canvas.configure(yscrollcommand=self.vsb.set)
        #places the scrollbar off screen
        self.vsb.place(x = self.mainCanvas.winfo_reqwidth()+30, y = 0)
        #packs the 'camvas' widet into the 'main' widget
        self.canvas.pack(side="left", fill="both", expand=True)
        #sets the 'frame' widget as a window of the 'canvas' widget
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")
        #binds 2 functions to the canvas, and 1 to the frame
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Double-Button-1>", self.backtoHome)

    #this function creates the parking lot objects and displays on the window
    def populate(self):
        #creates a list to store the parking lot objects
        self.lots = []
        global distances
        distances = [100,300,600,400]
        #creates parking lot objects using the object 'parkingLots' of the 'GetLot' class
        for lotname in self.parkingLots.listOfFolders:
            lot = ParkingLotInfo(files.rel_path, lotname)
            #appends each object to the 'lots' list
            self.lots.append(lot)
        #using each parking lot object from the 'lots' list, it:
        for i, lot in enumerate(self.lots):
            #creates a temporary "c" canvas, with a preset width and height 
            c = Canvas(self.frame, bg="azure", width=self.mainCanvas.winfo_reqwidth() - 10, height=self.mainCanvas.winfo_reqheight() - 5, )
            #creates and places a button 'back' within 'c', to back to previous window
            back = Button(c, text = "BACK", font = ('bold',15), highlightthickness = 0, relief = "flat", borderwidth = 0, bg = "alice blue", fg = "black", justify = "center", command = lambda : self.goback(0))
            back.place(x = 10, y = 10, width = 90, height = 30,)
            #adds some text with the parking lot name
            c.create_text(int(c.winfo_reqwidth()/2), 85, text = f"{lot.ParkingLot_name}", font = ('bold', 20), anchor = "center", tags = 'text')
            c.create_text(int(c.winfo_reqwidth()/2), 125, text = f"is {distances[i]} meters away", font = ('bold', 15), anchor = "center", tags = 'text')
            #creates and places a label 'l' within c, which displays the logo of the parking lot object
            l = Label(c, bg = "PaleTurquoise2", image=lot.image)
            l.place(x = int(c.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 150, )
            #adds some text with the parking lot available spots
            c.create_text(int((self.width - 20) / 2), 510, text = f'It currently has {lot.ParkingLot_amountAvailable} available parking spots.', font = ('bold', 13), anchor = "center", tags = 'text')
            #creates and places a button 'b' within 'c', to choose the preferred parking lot object.
            #the 'c' canvas, a colour and the parking lot object are passed in as parameters.
            b = self.setButton(c, "medium spring green", lot, i)
            b.place(x = int(c.winfo_reqwidth()/2) - int(b.winfo_reqwidth()/2), y = 570,)
            #'c' is packed into the 'frame' widget
            c.pack(fill="both", expand=True, )

    #this function allows the user to go back to a previous page
    def goback(self, i):
        if i == 0:
            try:
                self.vsb.destroy()
            except Exception:
                pass
            try:
                self.frame.unbind("<Configure>")
                self.frame.destroy()
            except Exception:
                pass
            try:
                self.canvas.unbind_all("<MouseWheel>")
                self.canvas.unbind_all("<Double-Button-1>")
                self.canvas.destroy()
            except Exception:
                pass
            try:
                self.main.destroy()
            except Exception:
                pass
            self.mainCanvas.destroy()
            self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
            self.mainCanvas.place(x = 0, y = 0)
            self.createMainButton()

    #this function creates a blurred rectangle canvas image object in place of a canvas rectange object
    def create_rectangle(self,canvas,x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            tags = kwargs.pop('tags')
            fill = self.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.shapes.append(ImageTk.PhotoImage(image))
            canvas.create_image(x1, y1, image=self.shapes[-1], anchor='nw', tags = tags)
        canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    #this function returns a button object with specific parameters
    #this button will have a command to set the referred parking lot
    def setButton(self, c, choice, lot, i):
        return Button(c, text="Reserve", font = ('bold',20), command = lambda : self.setParkingLot(lot, i), width = 10, height = 2, highlightthickness = 0, relief = "flat", borderwidth = 0, bg = choice, fg = "black")

    #this function sets the activeLot variable to the selected parking lot object
    def setParkingLot(self, lot, i):
        #reconfigures the command for the 'userLabelButton' button
        self.setUserButtonIfUserExists()
        try:
            #destroys the 'noUserPopupLabel' canvas if it exists
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
        self.activeLot = lot
        global distances
        self.distanceAway = distances[i]
        
        self.has_activeLot = True
        self.checker()

    #this function configues the 'canvas' canvas
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #this function configues the 'canvas' canvas scroll type
    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
        try:
            self.mailBoxCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass

    #this method selects a parking spot for the user
    def showGivenSpot(self):
        self.setActiveScreen(6)        
        #the 'mySpot' variable is assigned a random available spot (type - list)
        self.mySpot = choice(self.activeLot.ParkingLot_availableSpots)
        self.mainCanvas.destroy()
        self.create_mainCanvas()
        self.decorateCanvas(self.mainCanvas)
        self.create_userLabelButton()
        self.userLabelButton.config(state="disabled")
        #displays the progress bar
        self.setProgressBar()
        #creates map images
        self.getMapImages()

    #this function creates 2 images of the parking lot object to display
    def getMapImages(self):
        #imports the 'ParkingLot' class
        from Parking import ParkingLot
        index = ""
        #the 3rd item in the 'mySpot' variable is an integer
        #if this integer is less than 10, the 'index' string become '0+this integer'
        #eg. if the integer is 7, the index becomes "07"
        #if this integer is greater than 10, the 'index' string become 'this integer'
        #eg. if the integer is 17, the index becomes "17"
        if self.mySpot[2] < 10:
            index = f'0{self.mySpot[2]}'
        else:
            index = self.mySpot[2]
        #creates a ParkinLot object 'entrance', using specific parameters 
        entrance = ParkingLot(self.activeLot.ParkingLot_mapcontents, self.activeLot.ParkingLot_sides, "E", index, 1, self.mySpot[0], f"{self.activeLot.path}{self.mySpot[0]}_entrance.png", self.activeLot.ParkingLot_number)
        #creates an 'EntranceMap' image
        self.EntranceMap = ImageTk.PhotoImage(entrance.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        #creates a ParkinLot object 'exit', using specific parameters 
        exit = ParkingLot(self.activeLot.ParkingLot_mapcontents, self.activeLot.ParkingLot_sides, index, "X", 0, self.mySpot[0],  f"{self.activeLot.path}{self.mySpot[0]}_exit.png", self.activeLot.ParkingLot_number)
        #creates an 'ExitMap' image
        self.ExitMap = ImageTk.PhotoImage(exit.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        #If there is an active user present, send them a confirmation mail
        if self.userExists:
            #create entrance map 'mail' item
            mail = Mail(self.activeLot.ParkingLot_name, self.distanceAway, self.mySpot[0], "Entrance Map", 1, datetime.now(), image = self.EntranceMap)
            self.inbox.append(mail)
            #create exit map 'mail' item
            mail = Mail(self.activeLot.ParkingLot_name, self.distanceAway, self.mySpot[0], "Exit Map", 2, datetime.now(), image = self.ExitMap)
            self.inbox.append(mail)

    #this function sets the boolean for each screen
    def setActiveScreen(self, screenNum):
        if screenNum == 1:
            pass
        else:
            self.homeScreen_bool = False
        if screenNum == 2:
            self.apLoadingScreen_bool = True
        else:
            self.apLoadingScreen_bool = False
        if screenNum == 3:
            self.appMainScreen_bool = True
        else:
            self.appMainScreen_bool = False
        if screenNum == 4:
            self.gettingLotsScreen_bool = True
        else:
            self.gettingLotsScreen_bool = False
        if screenNum == 5:
            self.displayingLotsScreen_bool = True
        else:
            self.displayingLotsScreen_bool = False
        if screenNum == 6:
            self.gettingSpotScreen_bool = True
        else:
            self.gettingSpotScreen_bool = False
        if screenNum == 7:
            self.displayingSpotScreen_bool = True
        else:
            self.displayingSpotScreen_bool = False

# MAIL APP STUFF --------------------------------------------------------------------------------------------------

    #this function displays the mailbox window
    def mail(self):
        try:
            self.canvas.delete("text")
        except Exception:
            pass
        self.count = 1
        
        self.mainCanvas.unbind("<ButtonPress-1>")
        self.mainCanvas.bind("<Double-Button-1>", self.backtoHome)
        self.mainCanvas.config(bg = "azure")
        
        self.mainCanvas.create_text(200, 30, text = 'MAILBOX', font = ('bold', 30), anchor = "center", tags = 'text')
        if self.email:
            self.mainCanvas.create_text(200, 60, text = f'{self.email}', font = ('bold', 18), anchor = "center", tags = 'text',fill = "gray31")
        else:
            self.mainCanvas.create_text(200, 60, text = f'{self.demoEmail}', font = ('bold', 18), anchor = "center", tags = 'text',fill = "gray31")
        
        Button(self.mainCanvas, text = 'BACK', relief = "flat", font = ('bold', 15), fg = "blue2", activeforeground = "blue2", bg = "light cyan", activebackground = "light cyan", command = lambda : self.backHome()).place(x = 10, y  = 10)
            
        if len(self.inbox) == 0:
            amnt = "mail"
        else:
            amnt = "mails"
        self.mainCanvas.create_text(200, 85, text = f'{len(self.inbox)} {amnt} in Inbox', font = ('bold', 14), anchor = "center", tags = 'text',fill = "gray50")
        
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="rectangle")       
        
        self.mailBoxCanvas = Canvas(self.mainCanvas, bd = 0, highlightthickness  =2, relief = 'ridge', highlightbackground = "black", bg = "light cyan")
        self.mailBoxCanvas.bind("<Double-Button-1>", self.CloseMailnGoBacktoHome)
        
        #self.mailBoxCanvas.create_rectangle(0, 571, 288, 631, outline = "red", width = 2, tags="rectangle")
        #self.dummyMails()
        if len(self.inbox) == 0:
            self.emptyMailBox()
        else:
            self.gotMail()

    #creates a dummy image for the dummy emails    
    def createDummyImages(self):
        image = Image.open(files.dummy_entrance_image)
        nextimg = image.resize(self.newsize, Image.Resampling.LANCZOS)
        self.dummyEntImage = ImageTk.PhotoImage(nextimg)
        image = Image.open(files.dummy_exit_image)
        nextimg = image.resize(self.newsize, Image.Resampling.LANCZOS)
        self.dummyExtImage = ImageTk.PhotoImage(nextimg)
    
    #this function is used to check if 'self.gotMail()' works properly
    #function is called 14 lines up, and can be commented/uncommented if necessary
    def dummyMails(self):
        self.createDummyImages()
        mail = Mail("First Parking Lot", 100, "A4", "Entrance Map", 1, datetime.now(), self.dummyEntImage)
        self.inbox.append(mail)
        mail = Mail("First Parking Lot", 100, "A4", "Exit Map", 2, datetime.now(), self.dummyExtImage)
        self.inbox.append(mail)
        mail = Mail("Second Parking Lot", 200, "A4", "Entrance Map", 1, datetime.now(), self.dummyEntImage)
        self.inbox.append(mail)
        mail = Mail("Second Parking Lot", 200, "A4", "Exit Map", 2, datetime.now(), self.dummyExtImage)
        self.inbox.append(mail)
        mail = Mail("Third Parking Lot", 300, "A4", "Entrance Map", 1, datetime.now(), self.dummyEntImage)
        self.inbox.append(mail)
        mail = Mail("Third Parking Lot", 300, "A4", "Exit Map", 2, datetime.now(), self.dummyExtImage)
        self.inbox.append(mail)
        mail = Mail("Fourth Parking Lot", 400, "A4", "Entrance Map", 1, datetime.now(), self.dummyEntImage)
        self.inbox.append(mail)
        mail = Mail("Fourth Parking Lot", 400, "A4", "Exit Map", 2, datetime.now(), self.dummyExtImage)
        self.inbox.append(mail)
            
    #this function is called if the mailbox is empty
    def emptyMailBox(self):
        self.mailBoxCanvas.place(x = 100, y = 100, width = (int(self.mainCanvas.winfo_reqwidth() / 4) * 3) - 7, height = self.mainCanvas.winfo_reqheight() - 103,)
        self.listbox = Listbox(self.mainCanvas, font = ('bold', 60), bd = 0, highlightthickness = 2, relief = 'ridge', highlightbackground = "black", bg  ="snow2", selectmode = 'browse', activestyle = "dotbox",) 
        self.listbox.place(x = 2, y = 100, width = int(self.mainCanvas.winfo_reqwidth() / 4) + 3, height = self.mainCanvas.winfo_reqheight() - 103,)
        stop = 0
        while stop < 15:    
            self.listbox.insert(stop, f"",)
            #self.listbox.insert(END,"_ _ _ _")
            if stop % 3 == 0:
                self.listbox.itemconfigure(stop, background = 'papaya whip',)
            elif stop % 3 == 1:
                self.listbox.itemconfigure(stop, background = 'PaleTurquoise2',)
            else:
                self.listbox.itemconfigure(stop, background = 'azure3')
            stop += 1
            
        self.mailBoxCanvas.create_text(int(self.mainCanvas.winfo_reqwidth() / 2) - 50, int(self.mainCanvas.winfo_reqheight() / 2) - 50, text = 'MailBox Empty', font = ('bold', 20), anchor = "center", tags = 'e_mailbox', fill = "midnight blue")

    #this function is called when a populated mail is clicked
    def clickedmail(self, i = None, mail = None):
        popupMail_width = int(self.mainCanvas.winfo_reqwidth() - 12)
        popupMail_height = int(((self.mainCanvas.winfo_reqheight() / 8) * 7) - 7)
        if i is not None:
            if mail.type == 1: #Entrance Map
                txt1 = 'Please follow this guide map to get to'
                txt2 = f'{mail.spot} quickly and safely'
            elif mail.type == 2:
                txt1 = 'Please follow this guide map to get from'
                txt2 = f'{mail.spot} to the Exit quickly and safely' 
            bg = "honeydew4"
            top_fg = "black"
            outline = "black"
            mini_txt = "gray90"
            popupMail = Canvas(self.mainCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 310, y = 10)
            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"Find Me Parking: {mail.header}", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "F", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)
            Label(popupMail, text = "Find Me Parking", font = ('bold',12), fg = mini_txt, bg = bg).place(x = 65, y = 53)
            Label(popupMail, text = f'{mail.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 185, y = 56)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 71)
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = "gray85", tags="rectangle")
            #self, lot_name, distance, spot, header, type, time, image
            popupMail.create_text(int(popupMail_width / 2), 130, text = f'{mail.lot_name}', font = ('bold', 17))
            popupMail.create_text(int(popupMail_width / 2), 155, text = f'{mail.header}', font = ('bold', 15))
            popupMail.create_text(int(popupMail_width / 2), 180, text = f'Your parking spot is at {mail.spot}', font = ('bold', 15))
            image_label = Label(popupMail, bg = bg, image = mail.image)
            image_label.place(x = int(popupMail_width / 2) - int(image_label.winfo_reqwidth() / 2), y = 200)
            popupMail.create_text(int(popupMail_width / 2), 520, text = f'You are {mail.distance}m away', font = ('bold', 12))  
            popupMail.create_text(int(popupMail_width / 2), 540, text = txt1, font = ('bold', 12))
            popupMail.create_text(int(popupMail_width / 2), 560, text = txt2, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 595, text = f'Not satisfied with this spot?', font = ('bold', 9))
            popupMail.create_text(int(popupMail_width / 2), 612, text = f'You can change it in the Find Me Parking App', font = ('bold', 9))
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            popupMail.place(x = 6, y = 93, width = popupMail_width, height = popupMail_height)
        
    #this function creates a canvas widget to display mail information
    def setEmailCanvas(self, canvas, i = None,):
        c = Canvas(canvas, height = 80, width = self.mainCanvas.winfo_reqwidth() - 21, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "F", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.inbox[i].time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "Find Me Parking", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"{self.inbox[i].header} from Find Me Parking", font = ('bold', 12),)
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[Find Me Parking] Your parking spot at {self.inbox[i].lot_name} is...", font = ('bold', 10), )
        
        logo.place(x = 7, y = 7, width = 70, height = 70,)
        time.place(x = 325, y = 5)
        header.place(x = 80, y = 5)
        middle.place(x = 80, y = 36)
        footcontainer.place(x = 80, y = 60, width = 285)
        
        logo.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        time.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        header.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        middle.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        footcontainer.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        footer.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        c.bind("<ButtonPress-1>", lambda event, a = i, b = self.inbox[i]: self.clickedmail(a, b))
        
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

    #this function is calld if the length of the user inbox is not 0
    #it populates the inbox area with mini canvases to show mail information
    def gotMail(self):
        try:
            self.listbox.destroy()
        except Exception:
            pass
        stop = 0
        
        self.mailBoxCanvas.place(x = 2, y = 100, width = self.mainCanvas.winfo_reqwidth() - 4, height = self.mainCanvas.winfo_reqheight() - 103,)
        
        self.mailScroll()
        while stop < (len(self.inbox) + 8):
            if stop <= len(self.inbox) - 1:
                email_thumbnail = self.setEmailCanvas(self.frame, (len(self.inbox) - 1) - stop)                
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
    
    #this function sets the scrolling for the mailbox option
    def mailScroll(self):
        self.main = Canvas(self.mailBoxCanvas, bd = 0, highlightthickness = 0, width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 106,)
        self.main.place(x = 2, y = 2)
        #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
        self.canvas = Canvas(self.main, borderwidth=0, width = self.mainCanvas.winfo_reqwidth() - 12, height = self.mainCanvas.winfo_reqheight() - 111,)
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
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Double-Button-1>", self.backtoHome)

    #this function checks where on 'mainCanvas' the mouse was clicked twice (event)
    #and if the event happened in a certain region, certain specific action would take place
    #note: this event will not work on the home screen 
    def CloseMailnGoBacktoHome(self, event):
        if self.unbindEvent == 1:
            #if the event occured at the bottom of 'mainCanvas'
            if 0 < event.x < 288 and 571 < event.y < 631:
                self.unbindEvent = 0
                self.createUser = True
                self.mainCanvas.destroy()
                self.homePage()
    
    #this function also closes the mail app and takes the user back to the homepage
    def backHome(self):
        self.unbindEvent = 0
        self.createUser = True
        self.mainCanvas.destroy()
        self.homePage()
                
#The mail class
#this is a simple class to construct what the mail is to look like
class Mail:
    def __init__(self, lot_name, distance, spot, header, type, time, image = None):
        self.lot_name = lot_name
        self.distance = distance
        self.spot = spot
        self.image = image
        self.header = header
        self.time = time
        self.type = type

FindMeParkingApp()