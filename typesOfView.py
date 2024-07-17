from tkinter import Tk, Label, Button, font, Canvas, Frame, LabelFrame, PhotoImage
from tkinter.ttk import Combobox
from tkinter import ttk as ttk
from VideoPlayer import Camera
import files

class viewFeed(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        
        self.__window_bredth, self.__window_length = 1200, 670
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+100+50")        
        self.resizable(False, False)
        
        self.listOfFeeds = files.sources
        
        self.sideFrame = Frame(self, highlightthickness = 0, bd = 1,  relief = "flat", border = 1,  width = 155, height = self.__window_length,)
        self.sideFrame.place(x = 1050, y = 0,)
        
        self.containerFrame = Frame(self, highlightthickness = 0, bd = 2,  relief = "flat", border=0, bg="lightgrey")
        self.containerFrame.place(x = 0, y = 0, width = self.__window_bredth - self.sideFrame.winfo_reqwidth(), height = self.__window_length,)
        
        #frame for main window
        mainFrame = Frame(self.containerFrame, highlightthickness = 0, bd = 0, relief = "flat", width = self.__window_bredth - self.sideFrame.winfo_reqwidth(), height = self.__window_length, )
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
        self.doubleViewButton = Button(self.sideFrame, text = "Double", font = ('calibri', 18), fg = "black", bd= 0,highlightthickness = 0, border = 1, command=lambda: self.show_frame(DoubleView))
        self.doubleViewButton.place(x = 0, y = 250, width = self.sideFrame.winfo_reqwidth(), height = 210)
        self.quadViewButton = Button(self.sideFrame, text = "Quad", font = ('calibri', 18), fg = "black", bd= 0,highlightthickness = 0, border = 1, command=lambda: self.show_frame(QuadView))
        self.quadViewButton.place(x = 0, y = 460, width = self.sideFrame.winfo_reqwidth(), height = 210)
        #----------------------------------------------------------------------------------------------------------------
        self.show_frame(DoubleView) 
        
        #self.mainloop()
    
    def show_frame(self, anotherClass):
        frame = self.listOfViewFrames[anotherClass]
        # raises the current frame to the top
        frame.tkraise()
      
class SingleView(Frame):
    def __init__(self, parent, master, feeds,):
        Frame.__init__(self, parent)
        main_colour = "lightblue"
        self.config(bg = main_colour) 
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        self.canvasWidth, self.canvasHeight = 830, 545 # 800, 523
        self.feeds = feeds
        
        self.canvas_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")
        self.canvas_ComboBox['values'] = [x[0] for x in self.feeds]
        self.canvas_ComboBox.config(font = "None 15 normal")
        self.canvas_ComboBox.current(0)        
        self.canvas_ComboBox.place(x = self.__midpointAcross - 120, y = 35)        
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))
        self.canvas_ComboBox.bind("<<ComboboxSelected>>", self.option_selected)

        self.chooseFeedLabel = Label(self, text = "Please Choose a Feed", font = ('calibri', 17, 'underline'), justify = "center", bg = main_colour)
        self.chooseFeedLabel.place(x = self.__midpointAcross - (self.canvas_ComboBox.winfo_reqwidth() / 2) - (self.chooseFeedLabel.winfo_reqwidth()) + 70, y = 32)
        
        self.canvas_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth, height = self.canvasHeight, bg = main_colour)
        self.canvas_LabelFrame.place(x = self.__midpointAcross - (self.canvas_LabelFrame.winfo_reqwidth() / 2), y = self.__midpointDown - int(self.canvas_LabelFrame.winfo_reqheight() / 2) + 30,)

        self.getSourceFeed()
        
    def getSourceFeed(self):
        for source in self.feeds:
            if source[0] == self.canvas_ComboBox.get():
                self.vid = None                
                self.vid = Camera(self.canvas_LabelFrame, 1, source[0], source[1])
                self.vid.place(x = 0, y = 0)
            else:
                pass
    
    def option_selected(self, event):
        if self.vid:
            if not self.vid.active_playing:
                self.getSourceFeed()   
        
