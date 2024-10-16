import tkinter as tk
import webview
import threading

#Global variable to hold the webview window
webview_window = None

def load_my_url(window, url):
    #change url:
    window.load_url(url)

#Function to create the webview window
def create_my_webview_window():
    global webview_window
    if webview_window is None:
        width, height = 400, 750
        root.wm_deiconify()
        webview_window = webview.create_window(title='My Website', width=width, height=height, x=300, y=0, on_top=True, resizable=False, min_size=(width,height))

#Function to open webview on the main thread
def open_my_webview(url):
    global webview_window
    if webview_window is None:        
        #print(f"W: {root.winfo_reqwidth()}, H: {root.winfo_reqheight()}")
        open_button.config(command= lambda: open_my_webview(url), takefocus=0)
        create_my_webview_window()
        webview.start(gui='tkinter', debug=False, func=lambda:load_my_url(webview_window,url))
        close_my_webview(url)

#Function to close the webview window
def close_my_webview(url):
    global webview_window
    if webview_window is not None:
        try:
            webview.destroy_window()
        except Exception:
            pass
        webview_window = None
    else:
        webview_window = None
        root.wm_deiconify()
        open_button.config(command= lambda: open_my_webview(url), takefocus=0)


root = tk.Tk()
root.wm_title("Simple Tkinter App")
#root.overrideredirect(True)

w,h = 100,100
root.wm_geometry(f'{w}x{h}+300+30')
root.wm_resizable(False,False)

root.wm_minsize(w, h)
root.wm_maxsize(w, h)

url = 'https://www.google.com'

#Create the buttons
open_button = tk.Button(root, text="Open WebView", command=lambda:open_my_webview(url), takefocus=0)
open_button.grid(row = 0, column = 0)

close_button = tk.Button(root, text="Close WebView", command=lambda:root.destroy(), takefocus=0)
close_button.grid(row = 1, column = 0, rowspan=1)

#Run the tkinter event loop
root.wm_state("normal")
root.wm_deiconify()
root.mainloop()



url = 'http://www.google.com/maps/dir/HalfWayTree+Clock,+Constant+Spring+Road,+Kingston,+Jamaica/X684%2B77V+UDC+Multi-storey+parking+lot,+Port+Royal+St,+Kingston,+Jamaica/@17.9897083,-76.8114051,14z/'

url = 'https://www.google.com/maps/dir/18.012265695689663,+-76.79800557291115/18.0001557,+-76.7841809/ @18.0061198,-76.7961992,16z/'

url = 'https://www.google.com/maps/dir/18.012265695689663,+-76.79800557291115/18.0001557,+-76.7841809/'

#url = 'https://maps.app.goo.gl/6KczHvBhzYYic57R9'