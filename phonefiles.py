import os
def setPath():
    # get the current working directory
    return os.getcwd().replace('\\','/')
#set path for all files used
loading_gif = f"{setPath()}/croppedImages/"
rel_path = f"{setPath()}/ParkingLots/"
user_profile = f"{setPath()}/User/"
dummy_entrance_image = f"{setPath()}/A4_entrance.png"
dummy_exit_image = f"{setPath()}/A4_exit.png"
app_screen = f"{setPath()}/app_screen.jpg"
cat = f"{setPath()}/cat.png"
no_user = f"{setPath()}/noUser.png"


