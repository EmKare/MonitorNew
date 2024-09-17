from tkinter import Tk, Label, Button, Toplevel, font, LabelFrame, Canvas, PhotoImage, Frame, mainloop, NW, Entry, END
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from urllib.request import urlopen
from tkinter.ttk import Combobox
from tkinter import ttk as ttk
from PIL import ImageTk, Image
from utils import rescaleFrame
from geopy import distance 
from time import strftime
import threading as th
import files as files
import pickle as pkl
import cvzone as cz
import numpy as np
import cv2 as cv

#Main window
class App(Tk):
    def __init__(self, username, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.__window_bredth, self.__window_length = 1350, 760
        
        #setting up the window
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+50+10")
        self.resizable(False, False)
        self.title(f"Group 3 : Find Me Parking App - User: {username}")
        self.timeBool = True
        icon = Image.open(files.icon)
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)
        #-- getting streams --
        self.vids = files.sources
        #SideMenu Window -------------------------------------------------------------------------------------------------------
        #frame for sidemenu
        self.sidemenuFrame = Frame(self, highlightthickness = 0, bd = 2, width = 150, height = self.__window_length, relief = "flat", )
        self.sidemenuFrame.place(x = 0, y = 0, )
        #Title Window -----------------------------------------------------------------------------------------------------------
        #frame for title
        title_colour = "green"
        self.titleFrame = Frame(self, bg=title_colour, highlightthickness = 0, bd = 2, width = self.__window_bredth - self.sidemenuFrame.winfo_reqwidth(), height = 90,)
        self.titleFrame.place(x = self.sidemenuFrame.winfo_reqwidth(), y = 0, )
        #Container for Main Frame -------------------------------------------------------------------------------------------------
        self.container = LabelFrame(self, text="", highlightthickness = 0, bd = 2,  relief = "flat", border=0)
        self.container.place(x = self.sidemenuFrame.winfo_reqwidth(), 
                             y = self.titleFrame.winfo_reqheight(), 
                             width = self.__window_bredth - self.sidemenuFrame.winfo_reqwidth(), 
                             height = self.__window_length - self.titleFrame.winfo_reqheight(),)
        #Main Frame -----------------------------------------------------------------------------------------------------------
        #frame for main window
        mainWindowFrame = Frame(self.container, highlightthickness = 0, bd = 0, relief = "flat", 
                                width = self.__window_bredth - self.sidemenuFrame.winfo_reqwidth(), 
                                height = self.__window_length - self.titleFrame.winfo_reqheight(), )
        mainWindowFrame.pack(side="top", fill="both", expand=True)
        mainWindowFrame.grid_rowconfigure(0, weight=1)
        mainWindowFrame.grid_columnconfigure(0, weight=1)
        #(1200,670)
        #dictionary of frames
        self.listOfFrames = {}
        #key = class, value is the class with the frame in constructor
        for classes in (EditWindow, ViewWindow, AddFeed, ViewMap, Settings):
            theframe = classes(parent = mainWindowFrame, master = self, sources= self.vids)
            self.listOfFrames[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
        #Side Menu Buttons-----------------------------------------------------------------------------------------------------------
        self.editWindowButton = Button(self.sidemenuFrame, text = "Edit Feed", font = ('calibri', 18), fg = "black", bd= 1, command = lambda: self.show_frame(EditWindow))
        self.editWindowButton.place(x = 0, y = 0, width = self.sidemenuFrame.winfo_reqwidth(), height = (self.sidemenuFrame.winfo_reqheight() / 5))
        
        self.viewWindowButton = Button(self.sidemenuFrame, text = "View Feeds", font = ('calibri', 18), fg = "black", bd= 1, command = lambda: self.show_frame(ViewWindow))
        self.viewWindowButton.place(x = 0, y = 152, width = self.sidemenuFrame.winfo_reqwidth(), height = (self.sidemenuFrame.winfo_reqheight() / 5))
        
        self.addFeedDataWindowButton = Button(self.sidemenuFrame, text = "Add Feeds", font = ('calibri', 18), fg = "black", bd= 1, command=lambda: self.show_frame(AddFeed))
        self.addFeedDataWindowButton.place(x = 0, y = 304, width = self.sidemenuFrame.winfo_reqwidth(), height = (self.sidemenuFrame.winfo_reqheight() / 5))
        
        self.viewMapWindowButton = Button(self.sidemenuFrame, text = "View Map", font = ('calibri', 18), fg = "black", bd= 1, command=lambda: self.show_frame(ViewMap))
        self.viewMapWindowButton.place(x = 0, y = 456, width = self.sidemenuFrame.winfo_reqwidth(), height = (self.sidemenuFrame.winfo_reqheight() / 5))
        
        self.settingsWindowButton = Button(self.sidemenuFrame, text = "Settings", font = ('calibri', 18), fg = "black", bd= 1, command=lambda: self.show_frame(Settings), state = "disabled")
        self.settingsWindowButton.place(x = 0, y = 608, width = self.sidemenuFrame.winfo_reqwidth(), height = (self.sidemenuFrame.winfo_reqheight() / 5))
        #Title Window -----------------------------------------------------------------------------------------------------------
        #Name of Parking Lot being monitored
        self.bigLabel = Label(self.titleFrame, text = 'Find Me Parking Surveillance Monitor', font = ('calibri', 35), bg=title_colour)
        self.bigLabel.place(x = (self.titleFrame.winfo_reqwidth() / 2) - int(self.bigLabel.winfo_reqwidth() / 2), 
                            y = (self.titleFrame.winfo_reqheight() / 2) - int(self.bigLabel.winfo_reqheight() / 2))
        #LogOut Button
        self.logoutButton = Button(self.titleFrame, text = "Log Out", font = ('calibri', 18), fg = "red", bg = "white", command = lambda: self.closeApp())
        self.logoutButton.place(x = 0, y = 0,  width = 140, height = self.titleFrame.winfo_reqheight() - 2,)
        #Time label
        self.timeLabel = Label(self.titleFrame, font=('calibri', 20, 'bold'), bg=title_colour, fg='black')          
        #-----------------------------------------------------------------------------------------------------------------------

        #Beginning frame
        self.show_frame(ViewMap)  
        #starts clock module
        self.getTime()      
        #starts tkinter
        mainloop()
        
    def set_timeBool(self, timeBool):
        self.timeBool = timeBool
        
    def get_timeBool(self):
        return self.timeBool
    
    #sets time to time label
    def getTime(self):
        if self.get_timeBool():
            self.timeLabel.config(text = strftime('%h %d, %Y\n%I:%M:%S %p'))
            self.timeLabel.place(x = (self.titleFrame.winfo_reqwidth() / 2) + int(self.bigLabel.winfo_reqwidth() / 2) + 80,
                                y = (self.titleFrame.winfo_reqheight() / 2) - int(self.timeLabel.winfo_reqheight() / 2))
            self.timeLabel.after(1000, self.getTime)
        
    def show_frame(self, anotherClass):
        frame = self.listOfFrames[anotherClass]
        # raises the current frame to the top
        frame.tkraise()

    #Miscellaneous
    def popUpWindow(self):
        popUp = Toplevel(self)
        button = Button(popUp, text="Click To Close", command = lambda : popUp.destroy())
        button.pack()
        
    def closeApp(self):
        from Login import Login
        try:
            EditWindow.closeAll()
        except Exception:
            pass
        self.set_timeBool(False)
        self.destroy()
        Login()
        
class EditWindow(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross = int(self.__window_bredth / 2)

        #Variables
        self.done = True
        self.__space, self.__total = 0, 0, 
        self.__feed = 2
        self.__width, self.__height = 53, 22
        self.buffer = b''
        self.checkfeed = 0
        self.__lotNames = {}
        self.availableSpots = []
        self.__listOfFeeds = sources
        
        self.listLength = len(self.__listOfFeeds)
        #print(f' EditWindow: {self.listLength}') Digicel Main Parking Lot
        self.__listOfFeeds = ["MegaMart Parking Lot East", "NCB Parking Lot", "Sagicor Parking Lot",] #[x[0] for x in sources]
        #Get positions
        self.posList = self.getFileSetArray()
        
        #Name of Parking Lot being monitored
        self.parkingLotNameLabel = Label(self, text = '-------------------------------', font = ('bold', 12), bg = "black", fg = "white")
        self.parkingLotNameLabel.place(x = self.__midpointAcross - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), 
                                       y = 10)
                
        #label showing parking spot readings from footage
        self.readingsLabel = Label(self, text = '-------------------------------', font = ('bold', 12), bg = "black", fg = "white") 
        self.readingsLabel.place(x = self.__midpointAcross - int(self.readingsLabel.winfo_reqwidth() / 2),
                                 y = 40)
        
        #group label
        self.groupLabel = Label(self, text = 'Capstone Group 3', font = ('bold', 5), fg = 'black', justify='right')
        self.groupLabel.place(x = self.__window_bredth - 70, y = self.__window_length - 15)

        #------------------------------------------------------------------------------------------------------------------------
        
        #labelframe for combobox 
        self.comboBoxLabelFrame = LabelFrame(self, text = "  Select Feed  ", font = ('bold', 12), pady = 20, width = 565, height = 140)
        self.comboBoxLabelFrame.place(x = 25, y = 80)
        
        #labelframe for buttons
        self.buttonsLabelFrame = LabelFrame(self, text = "  Options  ", font = ('bold', 12), pady = 10, width = 565, height = 140)
        self.buttonsLabelFrame.place(x = self.__midpointAcross + 15, y = 80)
        
        #labelframe for video feed label
        self.feedLabelFrame = LabelFrame(self, text = "  Video Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400)
        self.feedLabelFrame.place(x = 25, y = 240)
        
        #labelframe for edit footage panel label
        self.editLabelFrame = LabelFrame(self, text = "  Edit Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400, )
        self.editLabelFrame.place(x = self.__midpointAcross + 15, y = 240)
        #------------------------------------------------------------------------------------------------------------------------
        #---BUTTONS---
        #start video feed
        self.startFeedButton = Button(self.buttonsLabelFrame, text = "Start Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.checker())
        self.startFeedButton.place(x = 30, y = 0)
        #stop video feed
        self.endFeedButton = Button(self.buttonsLabelFrame, text = "Stop Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.closer())
        self.endFeedButton.place(x = 210, y = 0)
        #Exit program
        self.exitButton = Button(self.buttonsLabelFrame, text = "Set Spots", font = ('bold', 10), width = 15, height = 5, fg = "black", bg = "red")#, command = lambda: self.closeAll())
        self.exitButton.place(x = 390, y = 0)
        
        #------------------------------------------------------------------------------------------------------------------------
        #Create ComboBox
        self.optionsComboBox = Combobox(self.comboBoxLabelFrame, width = 40, font = ('bold', 10), state = "readonly",)
        self.optionsComboBox['values'] = [x for x in self.__listOfFeeds]
        self.optionsComboBox.current(2)
        self.optionsComboBox.config(font = "None 16 normal")
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 15))
        self.optionsComboBox.place(x = 34, y = 10)
        self.optionsComboBox.bind("<<ComboboxSelected>>", self.option_selected)
        
        #canvas for edit footage panel
        self.createEditCanvas()
    
    def setWidth(self, width):
        #width setter
        self.__width = width
        
    def getWidth(self):
        #width getter
        return self.__width
    
    def setHeight(self, height):
        #height setter
        self.__height = height
        
    def getHeight(self):
        #height getter
        return self.__height

    def setSpaceCounter(self, space):
        #sets how many free spaces are in the parking lot
        self.__space = space
        
    def getSpaceCounter(self):
        #returns how many free spaces are in the parking lot
        return self.__space
    
    def setTotalSpace(self, total):
        #sets how many parking spaces are in the parking lot
        self.__total = total
        
    def getTotalSpace(self):
        #returns how many parking spaces are in the parking lot
        return self.__total
    
    def setFeed(self, feedNumber):
        #sets the feed selected
        self.__feed = feedNumber
    
    def getFeed(self):
        #returns the feed selected
        return self.__feed
    
    def getFileSetArray(self):
        #gets the position of the parking spaces in a parking lot
        try:
            with open('C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CarParkPos', 'rb') as f:
                return pkl.load(f)
        except Exception:
            return []
    
    def createFeedLabel(self):
        self.feedLabel = Label(self.feedLabelFrame, pady = 10,)
        self.feedLabel.configure(image = PhotoImage(width = 550, height = 360))
        self.feedLabel.place(x = 3, y = 0)
        
    def createFeedCanvas(self):
        width, height = 555, 365
        self.feedCanvas = Canvas(self.feedLabelFrame, width = width, height = height)
        self.feedCanvas.place(x = 0, y = 0)
    
    def createEditCanvas(self):
        width, height = 555, 365
        self.editCanvas = Canvas(self.editLabelFrame,  cursor="tcross", width = width, height = height,)
        self.editCanvas.create_text(int(width / 2), int(height / 2), text = "awaiting feed...", font = ('bold', 20), anchor = "center", tags = 'text')
        self.editCanvas.place(x = 0, y = 0)
        self.editCanvas.bind("<ButtonPress-1>", self.leftClick)
        self.editCanvas.bind("<ButtonPress-3>", self.rightClick)
    
    def option_selected(self, event):
        self.parkingLotNameLabel.config(text=self.optionsComboBox.get())
        self.setFeed(self.optionsComboBox.current())
        self.parkingLotNameLabel.place(x = self.__midpointAcross - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), y = 10)
        self.readingsLabel.config(text = '-------------------------------')         
    
    def checker(self):
        if self.checkfeed == 0:
            self.checkfeed = 1
            self.startVideoThread()
    
    def closer(self):
        if self.checkfeed == 1:
            self.closeVideo()
            self.checkfeed = 0
    
    def startVideoThread(self):
        try:
            self.closeVideo()
        except Exception:
            pass
        self.checkfeed = 1
        self.cap = None
        self.parkingLotNameLabel.config(text = self.optionsComboBox.get())
        self.parkingLotNameLabel.place(x = self.__midpointAcross - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), y = 10)
        
        if self.getFeed() == 0:
            self.streamdone = True
            self.cap = urlopen(files.local_cam)
            self.cameraStream()
        if self.getFeed() == 1:
            self.streamdone = True
            self.cap = urlopen(files.local_stream)
            self.cameraStream()
        if self.getFeed() == 2:            
            try:
                self.feedCanvas.destroy()
            except Exception:
                pass
            self.createFeedLabel()
            self.cap = cv.VideoCapture(files.video_name)
            self.im = Image.open(files.image_name)
            self.done = True        
            th.Thread(target = self.runParkingApp).start()
            th.Thread(target = self.settingSpots).start()
            th.Thread(target= self.getReadings, daemon=True).start()
        
    def runParkingApp(self):
        if self.checkfeed == 1:
            try:
                self.editCanvas.delete("text")
            except Exception:
                pass
            self.editCanvas.delete("rect")
            self.drawRectangles(self.posList)
            if self.cap.get(cv.CAP_PROP_POS_FRAMES) == self.cap.get(cv.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                    
            _, frame = self.cap.read()
            if _:            
                frame = rescaleFrame(frame, 0.5)
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                blur = cv.GaussianBlur(gray, (3 , 3), 1)
                binary = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
                median = cv.medianBlur(binary, 5)
                kernel = np.ones((3,3), np.uint8)
                dilate = cv.dilate(median, kernel, iterations = 1)       
                
                self.checkParkingSpace(dilate, frame)

                cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image = img)
                
                self.feedLabel.imgtk = imgtk
                self.feedLabel.configure(height=frame.shape[0], width=frame.shape[1], image = imgtk)
            self.feedLabel.after(1, self.runParkingApp)
        
    def checkParkingSpace(self, imgD, img):
        spaceCounter = 0
        if len(self.posList) > 0:
            for i, pos in enumerate(self.posList):
                x, y = int(pos[0] * 0.97) , int(pos[1] * 0.96)
                 
                imgCrop = imgD[y: y + self.getHeight(), x: x + self.getWidth()]
                count = cv.countNonZero(imgCrop)
                status = ""
                
                if count < 231:
                    colour = (0, 255, 0)
                    thickness = 2
                    spaceCounter += 1
                    status = "A"                    
                else:
                    colour = (0, 0, 255)
                    thickness = 1
                    status = "U"

                self.writeSpaceCounter(spaceCounter)                
                self.setTotalSpace(len(self.posList))
                
                cv.rectangle(img, (x, y), (x + self.getWidth(), y + self.getHeight()), colour, thickness)
                spotName = ""
                spot = ""
                if i <= 10:
                    spot = f"F{11 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)
                if i <= 22 and i >= 11:
                    spot = f"E{23 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)
                if i <= 33 and i >= 23 :
                    spot = f"D{34 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)
                if i <= 44 and i >= 34:
                    spot = f"C{45 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)
                if i <= 56 and i >= 45:
                    spot = f"B{57 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)
                if i <= 68 and i >= 57:
                    spot = f"A{69 - i}"
                    spotName = f"{i}#{spot}#{status}"
                    cz.putTextRect(img, spot, (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                    if status == "A":
                        self.availableSpots.append(spot)                
                self.__lotNames.update({pos:spotName})

    def writeSpaceCounter(self, spaceCounter):
        if spaceCounter is not self.getSpaceCounter():            
            try:
                f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/demoParking.txt", "w")
                f.write(str(spaceCounter))
                f.close()
            except Exception:
                pass                     
            self.setSpaceCounter(spaceCounter)
        
    def cameraStream(self):
        if self.checkfeed == 1:
            while self.streamdone:       
                self.buffer += self.cap.read(2560)
                head = self.buffer.find(b'\xff\xd8')
                end = self.buffer.find(b'\xff\xd9')
                try:
                    if head > -1 and end > -1:
                        jpg = self.buffer[head:end+2]
                        self.buffer = self.buffer[end+2:]
                        frame = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED)
                        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                        frame = rescaleFrame(frame, 0.5)
                        self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                        self.feedCanvas.create_image(5, 0, image = self.photo, anchor = NW)
                        break
                except Exception:
                    break
            self.feedCanvas.after(1, self.cameraStream)
        
    def getReadings(self):
        while self.done:
            self.readingsLabel.config(text = f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            self.readingsLabel.place(x = self.__midpointAcross - int(self.readingsLabel.winfo_reqwidth() / 2), y = 40)
            if not self.done:
                break
    
    def settingSpots(self):       
        newsize = (550, 360)
        self.im1 = self.im.resize(newsize, Image.Resampling.LANCZOS)
        
        self.tk_im = ImageTk.PhotoImage(self.im1)
        self.editCanvas.create_image(5, 5, anchor = "nw", image = self.tk_im)

    def drawRectangles(self, posList):
        if len(posList) > 0:
            for pos in posList:
                self.editCanvas.create_rectangle(pos[0], pos[1], pos[0] + self.getWidth(), pos[1] + self.getHeight(), outline='blue', tags = 'rect')
    
    def leftClick(self, event):
        self.posList.append((event.x, event.y)) if (event.x, event.y) not in self.posList else self.posList
            
    def rightClick(self, event):
        self.editCanvas.delete("rect")
        for i, pos in enumerate(self.posList):
            if pos[0] < event.x < pos[0] + self.getWidth() and pos[1] < event.y < pos[1] + self.getHeight():                
                self.posList.pop(i) 
                self.__lotNames.pop(pos)
    
    def closeVideo(self):
        try:
            f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/Monitor/ParkingLots/ParkingLot1/ParkingLot11.txt", "w")
            for x, y in self.__lotNames.items():
                f.write(f'#{y}\n')
            f.close()
        except Exception:
            pass
        try:
            self.cap.release()
        except Exception:
            pass
        try:
            self.cap.close()
        except Exception:
            pass
        try:
            cv.destroyAllWindows()
        except Exception:
            pass
        try:
            self.feedLabel.destroy()
        except Exception:
            pass
        try:
            self.editCanvas.destroy()
        except Exception:
            pass        
        try:
            self.feedCanvas.destroy()
        except Exception:
            pass        
        self.done = False
        self.streamdone = False
        self.buffer = b''
        self.createFeedCanvas()
        self.createEditCanvas()
      
    @staticmethod  
    def closeAll(self,master):
        try:
            with open('C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CarParkPos', 'wb') as f:
                pkl.dump(self.posList, f)
        except Exception:
            print("Error")
        self.done = False
        try:
            self.closeVideo()
        except Exception:
            pass
        try:
            f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/spotNames.txt", "w")
            for x, y in self.__lotNames.items():
                f.write(f'{x}#{y}\n')
            f.close()
        except Exception:
            pass
        try:
            f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/Monitor/ParkingLots/ParkingLot1/ParkingLot11.txt", "w")
            for x, y in self.__lotNames.items():
                f.write(f'#{y}\n')
            f.close()
        except Exception:
            pass
        print(self.__feed)
                         
class ViewWindow(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        from typesOfView import SingleView, DoubleView, QuadView
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.singleViewButton_bool, self.doubleViewButton_bool, self.quadViewButton_bool = True, True, True
        
        self.listOfFeeds = sources
        self.listLength = len(self.listOfFeeds)
        
        if self.listLength == 0:
            self.singleViewButton_bool, self.doubleViewButton_bool, self.quadViewButton_bool = False, False, False
        if self.listLength == 1:
            self.doubleViewButton_bool, self.quadViewButton_bool = False, False
        if self.listLength == 2:
            self.quadViewButton_bool = False
        
        self.sideFrame = Frame(self, highlightthickness = 0, bd = 1,  relief = "flat", border = 1,  width = 155, height = self.__window_length,)
        self.sideFrame.place(x = 1050, y = 0,)
        
        self.containerFrame = Frame(self, highlightthickness = 0, bd = 2,  relief = "flat", border=0, bg="lightgrey")
        self.containerFrame.place(x = 0, y = 0, width = self.__window_bredth - self.sideFrame.winfo_reqwidth(), height = self.__window_length,)
        
        #frame for main window
        mainFrame = Frame(self.containerFrame, highlightthickness = 0, bd = 0, relief = "flat", width = self.__window_bredth - self.sideFrame.winfo_reqwidth(), height = self.__window_length,)
        mainFrame.pack(side="top", fill="both", expand=True)
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)
         
        self.listOfViewFrames = {}
        
        for classes in (SingleView, DoubleView, QuadView):
            theframe = classes(parent = mainFrame, master = self, feeds = self.listOfFeeds)
            self.listOfViewFrames[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
            
        # Side Frame Label and Buttons ---------------------------------------------------------------------------------
        self.sideLabel = Label(self.sideFrame, text = "Viewing Options", font = ('calibri', 15, 'underline'), justify = "center", )
        self.sideLabel.place(x = 0, y = 0, width = self.sideFrame.winfo_reqwidth(), height = 40)
        
        self.singleViewButton = Button(self.sideFrame, text = "Single", font = ('calibri', 18), fg = "black", bd= 0,highlightthickness = 0, border = 1, command=lambda: self.show_frame(SingleView))
        self.singleViewButton.place(x = 0, y = 40, width = self.sideFrame.winfo_reqwidth(), height = 210)
        if not self.singleViewButton_bool:
            self.singleViewButton.config(state = "disabled")
        
        self.doubleViewButton = Button(self.sideFrame, text = "Double", font = ('calibri', 18), fg = "black", bd= 0,highlightthickness = 0, border = 1, command=lambda: self.show_frame(DoubleView))
        self.doubleViewButton.place(x = 0, y = 250, width = self.sideFrame.winfo_reqwidth(), height = 210)
        if not self.doubleViewButton_bool:
            self.doubleViewButton.config(state = "disabled")
        
        self.quadViewButton = Button(self.sideFrame, text = "Quad", font = ('calibri', 18), fg = "black", bd= 0,highlightthickness = 0, border = 1, command=lambda: self.show_frame(QuadView))
        self.quadViewButton.place(x = 0, y = 460, width = self.sideFrame.winfo_reqwidth(), height = 210)
        if not self.quadViewButton_bool:
            self.quadViewButton.config(state = "disabled")
        #----------------------------------------------------------------------------------------------------------------
        self.show_frame(SingleView)
    
    def show_frame(self, anotherClass):
        frame = self.listOfViewFrames[anotherClass]
        frame.tkraise()
                
class AddFeed(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        from editFeedOptions import addFeed, editFeed, deleteFeed
        self.config(bg="grey")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        self.tabs = Frame(self, highlightthickness = 0, bd = 1,  relief = "flat", border = 1,  width = self.__window_bredth, height = 64, bg = "lightgray")
        self.tabs.place(x = 0, y = 0,)
        
        self.tab_1 = Button(self.tabs, text = "Tab 1", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1,)
        self.tab_1.place(x = 0, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_2 = Button(self.tabs, text = "Tab 2", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1,)
        self.tab_2.place(x = int(self.tabs.winfo_reqwidth() / 3), y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_3 = Button(self.tabs, text = "Tab 3", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1,)
        self.tab_3.place(x = int(self.tabs.winfo_reqwidth() / 3) * 2, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 2)
        
        self.containerFrame = Frame(self, highlightthickness = 0, bd = 2,  relief = "flat", border=0,)
        self.containerFrame.place(x = 0, y = self.tabs.winfo_reqheight(), width = self.__window_bredth, height = self.__window_length - self.tabs.winfo_reqheight(),)
        #frame for main window
        mainFrame = Frame(self.containerFrame, highlightthickness = 0, bd = 0, relief = "flat", width = self.__window_bredth, height = self.__window_length - self.tabs.winfo_reqheight(), bg="lightblue")
        mainFrame.pack(side="top", fill="both", expand=True)
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)
        
        self.listOfFeeds = files.sources
        self.listOfParishes = files.parishes
        self.titles = files.titles
        
        self.listOfViewFrames = {}
        
        for classes in (addFeed, editFeed, deleteFeed):
            theframe = classes(parent = mainFrame, master = self, sources = self.listOfFeeds,)
            self.listOfViewFrames[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
        
        self.tab_1 = Button(self.tabs, text = "Add Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, command = lambda: self.show_frame(addFeed,1))
        self.tab_1.place(x = 0, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_2 = Button(self.tabs, text = "Edit Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, command = lambda: self.show_frame(editFeed,2))
        self.tab_2.place(x = int(self.tabs.winfo_reqwidth() / 3), y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_3 = Button(self.tabs, text = "Delete Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0,  command = lambda: self.show_frame(deleteFeed,3), state = "disabled")
        self.tab_3.place(x = int(self.tabs.winfo_reqwidth() / 3) * 2, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.show_frame(addFeed,1)        
    
    def show_frame(self, anotherClass, whichButtonToLower):
        frame = self.listOfViewFrames[anotherClass]
        frame.tkraise()
        if whichButtonToLower == 1:
            self.tab_1.config(border=0)
            self.tab_2.config(border=2)
            self.tab_3.config(border=2)
        elif whichButtonToLower == 2:
            self.tab_1.config(border=2)
            self.tab_2.config(border=0)
            self.tab_3.config(border=2)
        else:
            self.tab_1.config(border=2)
            self.tab_2.config(border=2)
            self.tab_3.config(border=0)
 
class ViewMap(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        import openrouteservice as ors
        self.client = ors.Client(key='5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.entryDefaultText = "                          search"
        self.entryDefaultTextColour = "lightgray"
        self.has_defaultText = False
        self.hasRoute = False
        self.entry_width = 240
        self.searchFrame_width = 320
        self.searchFrame_height = 34
        self.locationService = Nominatim(user_agent="Geopy Library")
        self.distanceService = Nominatim(user_agent="geoapiExercises")
        self.__weight_constant = 0.0001
        self.locations = []
        self.getLocations()
        self.setInOrder()
        #self.showLocations()
        #self.toGetDistanceExample()
                
    def toGetDistanceExample(self):
        Input_place1 = "May Pen"
        Input_place2 = "Kingston"

        # Get location of the input strings
        place1 = self.locationService.geocode(Input_place1)
        place2 = self.locationService.geocode(Input_place2)

        # Get latitude and longitude
        Loc1_lat, Loc1_lon = (place1.latitude), (place1.longitude)
        Loc2_lat, Loc2_lon = (place2.latitude), (place2.longitude)

        location1 = (Loc1_lat, Loc1_lon)
        location2 = (Loc2_lat, Loc2_lon)

        # display the distance
        print(distance.distance(location1, location2).km, " kms")
    
    def showLocations(self):
        from parkingLots import _parkingLots
        
        for x, y in _parkingLots.items():
            #print(x, y)
            self.map_widget.set_marker(y[0], y[1], text = x, text_color = "black")
        
    def getLocations(self):
        with open(files.places_in_Jamaica) as f:
            for line in f:
                if len(line) > 0:
                    if line not in self.locations:
                        self.locations.append(str(line.strip()))
    
    #this function is called to create a canvas to display the map on
    def setInOrder(self, location = None):
        self.mapCanvas = Canvas(self, bg = "red")
        self.mapCanvas.place(x = 1, y = 1, width = self.__window_bredth - 2, height = self.__window_length - 2,)
        self.createMap(location)
        self.createSearch()
    
    #this function creates the map on the canvas using 'TkinterMapView'  
    def createMap(self, location = None):   
        self.map_widget = TkinterMapView(self.mapCanvas, width = self.__window_bredth - 2, height = self.__window_length - 2, corner_radius=2)
        self.map_widget.place(x = 1, y = 1,)        
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22)  # google normal
        #if location is None:
        self.map_widget.set_position(18.1489364, -77.3290934, marker = False) #18.007943,-76.781315
        #else:
        #    self.map_widget.set_position(location.latitude, location.longitude, marker = True)
        #    self.map_widget.set_marker(location.latitude, location.longitude, text = location.address, text_color = "black")
        self.map_widget.set_zoom(9)
        self.clearRoute = Button(self.mapCanvas, text = "X", font = ('bold', 15), relief = "flat", bg = "#ffffff", activebackground = "#ffffff", bd= 0, highlightthickness = 0, border = 0)#, command = lambda : self.clearToEntry(), )
    
    #this function creates the default widgets needed to navigate the map    
    def createSearch(self):
        #creates a frame for search widgets
        self.searchFrame = Canvas(self.mapCanvas, width = self.searchFrame_width, height = self.searchFrame_height, bg = "#ffffff", bd = 0, borderwidth = 0, highlightthickness = 0)
        self.searchFrame.place(x = self.__midpointAcross - (self.searchFrame_width / 2), y = 20,)
        #creates a black rectange around frame
        self.searchFrame.create_rectangle(0,0,self.searchFrame_width-1,self.searchFrame_height-1,outline = "lightgray", width = 1, tags="rectangle")
        #creates an expand button that will be toggled for 'search a location' or 'map from - to'
        self.expandButton = Button(self.searchFrame, text = ">", font = ('calibri', 13, 'bold'), relief = "flat", bg = "lightgray", activebackground = "lightgray", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.expandEntry(), )
        self.expandButton.place(x = 1 , y = 1, width = 20, height = 32)
        #creates an Entry to input search data
        self.findLocation = Entry(self.searchFrame, bd = 0, bg = "#ffffff", font = ('bold',10), relief = "flat", highlightthickness = 0, border = 0, insertontime = 0)# foreground = self.entryDefaultTextColour)
        #self.has_defaultText = True
        #self.findLocation.icursor(0)
        self.findLocation.place(x = 25, y = 1, width = self.entry_width - 1, height = 32)
        #self.findLocation.bind('<FocusIn>', self.click_In)        
        #self.findLocation.insert(0,self.entryDefaultText)
        #creates a button to clear the data entered in the Entry
        self.clearButton = Button(self.searchFrame, text = "x", relief = "flat", bg = "#ffffff", activebackground = "#ffffff", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.clearEntry(), )
        self.clearButton.place(x = self.entry_width + 24 , y = 1, width = 20, height = 32)
        #creates a search button to search for the data entered into the Entry
        self.searchButton = Button(self.searchFrame, text = "find", relief = "flat", bg = "lightgray", activebackground = "lightgray", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.searchMap())
        self.searchButton.place(x = self.searchFrame_width - 36, y = 1, width = 35, height = 32)        
        #create a "search" label
        self.searchlabel = Label(self.searchFrame, text = "search", font = ('calibri', 8), bg = "#ffffff", fg = "lightgray")
        self.searchlabel.place(x = self.searchFrame_width / 2 - self.searchlabel.winfo_reqwidth(), y = 1, height = 8)
    
    #this function is called if the expand button is pressed. it changes the search widget into a 'from-to' widget
    def expandEntry(self):
        #expand search canvas and draw new rectange
        self.searchFrame.config(height = self.searchFrame_height * 2)
        self.searchFrame.create_rectangle(0,self.searchFrame_height-1,self.searchFrame_width-1,(self.searchFrame_height*2)-1,outline = "lightgray", width = 1, tags="expand")
        #expand height of expand button, and change text and command
        self.expandButton.config(text = "^", command = lambda : self.reduceEntry(),)        
        self.expandButton.place(x = 1 , y = 1, width = 20, height = (32 * 2) + 2)
        #create new entry for "to" position
        self.findToLocation = Entry(self.searchFrame, bd = 0, bg = "#ffffff", font = ('bold',10), relief = "flat", highlightthickness = 0, border = 0,)# foreground = self.entryDefaultTextColour)
        self.findToLocation.place(x = 25, y = 1 + self.searchFrame_height, width = self.entry_width - 1, height = 32)
        #create new clear button
        self.clearButton2 = Button(self.searchFrame, text = "x", relief = "flat", bg = "#ffffff", activebackground = "#ffffff", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.clearToEntry(), )
        self.clearButton2.place(x = self.entry_width + 24 , y = 1 + self.searchFrame_height, width = 20, height = 32)
        #expand height of search button, and configure text and command
        self.searchButton.config(text = "route", command = lambda : self.mapRoute() ) 
        self.searchButton.place(x = self.searchFrame_width - 36, y = 1, width = 35, height = (32 * 2) + 2)
        #destroy "search" label
        self.searchlabel.destroy()
        #create a "from" label
        self.fromlabel = Label(self.searchFrame, text = "from", font = ('calibri', 8), bg = "#ffffff", fg = "lightgray")
        self.fromlabel.place(x = self.searchFrame_width / 2 - self.fromlabel.winfo_reqwidth(), y = 1, height = 8)
        #create a "to" label
        self.tolabel = Label(self.searchFrame, text = "to   ", font = ('calibri', 8), bg = "#ffffff", fg = "lightgray")
        self.tolabel.place(x = self.searchFrame_width / 2 - self.tolabel.winfo_reqwidth(), y = 1 + self.searchFrame_height, height = 8)
        #self.searchFrame.create_line(0,self.searchFrame_height-10,self.searchFrame_width-1,self.searchFrame_height-10, activefill="red", width = 2, tags="expand")
        
    def mapRoute(self):
        #if the route bool is false, then there is no active routes
        if not self.hasRoute:
            #if there is data in the entry
            if len(self.findLocation.get().strip()) != 0:
                #tries to create a location variable based off the info given
                start_location = self.checkLocation(self.findLocation.get())
                start = self.locationService.geocode(start_location) #self.findToLocation.delete(0, END)
                #if the start variable is created sucessfully,
                if start:
                    #if there is data in the 2nd entry
                    if len(self.findToLocation.get().strip()) != 0:
                        #tries to create an end variable based off the info given
                        end_location = self.checkLocation(self.findToLocation.get())
                        end = self.locationService.geocode(end_location)
                        #if the end variable is created sucessfully,
                        if end:
                            button = 50
                            #creates a marker on the map to the start of the route
                            self.map_widget.set_marker(start.latitude, start.longitude, text = start.address, text_color = "green")
                            #creates a marker on the map to the end of the route
                            self.map_widget.set_marker(end.latitude, end.longitude, text = end.address, text_color = "red")
                            #place clear route button on screen
                            self.clearRoute.place(x = self.__window_bredth - button - 20 , y = self.__window_length - button - 20, width = button, height = button)
                            #send the start and end variable to another function for routing
                            self.getRoute(start, end)
                        #clears both entries 
                        else:
                            self.findLocation.delete(0, END)
                            self.findToLocation.delete(0, END)
                #clears both entries 
                else:
                    self.findLocation.delete(0, END)
                    self.findToLocation.delete(0, END)
    
    def checkLocation(self, location):
        if location in self.locations or location.capitalize() in self.locations or location.title() in self.locations:
            return f"{location}, Jamaica"
        else:
            return location
                          
    def getRoute(self, start, end):
        #sets bools value to true to ensure 'route' button is inactive
        self.hasRoute = True
        #sets starting and ending coordinates
        coords = [[start.longitude , start.latitude],[end.longitude, end.latitude]]
        #sets parameters for the routing of the trip
        route = self.client.directions(coordinates = coords, profile = 'driving-car', format = 'geojson',)
        #adds the coordiantes to a list of tuples
        route_coordinates = [tuple(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
        #adds the starting point to the beginning of the list
        route_coordinates.insert(0,(start.latitude, start.longitude))
        #adds the ending point to the end of the list
        route_coordinates.insert(len(route_coordinates),(end.latitude, end.longitude))
        #gets the middle coordinate from the list (middle of the route)
        middle = route_coordinates[int(len(route_coordinates)/2)]
        #sets the map middle position to the middle of the route
        self.map_widget.set_position(middle[0], middle[1], marker = False)
        print(len(route_coordinates))
        #creates the path from the starting point to the ending point
        path_1 = self.map_widget.set_path(route_coordinates)
        #if the length of the coordinates list is a certain amount, zoom a certain amount out/in
        if len(route_coordinates) > 38:
            self.map_widget.set_zoom(10)
            
        ###
        # With self.map_widget.delete_all_path() all path on the map will be deleted.
        ###
    
    def searchMap(self):
        #if there is data in the entry
        if len(self.findLocation.get().strip()) != 0:
            #dd
            the_location = self.checkLocation(self.findLocation.get())
            print(the_location)
            #tries to create a location variable based off the info given
            location = self.locationService.geocode(the_location)
            #if the variable is created sucessfully,
            if location:
            #    self.mapCanvas.destroy() 
            #    self.setInOrder(location)
                #sets the map middle position to the variable
                self.map_widget.set_position(location.latitude, location.longitude, marker = True)
                #creates a marker at the map middle position to the middle of the route
                self.map_widget.set_marker(location.latitude, location.longitude, text = location.address, text_color = "black")
                #sets the zoom
                self.map_widget.set_zoom(14)
                print(location.address)
                print(f"long: {location.longitude}, lat: {location.latitude}")
            #if the variable is not created sucessfully,
            else:
                #clears the entry of unwanted/bad/incorrect information
                self.findLocation.delete(0, END)
    
    def reduceEntry(self):
        #resets route bool
        self.hasRoute = False
        #reduce search canvas and delete new rectange
        self.searchFrame.config(height = self.searchFrame_height)
        self.searchFrame.delete("expand")
        #reduce height of expand button, and change text and command
        self.expandButton.config(text = ">", command = lambda : self.expandEntry(),)        
        self.expandButton.place(x = 1 , y = 1, width = 20, height = 32)
        #destroy new entry for "to" position
        self.findToLocation.destroy()
        #destroy new clear button
        self.clearButton2.destroy()
        #reduce height of search button, and configure text and command
        self.searchButton.config(text = "find", command = lambda : self.searchMap())
        self.searchButton.place(x = self.searchFrame_width - 36, y = 1, width = 35, height = 32)
        #destroy "from" label
        self.fromlabel.destroy()
        #destroy "to" label
        self.tolabel.destroy()
        #recreate a "search" label
        self.searchlabel = Label(self.searchFrame, text = "search", font = ('calibri', 8), bg = "#ffffff", fg = "lightgray")
        self.searchlabel.place(x = self.searchFrame_width / 2 - self.searchlabel.winfo_reqwidth(), y = 1, height = 8)
        
    def clearEntry(self):
        self.hasRoute = False
        self.findLocation.delete(0, END)
        self.map_widget.set_zoom(9)
        #self.reset_ToDefault()
        
    def clearToEntry(self):
        self.hasRoute = False
        self.findToLocation.delete(0, END)
    
    def reset_ToDefault(self):
        self.has_defaultText = True
        self.findLocation.configure(foreground = self.entryDefaultTextColour)
        self.findLocation.insert(0, self.entryDefaultText)
        self.findLocation.icursor(0)
        
    def click_In(self, event):
        if self.findLocation.get() == self.entryDefaultText:
            print("YES")
            self.has_defaultText = False
            self.findLocation.delete(0, END)
            self.findLocation.configure(foreground = "black")
            #self.findLocation.icursor(0)
            self.findLocation.bind('<FocusOut>', self.click_Out)
            
    def click_Out(self, event):
        if len(self.findLocation.get()) < 5 and not self.has_defaultText:
            print("EMPTY")
            self.reset_ToDefault()
            
class Settings(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        label = Label(self, text="Settings", fg="white")
        label.place(x = (parent.winfo_reqwidth() / 2) - int(label.winfo_reqwidth() / 2), 
                    y = (parent.winfo_reqheight() / 2) - int(label.winfo_reqheight() / 2))
        label.place(x = 800, y = 200)
        
App("Kareem")

"""
Boeing, G. (2024). Modeling and Analyzing Urban Networks and Amenities with OSMnx. Working paper.
https://geoffboeing.com/publications/osmnx-paper/
"""