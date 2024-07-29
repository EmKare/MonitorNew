import os
def setPath():
    # get the current working directory
    return os.getcwd().replace('\\','/')
#set path for all files used
app_screen = f"{setPath()}/app_screen.jpg"
user_profile = f"{setPath()}/User/"
loading_gif = f"{setPath()}/croppedImages/"
no_user = f"{setPath()}/noUser.png"
cat = f"{setPath()}/cat.png"
rel_path = f"{setPath()}/ParkingLots/"