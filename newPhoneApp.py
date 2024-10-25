from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, Checkbutton, BooleanVar, \
    Scrollbar, Frame,  Listbox, END, Text, CENTER, messagebox,\
        Entry, ARC, font, RIGHT, LEFT, BOTH, Y, NW, INSERT
from parkingLots_newWith_list import _parkingLots
from getParkingLot_NEW import ParkingLotInfo
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from random import choice, randint
from tkinter.ttk import Combobox
from time import strftime, time
from PIL import ImageTk, Image
import openrouteservice as ors
from datetime import datetime
from itertools import islice
from lorem_text import lorem
from geopy import distance
import phonefiles as files
from os import listdir
import webview as web
import win32api
import re

class FindMeParkingApp(Tk):
    #class contructor
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #set window width and height
        __screen_width = win32api.GetSystemMetrics(0)
        __screen_height = win32api.GetSystemMetrics(1)
        self.width, self.height = int(__screen_width/3.84), int(__screen_height/1.152)
        #set window geometry, along with window placement
        self.geometry(f'{self.width}x{self.height}+300+0')
        #window cannot be resized
        self.resizable(False, False)
        self.wm_minsize(self.width, self.height)
        self.wm_maxsize(self.width, self.height)
        #Make the window jump above all
        self.attributes('-topmost',True)
        self.title("Find Me Parking App")
        self.config(cursor = "hand2")
        #
        self.count, self.unbindEvent = 1, 0
        self.__checking = 0
        self.userExists = False
        self.distanceAway = None
        #booleans for each screen
        self.homeScreen_bool = False
        self.appLoadingScreen_bool = False
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
        self.months = [f"0{i}" if i < 10 else f"{i}" for i in range(1,13)] #["01","02","03","04","05","06","07","08","09","10","11","12"] 
        
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
        
        #NEW
        
        self.client = ors.Client(key = '5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')
        #self.distanceService = Nominatim(user_agent = "geoapiExercises")
        self.locationService = Nominatim(user_agent="Geopy Library")
        self.locations = []
        self.getLocations()
        self.previousbookings_List = []
        self.get_previousbookings()
        self.mySpot = None
        self.termsAgreed = bool(self.checkTerms())
        self.bankBalance = 1000 #MIGHT NEED A SETTER n GETTER
        self.available_lots = {}
        self.more_available_lots = {}
        self.COUNT = 1
        self.left_click, self.canvasCleared, self.right_click, self.route_set, self.selected_a_spot  = False, False, False, False, False
        self.first_weight_const = 0.000001
        self.colours = ['purple', 'gray', 'cadetblue', 'orange', 'pink', 'beige', 'green', 'darkgreen',
                        'lightgreen', 'darkblue', 'lightblue', 'purple', 'lightgray', 'black']        
        
        #NEW
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
        #self.parkingLots = GetLot()
        #size for parking lot company logo images 
        self.newsize = (500, 450)
        #frame that surrounds working area
        self.labelFrame = LabelFrame(self, width = self.width - 10, height = self.height - 10)
        self.labelFrame.pack()#lace(x = 5, y = 5)
        #checks if user already exists
        self.userCheck()
        #calls 'homePage' function
        self.homePage()
        
        self.deiconify()
        #calls the tkinter 'mainloop' function to start app
        #self.open_close()
        self.run_app()
        
    def set_bankBalance(self, bankBalance:int):
        self.bankBalance = bankBalance

    def run_app(self):
        #self.lift()
        self.mainloop()

    #this function checks if a user account exists
    def userCheck(self):
        try:
            with open(f"{files.user_profile}UserProfile.txt","r") as file:
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
                    #self.userExists = False
        except:
            pass
        self.userMetTerms()

    def userMetTerms(self):
        if self.userExists:
            self.termsMet(1)

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
        image = Image.open(files.phone_app_screen)
        #creates a image suitable for the tkinter library
        self.homeScreen_Image = ImageTk.PhotoImage(image)
        #adds image to 'mainCanvas'
        self.mainCanvas.create_image(4,4, image = self.homeScreen_Image, anchor = NW, tags = "homeScreen")
        #binds function 'checkClick' to 'mainCanvas' when the left click is made
        self.mainCanvas.bind("<ButtonPress-1>", self.checkClick)
        #self.mainCanvas.bind("<ButtonPress-1>", self.showClick)
        #unbinds the double left click function from 'mainCanvas'
        self.mainCanvas.unbind("<Double-Button-1>")
        
        #uncomment to see rectanges drawn on the home screen
        #self.mainCanvas.create_rectangle(23, 24, 130, 130, outline = "black", width = 2, tags="rectangle")
        #self.mainCanvas.create_rectangle(2, self.height - 80, self.width - 20, self.height - 19, outline = "black", width = 1, tags="rectangle")
        #self.mainCanvas.create_rectangle(125, 276, 240, 388, outline = "black", width = 2, tags="rectangle")
        #(2,670,380,731)

    #this function checks where on 'mainCanvas' the mouse was clicked once (event)
    #and if the event happened in certain regions, certain specific actions
    #would take place
    #note: these events will only work on the home screen
    def checkClick(self,event):
        if self.unbindEvent == 0:
            #if the event occured on or around the app logo
            if 125 < event.x < 240 and 276 < event.y < 388: #125, 276, 240, 388,
                self.unbindEvent = 1
                self.mainCanvas.delete("homeScreen")
                if not self.termsAgreed:
                    self.termsAndConditions()
                else:
                    self.start()
            #if the event occured on or around the mailbox logo
            elif 23 < event.x < 130  and 24 < event.y < 130: #23, 24, 130, 130,
                self.unbindEvent = 1 
                self.mainCanvas.delete("homeScreen")
                #self.view_previousbookings()
                self.mail()
                
    def checkTerms(self):
        try:
            with open(f"{files.user_profile}terms_met.txt","r") as file:                
                return int(file.read())
        except Exception:
            return 0

    def termsAndConditions(self):
        self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="main-rectangle")
        self.decorateCanvas(self.mainCanvas)
        self.create_rectangle(self.mainCanvas,3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, fill='snow', alpha=.6, tags = "blur")
        
        #self.mainCanvas.create_text(55, 155, text = ">>>", font=("bold",16), activefill = "red", tags = "terms")
               
        self.termsAndConditionsBox = Text(self.mainCanvas, font = ("calibri", 12), relief = "flat", width = 32, height = 19,)
        self.termsAndConditionsBox.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2),
                                         y = 155,)#int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight() / 2))
        self.termsAndConditionsBox.insert(INSERT, "\n\n")
        self.termsAndConditionsBox.insert(INSERT, self.getText())
        
        self.headerLabel = Label(self.mainCanvas, text = "TERMS AND CONDITIONS", font = ("calibri", 14, 'underline'), bg = "#ffffff")
        self.headerLabel.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), 
                               y = 125, width = self.termsAndConditionsBox.winfo_reqwidth(), height = 30)
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight()) - int(self.headerLabel.winfo_reqheight()) + 158, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 1, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()/2) + int(self.headerLabel.winfo_reqheight()/2) - 92, 
        outline = "black", width = 2, tags = "terms")
        
        self.check_variable = BooleanVar()
        self.agree_disagree = Checkbutton(self.mainCanvas, text = "   I accept these Terms and Conditions  ", onvalue = 1, offvalue = 0, font = ('bold', 10), bg = "#ffffff", variable = self.check_variable, command = self.toggle_button_state, )
        self.agree_disagree.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight() / 2) + int(self.headerLabel.winfo_reqheight() / 2) - 90, width=int(self.termsAndConditionsBox.winfo_reqwidth()))        
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2,
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight() / 2) + int(self.headerLabel.winfo_reqheight() / 2) - 91, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 1, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()/2) + int(self.headerLabel.winfo_reqheight() /2) - 59, 
        outline = "black", width = 2, tags = "terms")
        
        self.acceptTermsAndConditionButton = Button(self.mainCanvas, text = "continue", font = ('bold', 12), relief = "flat", state = "disabled", command = self.termsAndContidionsAgreed)
        self.acceptTermsAndConditionButton.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) , 
                                                 y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight() / 2) + int(self.headerLabel.winfo_reqheight() / 2) - 58, 
                                                 width = int(self.termsAndConditionsBox.winfo_reqwidth() ))
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2,
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight() / 2) + int(self.headerLabel.winfo_reqheight() / 2) - 59, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 1, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight() / 2) + int(self.headerLabel.winfo_reqheight() / 2) - 16, 
        outline = "black", width = 2, tags = "terms")

    def termsAndContidionsAgreed(self):
        self.termsMet(1)
        self.mainCanvas.delete("terms")
        self.mainCanvas.delete("blur")
        self.mainCanvas.delete("shapes")
        self.agree_disagree.destroy()
        self.headerLabel.destroy()
        self.termsAndConditionsBox.destroy()
        self.acceptTermsAndConditionButton.destroy()        
        self.start()

    def termsMet(self, met: int):
        self.termsAgreed = True
        with open(f"{files.user_profile}terms_met.txt","w") as file:
            file.write(str(met))

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

    #this function checks where on 'mainCanvas' the mouse was clicked twice (event)
    #and if the event happened in a certain region, certain specific action would take place
    #note: this event will not work on the home screen  
    def backtoHome(self, event):
        if self.unbindEvent == 1:
            #if the event occured at the bottom of 'mainCanvas'
            if 2 < event.x < self.width - 20 and self.height - 80 < event.y < self.height - 19:
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
        try:
            self.mainCanvas.unbind("<ButtonPress-1>")
        except Exception:
            pass
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
            self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth() / 2), 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
            self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")
            self.mainCanvas.create_text(self.mainCanvas.winfo_reqwidth() - 10, self.mainCanvas.winfo_reqheight() - 20, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group')
            #calls the after method for app loading screen
            self.setActiveScreen(2)
            global no_of_images
            no_of_images = len([image for image in listdir(files.loading_gif)])
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
            self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")
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
    def decorateCanvas(self, canvas: Canvas):
        try: canvas.delete("rectangle")
        except Exception: pass
        try: canvas.delete("shapes")
        except Exception: pass
        canvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")
        canvas.create_polygon([4, 4, (self.width - 20)/2, self.height-20, 4, self.height-20], fill='light sea green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), self.height-20 ,(self.width - 20)/2 , self.height-20], fill='spring green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) * 2, (self.width - 20), self.height-20], fill='medium spring green', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), (self.height - 20) / 3, (self.width - 20), ((self.height - 20) / 3) * 2], fill='aquamarine', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) / 2, (self.width - 20), (self.height - 20) / 3], fill='SpringGreen2', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2, (self.width - 20), ((self.height - 20) / 3) / 2], fill='PaleGreen1', tags="shapes")
        canvas.create_polygon([4, 4, (self.width - 20), 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2], fill='azure', tags="shapes")
        canvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="shapes")
        canvas.create_text(canvas.winfo_reqwidth() - 10, canvas.winfo_reqheight() - 20, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group') 

    #this function displays images from a folder in sequence
    #to simulate a loading animation
    def addImages(self):
        #there are 12 files in the directory.
        #this will be fixed to be more dynamic
        if self.count <= no_of_images:      
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
            #self.mainCanvas.create_text(200, 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
            self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth() / 2), 150, text = 'Capstone Group 3', font = ('bold', 20), anchor = "center", tags = 'text')
            self.mainCanvas.create_text(self.mainCanvas.winfo_reqwidth() - 10, self.mainCanvas.winfo_reqheight() - 20, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group')
            #loads, creates and displays an image on 'mainCanvas'
            loading_image = Image.open(files.loading_gif+f'{self.count}.png')
            self.loading_image = ImageTk.PhotoImage(loading_image.resize((251,156)))
            self.mainCanvas.create_image(int(self.mainCanvas.winfo_reqwidth() / 2) - 120, 320, image = self.loading_image, anchor = NW, tags = "loading_image")
            #increments the count             
            self.count += 1
            #function calls itself
            self.mainCanvas.after(300, self.addImages)
        else:
            #when the count is greater than 12, wait for 1/2 second
            self.mainCanvas.after(500,)
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
    def setProgressBar(self,):
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
        self.after(1000, self.loading) #car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str,

    #this function displays the progress bar.
    #for all posibilities afterwards, the Progressbar is destroyed,
    #and all elements from 'mainCanvas' with the "text' tag is deleted.
    #if route is 1, already assigned spot information is displayed
    #if route is 2, the app checks makes a wide check, to see 
    #if there are any available parking spaces
    #if route is 3, the user image button is configured
    #immages 251x156
    def loading(self,):
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
                self.termsAgreed = True
                self.userMetTerms()
                self.createSecondMainButton()
                self.checkWhichScreenIWasOn()
        else:
            #function calls itself
            self.p.after(1000, self.loading)

    #this function displays the either already assigned parking spot,
    #or the recently generated parking spot
    #note: both buttons created call the same function
    def displayParkingSpotInformation(self,):
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
        fill = "azure"
        #range is 2 seeing that there are ony 2 images to display
        for i in range(2):
            #creates a temporary canvas 's'
            global s
            s = Canvas(self.frame, bg=fill, width=self.mainCanvas.winfo_reqwidth() - 10, height=self.mainCanvas.winfo_reqheight() - 5, )
            #adds some default text to 's', with stored data
            lotname = self.lot_name.replace('\n', '')
            lot_lbl1 = Label(s, text = f"{lotname}", font = ('bold',20), fg = "green", bg = fill, justify = "center", wraplength=s.winfo_reqwidth()-20)
            if len(lotname) > 30:
                lot_lbl1.place(x = int(s.winfo_reqwidth()/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 70)
            else:
                lot_lbl1.place(x = int(s.winfo_reqwidth()/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 90)
                
            #s.create_text(int(s.winfo_reqwidth() / 2), 100, text = f'{self.lot_name}', font = ('bold', 20), anchor = "center", tags = 'text', fill = "green")
            s.create_text(int(s.winfo_reqwidth() / 2), 218, text = f'Your parking spot is at {self.mySpot[0]}', font = ('bold', 18), anchor = "center", tags = 'text')
            global distances
            s.create_text(int(s.winfo_reqwidth() / 2), 725, text =  f'You are {self.distanceFromYOU:.2f}km away', font = ('bold', 13), anchor = "center", tags = 'text')
            #creates a temporary button 'gb', which is also made global
            global gb
            gb = Button(s, text = btn_text, font = ('bold', 9), fg = "medium blue", bg = fill, highlightthickness = 0, relief = "flat", justify = "center", activebackground = "azure", activeforeground = "medium blue",)
            if self.userExists:            
                gb.config(command = lambda: self.changeParkingSpot())
            else:            
                gb.config(command = lambda: self.userAccount())
            gb.place(x = int(s.winfo_reqwidth() / 2) - 60, y = 860, width = 120)
            url_btn = Button(s, text = "click here for directions to your location", font = ('bold',9,'underline'), fg = "blue", bg = fill, justify = "center", relief='flat',highlightthickness=0, bd=0, borderwidth=0, activebackground = fill, activeforeground="blue", command=self.openURL)
            url_btn.place(x = int(s.winfo_reqwidth()/2) - int(url_btn.winfo_reqwidth()/2), y = 885)
            
            #for the 1st digit in the set range
            if i == 0:
                #adds some default text to 's', some with stored data
                s.create_text(int(s.winfo_reqwidth()/2), 175, text = f"Entrance Map", font = ('bold', 20), anchor = "center", tags = 'text')
                #creates and places a button 'back' within 's', to back to previous window
                back = Button(s, text = "BACK", font = ('bold',15), highlightthickness = 0, relief = "flat", borderwidth = 0, bg = "alice blue", fg = "black", justify = "center", command = lambda : self.goback(0))
                back.place(x = 10, y = 10, width = 90, height = 30,)
                #creates a temporary label 'l', and adds the map entrance image to it
                l = Label(s, bg = "PaleTurquoise2", image=self.EntranceMap)
                l.place(x = int(s.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 245, )
                s.create_text(int(s.winfo_reqwidth() / 2), 755, text =  'Please follow this guide map to get to', font = ('bold', 14), anchor = "center", tags = 'text', fill = "red")
                s.create_text(int(s.winfo_reqwidth() / 2), 785, text = f'{self.mySpot[0]} quickly and safely', font = ('bold', 14), anchor = "center", tags = 'text', fill = "red")
                #modified text
                s.create_text(int(s.winfo_reqwidth() / 2), 835, text = text_1, font = ('bold', 9), anchor = "center", tags = 'text') #580
                s.create_text(int(s.winfo_reqwidth() / 2), 852, text = text_2, font = ('bold', 9), anchor = "center", tags = 'text')                
                #temporary canvas 's' is packed into 'frame'
                s.pack(fill="both", expand=True, )
            #for the 1st digit in the set range
            elif i == 1:
                #adds some default text to 's', some with stored dat
                s.create_text(int(s.winfo_reqwidth()/2), 175, text = f"Exit Map", font = ('bold', 20), anchor = "center", tags = 'text')
                #creates and places a button 'back' within 's', to back to previous window
                back = Button(s, text = "BACK", font = ('bold',15), highlightthickness = 0, relief = "flat", borderwidth = 0, bg = "alice blue", fg = "black", justify = "center", command = lambda : self.goback(0))
                back.place(x = 10, y = 10, width = 90, height = 30,)
                #creates a temporary label 'l', and adds the map exit image to it
                l = Label(s, bg = "PaleTurquoise2", image=self.ExitMap)
                l.place(x = int(s.winfo_reqwidth()/2) - int(l.winfo_reqwidth()/2), y = 245, )
                s.create_text(int(s.winfo_reqwidth() / 2), 755, text =  'Please follow this guide map to get from', font = ('bold', 14), anchor = "center", tags = 'text', fill = "red")
                s.create_text(int(s.winfo_reqwidth() / 2), 785, text = f'{self.mySpot[0]} to the Exit quickly and safely', font = ('bold', 14), anchor = "center", tags = 'text', fill = "red")
                #modified text
                s.create_text(int(s.winfo_reqwidth() / 2), 835, text = text_1, font = ('bold', 9), anchor = "center", tags = 'text')
                s.create_text(int(s.winfo_reqwidth() / 2), 852, text = text_2, font = ('bold', 9), anchor = "center", tags = 'text')
                #temporary canvas 's' is packed into 'frame'
                s.pack(fill="both", expand=True, )
                
    def openURL(self):
        Browser(title=f"{self.mySpot[0]} @ {self.lot_name}", url=self.loturl, width = self.mainCanvas.winfo_reqwidth() - 70, height = self.mainCanvas.winfo_reqheight() - 120,)
                
    def changeParkingSpot(self,):
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
        try:
            self.userLabelButton.destroy()
        except Exception:
            pass
        global map_canvas
        map_canvas.bind_all("<MouseWheel>", lambda event, canvas = map_canvas: self._on_mousewheel(event, canvas))
        self.has_activeLot, self.selected_a_spot, self.route_set = False, False, False
        self.__checking = 0
        self.map_container.pack()        
        self.set_Max_Min_Zoom(3,22)
        #self.getLotsLoading()

    #this function configues 'userLabelButton' if a user exists or not
    def setUserButtonIfUserExists(self):
        if self.userExists is False:
            #opens 'no user' image, resizes it, and recreates it
            image = Image.open(files.no_user)
            image = image.resize((70,70), Image.Resampling.LANCZOS)
            self.userLabel_image = ImageTk.PhotoImage(image)
            self.userLabelButton.config(command = lambda : self.noUserButtonClick(), image = self.userLabel_image, state = "normal")
        else: #self.userLabelButton.config( command = lambda : self.closeUserSettings(),)
            #opens 'cat' image, resizes it, and recreates it
            image = Image.open(files.cat)
            image = image.resize((70,70), Image.Resampling.LANCZOS)
            self.userLabel_image = ImageTk.PhotoImage(image)
            self.userLabelButton.config(command = lambda : self.UserSettings(), image = self.userLabel_image, state = "normal")
    
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
        self.getReadingButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Find Close-By", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white", command = self.appMap,) #command = lambda: self.getLotsLoading(),)
        self.getReadingButton.config(width = 15, height = 2) #freeUseButton
        self.getReadingButton.place(x = int((self.width) / 2) - int(self.getReadingButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) - 60)
        self.createSecondMainButton()
        self.mainCanvas.bind("<Double-Button-1>", self.backtoHome)
        
    def createSecondMainButton(self):
        if self.userExists:
            self.reserveSpotButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Reserve Parking", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white")
            self.reserveSpotButton.config(width = 15, height = 2, )
            self.reserveSpotButton.place(x = int((self.width) / 2) - int(self.reserveSpotButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) + 60)

#NEW PROGRAM STUFF

    def backToMainScreen(self):
        self.clearMapMarkings()
        try:
            self.map_container.destroy()
        except Exception:
            pass
        try:
            self.map_frame.destroy()
        except Exception:
            pass
        try:
            self.map_main.destroy()
        except Exception:
            pass
        try:
            self.resultsCanvas.destroy()
        except Exception:
            pass
        try:
            self.searchFrame.destroy()
        except Exception:
            pass
        self.left_click = False
        self.createMainButton()
        
    def appMap(self):
        try:
            self.clearCanvasToLayMap()
        except Exception:
            pass
        try:
            self.userLabelButton.destroy()
        except Exception:
            pass
        try:
            self.getReadingButton.place_forget()
        except Exception:
            pass
        try:
            self.reserveSpotButton.place_forget()
        except Exception:
            pass
        
        self.map_container = Frame(self.mainCanvas, width = self.mainCanvas.winfo_reqwidth(), height = self.mainCanvas.winfo_reqheight(),)
        self.map_container.pack()#place(x = 0, y = 0)
        
        self.map_widget = TkinterMapView(self.map_container, width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 8,corner_radius = 2)
        self.map_widget.place(x = 4, y = 4)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22,)
        #coordinates_tuple = choice(files.locations)
        coordinates_tuple = (18.012265695689663, -76.79800557291115)#
        self.map_widget.set_position(coordinates_tuple[0], coordinates_tuple[1], marker = False,)
        
        self.map_widget.set_zoom(16)
        self.map_widget.add_left_click_map_command(self.left_click_event)
        
        self.left_click_event(coordinates_tuple)
        
        #0.005, 
        #if self.canvasCleared:
            #self.createUserButton()
            #self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")
            
    def create_squares(self, car_pos: tuple):
        self.map_widget.set_position(car_pos[0], car_pos[1], marker = False)
        self.map_widget.set_marker(car_pos[0], car_pos[1], text = "YOU", text_color = "black")
        FIRST_LIMIT = 8
        
        global COUNT, COLOUR
        btn_width, btn_height = 30, 30
        COLOUR = 0
        second_weight_const = 0.02
        EXCLUDE = False
        WEIGHT = self.first_weight_const
        
        doubleup = "\u21EE"
        up = "\u21E7"
        #down = "\u21E9"
        
        if not self.right_click:
            self.map_widget.add_right_click_menu_command(label = "Restart", pass_coords = False, command = lambda: self.right_click_event(btn_width, btn_height, up, doubleup), )
            self.right_click = True
        
        while len(self.available_lots) != FIRST_LIMIT :
            for name, coord in _parkingLots.items():
                self.check_if_in_range(car_pos, name, coord, WEIGHT)
            WEIGHT += self.first_weight_const
            self.COUNT += 1
            if WEIGHT >= second_weight_const:
                EXCLUDE = True
                break

        show_more = False        
        if len(self.available_lots) > 0:
            
            for name in self.available_lots.keys():            
                self.calculate_route_distance(car_pos, name, (self.available_lots[name][0][0], self.available_lots[name][0][1]), self.available_lots)
            
            if not EXCLUDE:
                self.exclude_already_added(car_pos, WEIGHT, second_weight_const)
                show_more = True
                
                cap = 5
                for lot in islice(self.more_available_lots.items(), cap):
                    self.calculate_route_distance(car_pos, lot[0], (lot[1][0][0], lot[1][0][1]), self.more_available_lots)

        self.addSearch_andResults(car_pos, up, doubleup, btn_width, btn_height, show_more)
        
    def check_if_in_range(self, car_pos: tuple, name: str, coord: list, weight: float):    
        lat = coord[0][0]
        lon = coord[0][1]
        if car_pos[0] + weight > lat and lon > car_pos[1] - weight:
            if car_pos[0] + weight > lat and lon < car_pos[1] + weight:
                if car_pos[0] - weight < lat and lon < car_pos[1] + weight:
                    if car_pos[0] - weight < lat and lon > car_pos[1] - weight:
                        self.add_to_map(car_pos, name, coord, weight)                    

    def add_to_map(self, car_pos: tuple, name: str, coord: list, weight: float):
        if name not in self.available_lots.keys():
            self.available_lots[name] = coord

    def calculate_route_distance(self, car_pos: tuple, name: str, found_lot: tuple, lots_dict: dict, draw_marker: bool = False, draw_route: bool = False,): 
        route = self.client.directions(coordinates = [[car_pos[1], car_pos[0]], [found_lot[1], found_lot[0]]],
                                profile = 'driving-car', format = 'geojson',)
        route_coordinates = [tuple(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
        route_coordinates.insert(0, tuple(car_pos))
        route_coordinates.insert(len(route_coordinates), (found_lot[0], found_lot[1]))
        if draw_marker:
            self.map_widget.set_marker(found_lot[0],found_lot[1], text = name, text_color = "green")
        if draw_route:
            self.map_widget.set_path(position_list = route_coordinates, color = self.colours[COLOUR], width = 2)
            COLOUR += 1
            
        route_distance, start, end = 0, 0, 1
        while end < len(route_coordinates): # <<<<<<<<< HERESO
            route_distance += distance.distance(route_coordinates[start], route_coordinates[end]).km
            start += 1
            end += 1

        lots_dict[name].append(distance.distance(car_pos, found_lot).km)
        lots_dict[name].append(route_coordinates)
        lots_dict[name].append(route_distance)

    def exclude_already_added(self, car_pos: tuple, weight2: float, final_weight: float):
        while weight2 <= final_weight:
            for name, coord in _parkingLots.items():
                if name not in self.available_lots.keys():
                    self.check_for_others(car_pos, name, coord, weight2)
                weight2 += self.first_weight_const       
                    
    def check_for_others(self, car_pos: tuple, name: str, coord: list, weight2: float):
        lat = coord[0][0]
        lon = coord[0][1]
        if car_pos[0] + weight2 > lat and lon > car_pos[1] - weight2:
            if car_pos[0] + weight2 > lat and lon < car_pos[1] + weight2:
                if car_pos[0] - weight2 < lat and lon < car_pos[1] + weight2:
                    if car_pos[0] - weight2 < lat and lon > car_pos[1] - weight2:
                        if name not in self.more_available_lots.keys():
                            self.more_available_lots[name] = coord

    def addSearch_andResults(self, car_pos:tuple, up:str, doubleup:str, btn_width:int, btn_height:int, show_more:bool = False,):

        self.entry_width = 220
        search_colour = "gray78"
        self.results_canvas_mini_height = 50
        self.results_canvas_mid_height = 380
        self.results_canvas_full_height = 710
        
        canvas_height = self.results_canvas_mini_height
        
        self.backToMainScreenButton = Button(self.map_container, text = "x", font = ("bold", 15), relief = "flat", bg = search_colour, activebackground = "#ffffff", bd = 0, highlightthickness = 0, border = 0, fg = "red", activeforeground = "red", command = lambda : self.backToMainScreen(),)
        self.backToMainScreenButton.place(x = self.mainCanvas.winfo_reqwidth() - 20 - 50, y = 20, width = 50, height = 50)
        
        self.searchFrame = Frame(self.map_container, bd = 0, bg = search_colour, width = 220 + 35 + 20 + 10, height = 32)
        #self.searchFrame.place(x = int(self.mainCanvas.winfo_reqwidth()/2) - int(self.searchFrame.winfo_reqwidth()/2) , y = 20,)
        
        self.findLocation = Entry(self.searchFrame, bd = 0, bg = search_colour, font = ('bold',15), relief = "flat", highlightthickness = 0, border = 0, fg = "gray18")
        self.findLocation.place(x = 10, y = 1, width = self.entry_width, height = 30)
        
        self.clearButton = Button(self.searchFrame, text = "x", relief = "flat", bg = search_colour, activebackground = "#ffffff", bd = 0, highlightthickness = 0, border = 0, activeforeground = "red", command = lambda : self.clearEntry(),)
        self.clearButton.place(x = self.entry_width + 10 , y = 1, width = 20, height = 30)
        
        self.searchButton = Button(self.searchFrame, text = "find", relief = "flat", bg = "lightgray", fg = "green", activebackground = "lightgray", activeforeground = "green", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.searchMap())
        self.searchButton.place(x = self.entry_width + 10 + 20, y = 1, width = 35, height = 30)
        
        self.resultsCanvas = Canvas(self.map_container, bg = search_colour, bd= 0, highlightthickness = 0, border = 0,)
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        self.resultsLabel = Label(self.resultsCanvas, text = f"Results:  {len(self.available_lots)}", font = ("calibri", 18, 'bold'), bg = search_colour)
        self.resultsLabel.place(x = 10, y = 7)        
        
        self.results_halfScreen = Canvas(self.resultsCanvas, relief = "flat", bg = search_colour, borderwidth = 0, bd = 0, highlightthickness = 0, border = 0,)
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = up, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        self.mini_panel, self.midi_panel, self.maxi_panel = True, False, False
        #self.checkPanelSize()
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = up,
                                     e = doubleup,
                                     #f = results_canvas_mini_height,
                                     #g = results_canvas_full_height
                                     : 
                                     self.midimize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_halfScreen.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief = "flat"))
        self.results_halfScreen.place(x = int(self.resultsCanvas.winfo_reqwidth()/2)-btn_width, y = 15, width = btn_width, height = btn_height)     
        
        self.results_fullScreen = Canvas(self.resultsCanvas, relief = "flat", bg = search_colour, borderwidth = 0, bd = 0, highlightthickness = 0, )
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = doubleup, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = up,
                                     e = doubleup,
                                     #f = results_canvas_mini_height,
                                     #g = results_canvas_mid_height
                                     : 
                                     self.maximize_resultsCanvas(event, a, b, c, d, e,))
        self.results_fullScreen.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief = "flat"))
        self.results_fullScreen.place(x = int(self.resultsCanvas.winfo_reqwidth()/2), y = 15, width = btn_width, height = btn_height)
        
        self.resultsCanvas.create_line(int(self.resultsCanvas.winfo_reqwidth()/2)-btn_width,10,int(self.resultsCanvas.winfo_reqwidth()/2)+btn_width,10, width = 5, fill = "gray64")
        
        self.sideWidgetDataPanel = Canvas(self.resultsCanvas, bg = "lightblue", bd= 0, highlightthickness = 0, border = 0,)
        #self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 4, height = canvas_height - 60 )
        
        self.populate_scroll(car_pos, btn_width, btn_height, up, doubleup)
        
        if show_more:
            ADDITIONAL = 5
            self.show_more_button = Button(self.resultsCanvas, text = "Show More", bg = search_colour, font = ("calibri", 10, 'bold', 'underline'), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black", command = lambda: self.show_more_lots(car_pos, ADDITIONAL,btn_width,btn_height,up,doubleup))
            self.show_more_button.place(x = self.resultsCanvas.winfo_reqwidth() - 150, y = 13, width = 80, height = 30)
        
        self.closeResults = Button(self.resultsCanvas, text = "X", font = ("calibri", 10, 'normal',), relief = "flat", fg = "#ffffff", bg = "gray64", activeforeground = "black", activebackground = "gray64", bd = 0, highlightthickness = 0, border = 0, command = lambda: self.right_click_event(btn_width, btn_height, up, doubleup))
        self.closeResults.place(x = self.resultsCanvas.winfo_reqwidth() - 40, y = 10, width = 20, height = 20)
        
    def checkPanelSize(self, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        if self.mini_panel:
            pass
        if self.midi_panel:
            pass
        if self.maxi_panel:
            try:
                global mid_event
                self.midimize_resultsCanvas(mid_event, car_pos, btn_width, btn_height, arrow1, arrow2)
            except Exception:
                global max_event
                self.midimize_resultsCanvas(max_event, car_pos, btn_width, btn_height, arrow1, arrow2)            

    def show_more_lots(self, car_pos:tuple, additional:int, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):    
        count = 0
        keys_to_remove = []

        for key in self.more_available_lots:
            if count < additional:
                keys_to_remove.append(key)
                count += 1
            else:
                break

        for key in keys_to_remove:
            self.calculate_route_distance(car_pos, key, (self.more_available_lots[key][0][0], self.more_available_lots[key][0][1]), self.more_available_lots, draw_marker = False)
            self.available_lots[key] = self.more_available_lots[key]
            del self.more_available_lots[key]
        
        self.resultsLabel.config(text = f"Results:  {len(self.available_lots)}")
        
        self.populate_scroll(car_pos,btn_width,btn_height,arrow1,arrow2)
        
    def minimize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str, ):
        self.mini_panel, self.midi_panel, self.maxi_panel = True, False, False
        self.map_widget.set_position(car_pos[0] , car_pos[1], marker = False,)
        canvas_height = self.results_canvas_mini_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height3
                                     : 
                                     self.midimize_resultsCanvas(event, a, b, c, d, e, ))

        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height2
                                     : 
                                     self.maximize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow2, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        #self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 13, height = canvas_height - 60,)

    def midimize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        global mid_event
        mid_event = event
        self.mini_panel, self.midi_panel, self.maxi_panel = False, True, False
        self.map_widget.set_position(car_pos[0] - 0.004, car_pos[1], marker = False,)
        canvas_height = self.results_canvas_mid_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda ev, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height, 
                                     #g = canvas_height3
                                     : 
                                     self.minimize_resultsCanvas(ev, a, b, c, d, e,))
        
        self.results_fullScreen.bind("<ButtonPress-1>", lambda ev, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height2,
                                     : 
                                     self.maximize_resultsCanvas(ev, a, b, c, d, e, ))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)

        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 13, height = canvas_height - 60,)
    
    def maximize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str, ):
        global max_event
        max_event = event
        self.mini_panel, self.midi_panel, self.maxi_panel = False, False, True
        canvas_height = self.results_canvas_full_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda ev, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height2, 
                                     #g = canvas_height
                                     : 
                                     self.midimize_resultsCanvas(ev, a, b, c, d, e, ))
        
        self.results_fullScreen.bind("<ButtonPress-1>", lambda ev, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height3,
                                     #g = canvas_height,
                                     : 
                                     self.minimize_resultsCanvas(ev, a, b, c, d, e,))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow2, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 13, height = canvas_height - 60,)

    def populate_scroll(self, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        try:
            self.map_frame.destroy()
        except Exception:
            pass        
        try:
            self.map_main.destroy() 
        except Exception:
            pass
        
        fullstar = "\u2605"
        nullstar = "\u2606"
        parking_types = ["Public Parking", "Private Parking", "Paid Parking"]
        num = 1
        
        self.create_scroll(self.sideWidgetDataPanel)

        for name, data_list in sorted(self.available_lots.items(), key = lambda item: item[1][4]):

            c = Canvas(self.map_frame, bg="azure", width = self.map_frame.winfo_reqwidth() - 10, height = 180,)
            c.pack(fill="both", expand=True, )
            
            c.create_text(20,15,text = f'{num}', font = ('bold', 10), fill = "lightgray")
            
            title = Label(c, text = name, font = ('bold', 15, 'underline'), bg = "azure")
            title.place(x = int(c.winfo_reqwidth()/2) - int(title.winfo_reqwidth()/2), y = 5)
            
            text = self.getReview(fullstar, nullstar)
            colour = "lightgray" if text == "No Reviews" else "gold"
            
            review = Label(c, font = ('bold', 13), text = text, bg = "azure", fg= colour)
            review.place(x = 20, y = 65)
            
            distance = Label(c, text = f"Distance: {data_list[4]:.2f} kms", font = ('bold', 12), bg = "azure", )
            distance.place(x = 20, y = 95)    
            
            parking = Label(c, text = choice(parking_types), font = ('bold', 12), bg = "azure", )
            parking.place(x = 20, y = 125)
            
            open = Label(c, text = self.opening_hours(), font = ('bold', 12), bg = "azure", fg= "green")
            open.place(x = 20, y = 150)
            
            url = f'https://www.google.com/maps/dir/{car_pos[0]},+{car_pos[1]}/{data_list[0][0]},+{data_list[0][1]}/'

            b1 = self.setSelectButton(c, url, 15, name, data_list[1], data_list[0], car_pos, data_list[3], btn_width, btn_height, arrow1, arrow2, data_list[4])
            b1.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 85, width = 80, height = 30)            
            
            b2 = self.setRouteButton(c, name, data_list[0], car_pos, data_list[3], btn_width, btn_height, arrow1, arrow2)
            b2.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 45, width = 80, height = 30)
            
            num += 1
    
    def setSelectButton(self, c:Canvas, url:str, font:int, name:str, lottype:int, coord:tuple, car_pos:tuple, route_coordinates:list, btn_width:int, btn_height:int, arrow1:str, arrow2:str, distance:float):
        return Button(c, text="Select", font = ('bold', font), command = lambda : self.correct_Selection(url, name, lottype, car_pos, coord, route_coordinates, btn_width, btn_height, arrow1, arrow2, distance), width = 10, height = 2, highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")

    def correct_Selection(self, url:str, name:str, lottype:int, car_pos:tuple, coord:tuple, route_coordinates:list, btn_width:int, btn_height:int, arrow1:str, arrow2:str, distance:float):
        if not self.selected_a_spot:
            global map_canvas
            map_canvas.unbind_all("<MouseWheel>")
            self.map_widget.set_position(car_pos[0] - 0.004, car_pos[1], marker = False,)        
            self.map_widget.set_zoom(16)
            self.set_Max_Min_Zoom(16,16)
            self.drawSpecificRoute(car_pos, coord, name, route_coordinates, btn_width, btn_height, arrow1, arrow2)
            self.selected_a_spot, self.route_set = True, True            
            self.printer(url, name, lottype, distance,)            
    
    def printer(self, url:str, name:str, lottype:int, distance:float,):

        if self.userExists:
            parkingLot = ParkingLotInfo(f"ParkingLot{lottype}")        

        self.create_rectangle(self.mainCanvas,2,2, 382, 731, fill='snow', alpha=.6, tags = "blur")
        self.mini_mainCanvas()
            
        lbl = Label(master = self.userAccountCanvas, text = f"You've selected:", font = ('bold',18), bg = "gray79", wraplength = 300)
        lbl.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl.winfo_reqwidth() / 2), y = 10)
        
        lbl1 = Label(master = self.userAccountCanvas, text = f"{name}", font = ('bold',18), bg = "gray79", fg = "green", wraplength = 300)
        lbl1.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl1.winfo_reqwidth() / 2), y = 50,)
        
        lbl2 = Label(master = self.userAccountCanvas, text = "Proceed?", font = ('bold',20), bg = "gray79", wraplength = 300)
        lbl2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl2.winfo_reqwidth() / 2), y = 170)
        
        btn1 = Button(self.userAccountCanvas, text = "PROCEED", font = ('bold', 13), relief = "groove", )
        btn1.place(x = 15, y = 230, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
        btn2 = Button(self.userAccountCanvas, text = "BACK", font = ('bold', 13), relief = "groove", command = lambda: self.bsck(parkingLot) )
        btn2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + 5, y = 230, width= int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
        btn1.config(command = lambda: self.yesUser_afterMap(url, name, parkingLot, distance,)) if self.userExists else btn1.config(command = lambda: self.noUser_afterMap(url, name))
        
    def yesUser_afterMap(self, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.userAccountCanvas.destroy()
        except Exception: pass
                
        mail = FMPLot_Mail(name, distance, datetime.now(), self.email, url=url, browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        self.mainCanvas.after(1000,)
        self.reserve_or_not(url, name, parkingLot, distance)
        
    def reserve_or_not(self, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        self.mini_mainCanvas()
        
        header = Label(master = self.userAccountCanvas, text = "Email Sent", font = ('bold',10), bg = "gray89", fg = "IndianRed1", wraplength = 300)
        header.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 10)
        
        lbl = Label(master = self.userAccountCanvas, text = f"You can reserve a spot at:", font = ('bold',16), bg = "gray79",)
        lbl.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl.winfo_reqwidth() / 2), y = 50)
        
        lbl1 = Label(master = self.userAccountCanvas, text = f"{name}", font = ('bold',18), bg = "gray79", fg = "green", wraplength = 300)
        lbl1.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl1.winfo_reqwidth() / 2), y = 95,)
        
        btn1 = Button(self.userAccountCanvas, text = "PROCEED", font = ('bold', 13), relief = "groove", command = lambda: self.proceed_to_reserve(url, name, parkingLot, distance))
        btn1.place(x = 15, y = 230, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
        btn2 = Button(self.userAccountCanvas, text = "BACK", font = ('bold', 13), relief = "groove", command = lambda: self.bsck(parkingLot) )
        btn2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + 5, y = 230, width= int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
    
    def set_lot_costs(self, lottype:int = 1):
        if lottype == 1:
            self.assisted_reserve_amount, self.self_reserve_amount = 100, 200
        if lottype == 2:
            self.assisted_reserve_amount, self.self_reserve_amount = 200, 400
        if lottype == 3:
            self.assisted_reserve_amount, self.self_reserve_amount = 300, 600
        if lottype == 4:
            self.assisted_reserve_amount, self.self_reserve_amount = 400, 800
        
    def proceed_to_reserve(self, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.userAccountCanvas.destroy()
        except Exception: pass
        try:self.map_container.pack_forget()
        except Exception: pass
        
        self.decorateCanvas(self.mainCanvas)
        
        self.set_lot_costs()
        
        self.reservationCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
        self.reservationCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.reservationCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.reservationCanvas.winfo_reqheight() / 2))
        
        cancel_button = Button(self.reservationCanvas, text = "CANCEL", font = ("bold",10), relief = "flat", fg = "red", bg = "gray79", command=lambda: self.cancel_reservation(parkingLot))
        cancel_button.place(x = self.reservationCanvas.winfo_reqwidth() - cancel_button.winfo_reqwidth() - 5, y = 5, height = 30)
        
        header = Label(self.reservationCanvas, text = "Make a Reservation", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
        header.place(x = int(self.reservationCanvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 50)

        random_choice_label = Label(self.reservationCanvas, text = f"Choose For Me - ${self.assisted_reserve_amount:.2f}", font = ("bold",20,"underline"), bg = "gray79")
        random_choice_label.place(x = 10, y = 150)
        
        random_choice_button = Button(self.reservationCanvas, text = "Choose\nFor\nMe", font = ("bold",20), relief = "flat", command = lambda: self.sim_pay(self.assisted_reserve_amount,1,url, name, parkingLot, distance,)) 
        random_choice_button.place(x = 250, y = 195, height = 130)
        
        random_choice_summary_label = Label(self.reservationCanvas, font = ("bold",10), fg = "gray48", bg = "gray79", wraplength= 220, justify="left")
        random_choice_summary_label.place(x = 10, y = 210)
        random_choice_summary_label.config(text = lorem.words(20))
        
        self_choice_label = Label(self.reservationCanvas, text = f"Let Me Choose - ${self.self_reserve_amount:.2f}", font = ("bold",20,"underline"), bg = "gray79")
        self_choice_label.place(x = 10, y = 380, )        
        
        self_choice_button = Button(self.reservationCanvas, text = "Let\nMe\nChoose", font = ("bold",20), relief = "flat", command = lambda: self.sim_pay(self.self_reserve_amount,2,url, name, parkingLot, distance,))
        self_choice_button.place(x = 250, y = 425, height = 130)
        
        self_choice_summary_label = Label(self.reservationCanvas, font = ("bold",10), fg = "gray48", bg = "gray79", wraplength= 220, justify="left")
        self_choice_summary_label.place(x = 10, y = 440)
        self_choice_summary_label.config(text = lorem.words(20))
        
    def sim_pay(self, amount:float, res_type:int, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.reservationCanvas.destroy()
        except Exception: pass
        self.mini_mainCanvas()
        self.userAccountCanvas.after(1000,)      
        
        self_or_assisted = "ASSISTED" if res_type == 1 else "SELF"        
        
        header = Label(self.userAccountCanvas, text = "Make Payment", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
        header.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 30)
        
        amount_label = Label(self.userAccountCanvas, text = "Transaction Amount:", font = ("bold",13,), bg = "gray79", fg = "grey35")
        amount_label.place(x = 20, y = 100)
        
        booking_amount_label = Label(self.userAccountCanvas, text = f"${amount:.2f}", font = ("bold",13,), bg = "gray79", fg = "green")
        booking_amount_label.place(x = 225, y = 100)
        
        type_label = Label(self.userAccountCanvas, text = "Type:", font = ("bold",13,), bg = "gray79", fg = "grey35")
        type_label.place(x = 20, y = 130)
        
        booking_type_label = Label(self.userAccountCanvas, text = f"{self_or_assisted} BOOKING", font = ("bold",13,), bg = "gray79", fg = "red",)
        booking_type_label.place(x = 80, y = 130)
        
        lot_label = Label(self.userAccountCanvas, text = "Lot:", font = ("bold",13,), bg = "gray79", fg = "grey35")
        lot_label.place(x = 20, y = 160)
        
        booking_lot_label = Label(self.userAccountCanvas, text = f"{name}", font = ("bold",13,), bg = "gray79", wraplength=420, justify = "left")
        booking_lot_label.place(x = 60, y = 160)
        
        btn1 = Button(self.userAccountCanvas, text = "PROCEED", font = ('bold', 13), relief = "groove", command = lambda: self.check_payment(amount, res_type, url, name, parkingLot, distance,))       
        btn1.place(x = 15, y = 235, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
        btn2 = Button(self.userAccountCanvas, text = "BACK", font = ('bold', 13), relief = "groove", command = lambda: self.proceed_to_reserve(url, name, parkingLot, distance))
        btn2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + 5, y = 235, width= int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
    def check_payment(self, amount:float, res_type:int, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        #self.set_bankBalance(50)
        balance_left = float(self.bankBalance) - float(amount)
        
        #creates a Booking object
        self.currentBooking = Booking(name)
        self.currentBooking.set_amount(amount)
        self.currentBooking.set_time(datetime.now())
        self.currentBooking.set_type(res_type)
        
        for widget in self.userAccountCanvas.winfo_children():
            widget.destroy()
        
        if balance_left >= 0:
            self.bankBalance = balance_left            
            self.currentBooking.set_outcome(True)            
                
            header = Label(self.userAccountCanvas, text = "Make Payment", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
            header.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 30)
            
            payment_label = Label(self.userAccountCanvas, text = "Payment Successful", font = ("bold",19,), bg = "gray79", fg = "green")
            payment_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(payment_label.winfo_reqwidth() / 2), y = 115)
            
            amount_label = Label(self.userAccountCanvas, text = f"${amount:.2f}", font = ("bold",20,), bg = "gray79", fg = "grey35")
            amount_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(amount_label.winfo_reqwidth() / 2), y = 180)
            
            tick = Label(self.userAccountCanvas, text = "\u2713", font = ("bold",40,), bg = "gray79", fg = "green")
            tick.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + int(amount_label.winfo_reqwidth() / 2) + 5, y = 153)
            
            processing_label = Label(self.userAccountCanvas, text = f"Processing...", font = ("bold",13,), bg = "gray79", fg = "grey55")
            processing_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(processing_label.winfo_reqwidth() / 2) + 5, y = 250)
            
            self.userAccountCanvas.after(2500,)
            
            if res_type == 1: #assisted
                self.userAccountCanvas.after(2500, lambda: self.chosen_for_me(url, name, parkingLot, distance,))                
            else: #self chosen
                self.userAccountCanvas.after(2500, lambda: self.list_all_available_spots(url, name, parkingLot, distance,))
        else:
            self.currentBooking.set_outcome(False)
            self.currentBooking.set_spot("NONE") 
            header = Label(self.userAccountCanvas, text = "Make Payment", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
            header.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 30)
            
            payment_label = Label(self.userAccountCanvas, text = "Payment Failed", font = ("bold",19,), bg = "gray79", fg = "red")
            payment_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(payment_label.winfo_reqwidth() / 2), y = 115)
            
            amount_label = Label(self.userAccountCanvas, text = f"${amount:.2f}", font = ("bold",20,), bg = "gray79", fg = "grey35")
            amount_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(amount_label.winfo_reqwidth() / 2), y = 180)
            
            tick = Label(self.userAccountCanvas, text = "\u2716", font = ("bold",40,), bg = "gray79", fg = "red")
            tick.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + int(amount_label.winfo_reqwidth() / 2) + 5, y = 158)
            
            processing_label = Label(self.userAccountCanvas, text = f"Returning to home...", font = ("bold",13,), bg = "gray79", fg = "grey55")
            processing_label.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(processing_label.winfo_reqwidth() / 2) + 5, y = 250)
            
            self.userAccountCanvas.after(2500, lambda: self.cancel_transaction(parkingLot))
    
    def list_all_available_spots(self, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.reservationCanvas.destroy()
        except Exception: pass
        try: self.userAccountCanvas.destroy()
        except Exception: pass
    
        self.all_available_spots_Canvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
        self.all_available_spots_Canvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.all_available_spots_Canvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.all_available_spots_Canvas.winfo_reqheight() / 2))
        
        header = Label(self.all_available_spots_Canvas, text = "Let Me Choose", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
        header.place(x = int(self.all_available_spots_Canvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 40)
        
        disc = Label(self.all_available_spots_Canvas, text = "Choose from the available spots listed", font = ("bold",13), bg = "gray79",)
        disc.place(x = 20, y = 120)
        
        #lottype = 2
        #parkingLot = ParkingLotInfo(f"ParkingLot{lottype}")
        columns = 3 if parkingLot.ParkingLot_amountAvailable <= 12 else 4
        
        available_spots_header = Label(self.all_available_spots_Canvas, text = f"Available Spots: {parkingLot.ParkingLot_amountAvailable}", bg = "gray79",)
        available_spots_header.place(x = int(self.all_available_spots_Canvas.winfo_reqwidth() / 2) - int(available_spots_header.winfo_reqwidth() / 2),
                                     y = int(self.all_available_spots_Canvas.winfo_reqheight() / 3) - 40, height = 30)  
        
        available_spots_frame = Frame(self.all_available_spots_Canvas, bg = "#ffffff", width = self.all_available_spots_Canvas.winfo_reqwidth() - 20, height = int(self.all_available_spots_Canvas.winfo_reqheight() / 3) * 2)
        available_spots_frame.place(x = 10, y = int(self.all_available_spots_Canvas.winfo_reqheight() / 3) - 10)
        
        width = int(available_spots_frame.winfo_reqwidth()) / columns
        # need to figure a way to make this more dynamic
        if parkingLot.ParkingLot_amountAvailable <= 9: # neeed 3 buttons going down
            height = int(available_spots_frame.winfo_reqheight()/3)
        elif parkingLot.ParkingLot_amountAvailable > 9 and parkingLot.ParkingLot_amountAvailable <= 16: # neeed 4 buttons going down
            height = int(available_spots_frame.winfo_reqheight()/4)
        else: # neeed 5 buttons going down
            height = int(available_spots_frame.winfo_reqheight()/5)
            
        row, col, num = 0, 0, 0
        
        for index, spot in enumerate(parkingLot.ParkingLot_availableSpots):
            but = self.setSelfChooseButton(available_spots_frame, index+1, spot, url, name, parkingLot, distance,)
            but.place(y = row, x = col, width = width, height = height)
            
            col += width
            num += 1
            if num == columns:
                col, num = 0, 0
                row += height
                
    def setSelfChooseButton(self, frame:Frame, index:int, spot:list, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        return Button(frame, text = f"{index}: {spot[0]}", font = ("bold",13), command = lambda: self.spotChosenConfirmation(index, spot, url, name, parkingLot, distance,) )
    
    def spotChosenConfirmation(self, index:int, spot:list, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.reservationCanvas.destroy()
        except Exception: pass
        try: self.userAccountCanvas.destroy()
        except Exception: pass
        try: self.all_available_spots_Canvas.destroy()
        except Exception: pass
        
        self.mini_mainCanvas()
        
        lbl = Label(master = self.userAccountCanvas, text = f"You've selected the spot:", font = ('bold',15), bg = "gray79", wraplength = 300)
        lbl.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl.winfo_reqwidth() / 2), y = 40)
        
        lbl1 = Label(master = self.userAccountCanvas, text = f"{spot[0]}", font = ('bold',30), bg = "gray79", fg = "green", wraplength = 300)
        lbl1.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl1.winfo_reqwidth() / 2), y = 95,)
        
        lbl2 = Label(master = self.userAccountCanvas, text = "Proceed?", font = ('bold',20), bg = "gray79", wraplength = 300)
        lbl2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - int(lbl2.winfo_reqwidth() / 2), y = 170)
        
        btn1 = Button(self.userAccountCanvas, text = "PROCEED", font = ('bold', 13), relief = "groove", command = lambda: self.setSpot(spot, url, name, parkingLot, distance,))
        btn1.place(x = 15, y = 230, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
        btn2 = Button(self.userAccountCanvas, text = "BACK", font = ('bold', 13), relief = "groove", command = lambda: self.userAccountCanvas.after(500, lambda: self.list_all_available_spots(url, name, parkingLot, distance,)))
        btn2.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + 5, y = 230, width= int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        
    def setSpot(self, spot:list, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.reservationCanvas.destroy()
        except Exception: pass
        try: self.userAccountCanvas.destroy()
        except Exception: pass
        self.mySpot = spot
        self.setParkingLot(parkingLot, url, name, distance,)

    def cancel_transaction(self, parkingLot:ParkingLotInfo):
        self.mainCanvas.delete("shapes")
        self.mainCanvas.delete("group")        
        self.document_booking()        
        
        try: del parkingLot
        except Exception: pass
        #try: del self.currentBooking
        #except Exception: pass
        
        self.selected_a_spot, self.route_set = False, False
        try: self.mainCanvas.destroy()
        except Exception: pass
        self.create_mainCanvas()
        self.start()
        
    def chosen_for_me(self, url:str, name:str, parkingLot:ParkingLotInfo, distance:float,):
        try: self.reservationCanvas.destroy()
        except Exception: pass
        try: self.userAccountCanvas.destroy()
        except Exception: pass
        self.setParkingLot(parkingLot, url, name, distance,)
        
    def cancel_reservation(self, parkingLot:ParkingLotInfo = None):
        self.mainCanvas.delete("shapes")
        self.mainCanvas.delete("group")
        self.reservationCanvas.destroy()
        self.map_container.pack()
        self.bsck(parkingLot)
        
    def noUser_afterMap(self, url:str, name:str):
        try: self.userAccountCanvas.destroy()
        except Exception: pass
        
        try: Browser(title=name, url=url, width = self.mainCanvas.winfo_reqwidth() - 70, height = self.mainCanvas.winfo_reqheight() - 120,)
        except Exception: pass
        
        self.bsck()        
        
    def bsck(self, parkingLot:ParkingLotInfo = None):
        self.set_Max_Min_Zoom(3,22)
        self.mainCanvas.delete("blur")
        try:
            del parkingLot
        except Exception:
            pass
        self.selected_a_spot, self.route_set = False, False
        global map_canvas
        map_canvas.bind_all("<MouseWheel>", lambda event, canvas = map_canvas: self._on_mousewheel(event, canvas))
        
        try: self.userAccountCanvas.destroy()
        except Exception: pass

    def document_booking(self):
        f = open(f"{files.user_profile}previous_bookings.txt", "a")
        lotname = self.currentBooking.get_lot_name().replace('\n', '')
        f.write(f"{lotname}#") #name
        f.write(f"{self.currentBooking.get_type()}#") #type
        f.write(f"{self.currentBooking.get_spot()}#") #spot
        f.write(f'{self.currentBooking.get_time().strftime("%Y-%m-%d %H:%M:%S")}#') #time
        f.write(f"{self.currentBooking.get_amount()}#") #amount
        f.write(f"{int(self.currentBooking.get_outcome())}\n") #outcome
        
        f.close()#name,type,spot,time,amount,outcome
        
    def get_previousbookings(self,):                        
        with open(f"{files.user_profile}previous_bookings.txt","r") as f: 
            for line in f:
                print(line)
                if len(line) > 0:
                    word = line.rstrip().split('#')
                    #name,type,spot,time,amount,outcome
                    booking = Booking(word[0].strip()) #name
                    booking.set_type(int(word[1].strip())) #type
                    booking.set_spot(word[2].strip()) #spot
                    date = word[3].strip()
                    booking.set_time(datetime.strptime(date, "%Y-%m-%d %H:%M:%S")) #time
                    booking.set_amount(float(word[4].strip())) #amount
                    outcome = int(word[5].strip())
                    booking.set_outcome(bool(outcome)) #outcome
                    self.previousbookings_List.append(booking)

    def set_Max_Min_Zoom(self, min:int, max:int):
        self.map_widget.max_zoom = max
        self.map_widget.min_zoom = min

    def opening_hours(self):
        type = randint(0,1)
        if type:
            return "Open 24 Hours"
        else:
            closing_times = [6,7,8,9,10]
            return f"Open. Closes {choice(closing_times)}PM "
    
    def getReview(self, fullstar:str, nullstar:str):
        max = 5
        rating = randint(0, max)
        if rating == 0:
            return "No Reviews"
        elif rating == max:
            review = ""
            while rating > 0:
                review = review + fullstar
                rating-=1
            return review
        else:
            review = ""
            extra = max - rating
            while rating > 0:
                review = review + fullstar
                rating-=1
            while extra > 0:
                review = review + nullstar
                extra-=1
            return review           

    def create_scroll(self, canvas_frame:Canvas):
        self.map_main = Canvas(canvas_frame, bd = 0, highlightthickness = 0, border = 0,)
        self.map_main.pack(side="left", fill="both", expand=True)
        #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
        global map_canvas
        map_canvas = Canvas(self.map_main, bg = "#ffffff", borderwidth=0, width=canvas_frame.winfo_reqwidth(), height=100, bd= 0, highlightthickness = 0, border = 0,)#canvas_frame.winfo_reqheight())
        ##create a new 'frame' canvas in the 'canvas' canvas, preset with the width and height of 'mainCanvas' ♠
        self.map_frame = Canvas(map_canvas, bg = "#ffffff", borderwidth=0, width = canvas_frame.winfo_reqwidth(), height = canvas_frame.winfo_reqheight() - 200, bd= 0, highlightthickness = 0, border = 0,)
        #'vsb' is a Scrollbar event, and it is placed on self
        vsb = Scrollbar(canvas_frame, orient="vertical", command=map_canvas.yview)
        #sets a yscrollcommand for the 'canvas' widget
        map_canvas.configure(yscrollcommand=vsb.set)
        #places the scrollbar off screen
        vsb.place(x = canvas_frame.winfo_reqwidth()+30, y = 0)
        #packs the 'camvas' widet into the 'main' widget
        map_canvas.pack(side="left", fill="both", expand=True)
        #sets the 'frame' widget as a window of the 'canvas' widget
        map_canvas.create_window((0,0), window= self.map_frame, anchor="nw",tags="frame",)
        #binds 2 functions to the canvas, and 1 to the frame
        self.map_frame.bind("<Configure>", lambda event, canvas = map_canvas: self.onFrameConfigure(event, canvas))
        map_canvas.bind_all("<MouseWheel>", lambda event, canvas = map_canvas: self._on_mousewheel(event, canvas))
        #canvas.bind_all("<Double-Button-1>", backtoHome)
        
    #this function configues the 'canvas' canvas
    def onFrameConfigure(self, event, canvas:Canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    #this function configues the 'canvas' canvas scroll type
    def _on_mousewheel(self, event, canvas:Canvas):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
        
    def setRouteButton(self, c:Canvas, name:str, coord:tuple, car_pos:tuple, route_coordinates:list, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        return Button(c, text="Route", font = ('bold',15), command = lambda : self.drawSpecificRoute(car_pos, coord, name, route_coordinates, btn_width, btn_height, arrow1, arrow2), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")
    
    def drawSpecificRoute(self, car_pos:tuple, coord:tuple, name:str, route_coordinates:list, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        if not self.route_set:
            self.checkPanelSize(car_pos, btn_width, btn_height, arrow1, arrow2)
            try:
                self.map_widget.delete_all_path()
            except Exception:
                pass
            try:
                self.map_widget.delete_all_marker()
            except Exception:
                pass
            self.map_widget.set_path(position_list = route_coordinates, color = "purple", width = 5)
            self.map_widget.set_marker(coord[0],coord[1], text = name, text_color = "green")
            self.map_widget.set_marker(car_pos[0], car_pos[1], text = "YOU", text_color = "black")
            self.map_widget.set_position(car_pos[0] - 0.004, car_pos[1], marker = False,)        
            self.map_widget.set_zoom(16)

    def clearEntry(self):
        #self.hasRoute = False
        self.findLocation.delete(0, END)
        
    def clearCanvasToLayMap(self):
        self.mainCanvas.delete("shapes")
        self.mainCanvas.delete("group")
        self.canvasCleared = True
        
    def left_click_event(self, coordinates_tuple: tuple):
        if not self.left_click:
            self.COLOUR = 0
            self.left_click = True
            start = time()
            print("Finding FMP parking for coordinates:", coordinates_tuple)
            self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text = "YOU", text_color = "blue")
            self.create_squares(coordinates_tuple)
            end = time()
            print(f'Execution time: {(end - start):.2f} seconds')
            print(f"total available FMP lots found: {len(self.available_lots) + len(self.more_available_lots)}")
            print("------------------------------------------------------------------------------------------")

    def right_click_event(self, btn_width:int, btn_height:int, up:str, doubleup:str):
        canvas_height = self.results_canvas_mini_height
        self.clearMapMarkings()
        try:
            self.map_frame.destroy()
        except Exception:
            pass        
        try:
            self.map_main.destroy() 
        except Exception:
            pass
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        try: self.show_more_button.destroy()
        except Exception: pass
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = up, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = doubleup, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        self.resultsLabel.config(text = "No Results")
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        self.left_click = False
        print("------------------------------------------------------------------------------------------")
        
    def clearMapMarkings(self):
        try:
            self.map_widget.delete_all_polygon()
        except Exception:
            pass
        try:
            self.map_widget.delete_all_marker()
        except Exception:
            pass
        try:
            self.map_widget.delete_all_path()
        except Exception:
            pass
        try:
            self.available_lots.clear()
            self.more_available_lots.clear()
        except Exception:
            pass

     #this function uses the information from the Entry widget to search through the map database
    
    def searchMap(self):
        #if there is data in the entry
        if len(self.findLocation.get().strip()) != 0:
            #dd
            the_location = self.checkLocation(self.findLocation.get())
            #tries to create a location variable based off the info given
            location = self.locationService.geocode(query=the_location, exactly_one=True)

            #if the variable is created sucessfully,
            if location:
                #sets the map middle position to the variable
                self.map_widget.set_position(location.latitude, location.longitude, marker = True)
            #if the variable is not created sucessfully,
            else:
                #clears the entry of unwanted/bad/incorrect information
                self.findLocation.delete(0, END)
        
    #this function checks if the location searched for is in a list.
    #if it exists, the location is editted for an easier search.
    def checkLocation(self, location):
        if location == "UCC" or location == "ucc" or location == "Ucc":
            return "University of the Commonwealth Caribbean, Jamaica"
        if location in self.locations or location.capitalize() in self.locations or location.title() in self.locations:
            return f"{location}, Jamaica"            
        else:
            return location

    #this function adds locations from across Jamaica, that the map can read, into a list
    def getLocations(self):
        with open(files.places_in_Jamaica) as f:
            for line in f:
                if len(line) > 0:
                    if line not in self.locations:
                        self.locations.append(str(line.strip()))
    """
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

    """    

#OLD PROGRAM STUFF

    #this function is called when 'userLabelButton' is initially clicked
    def noUserButtonClick(self):
        #'userLabelButton' has its command changed to a new function
        self.userLabelButton.config(command = lambda : self.closenoUserPopupLabel())
        #creates a small canvas 'noUserPopupLabel, adds some text to it, and 
        #creates a button 'noUserPopupLabelButton' on it, with its own command
        self.noUserPopupLabel = Canvas(self.mainCanvas, bg = "spring green", highlightbackground="gray40")
        
        self.noUserPopupLabel.place(x = int(self.mainCanvas.winfo_reqwidth() /2), y = 20, width = int(self.mainCanvas.winfo_reqwidth()/3.08), height = int(self.mainCanvas.winfo_reqwidth()/3.08)/2,)
        self.noUserPopupLabel.create_text(80, 25,font = ('bold', 10), anchor = "center",text = "Log In or Sign Up\nfor added features",)
        self.noUserPopupLabelButton = Button(self.noUserPopupLabel, bg = "forest green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "Get More", fg = "gray16", activebackground="forest green", activeforeground="gray16", command = lambda: self.userAccount())
        self.noUserPopupLabelButton.place(x = 50, y = 50, width = 60)
    
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
                self.frame.unbind("<Configure>")
            except Exception:
                pass
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass
            #creates a rectange image to blur out the background
            #note: this function uses '**kwargs'. all values that are not of type int
            #will be added to '**kwargs'; it act's like a tuple/set
            try:
                #self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")
                self.create_rectangle(self.mainCanvas,2,2, self.mainCanvas.winfo_reqwidth() - 2, self.mainCanvas.winfo_reqheight() - 2, fill='snow', alpha=.6, tags = "blur")
            except Exception:
                pass
            global s
            try:
                self.create_rectangle(s,2,2, self.mainCanvas.winfo_reqwidth() - 2, self.mainCanvas.winfo_reqheight() - 2, fill='snow', alpha=.6, tags = "blur")
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
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
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
    
        self.userAccountCanvas.create_text(160, 550, text = "Don't have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "login")
        
        self.register_Button = Button(self.userAccountCanvas, text = "Register", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.RegistrationScreen1())
        self.register_Button.place(x = 275, y = 540, width = 60, height = 25) 
        
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
            self.getReadingButton.config(state = "normal", command = lambda: self.appMap())
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
            self.frame.bind("<Configure>", self.on_NewFrameConfigure)
        except Exception:
            pass
        try:            
            self.canvas.bind_all("<MouseWheel>", self.new_on_mousewheel)
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
            self.sendMail()
            self.start()       

    #this function resets the previously disabled buttons, and also resets their commands.
    #also, all 'User information' is reset to their original states. 
    #'userAccountCanvas' is also destroyed, and also the rectange image with the blur 
    def close_resetAll(self):
        try:
            self.getReadingButton.config(state = "normal", command = lambda: self.appMap())
        except Exception:
            pass
        try:
            self.userLabelButton.config(state = "normal", command = lambda : self.noUserButtonClick())
        except Exception:
            pass
        try:
            self.frame.bind("<Configure>", self.on_NewFrameConfigure)
        except Exception:
            pass
        try:            
            self.canvas.bind_all("<MouseWheel>", self.new_on_mousewheel)
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
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
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
        
        self.userAccountCanvas.create_text(205, 150, text = "First Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.FnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global fname
        if len(fname) != 0:
            self.FnameEntry.insert(0, fname)
        self.FnameEntry.place(x = 100, y = 180, width = 200, height = 40)

        self.userAccountCanvas.create_text(110, 260, text = "Last Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.LnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global lname
        if len(lname) != 0:
            self.LnameEntry.insert(0, lname)
        self.LnameEntry.place(x = 20, y = 290, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.userAccountCanvas.create_text(145, 370, text = "Email Address", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.emailEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global email
        if len(email) != 0:
            self.emailEntry.insert(0, email)
        self.emailEntry.place(x = 20, y = 400, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Next", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda : self.checkBeforeContinueRegistering())
        self.register_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 70, y = 460, width = 140, height = 50)
        
        self.userAccountCanvas.create_text(160, 550, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "login")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 275, y = 540, width = 60, height = 25)
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 585, text = "NB: Please fill all fields", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
        
        self.FnameEntry.bind("<FocusIn>", self.clearLabel)
        self.LnameEntry.bind("<FocusIn>", self.clearLabel)
        self.emailEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)

    #this function clears the 'empty_Label' Label, once the user has selected a gender
    def clearLabel(self, event):
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
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
                
        self.userAccountCanvas.create_text(155, 150, text = "Contact Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.phoneEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global phone
        if phone != 0:
            self.phoneEntry.insert(0, phone)
        self.phoneEntry.place(x = 20, y = 180, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)

        self.userAccountCanvas.create_text(135, 260, text = "Card Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cardEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        global card
        if card != 0:
            self.cardEntry.insert(0, card)
        self.cardEntry.place(x = 20, y = 290, width = 210, height = 40)
        
        #self.cardType_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "red2" )
        #self.cardType_Label.place(x = 240, y = 290, width = 60, height = 40)
        
        self.userAccountCanvas.create_text(325, 260, text = "CVV", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cvvEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global cvv
        if cvv != 0:
            self.cvvEntry.insert(0, cvv)
        self.cvvEntry.place(x = 295, y = 290, width = 60, height = 40)
        
        self.userAccountCanvas.create_text(100, 375, text = "Expiry Date", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
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
        
        self.userAccountCanvas.create_text(305, 375, text = "Driver's ID", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
        self.idEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global id
        if len(id) != 0:
            self.idEntry.insert(0, id)
        self.idEntry.place(x = 240, y = 400, width = 130, height = 40)
        
        self.back_Button = Button(self.userAccountCanvas, text = "Back", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.setGlobals(1))
        self.back_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth()/2) - 131, y = 460, width = 130, height = 50)
        
        self.next_Button = Button(self.userAccountCanvas, text = "Next", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda:  self.checkBeforeFinishRegistering())
        self.next_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth()/2)+1, y = 460, width = 130, height = 50)        
        
        self.userAccountCanvas.create_text(160, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 275, y = 535, width = 60, height = 25)
        
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
    def setMonth(self, event):
        #this sets the expiration month user variable to 1 PLUS the index of 
        #the data received from the entry 
        self.exp_month = 1 + self.months.index(self.month_Combo.get())
        #calls 'clearLabel' to reset the 'empty_Label' label
        self.clearLabel(event)

    #this function sets the user expiration year variable. it is called when
    #the year combobox is interacted with.
    def setYear(self, event):
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
        self.userAccountCanvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
        self.userAccountCanvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.userAccountCanvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.userAccountCanvas.winfo_reqheight() / 2))
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84", command = self.close_resetAll)
        self.close_userAccountCanvasButton.place(x = self.userAccountCanvas.winfo_reqwidth() - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) ,  bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "login")
        
        self.userAccountCanvas.create_text(105, 170, text = "Username", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.RusernameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        global username
        if len(username) != 0:
            self.RusernameEntry.insert(0, username)
        self.RusernameEntry.place(x = 20, y = 210, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.userAccountCanvas.create_text(105, 330, text = "Password", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "login")
        self.RpasswordEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center", )
        self.RpasswordEntry.place(x = 20, y = 370, width = self.userAccountCanvas.winfo_reqwidth() - 40, height = 40)
        
        self.back_Button = Button(self.userAccountCanvas, text = "Back", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.setGlobals(2))
        self.back_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth()/2) - 131, y = 460, width = 130, height = 50)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Register", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.completeRegistration())
        self.register_Button.place(x = int(self.userAccountCanvas.winfo_reqwidth()/2)+1, y = 460, width = 130, height = 50)
        
        self.userAccountCanvas.create_text(160, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat", command = lambda: self.LoginScreen())
        self.login_Button.place(x = 275, y = 535, width = 60, height = 25)
        
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
        
        self.getReadingButton.config(state = "normal", command = lambda: self.appMap())
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
        self.userPopupLabel.place(x = int(self.mainCanvas.winfo_reqwidth() /2), y = 20, width = 150, height = 140)
        self.userPopupLabel.create_text(75,20,font = ('bold', 10), text = f"Welcome\n{self.fname}", justify = "center", fill = "gray14")
        self.userPopupLabel.create_text(75,50,font = ('bold', 8), text = f"{self.email}", justify = "center", fill = "gray66")
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "user profile", fg = "gray16", activebackground="medium spring green", activeforeground="gray16", command = lambda : self.viewProfile()).place(x = 15, y = 55, height = 30, width = 120)
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "previous bookings", fg = "gray16", activebackground="medium spring green", activeforeground="gray16", command = self.view_previousbookings).place(x = 15, y = 80, height = 30, width = 120)
        
        Button(self.userPopupLabel, bg = "spring green", highlightthickness=0, relief="flat", borderwidth=0, font = ('bold',8), text = "log out", fg = "gray16", activebackground="medium spring green", activeforeground="gray16", command = lambda : self.logoutUser()).place(x = 15, y = 105, height = 30, width = 120)
        
    def view_previousbookings(self):
        try: self.userLabelButton.config(state = "disabled", command = lambda : self.UserSettings(), )
        except Exception: pass        
        try: self.getReadingButton.config(state = "disabled")
        except Exception: pass
        try: self.reserveSpotButton.config(state = "disabled")
        except Exception: pass
        try: self.userPopupLabel.destroy()
        except Exception: pass
        
        self.decorateCanvas(self.mainCanvas)
        self.create_rectangle(self.mainCanvas, 0, 0, self.mainCanvas.winfo_reqwidth() - 4, self.mainCanvas.winfo_reqheight() - 4, fill='snow', alpha=.6, tags = "blur")
        
        self.previous_bookings_Canvas = Canvas(self.mainCanvas, bg = "gray79", width = int((self.mainCanvas.winfo_reqwidth() / 6) * 5), height = int((self.mainCanvas.winfo_reqheight() / 6) * 4))
        self.previous_bookings_Canvas.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.previous_bookings_Canvas.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.previous_bookings_Canvas.winfo_reqheight() / 2))
        
        back_button = Button(self.previous_bookings_Canvas, bg = "gray79", text = "back", fg = "red", font = ('bold',12), highlightthickness=0, relief="flat", borderwidth=0, bd = 0)
        back_button.place(y = 10, x = int(self.previous_bookings_Canvas.winfo_reqwidth()) - int(back_button.winfo_reqwidth()) - 10)
        
        header = Label(self.previous_bookings_Canvas, text = "Previous Bookings", font = ("bold",23,"underline"), bg = "gray79", fg = "blue")
        header.place(x = int(self.previous_bookings_Canvas.winfo_reqwidth() / 2) - int(header.winfo_reqwidth() / 2), y = 70)
                
        #self.previousbookings_List.clear()
        
        if len(self.previousbookings_List) > 0:
            previous_button = Button(self.previous_bookings_Canvas, text = "previous", font = ('normal',10), bg = "gray75", fg = "blue", highlightthickness=0, relief="flat", borderwidth=0, bd = 0, activeforeground="blue",)
            previous_button.place(x = 15, y = 140, width = 100)
            
            next_button = Button(self.previous_bookings_Canvas, text = "next", font = ('normal',10), bg = "gray76", fg = "blue", highlightthickness=0, relief="flat", borderwidth=0, bd = 0, activeforeground="blue",)
            next_button.place(x = self.previous_bookings_Canvas.winfo_reqwidth() - 115, y = 140, width = 100)
            
            previous_bookings_frame = Canvas(self.previous_bookings_Canvas, bg = "gray77", width = self.previous_bookings_Canvas.winfo_reqwidth() - 20, height = int((self.previous_bookings_Canvas.winfo_reqheight() / 4) * 3 ) - 40)
            previous_bookings_frame.place(x = 8, y = 182)
            
            # creating a frame and assigning it to container
            parent_container = Frame(previous_bookings_frame, height=previous_bookings_frame.winfo_reqheight(), width=previous_bookings_frame.winfo_reqwidth())
            # specifying the region where the frame is packed in root
            parent_container.pack(side="top", fill="both", expand=True)
            # configuring the location of the container using grid
            parent_container.grid_rowconfigure(0, weight=1)
            parent_container.grid_columnconfigure(0, weight=1)            
            # We will now create a dictionary of frames
            self.booking_frames = {}
            
            # we'll create the frames themselves later but let's add the components to the dictionary.
            for bookings in self.previousbookings_List:
                theframe = bookings(parent=parent_container, controller=self)
                # the windows class acts as the root window for the frames.
                self.frames[bookings] = theframe
                theframe.grid(row=0, column=0, sticky="nsew")
            
        else:
            no_previousbookings_label = Label(self.previous_bookings_Canvas, text = "NO PREVIOUS BOOKINGS", font = ('bold',17), fg = "indian red", bg = "gray79")
            no_previousbookings_label.place(x = int(self.previous_bookings_Canvas.winfo_reqwidth()/2) - int(no_previousbookings_label.winfo_reqwidth()/2),
                                            y = int(self.previous_bookings_Canvas.winfo_reqheight()/2) - int(no_previousbookings_label.winfo_reqheight()/2))
        
    def logoutUser(self):
        self.userPopupLabel.destroy()
        self.userLabelButton.config(state = "disabled", command = lambda : self.UserSettings(), image = self.userLabel_image)
        
        self.create_rectangle(self.mainCanvas, 0, 0, self.mainCanvas.winfo_reqwidth() - 4, self.mainCanvas.winfo_reqheight() - 4, fill='snow', alpha=.6, tags = "logout-blur")
        
        self.mini_mainCanvas()
        
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 40, text = "Logging Out", font = ('bold',30), tags = "logout-text",)
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 120, text = self.fname, font = ('bold',30), tags = "logout-text",)      
        self.userAccountCanvas.create_text(int(self.userAccountCanvas.winfo_reqwidth() / 2), 185, text = "Are You Sure?", font = ('bold',20), tags = "logout-text",)
        
        Button(self.userAccountCanvas, text = "LOGOUT", font = ('bold', 20), relief = "groove", command = lambda : self.logOut()).place(x = 15, y = 230, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
        Button(self.userAccountCanvas, text = "CANCEL", font = ('bold', 20), relief = "groove", command = lambda : self.cancelLogout()).place(x = int(self.userAccountCanvas.winfo_reqwidth() / 2) + 5, y = 230, width = int(self.userAccountCanvas.winfo_reqwidth() / 2) - 20)
    
    def logOut(self):
        self.userExists = False
        self.has_activeLot = False
        self.mainCanvas.after(2000,)
        try:
            self.mainCanvas.destroy()
        except Exception:
            pass
        
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        
        self.start() 
    
    def cancelLogout(self):
        self.mainCanvas.delete("logout-blur")
        self.userLabelButton.config(state = "normal",)
        self.userAccountCanvas.destroy()
    
    def viewProfile(self):
        try:
            self.userLabelButton.config(state = "normal", command = lambda : self.UserSettings(), image = self.userLabel_image)
        except Exception:
            pass
        try:
            self.userPopupLabel.destroy()
        except Exception:
            pass
        try:
            self.getReadingButton.destroy()
        except Exception:
            pass
        try:
            self.mainCanvas.destroy()
        except Exception:
            pass
        
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        self.decorateCanvas(self.mainCanvas)
        #light sea green, spring green, medium spring green, aquamarine, SpringGreen2, PaleGreen1, azure
        self.create_rectangle(self.mainCanvas, 0, 0, self.mainCanvas.winfo_reqwidth() - 4, self.mainCanvas.winfo_reqheight() - 4, fill='snow', alpha=.6, tags = "user-profile-blur")
        
        pic_lbl = Label(self.mainCanvas, image=self.userLabel_image, bd = 0)
        pic_lbl.place(x = self.mainCanvas.winfo_reqwidth() - pic_lbl.winfo_reqwidth() - 4, y = 4,)
        
        btn = Button(self.mainCanvas, text = "exit", font = ('bold',15), bg = self.from_rgb((214,255,214)), relief = "flat", activebackground = self.from_rgb((214,255,214)), command = lambda: self.saveUserProfile(),)
        btn.place(x = self.mainCanvas.winfo_reqwidth() - pic_lbl.winfo_reqwidth() - 4, y = 82,)
        
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth() / 2), 60, text = "User Profile", font = ('bold',30), fill = "black", anchor = "center", tags = "user-profile")
        self.editError = Label(self.mainCanvas,)
        
        #edit Firstname
        self.mainCanvas.create_text(70, 150, text = "FirstName", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.fname_lbl = Label(self.mainCanvas, text = self.fname, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.fname_lbl.place(x = 10, y = 180)        
        self.fname_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((203,255,237)))
        self.fname_lbl_edit.place(x = 145, y = 150)
        self.fname_lbl_edit.bind("<ButtonPress-1>", self.edit_fname)
        #edit Email
        self.mainCanvas.create_text(45, 270, text = "Email", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.email_lbl = Label(self.mainCanvas, text = self.email, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.email_lbl.place(x = 10, y = 300)        
        self.email_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((153,253,214)))
        self.email_lbl_edit.place(x = 145, y = 270)
        self.email_lbl_edit.bind("<ButtonPress-1>", self.edit_email)
        #edit ID
        self.mainCanvas.create_text(70, 390, text = "Driver's ID", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.id_lbl = Label(self.mainCanvas, text = self.id, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.id_lbl.place(x = 10, y = 420)        
        self.id_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((153,255,203)))
        self.id_lbl_edit.place(x = 145, y = 390)
        self.id_lbl_edit.bind("<ButtonPress-1>", self.edit_id)
        #edit Lastname
        self.mainCanvas.create_text(310, 150, text = "LastName", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.lname_lbl = Label(self.mainCanvas, text = self.lname, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.lname_lbl.place(x = 250, y = 180)        
        self.lname_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((153,248,200)))
        self.lname_lbl_edit.place(x = 380, y = 150)
        self.lname_lbl_edit.bind("<ButtonPress-1>", self.edit_lname)
        #edit Phone
        self.mainCanvas.create_text(310, 270, text = "Contact #", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.phone_lbl = Label(self.mainCanvas, text = self.phone, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.phone_lbl.place(x = 250, y = 300)        
        self.phone_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((203, 255, 237)))
        self.phone_lbl_edit.place(x = 380, y = 270)
        self.phone_lbl_edit.bind("<ButtonPress-1>", self.edit_phone)
        
        self.mainCanvas.create_line(0, 480, self.mainCanvas.winfo_reqwidth(), 480, joinstyle = "bevel", tags = "user-profile")        
        #CARD INFORMATION
        self.card_info = Label(self.mainCanvas, text = "edit Card Info", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((165, 224, 221)))
        self.card_info.place(x = 10, y = 520)
        self.mainCanvas.create_text(50, 570, text = "Card #", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        card_no = str(self.card)
        self.card_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", card_no[:-4]) + card_no[-4:], font = ('bold', 15), width = len(card_no), height = 1, bg = "gray85")
        self.card_lbl.place(x = 10, y = 600)
        
        self.mainCanvas.create_text(290, 570, text = "CVV", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.cvv_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", str(self.cvv)), font = ('bold', 15), width = len(str(self.cvv)), height = 1, bg = "gray85")
        self.cvv_lbl.place(x = 270, y = 600)
         
        self.mainCanvas.create_text(410, 570, text = "Expiry Date", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.date_lbl = Label(self.mainCanvas, text = f'{self.exp_month}/{self.exp_year}', font = ('bold', 15), width = 5, height = 1, bg = "gray85")
        self.date_lbl.place(x = 370, y = 600)
        self.card_info.bind("<ButtonPress-1>", self.edit_cardInfo)
        
        self.mainCanvas.create_line(0, 680, self.mainCanvas.winfo_reqwidth(), 680, joinstyle = "bevel", tags = "user-profile")
        #Username
        self.mainCanvas.create_text(75, 720, text = "UserName", font = ('bold', 15), anchor = "n", tags = "user-profile")
        self.username_lbl = Label(self.mainCanvas, text = self.username, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.username_lbl.place(x = 10, y = 750)        
        self.username_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((165,224,221)))
        self.username_lbl_edit.place(x = 150, y = 720)
        self.username_lbl_edit.bind("<ButtonPress-1>", self.edit_username)
        #Password
        self.mainCanvas.create_text(310, 720, text = "Password", font = ('bold',15), fill = "black", anchor = "n", tags = "user-profile")
        self.password_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", self.password), font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.password_lbl.place(x = 250, y = 750)        
        self.password_lbl_edit = Label(self.mainCanvas, text = "edit", font = ('bold', 12, 'underline'), fg = "blue", bg = self.from_rgb((153,255,203)))
        self.password_lbl_edit.place(x = 410, y = 720)
        self.password_lbl_edit.bind("<ButtonPress-1>", self.edit_password)
        
        self.mainCanvas.bind("<ButtonPress-1>", self.clear_error)
        
    def saveUserProfile(self):
        self.saveAccountInfo()
        self.mainCanvas.unbind("<ButtonPress-1>")
        try:
            self.mainCanvas.delete("user-password")
        except Exception:
            pass
        try:
            self.mainCanvas.delete("user-profile")
        except Exception:
            pass
        try:
            self.mainCanvas.delete("user-profile-blur")
        except Exception:
            pass
        self.mainCanvas.destroy()
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)
        self.createMainButton()
    
    def edit_password(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.password_lbl_edit.unbind("<ButtonPress-1>")
        self.password_lbl_edit.bind("<ButtonPress-1>", self.save_password)
        self.password_lbl_edit.config(text = "save")
        self.password_lbl.destroy()
        self.mainCanvas.create_text(355, 756, text = "Confirm Previous Password", font = ('bold',10), fill = "black", anchor = "n", tags = "user-password")
        self.confirmpassword_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.confirmpassword_Entry.place(x = 250, y = 776, width = 210, height = 30) #self.password_lbl.place(x = 250, y = 750)
        self.mainCanvas.create_text(330, 811, text = "Enter New Password", font = ('bold',10), fill = "black", anchor = "n", tags = "user-password")
        self.newpassword_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.newpassword_Entry.place(x = 250, y = 830, width = 210, height = 30)        

    def save_password(self, event):
        if len(self.confirmpassword_Entry.get()) != 0:
            if len(self.confirmpassword_Entry.get()) >= 8:
                if self.confirmpassword_Entry.get() == self.password:
                    if len(self.newpassword_Entry.get()) != 0:
                        if len(self.newpassword_Entry.get()) >= 8:
                            if self.newpassword_Entry.get() != self.password:
                                self.password = self.newpassword_Entry.get()
                                self.editError.config(text = "Password Updated", fg = "medium blue")
                                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100) 
                            else:
                                self.editError.config(text = "Error saving 'Password' 6", fg = "red2")
                                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                        else:
                            self.editError.config(text = "Error saving 'Password' 5", fg = "red2")
                            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)                           
                    else:
                        self.editError.config(text = "Error saving 'Password' 4", fg = "red2")
                        self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                else:
                    self.editError.config(text = "Error saving 'Password' 3", fg = "red2")
                    self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
            else:
                self.editError.config(text = "Error saving 'Password' 2", fg = "red2")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)                               
        else:
            self.editError.config(text = "Error saving 'Password' 1", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.password_lbl_edit.unbind("<ButtonPress-1>")
        self.password_lbl_edit.bind("<ButtonPress-1>", self.edit_password)
        self.password_lbl_edit.config(text = "edit")
        self.mainCanvas.delete("user-password")
        self.confirmpassword_Entry.destroy()
        self.newpassword_Entry.destroy()
        self.password_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", self.password), font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.password_lbl.place(x = 250, y = 750)
    
    def edit_username(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.username_lbl_edit.unbind("<ButtonPress-1>")
        self.username_lbl_edit.bind("<ButtonPress-1>", self.save_username)
        self.username_lbl_edit.config(text = "save")
        self.username_lbl.destroy()
        self.editusername_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editusername_Entry.place(x = 10, y = 750, width = 210, height = 30)
        self.editusername_Entry.insert(0, self.username)
        
    def save_username(self, event):
        if len(self.editusername_Entry.get()) != 0:
            self.username = self.editusername_Entry.get()
            self.editError.config(text = "Username Updated", fg = "medium blue")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'UserName'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.username_lbl_edit.unbind("<ButtonPress-1>")
        self.username_lbl_edit.bind("<ButtonPress-1>", self.edit_username)
        self.username_lbl_edit.config(text = "edit")
        self.editusername_Entry.destroy()
        self.username_lbl = Label(self.mainCanvas, text = self.username, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.username_lbl.place(x = 10, y = 750) 
      
    def edit_cardInfo(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.card_info.config(text = "save Card Info")
        self.card_info.unbind("<ButtonPress-1>")
        self.card_info.bind("<ButtonPress-1>", self.save_cardInfo)
        self.card_lbl.destroy()
        self.cvv_lbl.destroy()
        self.date_lbl.destroy()
        
        self.editcard_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editcard_Entry.place(x = 10, y = 600, width = 220, height = 30)
        
        self.editcvv_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editcvv_Entry.place(x = 270, y = 600, width = 50, height = 30)

        self.editmonth_Combo = Combobox(self.mainCanvas, font = ('bold', 10), state = "readonly")        
        self.editmonth_Combo['values'] = [x for x in self.months]
        self.editmonth_Combo.config(font = "None 15 normal", )                
        self.editmonth_Combo.place(x = 370, y = 600, height = 30, width = 50)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))
        
        cur_year = int(strftime('%y'))
        self.edityear_Combo = Combobox(self.mainCanvas, font = ('bold', 10), state = "readonly")        
        self.edityear_Combo['values'] = [x for x in range(cur_year,100)]
        self.edityear_Combo.config(font = "None 15 normal", )
        self.edityear_Combo.place(x = 420, y = 600, height = 30, width = 50)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))

    def save_cardInfo(self, event):
        if len(self.editcard_Entry.get()) != 0:
            regex = r'^\d{15,16}$'
            if(re.fullmatch(regex,self.editcard_Entry.get())):
                if len(self.editcvv_Entry.get()) != 0:
                    regex = r'^\d{3,4}$'
                    if(re.fullmatch(regex,self.editcvv_Entry.get())):
                        if (self.editmonth_Combo.get()) != "":
                            if (self.edityear_Combo.get()) != "":
                                eyear = strftime('%y')
                                emonth = strftime('%m')
                                if (int(self.editmonth_Combo.get()) >= int(emonth) and int(self.edityear_Combo.get()) >= int(eyear)) or (int(self.editmonth_Combo.get()) <= int(emonth) and int(self.edityear_Combo.get()) > int(eyear)):
                                    self.card = int(self.editcard_Entry.get())
                                    self.cvv = self.editcvv_Entry.get()
                                    self.exp_month = int(self.editmonth_Combo.get())
                                    self.exp_year = int(self.edityear_Combo.get())
                                    self.editError.config(text = "Card Info Updated", fg = "medium blue")
                                    self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                                else:
                                    self.editError.config(text = "Error saving 'DATE'", fg = "red2")
                                    self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                            else:
                                self.editError.config(text = "Error saving 'YEAR'", fg = "red2")
                                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                        else:
                            self.editError.config(text = "Error saving 'MONTH'", fg = "red2")
                            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                    else:
                        self.editError.config(text = "Error saving 'CVV' 2", fg = "red2")
                        self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
                else:
                    self.editError.config(text = "Error saving 'CVV' 1", fg = "red2")
                    self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
            else:
                self.editError.config(text = "Error saving 'Card #' 2", fg = "red2")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Card #' 1", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        
        self.card_info.config(text = "edit Card Info")
        self.card_info.unbind("<ButtonPress-1>")
        self.card_info.bind("<ButtonPress-1>", self.edit_cardInfo)
        
        self.editcard_Entry.destroy()
        self.editcvv_Entry.destroy()
        self.editmonth_Combo.destroy()
        self.edityear_Combo.destroy()
        
        card_no = str(self.card)
        self.card_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", card_no[:-4]) + card_no[-4:], font = ('bold', 15), width = len(card_no), height = 1, bg = "gray85")
        self.card_lbl.place(x = 10, y = 600)
        self.cvv_lbl = Label(self.mainCanvas, text = re.sub(".", "\u2022", str(self.cvv)), font = ('bold', 15), width = len(str(self.cvv)), height = 1, bg = "gray85")
        self.cvv_lbl.place(x = 270, y = 600)
        self.date_lbl = Label(self.mainCanvas, text = f'{self.exp_month}/{self.exp_year}', font = ('bold', 15), width = 5, height = 1, bg = "gray85")
        self.date_lbl.place(x = 370, y = 600)

    def edit_id(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.id_lbl_edit.unbind("<ButtonPress-1>")
        self.id_lbl_edit.bind("<ButtonPress-1>", self.save_id)
        self.id_lbl_edit.config(text = "save")
        self.id_lbl.destroy()
        self.editid_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editid_Entry.place(x = 10, y = 420, width = 210, height = 30)
        self.editid_Entry.insert(0, self.id)
    
    def save_id(self, event):
        if len(self.editid_Entry.get()) != 0:
            regex = r'^\d{9}$'
            if(re.fullmatch(regex,self.editid_Entry.get())):
                self.id = self.editid_Entry.get()
                self.editError.config(text = "Driver's ID Updated", fg = "medium blue")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
            else:
                self.editError.config(text = "Error saving 'Driver's ID'", fg = "red2")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Driver's ID'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.id_lbl_edit.unbind("<ButtonPress-1>")
        self.id_lbl_edit.bind("<ButtonPress-1>", self.edit_id)
        self.id_lbl_edit.config(text = "edit")
        self.editid_Entry.destroy()
        self.id_lbl = Label(self.mainCanvas, text = self.id, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.id_lbl.place(x = 10, y = 420) 
    
    def edit_phone(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.phone_lbl_edit.unbind("<ButtonPress-1>")
        self.phone_lbl_edit.bind("<ButtonPress-1>", self.save_phone)
        self.phone_lbl_edit.config(text = "save")
        self.phone_lbl.destroy()
        self.editphone_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editphone_Entry.place(x = 250, y = 300, width = 210, height = 30)
        self.editphone_Entry.insert(0, self.phone)
        
    def save_phone(self, event):
        if len(self.editphone_Entry.get()) != 0:
            regex = r'^\d{1,4}\d{7}$'
            if(re.fullmatch(regex, self.editphone_Entry.get())):
                self.phone = self.editphone_Entry.get()
                self.editError.config(text = "Contact # Updated", fg = "medium blue")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
            else:
                self.editError.config(text = "Error saving 'Contact #'", fg = "red2")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Contact #'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.phone_lbl_edit.unbind("<ButtonPress-1>")
        self.phone_lbl_edit.bind("<ButtonPress-1>", self.edit_phone)
        self.phone_lbl_edit.config(text = "edit")
        self.editphone_Entry.destroy()
        self.phone_lbl = Label(self.mainCanvas, text = self.phone, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.phone_lbl.place(x = 250, y = 300) 
   
    def edit_email(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.email_lbl_edit.unbind("<ButtonPress-1>")
        self.email_lbl_edit.bind("<ButtonPress-1>", self.save_email)
        self.email_lbl_edit.config(text = "save")
        self.email_lbl.destroy()
        self.editemail_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editemail_Entry.place(x = 10, y = 300, width = 210, height = 30) 
        self.editemail_Entry.insert(0, self.email)
        
    def save_email(self, event):
        if len(self.editemail_Entry.get()) != 0:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if(re.fullmatch(regex, self.editemail_Entry.get())):
                self.email = self.editemail_Entry.get()
                self.editError.config(text = "Email Updated", fg = "medium blue")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
            else:
                self.editError.config(text = "Error saving 'Email'", fg = "red2")
                self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Email'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.email_lbl_edit.unbind("<ButtonPress-1>")
        self.email_lbl_edit.bind("<ButtonPress-1>", self.edit_email)
        self.email_lbl_edit.config(text = "edit")
        self.editemail_Entry.destroy()
        self.email_lbl = Label(self.mainCanvas, text = self.email, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.email_lbl.place(x = 10, y = 300) 

    def edit_lname(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.lname_lbl_edit.unbind("<ButtonPress-1>")
        self.lname_lbl_edit.bind("<ButtonPress-1>", self.save_lname)
        self.lname_lbl_edit.config(text = "save")
        self.lname_lbl.destroy()
        self.editlname_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editlname_Entry.place(x = 250, y = 180, width = 210, height = 30)
        self.editlname_Entry.insert(0, self.lname)
        
    def save_lname(self, event):
        if len(self.editlname_Entry.get()) != 0:
            self.lname = self.editlname_Entry.get()
            self.editError.config(text = "LastName Updated", fg = "medium blue")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Lastname'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.lname_lbl_edit.unbind("<ButtonPress-1>")
        self.lname_lbl_edit.bind("<ButtonPress-1>", self.edit_lname)
        self.lname_lbl_edit.config(text = "edit")
        self.editlname_Entry.destroy()
        self.lname_lbl = Label(self.mainCanvas, text = self.lname, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.lname_lbl.place(x = 250, y = 180)
    
    def edit_fname(self, event):
        self.editError.config(fg = "red2")
        self.editError.place_forget()
        self.fname_lbl_edit.unbind("<ButtonPress-1>")
        self.fname_lbl_edit.bind("<ButtonPress-1>", self.save_fname)
        self.fname_lbl_edit.config(text = "save")
        self.fname_lbl.destroy()
        self.editfname_Entry = Entry(self.mainCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',12))
        self.editfname_Entry.place(x = 10, y = 180, width = 210, height = 30)
        self.editfname_Entry.insert(0, self.fname)
        
    def save_fname(self, event):
        if len(self.editfname_Entry.get()) != 0:
            self.fname = self.editfname_Entry.get()
            self.editError.config(text = "FirstName Updated", fg = "medium blue")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        else:
            self.editError.config(text = "Error saving 'Firstname'", fg = "red2")
            self.editError.place(x = int((self.mainCanvas.winfo_reqwidth() / 2) - (self.editError.winfo_reqwidth() / 2)), y = 100)
        self.fname_lbl_edit.unbind("<ButtonPress-1>")
        self.fname_lbl_edit.bind("<ButtonPress-1>", self.edit_fname)
        self.fname_lbl_edit.config(text = "edit")
        self.editfname_Entry.destroy()
        self.fname_lbl = Label(self.mainCanvas, text = self.fname, font = ('bold', 15), width = 14, height = 1, bg = "gray85")
        self.fname_lbl.place(x = 10, y = 180)

    def clear_error(self, event):
        self.editError.config(text = "", fg = "red2")
 
    def from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'        
 
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
    def checker(self,):
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
        self.frame.bind("<Configure>", self.on_NewFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self.new_on_mousewheel) 
        self.canvas.bind_all("<Double-Button-1>", self.backtoHome)

    #this function creates the parking lot objects and displays on the window
    def populate(self):
        #creates a list to store the parking lot objects
        self.lots = []
        global distances
        distances = [100,300,600,400,200, 150,250,350,450,550]
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
    def create_rectangle(self, canvas:Canvas , x1:int, y1:int, x2:int, y2:int, **kwargs):
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
    def setButton(self, c:Canvas, choice: str, lot:ParkingLotInfo, i:int):
        return Button(c, text="Reserve", font = ('bold',20), command = lambda : self. setParkingLot(lot, i), width = 10, height = 2, highlightthickness = 0, relief = "flat", borderwidth = 0, bg = choice, fg = "black")

    #this function sets the activeLot variable to the selected parking lot object
    def setParkingLot(self, lot:ParkingLotInfo, url:str, name:str, distance:float,):#self.setParkingLot(parkingLot, url, name, distance)
        #reconfigures the command for the 'userLabelButton' button
        #self.setUserButtonIfUserExists()
        try:
            #destroys the 'noUserPopupLabel' canvas if it exists
            self.noUserPopupLabel.destroy()
        except Exception:
            pass
        self.activeLot = lot
        self.loturl = url
        self.lot_name = name
        self.distanceFromYOU = distance
        
        self.has_activeLot = True
        self.checker()
        
    #this function configues the 'canvas' canvas
    def on_NewFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #this function configues the 'canvas' canvas scroll type
    def new_on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
        try:
            self.mailBoxCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass

    #this method selects a parking spot for the user
    def showGivenSpot(self,):
        self.setActiveScreen(6)        
        #the 'mySpot' variable is assigned a random available spot (type - list)
        if self.mySpot is None:
            self.mySpot = choice(self.activeLot.ParkingLot_availableSpots)
        self.currentBooking.set_spot(self.mySpot[0])
        print(f"mySpot: {self.mySpot}")
        self.document_booking()
        #self.mainCanvas.destroy()
        #self.create_mainCanvas()
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
        self.EntranceMap_mail = ImageTk.PhotoImage(entrance.output_image().resize((450,400), Image.Resampling.LANCZOS))
        #creates a ParkinLot object 'exit', using specific parameters 
        exit = ParkingLot(self.activeLot.ParkingLot_mapcontents, self.activeLot.ParkingLot_sides, index, "X", 0, self.mySpot[0],  f"{self.activeLot.path}{self.mySpot[0]}_exit.png", self.activeLot.ParkingLot_number)
        #creates an 'ExitMap' image
        self.ExitMap = ImageTk.PhotoImage(exit.output_image().resize(self.newsize, Image.Resampling.LANCZOS))
        self.ExitMap_mail = ImageTk.PhotoImage(exit.output_image().resize((450,400), Image.Resampling.LANCZOS))
        try:
            self.sendMail()
        except Exception:
            pass

    def sendMail(self):
        #If there is an active user present, send them a confirmation mail (450,400)
        if self.userExists:
            #create entrance map 'mail' item
            mail = FMPSpot_Mail(self.lot_name, self.distanceFromYOU, self.mySpot[0], "Entrance Map", 1, datetime.now(), self.email, image = self.EntranceMap_mail, url = self.loturl, browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
            #mail = Mail(self.lot_name, self.distanceFromYOU, self.mySpot[0], "Entrance Map", 1, datetime.now(), image = self.EntranceMap_mail)
            self.inbox.append(mail)
            #create exit map 'mail' item
            mail = FMPSpot_Mail(self.lot_name, self.distanceFromYOU, self.mySpot[0], "Exit Map", 2, datetime.now(), self.email, image = self.ExitMap_mail, url = self.loturl, browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
            #mail = Mail(self.lot_name, self.distanceFromYOU, self.mySpot[0], "Exit Map", 2, datetime.now(), image = self.ExitMap_mail)
            self.inbox.append(mail)

    #this function sets the boolean for each screen
    def setActiveScreen(self, screenNum:int):
        if screenNum == 1:
            pass
        else:
            self.homeScreen_bool = False
        if screenNum == 2:
            self.appLoadingScreen_bool = True
        else:
            self.appLoadingScreen_bool = False
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
        
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 30, text = 'MAILBOX', font = ('bold', 30), anchor = "center", tags = 'text')
        if self.userExists:
            self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 60, text = f'{self.email}', font = ('bold', 18), anchor = "center", tags = 'text',fill = "gray31")
        else:
            self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 60, text = f'{self.demoEmail}', font = ('bold', 18), anchor = "center", tags = 'text',fill = "gray31")
            
        #get dummy mails (if necessary) - used to fix mailbox
        self.setDummyMails()
        
        Button(self.mainCanvas, text = 'BACK', relief = "flat", font = ('bold', 15), fg = "blue2", activeforeground = "blue2", bg = "light cyan", activebackground = "light cyan", command = lambda : self.backHome()).place(x = 10, y  = 10)
            
        if len(self.inbox) == 0:
            amnt = "mail"
        else:
            amnt = "mails"
        self.mainCanvas.create_text(int(self.mainCanvas.winfo_reqwidth()/2+20), 85, text = f'{len(self.inbox)} {amnt} in Inbox', font = ('bold', 14), anchor = "center", tags = 'text',fill = "gray50")
        
        self.mainCanvas.create_rectangle(3, 3, self.mainCanvas.winfo_reqwidth() - 3, self.mainCanvas.winfo_reqheight() - 3, outline = "black", width = 2, tags="rectangle")   
        
        self.mailBoxCanvas = Canvas(self.mainCanvas, bd = 0, highlightthickness  =2, relief = 'ridge', highlightbackground = "black", bg = "light cyan")
        self.mailBoxCanvas.bind("<Double-Button-1>", self.CloseMailnGoBacktoHome)
        
        #self.mailBoxCanvas.create_rectangle(0, 571, 288, 631, outline = "red", width = 2, tags="rectangle")
        
        if len(self.inbox) == 0:
            self.emptyMailBox()
        else:
            self.gotMail()

    #creates a dummy image for the dummy emails    
    def createDummyImages(self):
        image = Image.open(files.dummy_entrance_image)
        nextimg = image.resize((450,400), Image.Resampling.LANCZOS)
        self.dummyEntImage = ImageTk.PhotoImage(nextimg)
        image = Image.open(files.dummy_exit_image)
        nextimg = image.resize((450,400), Image.Resampling.LANCZOS)
        self.dummyExtImage = ImageTk.PhotoImage(nextimg)
    
    #these functions are used to check if 'self.gotMail()' works properly
    def dummyMails1(self):
        self.createDummyImages()
        mail = FMPSpot_Mail("First Parking Lot", 100, "A4", "Entrance Map", 1, datetime.now(), self.email, self.dummyEntImage, url="http://www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("First Parking Lot", 100, "A4", "Exit Map", 2, datetime.now(), self.email, self.dummyExtImage, url="www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        #self.inbox.append(mail)
        mail = FMPSpot_Mail("Second Parking Lot", 200, "A4", "Entrance Map", 1, datetime.now(), self.email, self.dummyEntImage, url="www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        #self.inbox.append(mail)
        mail = FMPSpot_Mail("Second Parking Lot", 200, "A4", "Exit Map", 2, datetime.now(), self.email, self.dummyExtImage, url="www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        #self.inbox.append(mail)
        mail = FMPSpot_Mail("Third Parking Lot", 300, "A4", "Entrance Map", 1, datetime.now(), self.email, self.dummyEntImage, url="http://www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        #self.inbox.append(mail)
        mail = FMPSpot_Mail("ThirdParkingLot1234567890123456", 300, "A4", "Exit Map", 2, datetime.now(), self.email, self.dummyExtImage, url="http://www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Intersection of Maxfield Avenue \n& Hagley Park Road", 400, "A4", "Entrance Map", 1, datetime.now(), self.email, self.dummyEntImage, url="http://www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        mail = FMPSpot_Mail("Intersection of Maxfield Avenue \n& Hagley Park Road", 400, "A4", "Exit Map", 2, datetime.now(), self.email, self.dummyExtImage, url="www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        #self.inbox.append(mail)
        
    def dummyMails2(self):
        mail = FMPLot_Mail("SecondParkingLotdfdfdgh1234567", 400, datetime.now(), self.email, url="www.google.first", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        mail = FMPLot_Mail("SecondParkingLotdfdfdghghhhgdghdghghfgh12", 300, datetime.now(), self.email, url="www.google.second", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
        mail = FMPLot_Mail("Intersection of Maxfield Avenue &\n Hagley Park Road", 200, datetime.now(), self.email, url="www.google.com", browser_width= self.mainCanvas.winfo_reqwidth() - 70, browser_height=self.mainCanvas.winfo_reqheight() - 120)
        self.inbox.append(mail)
    
    def dummyMails3(self):
        mail = Bank_Statement(datetime.now(), self.fname, self.email, 300, )
        self.inbox.append(mail)
        mail = Bank_Statement(datetime.now(), self.fname, self.email, 500,  )
        self.inbox.append(mail)
        mail = Bank_Statement(datetime.now(), self.fname, self.email, 100.50, )
        self.inbox.append(mail) 

    def setDummyMails(self, one:bool = False, two:bool = False, three:bool = False):
        if one:
            self.dummyMails1()
        if two:
            self.dummyMails2()
        if three:
            self.dummyMails3()

    #this function is called if the mailbox is empty
    def emptyMailBox(self):
        self.mailBoxCanvas.place(x = 100, y = 100, width = (int(self.mainCanvas.winfo_reqwidth()) ) - 102, height = self.mainCanvas.winfo_reqheight() - 103,)
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

    #this function is calld if the length of the user inbox is not 0
    #it populates the inbox area with mini canvases to show mail information
    def gotMail(self):
        try: self.listbox.destroy()
        except Exception: pass
        stop = 0
        
        self.mailBoxCanvas.place(x = 2, y = 100, width = self.mainCanvas.winfo_reqwidth() - 6 , height = self.mainCanvas.winfo_reqheight() - 103,)
        
        self.mailScroll()
        while stop < (len(self.inbox) + 8):
            if stop <= len(self.inbox) - 1:
                popupMail_width = int(self.mainCanvas.winfo_reqwidth() - 12)
                popupMail_height = int(((self.mainCanvas.winfo_reqheight() / 8) * 7) - 7)
                email_thumbnail = self.inbox[stop].setMailCanvas(self.frame, 
                                                                 self.mainCanvas.winfo_reqwidth() - 21, 
                                                                 popupMail_width, 
                                                                 popupMail_height, 
                                                                 (len(self.inbox) - 1) - stop,
                                                                 self.mainCanvas)
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
        self.frame.bind("<Configure>", self.on_NewFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self.new_on_mousewheel)
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
#this are simple classes to construct what the 'emails' are to look like
class FMPSpot_Mail:
    def __init__(self, lot_name:str, distance:float, spot:str, header:str, type:int, time:datetime, email:str, image = None, url:str = "", browser_width:int = 0, browser_height:int = 0):
        self.lot_name = lot_name
        self.distance = distance
        self.spot = spot
        self.header = header
        self.type = type
        self.time = time
        self.email = email
        self.image = image
        self.url = url
        self.browser_width = browser_width
        self.browser_height = browser_height

    #this function creates a canvas widget to display mail information
    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i = None, parentCanvas:Canvas = None):  
        self.parentCanvas = parentCanvas     
        c = Canvas(canvas, height = 100, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "F", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "Find Me Parking", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"{self.header} from Find Me Parking", font = ('bold', 12), anchor="w")
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[Find Me Parking] Your parking spot at ...            ", font = ('bold', 10), )
        
        logo.place(x = 10, y = 15, width = 80, height = 80,)
        time.place(x = 400, y = 15)
        header.place(x = 95, y = 9)
        middle.place(x = 95, y = 44)
        footcontainer.place(x = 95, y = 70, width = 360)
        
        logo.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        time.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        header.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        middle.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        footcontainer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        footer.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        c.bind("<ButtonPress-1>", lambda event, a = i, b = popupMail_width, c = popupMail_height: self.clickedmail(b,c,a,))
        
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

    #this function is called when a populated mail is clicked
    def clickedmail(self, popupMail_width, popupMail_height, i = None, parentCanvas:Canvas = None):
        if i is not None:
            if self.type == 1: #Entrance Map
                txt1 = 'Please follow this guide map to get to'
                txt2 = f'{self.spot} quickly and safely'
            elif self.type == 2:
                txt1 = 'Please follow this guide map to get from'
                txt2 = f'{self.spot} to the Exit quickly and safely' 
            bg = "honeydew4"
            fill  = "gray85"
            outline = "black"
            mini_txt = "gray90"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 400, y = 8)
            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"Find Me Parking: {self.header}", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "F", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)
            Label(popupMail, text = "Find Me Parking", font = ('bold',12), fg = mini_txt, bg = bg).place(x = 65, y = 43)
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 405, y = 50)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 71)
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = "gray85", tags="rectangle")

            lotname = self.lot_name.replace('\n', '')
            lot_lbl1 = Label(popupMail, text = f"{lotname}", font = ('bold',17), fg = "green", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            if len(lotname) > 30:
                lot_lbl1.place(x = int(popupMail_width/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 114)
            else:
                lot_lbl1.place(x = int(popupMail_width/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 135)

            popupMail.create_text(int(popupMail_width / 2), 195, text = f'{self.header}', font = ('bold', 15), fill = 'blue')
            popupMail.create_text(int(popupMail_width / 2), 225, text = f'Your parking spot is at {self.spot}', font = ('bold', 15))
            image_label = Label(popupMail, bg = bg, image = self.image)
            image_label.place(x = int(popupMail_width / 2) - int(image_label.winfo_reqwidth() / 2), y = 250)
            popupMail.create_text(int(popupMail_width / 2), 672, text = f'You are {self.distance:.2f}km away', font = ('bold', 12))  
            popupMail.create_text(int(popupMail_width / 2), 692, text = txt1, font = ('bold', 12))
            popupMail.create_text(int(popupMail_width / 2), 712, text = txt2, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 737, text = 'Not satisfied with this spot?', font = ('bold', 9))
            popupMail.create_text(int(popupMail_width / 2), 754, text = 'You can change it in the Find Me Parking App', font = ('bold', 9))

            url_btn = Button(popupMail, text = "click here for directions to your location", font = ('bold',9,'underline'), fg = "blue", bg = fill, justify = "center", relief='flat',highlightthickness=0, bd=0, borderwidth=0, activebackground = fill, activeforeground="blue", command=self.openURL)
            url_btn.place(x = int(popupMail_width/2) - int(url_btn.winfo_reqwidth()/2), y = 766)
            
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)

    def openURL(self):
        Browser(f"{self.spot} @ {self.lot_name}",self.url, self.browser_width, self.browser_height,)

class FMPLot_Mail:
    def __init__(self, lot_name:str, distance:float, time:datetime, email:str, url:str = "", browser_width:int = 0, browser_height:int = 0):
        self.lot_name = lot_name
        self.distance = distance
        self.time = time
        self.email = email        
        self.url = url
        self.browser_width = browser_width
        self.browser_height = browser_height
    
    #this function creates a canvas widget to display mail information
    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i = None, parentCanvas:Canvas = None,):
        self.parentCanvas = parentCanvas       
        c = Canvas(canvas, height = 100, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "F", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "Find Me Parking", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"to {self.lot_name}", font = ('bold', 12), anchor="w")
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[Find Me Parking] Your parking lot choice is ...      ", font = ('bold', 10), )
        
        logo.place(x = 10, y = 15, width = 80, height = 80,)
        time.place(x = 400, y = 15)
        header.place(x = 95, y = 9)
        middle.place(x = 95, y = 44, width = 360)
        footcontainer.place(x = 95, y = 70, width = 360)
        
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

    #this function is called when a populated mail is clicked
    def clickedmail(self, popupMail_width, popupMail_height, i = None):
        if i is not None:
            txt1 = 'for directions to get to'
            txt2 = f'quickly and safely'
            
            bg = "honeydew4"
            outline = "black"
            mini_txt = "gray90"
            fill  = "gray85"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 400, y = 10)

            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"Find Me Parking", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "F", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)
            lotname = self.lot_name.replace('\n', '')
            if len(lotname) > 30:
                Label(popupMail, text = f"to {lotname}", font = ('bold',11), fg = mini_txt, bg = bg, justify = "left", wraplength=300).place(x = 65, y = 39)
                Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 83)
            else:    
                Label(popupMail, text = f"to {lotname}", font = ('bold',11), fg = mini_txt, bg = bg, justify = "left", wraplength=300).place(x = 65, y = 49)
                Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 73)
                
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 405, y = 56)
            
            
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = fill, tags="rectangle")
            
            popupMail.create_text(int(popupMail_width / 2), 163, text = 'Your parking lot choice is:', font = ('bold', 17))
            lot_lbl1 = Label(popupMail, text = f"{lotname}", font = ('bold',22), fg = "green", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            if len(lotname) > 24:
                lot_lbl1.place(x = int(popupMail_width/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 200)
            else:
                lot_lbl1.place(x = int(popupMail_width/2) - int(lot_lbl1.winfo_reqwidth()/2), y = 250)
            popupMail.create_text(int(popupMail_width / 2), 380, text = f'You are {self.distance:.2f}km away', font = ('bold', 17))
            
            url = Button(popupMail, text = "click here", font = ('bold',15,'underline'), fg = "blue", bg = fill, justify = "center", relief='flat',highlightthickness=0, bd=0, borderwidth=0, activebackground = fill, activeforeground="blue", command=self.openURL)
            url.place(x = int(popupMail_width/2) - int(url.winfo_reqwidth()/2), y = 490)
            
            popupMail.create_text(int(popupMail_width / 2), 540, text = txt1, font = ('bold', 12))
            
            lot_lbl2 = Label(popupMail, text = f"{lotname}", font = ('bold',12), fg = "black", bg = fill, justify = "center", wraplength=popupMail_width-6-6-10-10)
            lot_lbl2.place(x = int(popupMail_width/2) - int(lot_lbl2.winfo_reqwidth()/2), y = 553)

            if len(lotname) > 44: 
                popupMail.create_text(int(popupMail_width / 2), 615, text = txt2, font = ('bold', 12))
            else:
                popupMail.create_text(int(popupMail_width / 2), 595, text = txt2, font = ('bold', 12))
            
            popupMail.create_text(int(popupMail_width / 2), 745, text = 'Not satisfied with this lot?', font = ('bold', 9))
            popupMail.create_text(int(popupMail_width / 2), 762, text = 'You can change it in the Find Me Parking App', font = ('bold', 9))
            
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 6)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)
            
    def openURL(self):
        Browser(self.lot_name,'https://www.google.com/', self.browser_width, self.browser_height,)

class Bank_Statement:
    def __init__(self, time:datetime, name:str, email:str, balance:float,):
        self.distance = distance
        self.time = time
        self.name = name
        self.email = email        
        self.balance = balance

    #this function creates a canvas widget to display mail information
    def setMailCanvas(self, canvas:Canvas, width:int, popupMail_width:int, popupMail_height:int, i:int = None, parentCanvas:Canvas = None,):
        self.parentCanvas = parentCanvas       
        c = Canvas(canvas, height = 100, width = width, bd = 1, highlightbackground = "gray87",  relief = "flat", )
        logo = Label(c, text = "B", font = ('bold',50), borderwidth = 2, relief = "solid",)
        time = Label(c, text = f'{self.time.strftime("%b %d")}', font = ('bold', 10),)       
        header = Label(c,)
        header.config(text = "YOUR BANK", font = ('bold', 17))
        middle = Label(c,)
        middle.config(text = f"{self.name} Account", font = ('bold', 12), anchor="w")
        footcontainer = Label(c, borderwidth = 0, )
        footer = Label(footcontainer,)
        footer.grid(row = 0, column = 0)
        footer.config(text = f"[YOUR BANK]  Your account balance is: ...             ", font = ('bold', 10), )
        
        logo.place(x = 10, y = 15, width = 80, height = 80,)
        time.place(x = 400, y = 15)
        header.place(x = 95, y = 9)
        middle.place(x = 95, y = 44)
        footcontainer.place(x = 95, y = 70, width = 360)
        
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

    #this function is called when a populated mail is clicked
    def clickedmail(self, popupMail_width:int, popupMail_height:int, i = None):
        if i is not None:
            txt1 = 'thank you for choosing'
            txt2 = f'[BIG BANK]'
            
            bg = "honeydew4"
            outline = "black"
            mini_txt = "gray90"
            fill  = "gray85"
            popupMail = Canvas(self.parentCanvas, bg = bg, highlightbackground = outline)
            Button(popupMail, text = 'close', relief = "flat", font = ('bold', 12), fg = "red2", activeforeground = "red2", bg = bg, activebackground = bg, command = popupMail.destroy, bd = 2).place(x = 400, y = 10)

            headerContain = Label(popupMail, bg = bg)
            header = Label(headerContain, text = f"{txt2}", font = ('bold', 15), fg = outline, bg = bg)
            Label(popupMail, text = "B", font = ('bold',30), borderwidth = 2, relief = "solid", ).place(x = 10, y = 50, width = 50, height = 50)

            Label(popupMail, text = f"{self.name} Account Balance", font = ('bold',12), fg = mini_txt, bg = bg, justify = "left", wraplength=200).place(x = 65, y = 50)
            Label(popupMail, text = f'{self.time.strftime("%b %d")}', font = ('bold',9), fg = mini_txt, bg = bg).place(x = 405, y = 56)
            Label(popupMail, text = f'to: {self.email}', font = ('bold',10), fg = mini_txt, bg = bg).place(x = 65, y = 71)
            
            popupMail.create_rectangle(6, 110, popupMail_width - 6, popupMail_height - 7, outline = outline, width = 2, fill = fill, tags="rectangle")
            
            popupMail.create_text(int(popupMail_width / 2), 200, text = f'Hello {self.name}', font = ('bold', 17))
            popupMail.create_text(int(popupMail_width / 2), 240, text = 'Your account balance is:', font = ('bold', 17))
            balance_lbl = Label(popupMail, text = f"${self.balance:.2f}", font = ('bold',40), fg = "blue", bg = "#ffffff", justify = "center", wraplength=popupMail_width-6-6-10-10)
            balance_lbl.place(x = int(popupMail_width/2) - int(balance_lbl.winfo_reqwidth()/2), y = 340)
            
            popupMail.create_text(int(popupMail_width / 2), 520, text = txt1, font = ('bold', 12))            
            popupMail.create_text(int(popupMail_width / 2), 560, text = txt2, font = ('bold', 18))
            
            header.grid(row = 0, column = 0)
            headerContain.place(x = 8, y = 10)
            
            popupMail.create_text(popupMail_width - 50, popupMail_height+4, text = 'Capstone Group 3', font = ('bold', 6), fill = "dark green")
            popupMail.place(x = 6, y = 100, width = popupMail_width, height = popupMail_height+15)

class Browser:
    def __init__(self, title:str, url:str, width:int, height:int):
        self.webview_window = None
        self.title = title
        self.open_webview(url, width, height)
        
    def load_url(self, url:str):
        # change url:
        self.webview_window.load_url(url)
        
    # Function to create the webview window
    def create_webview_window(self, width:int, height:int):
        if self.webview_window is None:
            #width, height = 400, 750 #original sizes
            self.webview_window = web.create_window(title=f'from YOU to {self.title}', width=width, height=height, x=300, y=0, on_top=True, resizable=False, min_size=(width,height),)
            
    # Function to open webview on the main thread
    def open_webview(self, url:str, width:int, height:int):
        if self.webview_window is None:
            self.create_webview_window(width, height)
            web.start(gui='tkinter', debug=False, func=lambda:self.load_url(url))
            
    # Function to close the webview window
    def close_webview(self,):
        if self.webview_window is not None:
            try:
                web.destroy_window()
            except Exception:
                pass
        self.webview_window = None
        self.parent.deiconify()

class Booking: # type:str, spot:str, time:datetime, amount:int, success:bool):
    def __init__(booking, lot_name:str,):
        booking.__lot_name = lot_name
        #booking.type = f"{type} booking" 
        #booking.spot = spot
        #booking.time = time
        #booking.amount = amount
        #booking.success = "Successful" if success else "Failed"
        
    def set_lot_name(booking, lot_name:str):
        booking.__lot_name = lot_name
    
    def get_lot_name(booking,):
        return booking.__lot_name
        
    def set_type(booking, type:int):
        booking.__type = type
        
    def get_type(booking,):
        return booking.__type
    
    def get_type_string(booking):
        return "assisted booking" if booking.__type == 1 else "self booking"
        
    def set_spot(booking, spot:str):
        booking.__spot = spot
        
    def get_spot(booking):
        return booking.__spot
        
    def set_time(booking, time:datetime):
        booking.__time = time
        
    def get_time(booking,):
        return booking.__time
        
    def set_amount(booking, amount:float):
        booking.__amount = amount
        
    def get_amount(booking,):
        return booking.__amount 
        
    def set_outcome(booking, outcome:bool):
        booking.__outcome = outcome
    
    def get_outcome(booking,):
        return booking.__outcome 
    
    def get_outcome_string(booking,):
        return "Successful" if booking.__outcome else "Failed"

if __name__ == "__main__":
    a = web.create_window(title="CLOSE TO OPEN APP", width=300, height=10, resizable=False, focus=False)
    web.start()
    a = None
    if a is None: FindMeParkingApp()