class DoubleView(Frame):
    def __init__(self, parent, master, feeds, ):
        Frame.__init__(self, parent)
        main_colour = "lightblue"
        self.config(bg = main_colour)
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        self.canvasWidth, self.canvasHeight = 495, 324
        
        self.feeds = feeds
        
        self.video_source1 = self.feeds[0] #set ??
        self.video_source2 = self.feeds[1]

        self.canvas_1_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly",)
        self.canvas_1_ComboBox['values'] = [x[0] for x in self.feeds.copy()]
        self.canvas_1_ComboBox.config(font = "None 13 normal")
        self.canvas_1_ComboBox.current(0)
        #self.canvas_1_current = self.canvas_1_ComboBox.get()      
        self.canvas_1_ComboBox.place(x = 20, y = 105)
        self.canvas_1_ComboBox.bind("<<ComboboxSelected>>", self.canvas_1_option_selected)
        
        self.canvas_2_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")    
        self.canvas_2_ComboBox['values'] = [x[0] for x in self.feeds.copy()]
        self.canvas_2_ComboBox.config(font = "None 13 normal") 
        self.canvas_2_ComboBox.current(1)
        #self.canvas_2_current = self.canvas_2_ComboBox.get()        
        self.canvas_2_ComboBox.place(x = self.canvasWidth +  140, y = 105)
        self.canvas_2_ComboBox.bind("<<ComboboxSelected>>", self.canvas_2_option_selected)
        
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))

        self.chooseFeedLabel = Label(self, text = "Please Choose a Feed", font = ('calibri', 13, 'bold'), justify = "center", bg = main_colour)
        self.chooseFeedLabel.place(x = self.__midpointAcross - (self.chooseFeedLabel.winfo_reqwidth() / 2), y = 100)
        
        self.blankImage = PhotoImage(width = self.canvasWidth , height = self.canvasHeight,)
        
        self.canvas_1_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+20, height = self.canvasHeight+60, bg = main_colour)
        self.canvas_1_LabelFrame.place(x = 6, y = self.__midpointDown - int(self.canvas_1_LabelFrame.winfo_reqheight() / 2),)
        
        self.vid1 = Camera(self.canvas_1_LabelFrame, 1, self.video_source1[0], self.video_source1[1],)
        self.vid1.place(x = 0, y = 0)
               
        self.canvas_1 = Canvas(self.canvas_1_LabelFrame, width = self.canvasWidth, height = self.canvasHeight, bg = "white", border = 5,  bd = 5, highlightbackground = "black", highlightcolor= "black",  )
        
        self.canvas_2_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+20, height = self.canvasHeight+60, bg = main_colour)
        self.canvas_2_LabelFrame.place(x = self.canvasWidth + 29, y = self.__midpointDown - int(self.canvas_2_LabelFrame.winfo_reqheight() / 2))        
                   
        self.vid2 = Camera(self.canvas_2_LabelFrame, 1, self.video_source2[0], self.video_source2[1])
        self.vid2.place(x = 0, y = 0)
        
        self.canvas_2 = Canvas(self.canvas_2_LabelFrame, width = self.canvasWidth, height = self.canvasHeight, bg = "white", border = 4,  bd = 4, highlightbackground = "black", highlightcolor= "black", )

    def canvas_1_option_selected(self, event):
        demo = self.feeds.copy()
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
 
        to_pop = 0
        for feed in demo:
            if feed[0] == comb1cur:
                self.video_source1 = feed
                to_pop = demo.index(feed) #locates combo 1 value in new list
                demo.pop(to_pop) #pops combo 1 value from new list at this index
        
        if not self.vid1.active_playing:
            self.vid1 = Camera(self.canvas_1_LabelFrame, 1, self.video_source1[0], self.video_source1[1],)
            self.vid1.place(x = 0, y = 0)
                         
        self.canvas_2_ComboBox['values'] = [x[0] for x in demo] #assigns combo 2 values as those from new list
        
        if comb1cur == comb2cur:
            if to_pop == 0: 
                self.canvas_2_ComboBox.current(1)
            elif to_pop == len(demo):
                self.canvas_2_ComboBox.current(len(demo) - 1)
            else:
                self.canvas_2_ComboBox.current(to_pop - 1)       
        
    def canvas_2_option_selected(self, event):
        demo = self.feeds.copy() #creates copy of original list
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        
        to_pop = 0
        for feed in demo:
            if feed[0] == comb2cur:
                self.video_source2 = feed
                to_pop = demo.index(feed) #locates combo 1 value in new list
                demo.pop(to_pop) #pops combo 1 value from new list at this index
                
        if not self.vid2.active_playing:
            self.vid2 = Camera(self.canvas_2_LabelFrame, 1, self.video_source2[0], self.video_source2[1],)
            self.vid2.place(x = 0, y = 0)        

        self.canvas_1_ComboBox['values'] = [x[0] for x in demo] #assigns combo 1 values as those from new list
        
        if comb2cur == comb1cur:
            if to_pop == 0: 
                self.canvas_1_ComboBox.current(1)
            elif to_pop == len(demo):
                self.canvas_1_ComboBox.current(len(demo) - 1)
            else:
                self.canvas_1_ComboBox.current(to_pop - 1)   
          
