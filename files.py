import os
def setPath():
    # get the current working directory
    return os.getcwd().replace('\\','/')

loading_gif = f"{setPath()}/croppedImages/"
rel_path = f"{setPath()}/ParkingLots/"
user_profile = f"{setPath()}/User/"
dummy_entrance_image = f"{setPath()}/A4_entrance.png"
dummy_exit_image = f"{setPath()}/A4_exit.png"
app_screen = f"{setPath()}/app_screen.jpg"
cat = f"{setPath()}/cat.png"
no_user = f"{setPath()}/noUser.png"
icon = f"{setPath()}/icon.png"

image_name = f"{setPath()}/SoftwareMedia/carParkImg.png"
video_name = f"{setPath()}/SoftwareMedia/carPark.mp4"

local_cam = r"http://192.168.1.11:81/stream"
local_video = r"http://192.168.1.12:81/stream"
local_stream = r"http://192.168.1.13:81/stream"
local_live = r"http://192.168.1.14:81/stream"
local_tv = r"http://192.168.1.15:81/stream"

sources = [
        ('Camera 1', local_cam), 
        ('Camera 2', local_video),
        ('Camera 3', local_stream),
        ('Camera 4', local_live),
        ('Camera 5', local_tv),
        ]

parishes = [
        "Kingston","St. Andrew","St. Catherine","Clarendon","Manchester","St. Elizabeth","Westmoreland","Hanover","St. James","Trelawny","St. Ann","St. Mary","Portland"," St. Thomas"]

titles = ["Mr.", "Ms.", "Mrs."]

#text='☰'
#folderpath = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/"
#other_video = r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/parking-space-counter-master/data/parking_1920_1080.mp4"
#lot_path = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/ParkingLot1.txt"
#spot_names = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/spotNames.txt"
#amount_available = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/demoParking.txt"
#btn_image = r"C:/Users/DELL/Desktop/MyJourney/Python/ParkingApp/create_button_light.png"