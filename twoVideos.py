from tkinter import Tk, Label, Button, LEFT, RIGHT, BOTTOM
from PIL import Image, ImageTk
import numpy as np
import files as files
import cv2 as cv

global last_frame                                      #creating global              variable
last_frame = np.zeros((480, 640, 3), dtype=np.uint8)
global last_frame2                                      #creating global      variable
last_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
global cap
cap = cv.VideoCapture(files.video_name)

def show_vid():                                        #creating a function
    if not cap.isOpened():                             #checks for the opening of camera
        print("cant open the camera")
    flag, frame = cap.read()
    frame = cv.resize(frame,(400,500))
    if flag is None:
        print("Major error!")
    elif flag:
        global last_frame
        last_frame = frame.copy()
        global last_frame2
        last_frame2 = frame.copy()

    pic = cv.cvtColor(last_frame, cv.COLOR_BGR2RGB)     #we can change the display color of the frame gray,black&white here
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_vid)


def show_vid2():
    pic2 = cv.cvtColor(last_frame2, cv.COLOR_BGR2RGB)
    img2 = Image.fromarray(pic2)
    img2tk = ImageTk.PhotoImage(image=img2)
    lmain2.img2tk = img2tk
    lmain2.configure(image=img2tk)
    lmain2.after(10, show_vid2)

if __name__ == '__main__':
    root= Tk()                                     #assigning root variable        for Tkinter as tk
    lmain = Label(master=root)
    lmain2 = Label(master=root)
    lmain.pack(side = LEFT)
    lmain2.pack(side = RIGHT)
    root.title("Two Videos")            #you can give any title
    root.geometry("900x700+100+10") #size of window , x-axis, yaxis
    exitbutton = Button(root, text='Quit', fg="red", command=root.destroy).pack(side = BOTTOM,)
    show_vid()
    show_vid2()
    root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly
    cap.release()