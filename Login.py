from tkinter import Tk, Button, Label, Entry, LabelFrame, END
from PIL import ImageTk, Image
import files

#global userDetails
userDetails = {}
userDetails["Allaire909"] = "87654321"
userDetails["Kareem1011"] = "12345678"

class window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args,*kwargs)
        self.__width, self.__height, self.__left, self.__top = 0, 0, 0, 0
        self.__title = ""
        self.resizable(False, False)
        icon = Image.open(files.icon)
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)
        self.setWindow()
        self.labelFrame = LabelFrame(self, text = "",)
        self.labelFrame.place(x = 5, y = 5, width = self.get_Width() - 10, height = self.get_Height() - 10)
        
    def printuserDetails(self):
        for key, val in userDetails.items():
            print(f'Key: {key} - Value: {val}')
        
    def setLabel(self, lbl_text, lbl_fg):
        self.main_Label = Label(self, text = lbl_text, font = ('bold', 30) , fg = lbl_fg)
        self.main_Label.place(x = (self.get_Width() / 2) - int(self.main_Label.winfo_reqwidth() / 2), y = 30)
    
    def set_button(self, btn_text, btn_fg, btn_command, x_coord, y_coord):
        self.main_btn = Button(self, text = btn_text, font = ('bold',12), fg = btn_fg, command = btn_command)
        self.main_btn.place(x  = x_coord, y = y_coord, width = 60, height = 30)
    
    def setWindow(self,):
        self.geometry(f"{self.get_Width()}x{self.get_Height()}+{self.get_Left()}+{self.get_Top()}")
        self.title(f"{self.get_Title()}")
    
    def set_Width(self, width):
        self.__width = width
        
    def get_Width(self):
        return self.__width
        
    def set_Height(self, height):
        self.__height = height
        
    def get_Height(self):
        return self.__height
    
    def set_Title(self, title):
        self.__title = title
        
    def get_Title(self):
        return self.__title
    
    def set_Left(self, left):
        self.__left = left
        
    def get_Left(self):
        return self.__left
    
    def set_Top(self, top):
        self.__top = top
        
    def get_Top(self):
        return self.__top

