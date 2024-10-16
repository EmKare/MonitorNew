"""
import time
import webview
from tkinter import *


def load_url(window):
    # wait a few seconds before changing url:
    time.sleep(10)
    url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'
    # change url:
    window.load_url(url)

if __name__ == '__main__':
    window = Tk('URL Change Example')
    window.geometry("1800x600")
    
    window1 = webview.create_window(title='URL Change Exampled',)
    webview.start(load_url, window1)
"""    
    
"""
import time
from tkinter import *
import tkinterweb as tkw
import sys


def Browser(url:str):
    browser = tkw.HtmlFrame(window, messages_enabled = False)
    browser.load_website(url)
    browser.pack(expand=YES,fill=BOTH)
    
if __name__ == '__main__':
    
    
    url = "https://www.google.com/"
    window = Tk()
    window.geometry("800x600")
    
    Browser(url)
    
    window.mainloop()
    """
    
    


import time
import webview
from tkinter import *
import tkinter.messagebox as mbox
import threading as thr

def load_url(window, url):
    # change url:
    window.load_url(url)
    
def open_browser(url, pressed):
    
    window1 = webview.create_window(title='URL Change Example', url=url)    
    btn.config(command = thr.Thread(target=close,args=(window1,pressed,)))
    webview.start(load_url,window1,url)   

    
    
def close(window1, pressed):
    pressed = False
    window1.destroy()    
        
        
def checker(url, pressed):
    if not pressed:
        pressed = True
        thr.Thread(target=open_browser, args=(url, pressed,)).start()


if __name__ == '__main__':
    url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'
    
    pressed = False
    
    window = Tk('URL Change Example')
    window.geometry("100x130")
    
    btn = Button(window,text = "click", fg = 'black', command= lambda: checker(url,pressed))
    btn.pack()
    
    lbl = Label(window, text="not pressed")
    lbl.pack(pady=20)
    
    btn1 = Button(window,text = "close", fg = 'black', command= window.destroy)
    btn1.pack()
    
    
    
    mainloop()
    
    #window1 = webview.create_window(title='URL Change Exampled',)
    #webview.start(load_url, window1)



"""
import tkinter as tk #import Tkinter
from tkinterweb import HtmlFrame #import the HTML browser

root = tk.Tk() #create the tkinter window
frame = HtmlFrame(root,)# messages_enabled = False) #create HTML browser
url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'

#url = "www.google.com"
frame.load_website(url) #load a website
frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
root.mainloop() 

"""


"""

import time
from tkinter import *
import tkinterweb as tkw
import sys


def Browser(url:str, window):
    browser = tkw.HtmlFrame(window, messages_enabled = False)
    browser.load_website(url)
    browser.pack(expand=YES,fill=BOTH)
    
if __name__ == '__main__':
    
    
    url = 'http://www.google.com/maps/dir/Half-Way-Tree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'
    window = Tk()
    window.geometry("800x600")
    
    Browser(url, window)
    
    window.mainloop()


"""