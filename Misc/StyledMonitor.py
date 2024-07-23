
from tkinter import Label, Menu, Toplevel, Canvas, NW
from urllib.request import urlopen
from utils import rescaleFrame
from PIL import Image, ImageTk
import customtkinter as ctk
import threading as th
import pickle as pkl
import cvzone as cz
import numpy as np
import cv2 as cv
import time

logo = "C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/FindMeParking.png"
video_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4"
image_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/trial/carParkImg.png"
local_cam = "http://192.168.1.9:81/stream"
#local_cam = "https://f163-2409-8a55-3a12-46c0-3b13-c09a-136-568d.ngrok-free.app/stream"
local_stream = "http://192.168.1.10:81/stream" 
#local_stream = "https://d02f-2409-8a55-3a12-46c0-3b13-c09a-136-568d.ngrok-free.app/stream"


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ParkingApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__window_bredth, self.__window_length = 1200, 780
        self.__window_midpoint = int(self.__window_bredth / 2)
        self.__window_fourth = int(self.__window_midpoint / 4)
        self.__window_old_midpoint = self.__window_midpoint + self.__window_fourth
        
        #setting up the window
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+{150}+{0}")
        self.resizable(False, False)
        self.title("Find Me Parking App")
        
        #Variables
        self.done = True
        self.__space, self.__total = 0, 0, 
        self.__feed = 2
        self.__width, self.__height = 53, 22
        self.buffer = b''
        self.checkfeed = 0
        self.__listOfFeeds = ["MegaMart Parking Lot #1", "Sagicor Life Building Parking Lot", "NewLife Mall #3 Parking Lot"]
        
        #Get positions
        self.posList = self.getFileSetArray()
        
        #Name of Parking Lot being monitored
        self.titleFrame = ctk.CTkFrame(self, width = self.__window_bredth - 20, height = 150)
        self.titleFrame.place(x = 10, y = 5)
        
        self.logo_image = ctk.CTkImage(light_image = Image.open(logo), size = (260, 130))
        self.logo_label = ctk.CTkLabel(self.titleFrame, image = self.logo_image, text = "",corner_radius = 20)
        self.logo_label.place(x = 100, y = 10)
        
        self.bigLabel = ctk.CTkLabel(self.titleFrame, text = 'Find Me Parking Surveillance Monitor', font = ('bold', 40), anchor = "center")
        self.bigLabel.place(x = 400, y = 50)
        # DROPDOWN ELEMENTS ----------------------------------------------------------------------------------------------
        self.dropdownFrame = ctk.CTkFrame(self, width = 390, height = 140)
        self.dropdownFrame.place(x = 10, y = 170)

        self.dropdownFrameTitle = ctk.CTkLabel(self.dropdownFrame, text="Select Feed", font = ctk.CTkFont(size = 20, weight = "bold"))
        self.dropdownFrameTitle.place(x = 3, y = 0)
        
        self.selectFeedMenu = ctk.CTkOptionMenu(self.dropdownFrame, values = self.__listOfFeeds, font = ctk.CTkFont(size = 22, weight = "bold"), dropdown_font= ctk.CTkFont(size = 20, weight = "bold"), width = 375, height = 30, dynamic_resizing = False, command = self.option_selected)
        self.selectFeedMenu.set(self.__listOfFeeds[2])
        self.selectFeedMenu.place(x = 5, y = 55)
        # READINGS ------------------------------------------------------------------------------------------------------
        self.readingsFrame = ctk.CTkFrame(self, width = 390, height = 140,)
        self.readingsFrame.place(x = 405, y = 170)
        
        self.readingsFrameTitle = ctk.CTkLabel(self.readingsFrame, text="Location", font = ctk.CTkFont(size=20, weight="bold"))
        self.readingsFrameTitle.place(x = 3, y = 0)
        
        #Name of Parking Lot being monitored
        self.parkingLotNameLabel = Label(self, text = '-------ABC------------------------', font = ('bold', 16), bg = "black", fg = "white")
        self.parkingLotNameLabel.place(x = self.__window_old_midpoint - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), y = 270)
                
        #label showing parking spot readings from footage
        self.readingsLabel = Label(self, text = '-----------------------DEF--------', font = ('bold', 16), bg = "black", fg = "white")
        self.readingsLabel.place(x = self.__window_old_midpoint - int(self.readingsLabel.winfo_reqwidth() / 2), y = 330)
         
        #BUTTON ELEMENTS ------------------------------------------------------------------------------------------------
        self.optionsFrame = ctk.CTkFrame(self, width = 390, height = 140)
        self.optionsFrame.place(x = 800, y = 170)
        
        self.optionsFrameTitle = ctk.CTkLabel(self.optionsFrame, text="Options", font = ctk.CTkFont(size=20, weight="bold"))
        self.optionsFrameTitle.place(x = 3, y = 0)
        
        self.startFeedButton = ctk.CTkButton(self.optionsFrame, text = "Start Feed", font = ('bold', 15), text_color = "black", width = 110, height = 50, fg_color = "blue", command = lambda: self.checker())
        self.startFeedButton.place(x = 15, y = 55)
        #stop video feed
        self.endFeedButton = ctk.CTkButton(self.optionsFrame, text = "Stop Feed", font = ('bold', 15), text_color = "black", width = 110, height = 50, fg_color = "blue", command = lambda: self.closer())
        self.endFeedButton.place(x = 145, y = 55)
        #Exit program
        self.exitButton = ctk.CTkButton(self.optionsFrame, text = "EXIT", font = ('bold', 15), text_color = "black", width = 110, height = 50, fg_color = "red", hover_color="#9C3F2A", command = lambda: self.destroy())
        self.exitButton.place(x = 265, y = 55)
        
        # LIVE FEED ---------------------------------------------------------------------------------------------------------
        self.feedFrame = ctk.CTkFrame(self, width = self.__window_midpoint - 15, height = 430)
        self.feedFrame.place(x = 10, y = 320)
        
        self.feedFrameTitle = ctk.CTkLabel(self.feedFrame, text="View Feed", font = ctk.CTkFont(size=20, weight="bold"))
        self.feedFrameTitle.place(x = 3, y = 0)
        
        #self.createFeedCanvas()
        # EDITOR -----------------------------------------------------------------------------------------------------------
        self.editFrame = ctk.CTkFrame(self, width = self.__window_midpoint - 15, height = 430)
        self.editFrame.place(x = self.__window_midpoint + 5, y = 320)        
        
        self.editFrameTitle = ctk.CTkLabel(self.editFrame, text="Edit Feed", font = ctk.CTkFont(size=20, weight="bold"))
        self.editFrameTitle.place(x = 3, y = 0)        
        
        #canvas for edit footage panel
        self.createEditCanvas()
        
        #self.editor_image = ctk.CTkImage(light_image = Image.open(image_name), size = (555, 365))
        #self.editor_label = ctk.CTkLabel(self.editFrame, image = self.editor_image, text = "",corner_radius = 20)
        #self.editor_label.place(x = 0, y = 35)
        
        #----------------------------------------------------------------------------------------------------------------
        
        self.groupLabel = ctk.CTkLabel(self, text = 'Capstone Group 3', font = ('bold', 10))#, justify='right')
        self.groupLabel.place(x = 1105, y = 750)
        
        self.menubar = Menu(self)
        self.createMenuBar(self.menubar)
        self.config(menu = self.menubar)
        #self.createFeedLabel()
        
        self.mainloop()
        
    def setWidth(self, width):
        self.__width = width
        
    def getWidth(self):
        return self.__width
    
    def setHeight(self, height):
        self.__height = height
        
    def getHeight(self):
        return self.__height

    def setSpaceCounter(self, space):
        self.__space = space
        
    def getSpaceCounter(self):
        return self.__space
    
    def setTotalSpace(self, total):
        self.__total = total
        
    def getTotalSpace(self):
        return self.__total
    
    def setFeed(self, feedNumber):
        self.__feed = feedNumber
    
    def getFeed(self):
        return self.__feed
    
    def getFileSetArray(self):
        try:
            with open('C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CarParkPos', 'rb') as f:
                return pkl.load(f)
        except Exception:
            return []
        
    def createMenuBar(self, menubar):
        self.filemenu = Menu(menubar, tearoff = 0)
        self.filemenu.add_command(label = "New", command = self.popUpWindow)
        self.filemenu.add_command(label = "Open", command = self.popUpWindow)
        self.filemenu.add_command(label = "Save", command = self.popUpWindow)
        self.filemenu.add_command(label = "Save as...", command = self.popUpWindow)
        self.filemenu.add_command(label ="Close", command = self.popUpWindow)
        self.filemenu.add_separator() #--------------------------------------------
        self.filemenu.add_command(label = "Exit", command = self.quit)
        menubar.add_cascade(label = "File", menu = self.filemenu)
    
        self.editmenu = Menu(menubar, tearoff = 0)
        self.editmenu.add_command(label = "Undo", command = self.popUpWindow)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = "Cut", command = self.popUpWindow)
        self.editmenu.add_command(label = "Copy", command = self.popUpWindow)
        self.editmenu.add_command(label = "Paste", command = self.popUpWindow)
        self.editmenu.add_command(label = "Delete", command = self.popUpWindow)
        self.editmenu.add_command(label = "Select All", command = self.popUpWindow)
        menubar.add_cascade(label = "Edit", menu = self.editmenu)
    
        self.videomenu = Menu(menubar, tearoff = 0)
        for i in range(5):
            self.videomenu.add_command(label = f"Video-0{i}", command = self.popUpWindow)
        menubar.add_cascade(label = "Footage", menu = self.videomenu)
        
        self.helpmenu = Menu(menubar, tearoff = 0)
        self.helpmenu.add_command(label = "Help Index", command = self.popUpWindow)
        self.helpmenu.add_command(label = "About...", command = self.popUpWindow)
        menubar.add_cascade(label = "Help", menu = self.helpmenu)
        
        self.config(menu = menubar)
        
    def createFeedLabel(self):
        self.feedLabel = ctk.CTkLabel(self.feedFrame, pady = 10, text = "")
        #self.feedLabel.configure(image = PhotoImage(width = 550, height = 360))
        self.feedLabel.place(x = 13, y = 40)
        
    def createFeedCanvas(self):
        width, height = 565 + int(565/4), 375 + int(375/4)
        #col = self.feedFrame.cget("fg_color")
        self.feedCanvas = Canvas(self.feedFrame, width = width, height = height)#, highlightbackground = col[1], bg = col[1])
        self.feedCanvas.place(x = 10, y = 50)#grid(row = 0, column = 0, padx = 10, pady = 10)
        
    def createEditCanvas(self):
        width, height = 565 + int(565/4), 375 + int(375/4) #width = 555, height = 370
        col = self.editFrame.cget("fg_color")
        self.editCanvas = Canvas(self.editFrame,  cursor="tcross", width = width, height = height, highlightbackground = col[1], bg = col[1])        
        self.editCanvas.create_text(int(width / 2), int(height / 2), text = "awaiting feed...", font = ('bold', 20), anchor = "center", tags = 'text', fill=col[0])
        self.editCanvas.place(x = 13, y = 40)
        self.editCanvas.bind("<ButtonPress-1>", self.leftClick)
        self.editCanvas.bind("<ButtonPress-3>", self.rightClick)
        #self.editCanvas.bind("<ButtonRelease-1>", self.on_button_release))
        
    def option_selected(self, event):
        selected_option = self.selectFeedMenu.get()
        self.parkingLotNameLabel.config(text=selected_option)
        self.setFeed(self.__listOfFeeds.index(selected_option))
        self.parkingLotNameLabel.place(x = self.__window_old_midpoint - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), y = 270)
        
    def popUpWindow(self):
        popUp = Toplevel(self,pady = 4)
        button = ctk.CTkButton(popUp, text = "Click To Close", font = ('bold', 15), text_color = "black", width = 80, height = 30, fg_color = "blue", bg_color = "white", command = lambda : popUp.destroy())
        button.pack()         
    
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
        print(f'Feed {self.getFeed()}')
        
        self.cap = None
        
        if self.getFeed() == 0:
            self.streamdone = True
            self.cap = urlopen(local_cam)
            self.cameraStream()
        if self.getFeed() == 1:
            self.streamdone = True
            self.cap = urlopen(local_stream)
            self.cameraStream()
        if self.getFeed() == 2:
            try:
                self.feedCanvas.destroy()
            except Exception:
                pass
            self.createFeedLabel()
            self.cap = cv.VideoCapture(video_name)
            self.image = image_name 
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
            if self.cap.get(cv.CAP_PROP_POS_FRAMES) == self.cap.get(cv.CAP_PROP_FRAME_COUNT): #to loop video
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
                #imgtk = ImageTk.PhotoImage(image = img)
                imgtk = ctk.CTkImage(light_image = img, size = (555, 365))
                
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
                
                if count < 231:
                    colour = (0, 255, 0)
                    thickness = 2
                    spaceCounter += 1
                else:
                    colour = (0, 0, 255)
                    thickness = 1

                self.writeSpaceCounter(spaceCounter)                
                self.setTotalSpace(len(self.posList))
                
                cv.rectangle(img, (x, y), (x + self.getWidth(), y + self.getHeight()), colour, thickness)
                if i < 23:
                    cz.putTextRect(img, f"A{i}", (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                if i >= 23 and i < 45:
                    cz.putTextRect(img, f'B{i - 23}', (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
                if i >= 45 and i < 69:
                    cz.putTextRect(img, f'C{i - 45}', (x, y + self.getHeight() - 1), scale = 1, thickness = 1, offset = 0, colorR = colour, colorT = (0, 0, 0))
            #cz.putTextRect(img, f'Available Space: {spaceCounter}/{len(self.posList)}', (25, 25), scale = 1, thickness = 2, offset = 1, colorR = (0, 0, 0))

    def writeSpaceCounter(self, spaceCounter):
        if spaceCounter is not self.getSpaceCounter():            
            try:
                f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/demoParking.txt", "w")
                f.write(str(spaceCounter))
                f.close()
            except Exception:
                print("couldn't write to file")
                        
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
                        frame = rescaleFrame(frame, 0.6)
                        self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                        self.feedCanvas.create_image(0, 0, image = self.photo, anchor = NW)
                        break
                except Exception:
                    break

            self.feedCanvas.after(1, self.cameraStream)
            
    def getReadings(self):
        time.sleep(1)
        while self.done:
            self.readingsLabel.config(text = f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            #print(f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            time.sleep(3)
            if not self.done:
                print("Feed Stopped")
                break
    
    def settingSpots(self):           
        self.image = Image.open(self.image)
        
        newsize = (555 + int(555/4), 365 + int(365/4))
        
        self.resized_image = self.image.resize(newsize, Image.Resampling.LANCZOS)
        
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.editCanvas.create_image(5, 5, anchor = "nw", image = self.tk_image)

    def drawRectangles(self, posList):
        if len(posList) > 0:
            for pos in posList:
                self.editCanvas.create_rectangle(pos[0], pos[1], pos[0] + self.getWidth(), pos[1] + self.getHeight(), outline='blue', tags = 'rect')
    
    def leftClick(self, event):
        self.posList.append((event.x, event.y)) if (event.x, event.y) not in self.posList else self.posList
            
    def rightClick(self, event):
        print("Right")
        self.editCanvas.delete("rect")
        for i, pos in enumerate(self.posList):
            if pos[0] < event.x < pos[0] + self.getWidth() and pos[1] < event.y < pos[1] + self.getHeight():                
                self.posList.pop(i)
    
    def closeVideo(self):
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
        
    def closeAll(self):
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
        self.destroy()
        
ParkingApp()


"""    
    def liveView(self):
        _, frame = self.cap.read()
        if _:
            frame = rescaleFrame(frame, 0.8)
            cvImage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            img = Image.fromarray(cvImage)
            imgtk = ImageTk.PhotoImage(image = img)
            self.feedLabel.imgtk = imgtk
            self.feedLabel.configure(image = self.feedLabel.imgtk)
        self.after(1, self.liveView)     
    
        #self.image = image_name 
        #self.done = True        
        #th.Thread(target = self.runParkingApp).start() n
        #th.Thread(target = self.settingSpots).start()
        #th.Thread(target= self.getReadings, daemon=True).start()
        
"""