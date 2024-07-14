from tkinter import Tk, Label, Button, Menu, Toplevel, font, LabelFrame, Canvas, PhotoImage
from tkinter import ttk as tk


video_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4"
image_name = "C:/Users/DELL/Desktop/MyJourney/Python/Parking/trial/carParkImg.png" 

class ParkingApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.__window_bredth, self.__window_length = 1400, 760
        self.__window_midpoint = int(self.__window_bredth / 2)
        
        #setting up the window
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+50+10")
        self.resizable(False, False)
        self.title("Find Me Parking App")
        
        #Variables
        self.done = True
        self.__space, self.__total = 0, 0, 
        self.__feed = 0
        self.__width, self.__height = 53, 22
        self.__listOfFeeds = ["MegaMart Parking Lot #1", "Sagicor Life Building Parking Lot", "NewLife Mall #3 Parking Lot"]
        
        #Get positions
        #self.posList = self.getFileSetArray()
        
        #------------------------------------------------------------------------------------------------------------------------

        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 100, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 200, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 300, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 400, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 500, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='green').place(x = 600, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='yellow').place(x = 700, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='blue').place(x = 800, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 900, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1000, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1100, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1200, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1300, y = 60)
        Label(self, text = '*', font = ('bold', 20), fg='red').place(x = 1400, y = 60)
                
        #Name of Parking Lot being monitored
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
        self.groupLabel.place(x = 1330, y = 745)
        
        #------------------------------------------------------------------------------------------------------------------------
        
        #labelframe for sidemenu
        self.sidemenuLabelFrame = LabelFrame(self, text = "", font = ('bold', 12), pady = 10, width = 150, height = self.__window_length )
        self.sidemenuLabelFrame.place(x = 0, y = 0)
        
        #labelframe for combobox
        self.comboBoxLabelFrame = LabelFrame(self, text = "  Select Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 140)
        self.comboBoxLabelFrame.place(x = 220, y = 170)
        
        #labelfrme for buttons
        self.buttonsLabelFrame = LabelFrame(self, text = "  Options  ", font = ('bold', 12), pady = 10, width = 565, height = 140)
        self.buttonsLabelFrame.place(x = 815, y = 170)
        
        #labelframe for video feed label
        self.feedLabelFrame = LabelFrame(self, text = "  Video Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400, bg="green")
        self.feedLabelFrame.place(x = 220, y = 340)
        
        #labelframe for edit footage panel label
        self.editLabelFrame = LabelFrame(self, text = "  Edit Feed  ", font = ('bold', 12), pady = 10, width = 565, height = 400, bg="blue")
        self.editLabelFrame.place(x = 815, y = 340)
        #------------------------------------------------------------------------------------------------------------------------
        self.editwindowLabel = Label(self.sidemenuLabelFrame, text = "Edit", bg="red")
        self.editwindowLabel.place(x = 0, y = 0, width = 146, height = 152)
        #------------------------------------------------------------------------------------------------------------------------
        
        #---BUTTONS---
        #start video feed
        self.startFeedButton = Button(self.buttonsLabelFrame, text = "Start Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", )
        self.startFeedButton.place(x = 30, y = 0)
        #stop video feed
        self.endFeedButton = Button(self.buttonsLabelFrame, text = "Stop Feed", font = ('bold', 10), width = 15, height = 5, fg = "blue", bg = "white", )
        self.endFeedButton.place(x = 210, y = 0)
        #Exit program
        self.exitButton = Button(self.buttonsLabelFrame, text = "EXIT", font = ('bold', 10), width = 15, height = 5, fg = "black", bg = "red", )
        self.exitButton.place(x = 390, y = 0)
        
        #Create ComboBox
        self.optionsComboBox = tk.Combobox(self.comboBoxLabelFrame, width = 40, font = ('bold', 10))
        self.optionsComboBox['values'] = [x for x in self.__listOfFeeds]
        self.optionsComboBox.current(0)
        self.optionsComboBox.config(font = "None 16 normal")
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 15))
        self.optionsComboBox.place(x = 34, y = 10)
        self.optionsComboBox.bind("<<ComboboxSelected>>", self.option_selected)
        
        #label for video feed 
        #self.createFeedLabel() 
        #image = PhotoImage(width = 550, height = 360)
        
        #canvas for edit footage panel
        self.createEditCanvas()    
        
        #Create a Menu  
        self.menubar = Menu(self)
        self.createMenuBar(self.menubar) 
        #starts tkinter
        self.mainloop()
        
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
        self.feedLabel = Label(self.feedLabelFrame, bg="red", text="Label", pady = 10,)
        self.feedLabel.configure(image = PhotoImage(width = 550, height = 360))
        self.feedLabel.place(x = 3, y = 0)
    
    def createEditCanvas(self):
        width, height = 555, 365 #width = 555, height = 370
        self.editCanvas = Canvas(self.editLabelFrame,  cursor="tcross", width = width, height = height, bg="yellow")
        self.editCanvas.create_text(int(width / 2), int(height / 2), text = "awaiting feed...", font = ('bold', 20), anchor = "center", tags = 'text')
        self.editCanvas.place(x = 0, y = 0)#grid(row = 0, column = 0, padx = 10, pady = 10)
        #self.editCanvas.bind("<ButtonPress-1>", self.leftClick)
        #self.editCanvas.bind("<ButtonPress-3>", self.rightClick)
        #self.editCanvas.bind("<ButtonRelease-1>", self.on_button_release)
        
    def popUpWindow(self):
        popUp = Toplevel(self.parkingApp)
        button = Button(popUp, text="Click To Close", command = lambda : popUp.destroy())
        button.pack()
        
    def option_selected(self, event):
        selected_option = self.optionsComboBox.get()
        self.parkingLotNameLabel.config(text=selected_option)
        x = int(self.parkingLotNameLabel.winfo_reqwidth() / 2)
        self.parkingLotNameLabel.place(x = self.__window_midpoint - x, y = 80)
        #Label(self, text = '*', font = ('bold', 20), fg='green').place(x = 600, y = 60)

        
if __name__ == "__main__":
    ParkingApp()