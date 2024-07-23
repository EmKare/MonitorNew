folderpath = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/"
image_name = r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/trial/carParkImg.png"
video_name = r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4"
other_video = r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/parking-space-counter-master/data/parking_1920_1080.mp4"

local_live = r"http://192.168.1.10:81/stream"
local_cam = r"http://192.168.1.11:81/stream"
local_video = r"http://192.168.1.12:81/stream"
local_stream = r"http://192.168.1.13:81/stream"

sources = [
        ('Camera 1', local_live), 
        ('Camera 2', local_cam),
        ('Camera 3', local_video),
        ('Camera 4', local_stream),
        ('Camera 5', local_stream),
        ]

parishes = [
        "Kingston","St. Andrew","St. Catherine","Clarendon","Manchester","St. Elizabeth","Westmoreland","Hanover","St. James","Trelawny","St. Ann","St. Mary","Portland"," St. Thomas"]

titles = ["Mr.", "Ms.", "Mrs."]



app_screen = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/Misc/app4.jpg"
loading_gif = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/Misc/croppedImages/"
lot_path = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/ParkingLot1.txt"
spot_names = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/spotNames.txt"
amount_available = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/demoParking.txt"
#text='☰'
btn_image = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/create_button_light.png"
rel_path = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/Monitor/ParkingLots/"

"""
import os, os.path
import files


if os.path.exists(files.rel_path+"ParkingLot1"):
   print("Folder exists")
   if os.path.isfile(files.rel_path+"ParkingLot1/ParkingLot1.txt"):
      print("File exists")
   else:
      print("File Doesn't exist")          
else:
   print("Folder Doesn't exist")
   


# simple version for working with CWD
#print(len([name for name in os.listdir(files.rel_path) if os.path.isfile(name)]))

# path joining version for other paths
DIR = files.rel_path+"ParkingLot1"
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
for name in os.listdir(DIR):
   print(name)
   
def folders_in(path_to_parent):
        for fname in os.listdir(path_to_parent):
                if os.path.isdir(os.path.join(path_to_parent,fname)):
                        yield os.path.join(path_to_parent,fname)

import files, os
theList = list(folders_in(files.rel_path))

for name in theList:
    print(name)
    
from tkinter import Tk, Button, END, Listbox
from tkinter import filedialog
import os
import files

# path = files.rel_path
# os.startfile(path)
# ----------------------------
# import webbrowser
# webbrowser.open('file:///' + path)

def open_directory():
    directory = filedialog.askdirectory()
    if directory: # if user didn't choose directory tkinter returns ''
        os.chdir(directory) # change current working directory
        for file_name in os.listdir(directory): # for every file in directory
            if os.path.isfile(os.path.join(directory, file_name)): # if it's file add file name to the list
                Listbox.insert(END, file_name)

root = Tk()
Button(root, text="Choose Directory", command=open_directory).pack()  # create a button which will call open_directory function
root.mainloop()
"""