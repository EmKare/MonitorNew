from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Scrollbar,\
Frame, RIGHT, LEFT, BOTH, Y, Listbox, END, Entry, font
from tkinter.ttk import Combobox
from time import strftime
import re


class Register(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width, self.height = 320,611
        self.geometry(f'{self.width}x{self.height}+10+10')
        self.resizable(False, False)
        
        self.gender = None
        self.fname, self.lname, self.email = "", "", ""
        self.phone, self.card = 0, 0
        self.cvv = 0
        self.exp_month, self.exp_year = None, None        
        self.months = ["01","02","03","04","05","06","07","08","09","10","11","12"]      
        
        #self.RegistrationScreen1()
        self.RegistrationScreen2()
        self.mainloop()        
        
    def RegistrationScreen1(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self, bg = "gray79", )
        self.userAccountCanvas.place(x = 0, y = 0, width = self.width , height = self.height)
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84")# command = self.checkBeforeContinueRegistering)
        self.close_userAccountCanvasButton.place(x = self.width - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) ,  bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.width / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "register")
        self.userAccountCanvas.create_text(50, 150, text = "M/F", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        
        self.gender_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.gender_Combo['values'] = ["M","F"]
        self.gender_Combo.config(font = "None 15 normal", )       
        self.gender_Combo.place(x = 20, y = 180, height = 40, width = 50)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 13))
        self.gender_Combo.bind("<<ComboboxSelected>>", self.setGender)
        
        self.userAccountCanvas.create_text(180, 150, text = "First Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.FnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        self.FnameEntry.place(x = 100, y = 180, width = 200, height = 40)

        self.userAccountCanvas.create_text(100, 260, text = "Last Name", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.LnameEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        self.LnameEntry.place(x = 20, y = 290, width = self.width - 40, height = 40)
        
        self.userAccountCanvas.create_text(120, 370, text = "Email Address", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.emailEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        self.emailEntry.place(x = 20, y = 400, width = self.width - 40, height = 40)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Next", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = self.checkBeforeContinueRegistering)
        self.register_Button.place(x = int(self.width / 2) - 70, y = 460, width = 140, height = 50)        
        
        self.userAccountCanvas.create_text(110, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat",)
        self.login_Button.place(x = 195, y = 535, width = 60, height = 25)
        
        self.userAccountCanvas.create_text(150, 585, text = "NB: Please fill all fields with an ", font = ('bold', 9), justify = "left", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(240, 585, text = "'*'", font = ('bold', 9), justify = "left", fill = "red2", tags = "register")
        self.userAccountCanvas.create_text(int(self.width / 2), 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "center", fill = "black", tags = "register")
                
        self.FnameEntry.bind("<FocusIn>", self.clearLabel)
        self.LnameEntry.bind("<FocusIn>", self.clearLabel)
        self.emailEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)
        
    def clearLabel(self,event):
        if self.gender is not None:
            self.empty_Label.config(text = "", fg = "gray79", bg = "gray79")
        
    def checkBeforeContinueRegistering(self):
        if self.gender is not None:
            if len(self.FnameEntry.get()) != 0:
                self.fname = self.FnameEntry.get()
                if len(self.LnameEntry.get()) != 0:
                    self.lname = self.LnameEntry.get()
                    if len(self.emailEntry.get()) != 0:
                        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                        if(re.fullmatch(regex, self.emailEntry.get())):
                            self.email = self.emailEntry.get()
                            #self.empty_Label.config(text = "", fg = "gray79", bg = "gray79")
                            self.RegistrationScreen2()
                            print("Success")
                        else:
                            self.empty_Label.config(text = "'Email Address' not valid", fg = "old lace", bg = "red2")    
                    else:
                        self.empty_Label.config(text = "'Email Address' is blank", fg = "old lace", bg = "red2")
                else:
                    self.empty_Label.config(text = "'Last Name' is blank", fg = "old lace", bg = "red2")
            else:
                self.empty_Label.config(text = "'First Name' is blank", fg = "old lace", bg = "red2")
        else:
            self.empty_Label.config(text = "'Gender' is blank", fg = "old lace", bg = "red2")
        self.empty_Label.place(x = int(self.width / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)
    
    def setGender(self, event):
        self.gender = self.gender_Combo.get()
        self.clearLabel(event)
        
    def RegistrationScreen2(self):
        try:
            self.empty_Label.destroy()
        except Exception:
            pass
        try:
            self.userAccountCanvas.destroy()
        except Exception:
            pass
        self.userAccountCanvas = Canvas(self, bg = "gray79", )
        self.userAccountCanvas.place(x = 0, y = 0, width = self.width , height = self.height)
        
        self.close_userAccountCanvasButton = Button(self.userAccountCanvas, text = "Close", font = ('bold',10), fg = "red2", highlightthickness = 0,  bd = 0, relief = "flat", bg = "gray84")# command = self.checkBeforeContinueRegistering)
        self.close_userAccountCanvasButton.place(x = self.width - 60, y = 10, width = 50, height = 30)
        
        self.empty_Label = Label( self.userAccountCanvas, font = ('bold', 15) , bg = "gray79")
        
        self.userAccountCanvas.create_text(int(self.width / 2), 70, text = "Register", font = ('bold', 30), justify = "center", fill = "medium blue", tags = "register")
                
        self.userAccountCanvas.create_text(130, 150, text = "Contact Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.phoneEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        self.phoneEntry.place(x = 20, y = 180, width = self.width - 40, height = 40)

        self.userAccountCanvas.create_text(110, 260, text = "Card Number", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cardEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "left")
        self.cardEntry.place(x = 20, y = 290, width = 205, height = 40)
        
        self.userAccountCanvas.create_text(270, 260, text = "CVV", font = ('bold', 23), justify = "left", fill = "medium blue", tags = "register")
        self.cvvEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        self.cvvEntry.place(x = 240, y = 290, width = 60, height = 40)
        
        self.userAccountCanvas.create_text(85, 375, text = "Expiry Date", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
        self.month_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.month_Combo['values'] = [x for x in self.months]
        self.month_Combo.config(font = "None 15 normal", )       
        self.month_Combo.place(x = 20, y = 400, height = 40, width = 70)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))
        self.month_Combo.bind("<<ComboboxSelected>>", self.setMonth)
        
        self.year_Combo = Combobox(self.userAccountCanvas, font = ('bold', 10), state = "readonly")        
        self.year_Combo['values'] = [x for x in range(24,100)]
        self.year_Combo.config(font = "None 15 normal", )       
        self.year_Combo.place(x = 90, y = 400, height = 40, width = 70)
        self.option_add("*TCombobox*Listbox*Font", font.Font(family = "Helvetica", size = 10))
        self.year_Combo.bind("<<ComboboxSelected>>", self.setYear)
        
        self.userAccountCanvas.create_text(240, 375, text = "Driver's ID", font = ('bold',19), justify = "left", fill = "medium blue", tags = "register")
        self.idEntry = Entry(self.userAccountCanvas, bd = 0, bg = "#ffffff", highlightthickness = 0, border = 1, font=('bold',15), justify = "center")
        self.idEntry.place(x = 185, y = 400, width = 115, height = 40)
        
        self.back_Button = Button(self.userAccountCanvas, text = "Back", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = self.checkBeforeContinueRegistering)
        self.back_Button.place(x = 20, y = 460, width = 130, height = 50)
        
        self.register_Button = Button(self.userAccountCanvas, text = "Register", font = ('bold',20), fg = "blue", highlightthickness = 0,  bd = 0, relief = "flat", command = self.checkBeforeFinishRegistering)
        self.register_Button.place(x = 170, y = 460, width = 130, height = 50)        
        
        self.userAccountCanvas.create_text(110, 545, text = "Already have an account?", font = ('bold', 10), justify = "left", fill = "cornflower blue", tags = "register")
        
        self.login_Button = Button(self.userAccountCanvas, text = "Login", font = ('bold',10), fg = "red", highlightthickness = 0,  bd = 0, relief = "flat",)
        self.login_Button.place(x = 195, y = 535, width = 60, height = 25)
        
        self.userAccountCanvas.create_text(140, 585, text = "NB: Please fill all fields with an ", font = ('bold', 9), justify = "left", fill = "black", tags = "register")
        self.userAccountCanvas.create_text(231, 585, text = "'*'", font = ('bold', 9), justify = "left", fill = "red2", tags = "register")
        self.userAccountCanvas.create_text(140, 600, text = "Please ensure all information is accurate ", font = ('bold', 9), justify = "left", fill = "black", tags = "register")
        
        self.phoneEntry.bind("<FocusIn>", self.clearLabel)
        self.cardEntry.bind("<FocusIn>", self.clearLabel)
        self.cvvEntry.bind("<FocusIn>", self.clearLabel)
        self.userAccountCanvas.bind("<ButtonPress-1>", self.clearLabel)
    
    def setMonth(self,event):
        self.exp_month = 1 + self.months.index(self.month_Combo.get())
        print(self.exp_month)
        self.clearLabel(event)
        
    def setYear(self,event):        
        self.exp_year = int(self.year_Combo.get())
        print(self.exp_year)
        self.clearLabel(event)
        
    def checkBeforeFinishRegistering(self):
        if len(self.phoneEntry.get()) != 0:
            regex = r'^\d{1,4}\d{7}$'
            if(re.fullmatch(regex,self.phoneEntry.get())):
                self.phone = int(self.phoneEntry.get())
                if len(self.cardEntry.get()) != 0:
                    regex = r'^\d{15,16}$'
                    if(re.fullmatch(regex,self.cardEntry.get())):
                        self.card = int(self.cardEntry.get())
                        if len(self.cvvEntry.get()) != 0:
                            regex = r'^\d{3,4}$'
                            if(re.fullmatch(regex,self.cvvEntry.get())):
                                self.cvv = int(self.cvvEntry.get())
                                if self.exp_month is not None:
                                    if self.exp_year is not None:
                                        year = strftime('%y')
                                        month = strftime('%m')
                                        if (self.exp_month >= int(month) and self.exp_year >= int(year)) or (self.exp_month <= int(month) and self.exp_year > int(year)): 
                                            print("success")
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
        self.empty_Label.place(x = int(self.width / 2) - int(self.empty_Label.winfo_reqwidth() / 2), y = 15)
        
Register()