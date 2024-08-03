# Import Required Library 
from tkinter import Tk, Button
  
# Create Object 
root = Tk() 
  
# Set geometry 
root.geometry("200x530") 
  
# List of cursors 
cursors =[ 
        "arrow", 
        "circle", 
        "clock", 
        "cross", 
        "dotbox", 
        "exchange", 
        "fleur", 
        "hand1",
        "hand2",
        "heart", 
        "man", 
        "mouse", 
        "pirate", 
        "plus", 
        "shuttle", 
        "sizing", 
        "spider", 
        "spraycan", 
        "star", 
        "target", 
        "tcross", 
        "trek"
] 
  
  
  
# Iterate through all cursors 
for cursor in cursors: 
    Button(root,text=cursor,cursor=cursor).pack() 
  
  
# Execute Tkinter 
root.mainloop()