class Login(window):
    def __init__(self):
        super().__init__()
        self.__loginTries = 3
        self.set_Width(400)
        self.set_Height(500)
        self.set_Left(600)
        self.set_Top(50)
        self.set_Title("Login")        
        self.setWindow()
        self.setLabel("Login", "red")
        self.__set_EntriesandLabels()
        
        
        self.mainloop()
    
    def __set_EntriesandLabels(self):
        
        self.usernameLabel = Label( self, text = "Username", font = ('bold', 20) , fg = "black" )
        self.usernameLabel.place(x = 50, y = 135)
        self.usernameEntry =  Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        self.usernameEntry.place(x = 50, y = 175, width = 300, height = 30)
        self.usernameEntryBlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        
        self.passwordLabel = Label( self, text = "Password", font = ('bold', 20) , fg = "black")
        self.passwordLabel.place(x = 50, y = 230)
        self.passwordEntry = Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), show = "\u2022", justify = "center",) #"\u2217"
        self.passwordEntry.place(x = 50, y = 270, width = 300, height = 30)
        self.passwordEntryBlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        
        self.loginAttemptsLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        #self.loginAttemptsLabel.place(x = (self.get_Width() / 2) - (self.loginAttemptsLabel.winfo_reqwidth() / 2), y = 305)
        
        self.login_Button = Button(self, text = "Login", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 1, command = lambda: self.checkLogin())
        self.login_Button.place(x = 130, y = 335, width = 160, height = 50)
        
        self.registerLabel = Label( self, text = "Don't have an account?", font = ('bold', 10) , fg = "black" )
        self.registerLabel.place(x = 90, y = 413)
        
        self.register_Button = Button(self, text = "Register", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 1, command = lambda: self.Register())
        self.register_Button.place(x = 110 + self.registerLabel.winfo_reqwidth(), y = 410, width = 60, height = 25)
        
    def set__loginTries(self, tries):
        self.__loginTries = tries
    
    def get__loginTries(self):
        return self.__loginTries
        
    def checkLogin(self):        
        self.clearAllLabels()
        self.set__loginTries(self.get__loginTries() - 1)   
           
        if self.get__loginTries() < 1:
            self.loginAttemptsLabel.config(text = f"{self.get__loginTries()} Attempts Remaining. Closing Program")
            self.loginAttemptsLabel.place(x = (self.get_Width() / 2) - (self.loginAttemptsLabel.winfo_reqwidth() / 2), y = 305)
            self.destroy()
        else:
            if userDetails.get(self.usernameEntry.get()) == self.passwordEntry.get():
                self.set__loginTries(3)
                self.Login(self.usernameEntry.get())
            else:
                if len(self.usernameEntry.get()) == 0 and len(self.passwordEntry.get()) == 0:
                    self.clearAllLabels()
                    self.loginAttemptsLabel.config(text = "Please Enter a Valid Username and Password")
                    self.loginAttemptsLabel.place(x = (self.get_Width() / 2) - (self.loginAttemptsLabel.winfo_reqwidth() / 2), y = 305)
                    self.usernameEntry.delete(0, END)
                    self.passwordEntry.delete(0, END)
                    
                elif len(self.usernameEntry.get()) == 0:
                    self.clearAllLabels()
                    self.usernameEntryBlankLabel.config(text = "Please Enter a Valid Username")
                    self.usernameEntryBlankLabel.place(x = (self.get_Width() / 2) - (self.usernameEntryBlankLabel.winfo_reqwidth() / 2), y = 207)
                    self.usernameEntry.delete(0, END)
                    self.passwordEntry.delete(0, END)
                    
                elif len(self.passwordEntry.get()) == 0:
                    self.clearAllLabels()
                    self.passwordEntryBlankLabel.config(text = "Please Enter a Valid Password")
                    self.passwordEntryBlankLabel.place(x = (self.get_Width() / 2) - (self.passwordEntryBlankLabel.winfo_reqwidth() / 2), y = 307)
                    self.usernameEntry.delete(0, END)
                    self.passwordEntry.delete(0, END)
                    
                else:
                    self.clearAllLabels()
                    self.loginAttemptsLabel.config(text = f"Incorrect User Credentials. {self.get__loginTries()} Attempts Remaining")
                    self.loginAttemptsLabel.place(x = (self.get_Width() / 2) - (self.loginAttemptsLabel.winfo_reqwidth() / 2), y = 305)
                    self.usernameEntry.delete(0, END)
                    self.passwordEntry.delete(0, END)
        #print(f'{self.get__loginTries()}')
        
    def clearAllLabels(self):
        self.usernameEntryBlankLabel.config(text = "")
        self.passwordEntryBlankLabel.config(text = "")
        self.loginAttemptsLabel.config(text = "")

    def Login(self, username):
        from NewLayout import App
        self.destroy()
        App(username)
        
    def Register(self):
        self.destroy()
        Registration()
        
