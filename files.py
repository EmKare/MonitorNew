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