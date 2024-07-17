from tkinter import Tk, Label, Button, font, Canvas, Frame, LabelFrame, PhotoImage, Entry # noqa
from tkinter.ttk import Combobox # noqa
from tkinter import ttk as ttk
import files

class feedEditor(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.config(bg="grey")
        self.__window_bredth, self.__window_length = 1200, 670
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
        self.listOfParishes = files.parishes
        self.titles = files.titles
        
        self.listOfViewFrames = {}
        
        for classes in (addFeed, editFeed, deleteFeed):
            theframe = classes(parent = mainFrame, master = self, sources = self.listOfFeeds,)
            self.listOfViewFrames[classes] = theframe
            theframe.grid(row = 0, column = 0, sticky = "nsew")
        
        self.tab_1 = Button(self.tabs, text = "Add Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(addFeed,1))
        self.tab_1.place(x = 0, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_2 = Button(self.tabs, text = "Edit Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(editFeed,2))
        self.tab_2.place(x = int(self.tabs.winfo_reqwidth() / 3), y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 1)
        
        self.tab_3 = Button(self.tabs, text = "Delete Feed", font = ('calibri', 18), fg = "black", bd= 0, highlightthickness = 0, border = 1, command = lambda: self.show_frame(deleteFeed,3))
        self.tab_3.place(x = int(self.tabs.winfo_reqwidth() / 3) * 2, y = 0, height = self.tabs.winfo_reqheight() - 1, width = int(self.tabs.winfo_reqwidth() / 3) - 2)
        
        self.show_frame(addFeed,1)        
        #self.mainloop()
    
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
        
class addFeed(Frame):
    def __init__(self, parent, master, sources = None,):
        Frame.__init__(self, parent)
        parent_colour = "lightblue"
        self.config(bg=parent_colour)
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        # ------- FEED LABELFRAME ---------------------------------------------------------------------------------------
        self.aboutFeed_Labelframe = LabelFrame(self, text = " Feed Data ", font = ('bold', 20), width = 550, height = 480, )
        self.aboutFeed_Labelframe.place(x = 33, y = 40)
        
        self.feedname_Label = Label( self.aboutFeed_Labelframe , text = "Feed Name", font = ('bold', 15) , fg = "black" , )
        self.feedname_Label.place(x = 20, y = 15)
        self.feedname_Entry = Entry(self.aboutFeed_Labelframe , bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedname_Entry.place(x = 20, y = 45, width = self.aboutFeed_Labelframe.winfo_reqwidth() - 50, height = 30)
        self.feedname_Entry_BlankLabel = Label( self. aboutFeed_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        self.feedlink_Label = Label( self.aboutFeed_Labelframe, text = "Feed Link", font = ('bold', 15) , fg = "black" , )
        self.feedlink_Label.place(x = 20, y = 95)
        self.feedlink_Entry = Entry(self.aboutFeed_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedlink_Entry.place(x = 20, y = 125,  width = self.aboutFeed_Labelframe.winfo_reqwidth() - 50, height = 30)
        self.feedlink_Entry_BlankLabel = Label( self.aboutFeed_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        self.feedXcoord_Label = Label( self.aboutFeed_Labelframe, text = "Longtitude", font = ('bold', 15) , fg = "black" , )
        self.feedXcoord_Label.place(x = 20, y = 185)
        self.feedXcoord_Entry = Entry(self.aboutFeed_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedXcoord_Entry.place(x = 20, y = 215,  width = int((self.aboutFeed_Labelframe.winfo_reqwidth() - 50) / 2) - 10, height = 30)
        self.feedXcoord_Entry_BlankLabel = Label( self.aboutFeed_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        self.feedYcoord_Label = Label( self.aboutFeed_Labelframe, text = "Latitude", font = ('bold', 15) , fg = "black" , )
        self.feedYcoord_Label.place(x = 20 + int((self.aboutFeed_Labelframe.winfo_reqwidth() - 50) / 2) + 10, y = 185)
        self.feedYcoord_Entry = Entry(self.aboutFeed_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedYcoord_Entry.place(x = 20 + int((self.aboutFeed_Labelframe.winfo_reqwidth() - 50) / 2) + 10, y = 215, width = int((self.aboutFeed_Labelframe.winfo_reqwidth() - 50) / 2) - 10, height = 30)
        self.feedYcoord_Entry_BlankLabel = Label( self.aboutFeed_Labelframe, text = "", font = ('bold', 10) , fg = "red")

        self.feedaddress_Label = Label( self.aboutFeed_Labelframe, text = "Address", font = ('bold', 15) , fg = "black" , )
        self.feedaddress_Label.place(x = 20, y = 275)
        self.feedaddress_Entry = Entry(self.aboutFeed_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.feedaddress_Entry.place(x = 20, y = 305, width = self.aboutFeed_Labelframe.winfo_reqwidth() - 50, height = 30)
        self.feedaddress_Entry_BlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red")
         
        self.feedParish_Label = Label( self.aboutFeed_Labelframe, text = "Parish", font = ('bold', 15) , fg = "black" , )
        self.feedParish_Label.place(x = 20, y = 355)        
        self.feedParish_Combo = Combobox(self.aboutFeed_Labelframe, width = 40, font = ('bold', 10), state = "readonly")        
        self.feedParish_Combo['values'] = [x for x in master.listOfParishes]
        self.feedParish_Combo.config(font = "None 15 normal", )
        self.feedParish_Combo.current(0)        
        self.feedParish_Combo.place(x = 20, y = 385, height = 30,)        
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))
        #self.feedParish_Combo.bind("<<ComboboxSelected>>", self.option_selected)        
        self.feedParish_Combo_BlankLabel = Label( self.aboutFeed_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        # ------- CONTACT LABELFRAME ---------------------------------------------------------------------------------------
        self.contactPerson_Labelframe = LabelFrame(self, text = " Contact ", font = ('bold', 20), width = 550, height = 480, )
        self.contactPerson_Labelframe.place(x = self.__midpointAcross + 20, y = 40)

        self.contactTitle_Label = Label( self.contactPerson_Labelframe , text = "Title", font = ('bold', 15) , fg = "black" , )
        self.contactTitle_Label.place(x = 20, y = 15)
        
        self.contactTitle_Combo = Combobox(self.contactPerson_Labelframe,  font = ('bold', 10), state = "readonly")        
        self.contactTitle_Combo['values'] = [x for x in master.titles]
        self.contactTitle_Combo.config(font = "None 15 normal", )
        self.contactTitle_Combo.current(0)        
        self.contactTitle_Combo.place(x = 20, y = 45, height = 30, width = 70,)
        self.contactTitle_Combo.bind("<<ComboboxSelected>>", self.contactTitle_option_selected)      
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))        
        
        self.contactFName_Label = Label( self.contactPerson_Labelframe, text = "First Name", font = ('bold', 15) , fg = "black" , )
        self.contactFName_Label.place(x = 120, y = 15)
        self.contactFName_Entry = Entry(self.contactPerson_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.contactFName_Entry.place(x = 120, y = 45, width = int(self.contactPerson_Labelframe.winfo_reqwidth() ) - 150 , height = 30)
        self.contactFName_Entry_BlankLabel = Label( self.contactPerson_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        self.contactLName_Label = Label( self.contactPerson_Labelframe, text = "Last Name", font = ('bold', 15) , fg = "black" , )
        self.contactLName_Label.place(x = 20, y = 95)
        self.contactLName_Entry = Entry(self.contactPerson_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.contactLName_Entry.place(x = 20, y = 125,  width = self.contactPerson_Labelframe.winfo_reqwidth() - 50, height = 30)
        self.contactLName_Entry_BlankLabel = Label( self.contactPerson_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        self.contactaddress_Label = Label( self.contactPerson_Labelframe, text = "Address", font = ('bold', 15) , fg = "black" , )
        self.contactaddress_Label.place(x = 20, y = 185)
        self.contactaddress_Entry = Entry(self.contactPerson_Labelframe, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), )
        self.contactaddress_Entry.place(x = 20, y = 215, width = self.contactPerson_Labelframe.winfo_reqwidth() - 50, height = 30)
        self.contactaddress_Entry_BlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red")
         
        self.contactParish_Label = Label( self.contactPerson_Labelframe, text = "Parish", font = ('bold', 15) , fg = "black" , )
        self.contactParish_Label.place(x = 20, y = 275)        
        self.contactParish_Combo = Combobox(self.contactPerson_Labelframe, width = 40, font = ('bold', 10), state = "readonly")        
        self.contactParish_Combo['values'] = [x for x in master.listOfParishes]
        self.contactParish_Combo.config(font = "None 15 normal", )
        self.contactParish_Combo.current(0)        
        self.contactParish_Combo.place(x = 20, y = 305, height = 30,)        
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))
        
        self.contactTele_Label = Label( self.contactPerson_Labelframe, text = "Phone", font = ('bold', 15) , fg = "black" , )
        self.contactTele_Label.place(x = 20, y = 355) 
        self.contactTele_Entry = Entry(self.contactPerson_Labelframe, bd = 0, fg = "gray", highlightthickness = 0, border = 1, font=('bold',12),)
        self.tele_text = " 876-555-5555"
        self.contactTele_Entry.insert(0, self.tele_text)
        self.contactTele_Entry.place(x = 20, y = 385, width = int((self.contactPerson_Labelframe.winfo_reqwidth() - 50) / 2) - 10, height = 30)
        self.contactTele_Entry.bind("<FocusIn>", self.contactTele_Entry_temptext)
        self.contactTele_Entry.bind("<FocusOut>", self.contactTele_Entry_addtemptext)
        self.contactTele_Entry_BlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red")
        
        self.contactEmail_Label = Label( self.contactPerson_Labelframe, text = "Email", font = ('bold', 15) , fg = "black" , )
        self.contactEmail_Label.place(x = 20 + int((self.contactPerson_Labelframe.winfo_reqwidth() - 50) / 2) + 10, y = 355)
        self.contactEmail_Entry = Entry(self.contactPerson_Labelframe, bd = 0, fg = "gray", highlightthickness = 0, border = 1, font=('bold',12), )
        self.email_text = " john_doe@email.com"
        self.contactEmail_Entry.insert(0, self.email_text)
        self.contactEmail_Entry.place(x = 20 + int((self.contactPerson_Labelframe.winfo_reqwidth() - 50) / 2) + 10, y = 385, width = int((self.aboutFeed_Labelframe.winfo_reqwidth() - 50) / 2) - 10, height = 30)
        self.contactEmail_Entry.bind("<FocusIn>", self.contactEmail_Entry_temptext)
        self.contactEmail_Entry.bind("<FocusOut>", self.contactEmail_Entry_addtemptext)
        self.contactEmail_Entry_BlankLabel = Label( self.contactPerson_Labelframe, text = "", font = ('bold', 10) , fg = "red")
        
        #------ BUTTONS -----------------------------------------------------------------------------------------------------
        self.acceptInfo_Button = Button(self, text = "Add Feed", font = ('bold', 15), bd= 0, highlightthickness = 0, border = 0)
        self.acceptInfo_Button.place(x = self.__midpointAcross - 160, y = 540, width = 150, height = 40)
        
        self.resetInfo_Button = Button(self, text = "Reset", font = ('bold', 15), fg = "red", bd= 0, highlightthickness = 0, border = 0, command = lambda : self.resetValues())
        self.resetInfo_Button.place(x = self.__midpointAcross + 10, y = 540, width = 150, height = 40)
        
    def resetValues(self):
        self.feedname_Entry.delete(0,'end')
        self.feedlink_Entry.delete(0,'end')
        self.feedXcoord_Entry.delete(0,'end')
        self.feedYcoord_Entry.delete(0,'end')
        self.feedaddress_Entry.delete(0,'end')
        self.feedParish_Combo.current(0)
        self.contactTitle_Combo.current(0)
        self.contactFName_Entry.delete(0,'end')
        self.contactLName_Entry.delete(0,'end')
        self.contactaddress_Entry.delete(0,'end')
        self.contactParish_Combo.current(0)
        self.contactTele_Entry.delete(0,'end')
        self.contactTele_Entry.config(font=('bold',12), fg = "gray")
        self.contactTele_Entry.insert(0, self.tele_text)
        self.contactEmail_Entry.delete(0,'end')
        self.contactEmail_Entry.config(font=('bold',12), fg = "gray")
        self.contactEmail_Entry.insert(0, " john_doe@email.com")
    
    def contactTele_Entry_temptext(self,e):
        if self.contactTele_Entry.get() == self.tele_text:
            self.contactTele_Entry.delete(0,'end')
            self.contactTele_Entry.config(font=('bold',15), fg = "black")
        
    def contactTele_Entry_addtemptext(self,e):
        if self.contactTele_Entry.get() == "":
            self.contactTele_Entry.config(font=('bold',12), fg = "gray")
            self.contactTele_Entry.insert(0, self.tele_text)
        
    def contactEmail_Entry_temptext(self,e):
        if self.contactEmail_Entry.get() == self.email_text:
            self.contactEmail_Entry.delete(0,'end')
            self.contactEmail_Entry.config(font=('bold',15), fg = "black")
        
    def contactEmail_Entry_addtemptext(self,e):
        if self.contactEmail_Entry.get() == "":
            self.contactEmail_Entry.config(font=('bold',12), fg = "gray")
            self.contactEmail_Entry.insert(0, self.email_text)
        
    def contactTitle_option_selected(self, event):
        not_email_text = ""  
        if self.contactTitle_Combo.get() == "Mr.":
            self.email_text = " john_doe@email.com"
            not_email_text = " jane_doe@email.com"
        else:
            self.email_text = " jane_doe@email.com"
            not_email_text = " john_doe@email.com"           
            
        if self.contactEmail_Entry.get() == "" or self.contactEmail_Entry.get() == not_email_text:
            self.contactEmail_Entry.delete(0,'end')
            self.contactEmail_Entry.config(font=('bold',12), fg = "gray")
            self.contactEmail_Entry.insert(0, self.email_text)        

class editFeed(Frame):
    def __init__(self, parent, master, sources = None,):
        Frame.__init__(self, parent)
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        label = Label(self, text="Edit", bg="white", fg="black")
        label.place(x = (parent.winfo_reqwidth() / 2) - int(label.winfo_reqwidth() / 2), 
                    y = (parent.winfo_reqheight() / 2) - int(label.winfo_reqheight() / 2))
        
class deleteFeed(Frame):
    def __init__(self, parent, master, sources = None, ):
        Frame.__init__(self, parent)
        self.config(bg="lightblue")
        self.__window_bredth, self.__window_length = parent.winfo_reqwidth(), parent.winfo_reqheight()
        self.__midpointAcross, self.__midpointDown = int(self.__window_bredth / 2), int(self.__window_length / 2)
        
        label = Label(self, text="Delete", bg="white", fg="black")
        label.place(x = (parent.winfo_reqwidth() / 2) - int(label.winfo_reqwidth() / 2), 
                    y = (parent.winfo_reqheight() / 2) - int(label.winfo_reqheight() / 2))
     
        
#feedEditor()      