class QuadView(Frame):
    def __init__(self, parent, master, feeds,):
        Frame.__init__(self, parent,)
        main_colour = "lightblue"
        self.config(bg = main_colour)
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.canvasWidth, self.canvasHeight = 400, 263   
             
        self.feeds = feeds
        
        self.video_source1 = self.feeds[0] #set ??
        self.video_source2 = self.feeds[1]
        self.video_source3 = self.feeds[2]
        
        #----- canvas 1 -----------------------------------------------------------------------------------------------
        self.canvas_1_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")
        self.canvas_1_ComboBox['values'] = [x[0] for x in self.feeds]
        self.canvas_1_ComboBox.config(font = "None 10 normal")
        self.canvas_1_ComboBox.current(0)
        self.canvas_1_current = self.canvas_1_ComboBox.get()
        self.canvas_1_ComboBox.place(x = 120, y = 20)
        self.canvas_1_ComboBox.bind("<<ComboboxSelected>>", self.canvas_1_option_selected)
        self.canvas_1_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+80, height = self.canvasHeight+8, bg = main_colour)
        self.canvas_1_LabelFrame.place(x = 30, y = 60)
        self.vid1 = Camera(self.canvas_1_LabelFrame, 2, self.video_source1[0], self.video_source1[1], )
        self.vid1.place(x = 0, y = 0)
        #----- canvas 2 -----------------------------------------------------------------------------------------------
        self.canvas_2_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")
        self.canvas_2_ComboBox['values'] = [x[0] for x in self.feeds]
        self.canvas_2_ComboBox.config(font = "None 10 normal")
        self.canvas_2_ComboBox.current(1)
        self.canvas_2_current = self.canvas_2_ComboBox.get()
        self.canvas_2_ComboBox.place(x = 610, y = 20)
        self.canvas_2_ComboBox.bind("<<ComboboxSelected>>", self.canvas_2_option_selected)   
        self.canvas_2_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+80, height = self.canvasHeight+8, bg = main_colour)
        self.canvas_2_LabelFrame.place(x = 535, y = 60)
        self.vid2 = Camera(self.canvas_2_LabelFrame, 2, self.video_source2[0], self.video_source2[1],)
        self.vid2.place(x = 0, y = 0)
        #----- canvas 3 -----------------------------------------------------------------------------------------------
        self.canvas_3_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")
        self.canvas_3_ComboBox['values'] = [x[0] for x in self.feeds]
        self.canvas_3_ComboBox.config(font = "None 10 normal")
        self.canvas_3_ComboBox.current(2)
        self.canvas_3_current = self.canvas_3_ComboBox.get()
        self.canvas_3_ComboBox.place(x = 120, y = 350)
        self.canvas_3_ComboBox.bind("<<ComboboxSelected>>", self.canvas_3_option_selected)
        self.canvas_3_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+80, height = self.canvasHeight+8, bg = main_colour)
        self.canvas_3_LabelFrame.place(x = 30, y = 390)
        self.vid3 = Camera(self.canvas_3_LabelFrame, 2, self.video_source3[0], self.video_source3[1],)
        self.vid3.place(x = 0, y = 0)
        #----- canvas 4 -----------------------------------------------------------------------------------------------
        self.canvas_4_ComboBox = Combobox(self, width = 40, font = ('bold', 10), state = "readonly")
        self.canvas_4_ComboBox['values'] = [x[0] for x in self.feeds]
        self.canvas_4_ComboBox.config(font = "None 10 normal")
        self.canvas_4_ComboBox.current(3)
        self.canvas_4_current = self.canvas_4_ComboBox.get()
        self.canvas_4_ComboBox.place(x = 610, y = 350)
        self.canvas_4_ComboBox.bind("<<ComboboxSelected>>", self.canvas_4_option_selected)
        self.canvas_4_LabelFrame = LabelFrame(self, text = "", width = self.canvasWidth+80, height = self.canvasHeight+8, bg = main_colour)
        self.canvas_4_LabelFrame.place(x = 535, y = 390)
        if len(self.feeds) > 3:
            self.video_source4 = self.feeds[3]
            self.vid4 = Camera(self.canvas_4_LabelFrame, 2, self.video_source4[0], self.video_source4[1],)
            self.vid4.place(x = 0, y = 0)
        #------------------------------------------------------------------------------------------------------------------------
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 8))
        #------------------------------------------------------------------------------------------------------------------------
        self.chooseFeedLabel_1 = Label(self, text = "Please Choose a Feed", font = ('calibri', 12, 'bold'), justify = "center", bg = main_colour,)
        self.chooseFeedLabel_1.place(x = self.__midpointAcross - (self.chooseFeedLabel_1.winfo_reqwidth() / 2), y = 18)
        self.chooseFeedLabel_2 = Label(self, text = "Please Choose a Feed", font = ('calibri', 12, 'bold'), justify = "center", bg = main_colour,)
        self.chooseFeedLabel_2.place(x = self.__midpointAcross - (self.chooseFeedLabel_2.winfo_reqwidth() / 2), y = 348)
        
    def canvas_1_option_selected(self, event):
        demo = self.feeds.copy()
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
        to_set = 0
        for feed in demo:
            if feed[0] == self.canvas_1_current:                
                to_set = demo.index(feed) #locates combo 1 value in new list

        if comb1cur == self.canvas_2_ComboBox.get():
            self.canvas_2_ComboBox.current(to_set)
            
        if comb1cur == self.canvas_3_ComboBox.get():
            self.canvas_3_ComboBox.current(to_set)
            
        if comb1cur == self.canvas_4_ComboBox.get():
            self.canvas_4_ComboBox.current(to_set)
        
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        comb3cur = self.canvas_3_ComboBox.get() #gets combo 3 value
        comb4cur = self.canvas_4_ComboBox.get() #gets combo 4 value
        
        for feed in demo:
            if feed[0] == comb1cur:
                self.video_source1 = feed
                try:
                    demo.pop(demo.index(feed))
                except Exception:
                    pass
            if feed[0] == comb2cur:
                try:
                    to_pop = demo.index(comb2cur) #locates combo 2 value in list
                    demo.pop(to_pop) #pops combo 2 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb3cur:
                try:
                    to_pop = demo.index(comb3cur) #locates combo 3 value in list
                    demo.pop(to_pop) #pops combo 3 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb4cur:           
                try:
                    to_pop = demo.index(comb4cur) #locates combo 4 value in list
                    demo.pop(to_pop) #pops combo 4 value from list at this index
                except Exception:
                    pass
                
        if not self.vid1.active_playing:
            self.vid1 = Camera(self.canvas_1_LabelFrame, 2, self.video_source1[0], self.video_source1[1],)
            self.vid1.place(x = 0, y = 0)            
        
        if len(demo) > 0:
            self.canvas_1_ComboBox['values'] = [x[0] for x in demo] #assigns combo 1 values as those from new list
            self.canvas_2_ComboBox['values'] = [x[0] for x in demo] #assigns combo 2 values as those from new list
            self.canvas_3_ComboBox['values'] = [x[0] for x in demo] #assigns combo 3 values as those from new list
            self.canvas_4_ComboBox['values'] = [x[0] for x in demo] #assigns combo 4 values as those from new list        
        self.canvas_1_current = comb1cur
        
    def canvas_2_option_selected(self, event):
        demo = self.feeds.copy()
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        to_set = 0
        for feed in demo:
            if feed[0] == self.canvas_2_current:                
                to_set = demo.index(feed) #locates combo 2 value in new list

        if comb2cur == self.canvas_1_ComboBox.get():
            self.canvas_1_ComboBox.current(to_set)
            
        if comb2cur == self.canvas_3_ComboBox.get():
            self.canvas_3_ComboBox.current(to_set)
            
        if comb2cur == self.canvas_4_ComboBox.get():
            self.canvas_4_ComboBox.current(to_set)
        
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
        comb3cur = self.canvas_3_ComboBox.get() #gets combo 3 value
        comb4cur = self.canvas_4_ComboBox.get() #gets combo 4 value
        
        for feed in demo:
            if feed[0] == comb2cur:
                self.video_source2 = feed
                try:
                    demo.pop(demo.index(feed))
                except Exception:
                    pass
            if feed[0] == comb1cur:
                try:
                    to_pop = demo.index(comb1cur) #locates combo 1 value in list
                    demo.pop(to_pop) #pops combo 1 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb3cur:
                try:
                    to_pop = demo.index(comb3cur) #locates combo 3 value in list
                    demo.pop(to_pop) #pops combo 3 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb4cur:           
                try:
                    to_pop = demo.index(comb4cur) #locates combo 4 value in list
                    demo.pop(to_pop) #pops combo 4 value from list at this index
                except Exception:
                    pass
        
        if not self.vid2.active_playing:
            self.vid2 = Camera(self.canvas_2_LabelFrame, 2, self.video_source2[0], self.video_source2[1],)
            self.vid2.place(x = 0, y = 0)
        
        if len(demo) > 0:    
            self.canvas_2_ComboBox['values'] = [x[0] for x in demo] #assigns combo 2 values as those from new list
            self.canvas_1_ComboBox['values'] = [x[0] for x in demo] #assigns combo 1 values as those from new list
            self.canvas_3_ComboBox['values'] = [x[0] for x in demo] #assigns combo 3 values as those from new list
            self.canvas_4_ComboBox['values'] = [x[0] for x in demo] #assigns combo 4 values as those from new list
        
        self.canvas_2_current = comb2cur
        
    def canvas_3_option_selected(self, event):
        demo = self.feeds.copy()
        comb3cur = self.canvas_3_ComboBox.get() #gets combo 3 value
        to_set = 0
        for feed in demo:
            if feed[0] == self.canvas_3_current:                
                to_set = demo.index(feed) #locates combo 3 value in new list

        if comb3cur == self.canvas_1_ComboBox.get():
            self.canvas_1_ComboBox.current(to_set)
            
        if comb3cur == self.canvas_2_ComboBox.get():
            self.canvas_2_ComboBox.current(to_set)
            
        if comb3cur == self.canvas_4_ComboBox.get():
            self.canvas_4_ComboBox.current(to_set)
        
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        comb4cur = self.canvas_4_ComboBox.get() #gets combo 4 value
        
        for feed in demo:
            if feed[0] == comb3cur:
                self.video_source3 = feed
                try:
                    demo.pop(demo.index(feed))
                except Exception:
                    pass
            if feed[0] == comb1cur:
                try:
                    to_pop = demo.index(comb1cur) #locates combo 1 value in list
                    demo.pop(to_pop) #pops combo 1 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb2cur:
                try:
                    to_pop = demo.index(comb2cur) #locates combo 2 value in list
                    demo.pop(to_pop) #pops combo 2 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb4cur:           
                try:
                    to_pop = demo.index(comb4cur) #locates combo 4 value in list
                    demo.pop(to_pop) #pops combo 4 value from list at this index
                except Exception:
                    pass
        
        if not self.vid3.active_playing:
            self.vid3 = Camera(self.canvas_3_LabelFrame, 2, self.video_source3[0], self.video_source3[1],)
            self.vid3.place(x = 0, y = 0)
        
        if len(demo) > 0:    
            self.canvas_3_ComboBox['values'] = [x[0] for x in demo] #assigns combo 3 values as those from new list
            self.canvas_1_ComboBox['values'] = [x[0] for x in demo] #assigns combo 1 values as those from new list
            self.canvas_2_ComboBox['values'] = [x[0] for x in demo] #assigns combo 2 values as those from new list
            self.canvas_4_ComboBox['values'] = [x[0] for x in demo] #assigns combo 4 values as those from new list
        
        self.canvas_3_current = comb3cur
       
    def canvas_4_option_selected(self, event):
        demo = self.feeds.copy()
        comb4cur = self.canvas_4_ComboBox.get() #gets combo 4 value
        to_set = 0
        for feed in demo:
            if feed[0] == self.canvas_4_current:                
                to_set = demo.index(feed) #locates combo 4 value in new list

        if comb4cur == self.canvas_1_ComboBox.get():
            self.canvas_1_ComboBox.current(to_set)
            
        if comb4cur == self.canvas_2_ComboBox.get():
            self.canvas_2_ComboBox.current(to_set)
            
        if comb4cur == self.canvas_3_ComboBox.get():
            self.canvas_3_ComboBox.current(to_set)
        
        comb1cur = self.canvas_1_ComboBox.get() #gets combo 1 value
        comb2cur = self.canvas_2_ComboBox.get() #gets combo 2 value
        comb3cur = self.canvas_3_ComboBox.get() #gets combo 3 value
        
        for feed in demo:
            if feed[0] == comb4cur:
                self.video_source4 = feed
                try:
                    demo.pop(demo.index(feed))
                except Exception:
                    pass
            if feed[0] == comb1cur:
                try:
                    to_pop = demo.index(comb1cur) #locates combo 1 value in list
                    demo.pop(to_pop) #pops combo 1 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb2cur:
                try:
                    to_pop = demo.index(comb2cur) #locates combo 2 value in list
                    demo.pop(to_pop) #pops combo 2 value from list at this index
                except Exception:
                    pass
            if feed[0] == comb3cur:           
                try:
                    to_pop = demo.index(comb3cur) #locates combo 3 value in list
                    demo.pop(to_pop) #pops combo 3 value from list at this index
                except Exception:
                    pass
                
        if not self.vid4.active_playing:
            self.vid4 = Camera(self.canvas_4_LabelFrame, 2, self.video_source4[0], self.video_source4[1],)
            self.vid4.place(x = 0, y = 0)
        
        if len(demo) > 0:    
            self.canvas_4_ComboBox['values'] = [x[0] for x in demo] #assigns combo 4 values as those from new list
            self.canvas_1_ComboBox['values'] = [x[0] for x in demo] #assigns combo 1 values as those from new list
            self.canvas_2_ComboBox['values'] = [x[0] for x in demo] #assigns combo 2 values as those from new list
            self.canvas_3_ComboBox['values'] = [x[0] for x in demo] #assigns combo 3 values as those from new list
        
        self.canvas_4_current = comb4cur
      
