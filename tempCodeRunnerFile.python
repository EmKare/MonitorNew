# Python program to temporarily remove a 
# Tkinter widget without using just place 

# Import the Tkinter library 
from tkinter import *

# Create a GUI app 
app=Tk() 

# Set the title and geometry of the window 
app.title('Remove Tkinter Widget') 
app.geometry("600x400") 

# Make a function to remove the widget 
def remove_widget(): 
    label.place_forget()
    button.config(command=append_widget,text="Append Widget")
    
def append_widget(): 
    label.place(relx=0.5, rely=0.3, anchor=CENTER)
    button.config(command=remove_widget, text="Remove Widget")

# Create a label widget to display text 
label=Label(app, text="Tkinter Widget", font='Helvetica 20 bold') 
label.place(relx=0.5, rely=0.3, anchor=CENTER) 

# Create a button to remove text 
button=Button(app, text="Remove Widget", command=remove_widget) 
button.place(relx=0.5, rely=0.7, anchor=CENTER) 

# Make infinite loop for displaying app 
# on the screen 
app.mainloop()