class Registration(window):
    def __init__(self):
        super().__init__()
        
        self.set_Width(400)
        self.set_Height(600)
        self.set_Left(600)
        self.set_Top(50)
        self.set_Title("Registration")        
        self.setWindow()
        self.setLabel("Register", "red")       
        self.__set_EntriesandLabels()
              
        self.mainloop()
        
    def __set_EntriesandLabels(self):
        #USERNAME
        self.usernameLabel = Label( self, text = "Username", font = ('bold', 20) , fg = "black" )
        self.usernameLabel.place(x = 50, y = 135)
        self.usernameEntry =  Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center",)
        self.usernameEntry.place(x = 50, y = 175, width = 300, height = 30)
        self.usernameEntryBlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        #PASSWORD 
        self.passwordLabel = Label( self, text = "Password", font = ('bold', 20) , fg = "black")
        self.passwordLabel.place(x = 50, y = 230)
        self.passwordEntry = Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), show = "\u2022", justify = "center",)
        self.passwordEntry.place(x = 50, y = 270, width = 300, height = 30)
        self.passwordEntryBlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        #REENTER PASSWORD
        self.reenterpasswordLabel = Label( self, text = "Re-Enter Password", font = ('bold', 20) , fg = "black")
        self.reenterpasswordLabel.place(x = 50, y = 330)
        self.reenterpasswordEntry = Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), show = "\u2022", justify = "center",)
        self.reenterpasswordEntry.place(x = 50, y = 370, width = 300, height = 30)
        self.reenterpasswordEntryBlankLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        #LOGIN ATTEMPTS
        self.registerAttemptsLabel = Label( self, text = "", font = ('bold', 10) , fg = "red" )
        #self.registerAttemptsLabel.place(x = (self.get_Width() / 2) - (self.loginAttemptsLabel.winfo_reqwidth() / 2), y = 405)
        
        self.register_Button = Button(self, text = "Register", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 1,command = lambda: self.Register())
        self.register_Button.place(x = 130, y = 435, width = 160, height = 50)
        
        self.loginLabel = Label( self, text = "Already have an account?", font = ('bold', 10) , fg = "black" )
        self.loginLabel.place(x = 90, y = 513)
        
        self.login_Button = Button(self, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 1, command = lambda : self.Login())
        self.login_Button.place(x = 110 + self.loginLabel.winfo_reqwidth(), y = 510, width = 60, height = 25)
        
    def Login(self):
        self.destroy()
        Login()
        
    def Register(self):        
        self.clearAllLabels()

        if len(self.usernameEntry.get()) == 0 and len(self.passwordEntry.get()) == 0 and len(self.reenterpasswordEntry.get()) == 0:           
            self.clearAllLabels()           
            self.registerAttemptsLabel.config(text = "Please Enter Valid User Credentials")
            self.registerAttemptsLabel.place(x = (self.get_Width() / 2) - (self.registerAttemptsLabel.winfo_reqwidth() / 2), y = 405)
            self.clearAllEntries()
            
        elif len(self.usernameEntry.get()) == 0:
            self.clearAllLabels()
            self.usernameEntryBlankLabel.config(text = "Please Enter a Valid Username")
            self.usernameEntryBlankLabel.place(x = (self.get_Width() / 2) - (self.usernameEntryBlankLabel.winfo_reqwidth() / 2), y = 207)
            self.clearAllEntries()
            
        elif len(self.passwordEntry.get()) == 0:
            self.clearAllLabels()
            self.passwordEntryBlankLabel.config(text = "Please Enter a Valid Password")
            self.passwordEntryBlankLabel.place(x = (self.get_Width() / 2) - (self.passwordEntryBlankLabel.winfo_reqwidth() / 2), y = 307)
            self.reenterpasswordEntry.delete(0, END)
            
        elif len(self.reenterpasswordEntry.get()) == 0:
            self.clearAllLabels()
            self.passwordEntryBlankLabel.config(text = "Please Re-Enter Password")
            self.passwordEntryBlankLabel.place(x = (self.get_Width() / 2) - (self.passwordEntryBlankLabel.winfo_reqwidth() / 2), y = 407)
            self.reenterpasswordEntry.delete(0, END)
            
        elif self.passwordEntry.get() != self.reenterpasswordEntry.get():
            self.clearAllLabels()           
            self.registerAttemptsLabel.config(text = "Passwords Do Not Match")
            self.registerAttemptsLabel.place(x = (self.get_Width() / 2) - (self.registerAttemptsLabel.winfo_reqwidth() / 2), y = 405)
            self.passwordEntry.delete(0, END)
            self.reenterpasswordEntry.delete(0, END)
        
        else:
            self.clearAllLabels()
            userDetails.update({self.usernameEntry.get() : self.reenterpasswordEntry.get()})
            self.clearAllEntries()
            self.Login()
        
    def clearAllLabels(self):
        self.usernameEntryBlankLabel.config(text = "")
        self.passwordEntryBlankLabel.config(text = "")
        self.reenterpasswordEntryBlankLabel.config(text = "")
        self.registerAttemptsLabel.config(text = "")
        
    def clearAllEntries(self):
        self.usernameEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.reenterpasswordEntry.delete(0, END)
        
#Login()
    
        



        
        
        
        
        
        
        
        
        
        
        
        
        
        

"""
        
    def set_button(self):
    self.main_button = Button(self, text = "Click Me!", font = ('bold',12), fg = "blue", command = lambda:self.resetSize())
        self.main_button.place(x = self.get_Width() - 100, y = self.get_Height() - 50, )
        
    def resetSize(self):
        sleep(1)
        self.set_Width(900)
        self.set_Height(800)
        self.set_Left(100)
        self.set_Top(10)
        self.set_Title("Main Window")
        self.setWindow()
        self.main_button.config(text = "Welome", fg = "red", command = lambda:self.destroy())
        self.main_button.place(x = self.get_Width() - 100, y = self.get_Height() - 50, )
        
"""