#viewFeed()

"""
        self.canvas_startButton = Button(self, text = "Start", font = ('bold', 10), fg = "blue", relief = "flat", command = lambda : self.setCap())
        self.canvas_startButton.place(x = self.__midpointAcross + 80, y = 36, width = 100)
        self.canvas_stopButton = Button(self, text = "Record", font = ('bold', 10), fg = "red", relief = "flat", )
        self.canvas_stopButton.place(x = self.__midpointAcross + 200, y = 36, width = 100)
        self.canvas_snapButton = Button(self, text = "Snapshot", font = ('bold', 10), fg = "red", relief = "flat", command = lambda : self.snapshot())
        self.canvas_snapButton.place(x = self.__midpointAcross + 320, y = 36, width = 100)
        
        self.blankImage = PhotoImage(width = self.canvasWidth , height = self.canvasHeight,)
        
        self.canvas_main = Canvas(self, width = self.canvasWidth, height = self.canvasHeight, bg = "white", border = 4,  bd = 4, highlightbackground = "black", highlightcolor= "black",  )
        self.canvas_main.place(x = self.__midpointAcross - (self.canvas_main.winfo_reqwidth() / 2), y = 85)
        
        self.canvas_bg = self.canvas_main.create_image(5, 5, anchor = NW, image = self.blankImage)
        #------------------------------------------------------------------------------------------------------------------------
        self.canvas_1_cap = None
        self.canvas1_startstopButton = Button(self.canvas_1_LabelFrame, text = "Start/Stop", font = ('bold', 10), fg = "green", relief = "flat", command = lambda : self.setCap(self.canvas_1_cap, self.canvas_1, self.canvas_1_bg, files.video_name))        
        self.canvas1_startstopButton.place(x = 0, 
                                      y = self.canvas_1_LabelFrame.winfo_reqheight() - 45, 
                                      width = int(self.canvas_1_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
        
        self.canvas1_recordButton = Button(self.canvas_1_LabelFrame, text = "Start/Stop Record", font = ('bold', 10), fg = "purple", relief = "flat", command = lambda : self.stopFeed(self.canvas_1, self.canvas_1_bg,))
        self.canvas1_recordButton.place(x = int(self.canvas_1_LabelFrame.winfo_reqwidth() / 3) - 1 ,
                                      y = self.canvas_1_LabelFrame.winfo_reqheight() - 45,
                                      width = int(self.canvas_1_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
        
        self.canvas1_snapshotButton = Button(self.canvas_1_LabelFrame, text = "Snapshot", font = ('bold', 10), fg = "red", relief = "flat", command = lambda : self.stopFeed(self.canvas_1, self.canvas_1_bg,))
        self.canvas1_snapshotButton.place(x = (int(self.canvas_1_LabelFrame.winfo_reqwidth() / 3) * 2) - 2,
                                      y = self.canvas_1_LabelFrame.winfo_reqheight() - 45,
                                      width = int(self.canvas_1_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
        #------------------------------------------------------------------------------------------------------------------------
        self.canvas2_startstopButton = Button(self.canvas_2_LabelFrame, text = "Start/Stop", font = ('bold', 10), fg = "green", relief = "flat", command = lambda : self.setCap(self.canvas_2_cap, self.canvas_2, self.canvas_2_bg, files.video_name))        
        self.canvas2_startstopButton.place(x = 0, 
                                      y = self.canvas_2_LabelFrame.winfo_reqheight() - 45, 
                                      width = int(self.canvas_2_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
        
        self.canvas2_recordButton = Button(self.canvas_2_LabelFrame, text = "Start/Stop Record", font = ('bold', 10), fg = "purple", relief = "flat", command = lambda : self.stopFeed(self.canvas_2, self.canvas_2_bg,))
        self.canvas2_recordButton.place(x = int(self.canvas_2_LabelFrame.winfo_reqwidth() / 3) - 1,
                                      y = self.canvas_2_LabelFrame.winfo_reqheight() - 45,
                                      width = int(self.canvas_2_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
        
        self.canvas2_snapshotButton = Button(self.canvas_2_LabelFrame, text = "Snapshot", font = ('bold', 10), fg = "red", relief = "flat", command = lambda : self.stopFeed(self.canvas_2, self.canvas_2_bg,))
        self.canvas2_snapshotButton.place(x = (int(self.canvas_2_LabelFrame.winfo_reqwidth() / 3) * 2) - 2,
                                      y = self.canvas_2_LabelFrame.winfo_reqheight() - 45,
                                      width = int(self.canvas_2_LabelFrame.winfo_reqwidth() / 3) - 2, height = 40)
                                      
                                      
        self.canvas_2 = Canvas(self.canvas_2_LabelFrame, width = self.canvasWidth, height = self.canvasHeight, bg = "yellow")
        self.canvas_2.place(x = 0, y = 0)
        self.canvas_2_startButton = Button(self.canvas_2_LabelFrame, text = "Start", font = ('bold', 10), fg = "blue", relief = "flat",)
        self.canvas_2_startButton.place(x = self.canvas_2.winfo_reqwidth(), 
                                       y = 0, 
                                       width = 72,
                                       height = int(self.canvasHeight / 3) + 1)
        self.canvas_2_stopButton = Button(self.canvas_2_LabelFrame, text = "Stop", font = ('bold', 10), fg = "red", relief = "flat",)
        self.canvas_2_stopButton.place(x = self.canvas_2.winfo_reqwidth(), 
                                       y = int(self.canvasHeight / 3) + 3, 
                                       width = 72,
                                       height = int(self.canvasHeight / 3) + 1)
        self.canvas_2_snapshotButton = Button(self.canvas_2_LabelFrame, text = "Snapshot", font = ('bold', 10), fg = "purple", relief = "flat",)
        self.canvas_2_snapshotButton.place(x = self.canvas_2.winfo_reqwidth(), 
                                       y = (int(self.canvasHeight / 3) * 2) + 6, 
                                       width = 72,
                                       height = int(self.canvasHeight / 3) )

"""

    # ----- FROM SINGLEVIEW -----------------------
    # def setCap(self):
    #     self.cap = cv.VideoCapture(files.local_video) 
    #     self.canvas_startButton.config(text = "Stop", command = lambda : self.stopFeed())
    #     self.startFeed()
        
    # def startFeed(self):
    #     #if self.cap.get(cv.CAP_PROP_POS_FRAMES) == self.cap.get(cv.CAP_PROP_FRAME_COUNT): 
    #     #    self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                    
    #     self._, frame = self.cap.read()
    #     if self._:
    #         frame = self.rescale(frame, self.canvasWidth, self.canvasHeight)
    #         cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #         img = Image.fromarray(cv2image)
    #         self.imgtk = ImageTk.PhotoImage(image = img)
    #         self.canvas_main.itemconfig(self.canvas_bg, image = self.imgtk)
    #     self.canvas_main.after(1, self.startFeed)
    
    # def stopFeed(self):
    #     self._ = False
    #     self.canvas_main.itemconfig(self.canvas_bg, image = self.blankImage)
    #     if self.cap.isOpened():
    #         self.cap.release()
    #     cv.destroyAllWindows()
    #     self.canvas_startButton.config(text = "Start", command = lambda : self.setCap())
    
    # def snapshot(self):
    #         # Get a frame from the video source
    #     try:      
    #         if self.cap.isOpened():
    #             ret, frame = self.cap.read()
    #             if ret:
    #                 frame = cv.resize(frame, (400, 300))
    #                 # Return a boolean success flag and the current frame converted to BGR
    #                 cv.imwrite("frame-" + strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv.cvtColor(frame, cv.COLOR_RGB2BGR))
    #     except Exception:
    #         pass

    # def rescale(self, frame, width, height):
    #     dimensions = (width, height)
    #     return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)