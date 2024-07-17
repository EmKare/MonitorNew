from tkinter import Tk, Label, Button, font, Canvas, Frame, LabelFrame, PhotoImage, Entry
from tkinter.ttk import Combobox
from tkinter import ttk as ttk
import files

class feedEditor(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.config(bg="grey")
        self.__window_bredth, self.__window_length = 1200, 606
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        self.geometry(f"{self.__window_bredth}x{self.__window_length}+100+50")        
        self.resizable(False, False)
        
        self.tabs = Frame(self, highlightthickness = 0, bd = 1,  relief = "flat", border = 1,  width = self.__window_bredth, height = 64, bg = "lightgray")
        self.tabs.place(x = 0, y = 0,)
        
        self.containerFrame = Frame(self, highlightthickness = 0, bd = 2,  relief = "flat", border=0,)
        self.containerFrame.place(x = 0, y = self.tabs.winfo_reqheight(), width = self.__window_bredth, height = self.__window_length - self.tabs.winfo_reqheight(),)
        
        #frame for main window
        mainFrame = Frame(self.containerFrame, highlightthickness = 0, bd = 0, relief = "flat", width = self.__window_bredth, height = self.__window_length - self.tabs.winfo_reqheight(), bg="lightblue")
        mainFrame.pack(side="top", fill="both", expand=True)
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)
        
        self.listOfFeeds = files.sources
        
        self.listOfViewFrames = {}
        
        for classes in (addFeed, editFeed, deleteFeed):
            theframe = classes(parent = mainFrame, master = self, sources = self.listOfFeeds)
            self.listOfViewFrames[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
        
        self.tab_1 = Button(self.tabs, text = "Add Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(addFeed))
        self.tab_1.place(x = 0, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_2 = Button(self.tabs, text = "Edit Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(editFeed))
        self.tab_2.place(x = int(self.tabs.winfo_reqwidth() / 3), y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_3 = Button(self.tabs, text = "Delete Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(deleteFeed))
        self.tab_3.place(x = int(self.tabs.winfo_reqwidth() / 3) * 2, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 2)
        
        self.show_frame(addFeed)        
        self.mainloop()
    
    def show_frame(self, anotherClass):
        frame = self.listOfViewFrames[anotherClass]
        frame.tkraise()
        
class addFeed(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        parent_colour = "white"
        self.config(bg=parent_colour)
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        self.feedname_Label = Label( self, text = "Feed Name", font = ('bold', 20) , fg = "black" , bg = parent_colour)
        self.feedname_Label.place(x = 20, y = 30)
        self.feedname_Entry =  Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedname_Entry.place(x = 20, y = 65, width = 300, height = 30)
        self.feedname_Entry_BlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red")
        
        self.feedlink_Label = Label( self, text = "Feed Link", font = ('bold', 20) , fg = "black" , bg = parent_colour)
        self.feedlink_Label.place(x = 20, y = 110)
        self.feedlink_Entry =  Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedlink_Entry.place(x = 20, y = 145, width = 300, height = 30)
        self.feedlink_Entry_BlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red")

class editFeed(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        label = Label(self, text="Edit", bg="white", fg="black")
        label.place(x = (parent.winfo_reqwidth() / 2) - int(label.winfo_reqwidth() / 2), 
                    y = (parent.winfo_reqheight() / 2) - int(label.winfo_reqheight() / 2))
        
class deleteFeed(Frame):
    def __init__(self, parent, master, sources = 0):
        Frame.__init__(self, parent)
        self.config(bg="orange")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        label = Label(self, text="Delete", bg="white", fg="black")
        label.place(x = (parent.winfo_reqwidth() / 2) - int(label.winfo_reqwidth() / 2), 
                    y = (parent.winfo_reqheight() / 2) - int(label.winfo_reqheight() / 2))
     
        
feedEditor()      