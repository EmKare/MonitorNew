from tkinter import Tk, Label, Button, Menu, Toplevel, PhotoImage, font, LabelFrame, Canvas, NW
from urllib.request import urlopen
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from utils import rescaleFrame
import threading as th
import files as files
import pickle as pkl
import cvzone as cz
import numpy as np
import cv2 as cv
#import time

class ParkingMonitoringApp(Tk):
    def __init__(self, username, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.__window_bredth, self.__window_length = 1200, 760
        self.__window_midpoint = int(self.__window_bredth / 2)
        #self.config(bg="white")
        
        #setting up the window
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+150+0")
        self.resizable(False, False)
        self.title(f"Find Me Parking App - User: {username}")
        
        #Variables
        self.done = True
        self.__space, self.__total = 0, 0, 
        self.__feed = 2
        self.__width, self.__height = 53, 22
        self.buffer = b''
        self.checkfeed = 0
        self.__lotNames = {}
        self.availableSpots = []
        self.__listOfFeeds = ["MegaMart Parking Lot #1", "Sagicor Life Building Parking Lot", "NewLife Mall #3 Parking Lot"]
        
        #Get positions
        self.posList = self.getFileSetArray()
        """
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 0, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 100, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 200, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 300, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 400, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 500, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='green').place(x = 600, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 700, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 800, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 900, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1000, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1100, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1200, y = 60)
        """
        #------------------------------------------------------------------------------------------------------------------------
        
        self.bigLabel = Label(self, text = 'Find Me Parking Surveillance Monitor', font = ('bold', 30))
        self.bigLabel.place(x = self.__window_midpoint - int(self.bigLabel.winfo_reqwidth() / 2), 
                            y = 10)
        
        #Name of Parking Lot being monitored
        self.parkingLotNameLabel = Label(self, text = '-------------------------------', font = ('bold', 12), bg = "black", fg = "white")
        self.parkingLotNameLabel.place(x = self.__window_midpoint - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), 
                                       y = 80)
                
        #label showing parking spot readings from footage
        self.readingsLabel = Label(self, text = '-------------------------------', font = ('bold', 12), bg = "black", fg = "white") 
        self.readingsLabel.place(x = self.__window_midpoint - int(self.readingsLabel.winfo_reqwidth() / 2),
                                 y = 110)
        
        #group label
        self.groupLabel = Label(self, text = 'Capstone Group 3', font = ('bold', 5), fg = 'blue', justify='right')
        self.groupLabel.place(x = 1130, y = 745)
        
        #------------------------------------------------------------------------------------------------------------------------
        
        #labelframe for combobox 
        self.comboBoxLabelFrame = LabelFrame(self, text = "  Select Feed  ", font = ('bold', 12), pady = 20, width = 565, height = 140)
        self.comboBoxLabelFrame.place(x = 20, y = 170)
        
        #labelframe for buttons
        self.buttonsLabelFrame = LabelFrame(self, text = "  Options  ", font = ('bold', 12), pady = 10, width = 565, height = 140)
        self.buttonsLabelFrame.place(x = 615, y = 170)
        
        #labelframe for video feed label
        self.feedLabelFrame = LabelFrame(self, text = "  Video Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400)
        self.feedLabelFrame.place(x = 20, y = 340)
        
        #labelframe for edit footage panel label
        self.editLabelFrame = LabelFrame(self, text = "  Edit Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400, )
        self.editLabelFrame.place(x = 615, y = 340)
        
        #------------------------------------------------------------------------------------------------------------------------
        
        #---BUTTONS---
        #start video feed
        self.startFeedButton = Button(self.buttonsLabelFrame, text = "Start Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.checker())
        self.startFeedButton.place(x = 30, y = 0)
        #stop video feed
        self.endFeedButton = Button(self.buttonsLabelFrame, text = "Stop Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.closer())
        self.endFeedButton.place(x = 210, y = 0)
        #Exit program
        self.exitButton = Button(self.buttonsLabelFrame, text = "Log Out", font = ('bold', 10), width = 15, height = 5, fg = "black", bg = "red", command = lambda: self.closeAll())
        self.exitButton.place(x = 390, y = 0)
        
        #Create ComboBox
        self.optionsComboBox = Combobox(self.comboBoxLabelFrame, width = 40, font = ('bold', 10))
        self.optionsComboBox['values'] = [x for x in self.__listOfFeeds]
        self.optionsComboBox.current(2)
        self.optionsComboBox.config(font = "None 16 normal")
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 15))
        self.optionsComboBox.place(x = 34, y = 10)
        self.optionsComboBox.bind("<<ComboboxSelected>>", self.option_selected)
        
        #canvas for edit footage panel
        self.createEditCanvas()

        #Create a Menu  
        self.menubar = Menu(self)
        self.createMenuBar(self.menubar)
        
        #starts tkinter
        self.mainloop()
        
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
        self.filemenu.add_command(label = "Exit", command = lambda : self.closeAll())
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
        self.feedLabel = Label(self.feedLabelFrame, pady = 10,)
        self.feedLabel.configure(image = PhotoImage(width = 550, height = 360))
        self.feedLabel.place(x = 3, y = 0)
        
    def createFeedCanvas(self):
        width, height = 555, 365
        self.feedCanvas = Canvas(self.feedLabelFrame, width = width, height = height)
        self.feedCanvas.place(x = 0, y = 0)#grid(row = 0, column = 0, padx = 10, pady = 10)
    
    def createEditCanvas(self):
        width, height = 555, 365 #width = 555, height = 370
        self.editCanvas = Canvas(self.editLabelFrame,  cursor="tcross", width = width, height = height,)
        self.editCanvas.create_text(int(width / 2), int(height / 2), text = "awaiting feed...", font = ('bold', 20), anchor = "center", tags = 'text')
        self.editCanvas.place(x = 0, y = 0)#grid(row = 0, column = 0, padx = 10, pady = 10)
        self.editCanvas.bind("<ButtonPress-1>", self.leftClick)
        self.editCanvas.bind("<ButtonPress-3>", self.rightClick)
        #self.editCanvas.bind("<ButtonRelease-1>", self.on_button_release)
        
    def option_selected(self, event):
        self.parkingLotNameLabel.config(text=self.optionsComboBox.get())
        self.setFeed(self.optionsComboBox.current())
        x = int(self.parkingLotNameLabel.winfo_reqwidth() / 2)
        self.parkingLotNameLabel.place(x = self.__window_midpoint - x, y = 80)
        self.readingsLabel.config(text = '-------------------------------')
        
    def popUpWindow(self):
        popUp = Toplevel(self)
        button = Button(popUp, text="Click To Close", command = lambda : popUp.destroy())
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
        self.cap = None
        self.parkingLotNameLabel.config(text = self.optionsComboBox.get())
        self.parkingLotNameLabel.place(x = self.__window_midpoint - int(self.parkingLotNameLabel.winfo_reqwidth() / 2), y = 80)
        
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
                    colour = (0, 255, 0) #available
                    thickness = 2
                    spaceCounter += 1
                    status = "A"
                    
                else:
                    colour = (0, 0, 255) #unavailable
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
                
                #if status == "A":
                    #if spot not in self.availableSpots:
                    #croppedImage = self.im1.crop((x, y, x + self.getWidth(), y + self.getHeight())) 
                    #croppedImage.save(f"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CroppedLots/{spot}.png") 
                self.__lotNames.update({pos:spotName})
            #cz.putTextRect(img, f'Available Space: {spaceCounter}/{len(self.posList)}', (25, 25), scale = 1, thickness = 2, offset = 1, colorR = (0, 0, 0))

    def writeSpaceCounter(self, spaceCounter):
        if spaceCounter is not self.getSpaceCounter():            
            try:
                f = open("C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/demoParking.txt", "w")
                f.write(str(spaceCounter))
                f.close()
            except Exception:
                #pass
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
                        frame = rescaleFrame(frame, 0.5)
                        self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                        self.feedCanvas.create_image(5, 0, image = self.photo, anchor = NW)
                        break
                except Exception:
                    break
            self.feedCanvas.after(1, self.cameraStream)
    
    def liveView(self):
        _, frame = self.cap.read() #feedLabelFrame
        if _:
            frame = rescaleFrame(frame, 0.8)
            cvImage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            img = Image.fromarray(cvImage)
            imgtk = ImageTk.PhotoImage(image = img)
            self.feedLabel = Label(self.feedLabelFrame, pady = 10)
            self.feedLabel.imgtk = imgtk
            self.feedLabel.configure(image = self.feedLabel.imgtk)
            self.feedLabel.after(1, self.liveView) 
        
    def getReadings(self):
        #time.sleep(1)
        while self.done:
            self.readingsLabel.config(text = f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            #print(f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            #time.sleep(3)
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
        from Login import Login
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

        self.destroy()
        Login()
                   
if __name__ == "__main__":
    ParkingMonitoringApp("Kareem")