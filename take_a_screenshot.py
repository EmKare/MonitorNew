from tkinter import *
import time
from PIL import ImageTk, Image
import pyautogui as pg

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Define a function for taking screenshot
def screenshot():
   random = int(time.time())
   filename = "C:/Users/DELL/Desktop/"+str(random)+".jpg" 
   ss = pg.screenshot(filename)
   ss.show()
   win.deiconify()

def hide_window():
   # hiding the tkinter window while taking the screenshot
   win.withdraw()
   win.after(1000, screenshot)

# Add a Label widget
   Label(win, text="Click the Button to Take the Screenshot", font=('Times New Roman', 18, 'bold')).pack(pady=10)

# Create a Button to take the screenshots
button = Button(win, text="Take Screenshot", font=('Aerial 11 bold'), background="#aa7bb1", foreground="white", command=hide_window)
button.pack(pady=20)

win.mainloop()