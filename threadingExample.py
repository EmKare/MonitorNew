
from random import randint
import threading as th
from tkinter import *
import time

root = Tk()

def checkPress(pressed):    
    if not pressed:
        pressed = True
        th.Thread(target=fivesec, args=(pressed,)).start()

def fivesec(pressed):    
    lbl.config(text="will change in 5 sec")    
    time.sleep(5)
    lbl.config(text="5 seconds are up")
    pressed = False
    
def rando():
    lbl2.config(text=f"random #: {randint(1,100)}")

root.title("Thread")
root.geometry("500x400")

pressed = False
lbl = Label(root, text="hello")
lbl.pack(pady=20)

btn = Button(root, text="5 sec", command= lambda : checkPress(pressed) )
btn.pack(pady=20)

btn2 = Button(root, text="pick random number", command=rando)
btn2.pack(pady=20)

lbl2 = Label(root, text="")
lbl2.pack(pady=20)

root.mainloop()