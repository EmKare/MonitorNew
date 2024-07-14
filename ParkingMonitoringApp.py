from tkinter import Tk, Label, Frame, Button, Menu, Toplevel, PhotoImage
from tkinter import IntVar, Radiobutton, LabelFrame, Canvas, W, EW, NW
from urllib.request import urlopen
from PIL import ImageTk, Image
from utils import rescaleFrame
import threading as th
import pickle as pkl
import cvzone as cz
import numpy as np
import cv2 as cv
import time

video_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4"
image_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/trial/carParkImg.png" 
local_cam = "http://192.168.1.9:81/stream"
#local_cam = "https://f163-2409-8a55-3a12-46c0-3b13-c09a-136-568d.ngrok-free.app/stream"
local_stream = "http://192.168.1.10:81/stream" 
#local_stream = "https://d02f-2409-8a55-3a12-46c0-3b13-c09a-136-568d.ngrok-free.app/stream"

class ParkingMonitoringApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        #setting up the window
        self.geometry("1200x780+150+0")
        self.resizable(False, False)
        self.title("Find Me Parking Monitor App")
        
        #Variables
        self.done = True
        self.__space, self.__total = 0, 0, 
        self.__feed = 0
        self.__width, self.__height = 53, 22
        self.buffer = b''
        self.checkfeed = 0
        
        #Get positions
        self.posList = self.getFileSetArray()
        
        #label displaying name
        self.bigLabel = Label(self, text = 'Find Me Parking Surveillance Monitor', font = ('bold', 20), pady = 10)
        self.bigLabel.grid (row = 0, column = 0, columnspan= 1, rowspan = 1, pady = 10, padx = 10)
        
        #label showing parking spot readings from footage
        self.readingsLabel = Label(self, text = '-------------------------------', font = ('bold', 12), pady = 10, bg = "black", fg = "white")
        self.readingsLabel.grid (row = 1, column = 3, columnspan= 1, rowspan = 1, pady = 10, padx = 10)
        
        #labelframe for video feed label
        self.feedLabelFrame = LabelFrame(self, text = "  Video Feed  ", font = ('bold', 12), pady = 10)
        self.feedLabelFrame.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)
        
        #label for video feed 
        #self.createFeedLabel()
        self.createFeedCanvas()
        
        #labelframe for radio buttons
        self.radioButtonFrame = Frame(self, bg = "red", pady = 10, padx = 10)
        self.radioButtonFrame.grid(row = 3, column = 0,  padx = 10, pady = 10)
        
        #radio buttons to select feed
        self.radioOption = IntVar()
        self.feedRadiobutton = Radiobutton(self.radioButtonFrame, text=' Live Feed ', font = ('bold', 12), variable = self.radioOption, value = 0, pady = 10, padx = 20, command = self.setFeed)
        self.feedRadiobutton.grid(row = 0, column = 0, sticky = W, pady = 30)
        self.videoRadiobutton = Radiobutton(self.radioButtonFrame, text=' Live Stream ', font = ('bold', 12), variable = self.radioOption, value = 2, pady = 10, padx = 20, command = self.setFeed)
        self.videoRadiobutton.grid(row = 0, column = 1, sticky = W, pady = 10, padx = 20)
        self.liveFeedRadiobutton = Radiobutton(self.radioButtonFrame, text=' Video Feed ', font = ('bold', 12), variable = self.radioOption, value = 1, pady = 10, padx = 20, command = self.setFeed)
        self.liveFeedRadiobutton.grid(row = 0, column = 2, sticky = W, pady = 10, padx = 20)
        
        #labelframe for edit footage panel label
        self.editLabelFrame = LabelFrame(self, text = "  Edit Feed  ", font = ('bold', 12), pady = 10)
        self.editLabelFrame.grid(row = 2, column = 3, sticky = EW, padx = 10, pady = 10)
        
        #canvas for edit footage panel 
        self.createEditCanvas()
        
        #labelfrme for buttons
        self.buttonsLabelFrame = LabelFrame(self, text = "  Options  ", font = ('bold', 12), pady = 10, padx = 10)
        self.buttonsLabelFrame.grid(row = 3, column = 3, sticky = W, padx = 10, pady = 10, columnspan = 3)
        
        #---BUTTONS---
        #start video feed
        self.startFeedButton = Button(self.buttonsLabelFrame, text = "Start Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.checker())
        self.startFeedButton.grid(row = 3, column = 2, padx = 10, pady = 10)
        #stop video feed
        self.endFeedButton = Button(self.buttonsLabelFrame, text = "Stop Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", command = lambda: self.closer())
        self.endFeedButton.grid(row = 3, column = 3, padx = 10, pady = 10) 
        #Exit program
        self.exitButton = Button(self.buttonsLabelFrame, text = "EXIT", font = ('bold', 10), width = 15, height = 5, fg = "black", bg = "red", command = lambda: self.closeAll())
        self.exitButton.grid(row = 3, column = 4, padx = 10, pady = 10)
        
        #Create a Menu  
        self.menubar = Menu(self)
        self.createMenuBar(self.menubar)

        #starts tkinter
        self.mainloop()
        
    def createFeedLabel(self):
        self.feedLabel = Label(self.feedLabelFrame, pady = 10)
        self.feedLabel.configure(image = PhotoImage(width = 550, height = 360))
        self.feedLabel.grid(row = 0, column = 0, padx = 10, pady = 10)
        
    def createFeedCanvas(self):
        width, height = 555, 365
        self.feedCanvas = Canvas(self.feedLabelFrame, width = width, height = height)
        self.feedCanvas.grid(row = 0, column = 0, padx = 10, pady = 10)
    
    def createEditCanvas(self):
        width, height = 555, 365
        self.editCanvas = Canvas(self.editLabelFrame,  cursor="tcross", width = width, height = height)
        self.editCanvas.create_text(int(width / 2), int(height / 2), text = "awaiting feed...", font = ('bold', 20), anchor = "center", tags = 'text')
        self.editCanvas.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.editCanvas.bind("<ButtonPress-1>", self.leftClick)
        self.editCanvas.bind("<ButtonPress-3>", self.rightClick)
        #self.editCanvas.bind("<ButtonRelease-1>", self.on_button_release)
        
    def setFeed(self):
        self.__feed = self.radioOption.get()
    
    def getFeed(self):
        return self.__feed
    
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
    
    def checker(self):
        if self.checkfeed == 0:
            self.checkfeed = 1
            self.startVideoThread()
    
    def closer(self):
        if self.checkfeed == 1:
            self.checkfeed = 0 
            self.closeVideo()             
           
    def startVideoThread(self):
        try:
            self.closeVideo()
        except Exception:
            pass
        self.checkfeed = 1
        
        if self.getFeed() == 0:
            self.streamdone = True
            self.cap = urlopen(local_cam)
            self.cameraStream()
        if self.getFeed() == 1:
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
            th.Thread(target= self.getReadings).start()
        if self.getFeed() == 2:
            self.streamdone = True
            self.cap = urlopen(local_stream)
            self.cameraStream()       
        
    def closeVideo(self):
        try:
            self.cap.release()
        except Exception:
            self.cap = None
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
        self.createFeedCanvas()
        self.createEditCanvas()
    
    def getFileSetArray(self):
        try:
            with open('C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CarParkPos', 'rb') as f:
                return pkl.load(f)
        except Exception:
            return []
        
    def closeAll(self):
        with open('C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/CarParkPos', 'wb') as f:
            pkl.dump(self.posList, f)
        self.done = False
        try:
            self.closeVideo()
        except Exception:
            pass
        self.destroy()

    def setSpaceCounter(self, space):
        self.__space = space
        
    def getSpaceCounter(self):
        return self.__space
    
    def setTotalSpace(self, total):
        self.__total = total
        
    def getTotalSpace(self):
        return self.__total        
            
    def popUpWindow(self):
        popUp = Toplevel(self)
        button = Button(popUp, text="Click To Close", command = lambda : popUp.destroy())
        button.pack()
        
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
        
    def liveView(self):
        _, frame = self.cap.read()
        frame = rescaleFrame(frame, 0.8)
        cvImage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        img = Image.fromarray(cvImage)
        imgtk = ImageTk.PhotoImage(image = img)
        self.feedLabel.imgtk = imgtk
        self.feedLabel.configure(image = self.feedLabel.imgtk)
        self.feedLabel.after(1, self.liveView)     
        
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
                        self.feedCanvas.create_image(25, 0, image = self.photo, anchor = NW)
                        break
                except Exception:
                    pass

            self.after(1, self.cameraStream)
    
    def settingSpots(self):           
        self.im = Image.open(self.image)
        
        newsize = (550, 360) 
        self.im1 = self.im.resize(newsize)
        
        self.tk_im = ImageTk.PhotoImage(self.im1)
        self.editCanvas.create_image(10, 10, anchor = "nw", image = self.tk_im)     
        
    def getReadings(self):
        time.sleep(1)
        while self.done:
            self.readingsLabel.config(text = f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            #print(f'Available Space: {self.getSpaceCounter()}/{self.getTotalSpace()}')
            time.sleep(3)
            if not self.done:
                print("Feed Stopped")
                break
            
    def setWidth(self, width):
        self.__width = width
        
    def getWidth(self):
        return self.__width
    
    def setHeight(self, height):
        self.__height = height
        
    def getHeight(self):
        return self.__height
    
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
        
if __name__ == "__main__":
    ParkingMonitoringApp()

#Button(self.parkingApp, text="EXIT APP", command = lambda: self.destroy()).grid(row = 4,column = 5)