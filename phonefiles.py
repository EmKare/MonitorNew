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
places_in_Jamaica = f"{setPath()}/places_in_Jamaica.txt"
locations = [
    (18.012265695689663, -76.79800557291115), #hwt
    (17.966814698972417, -76.80206888632081), #downtown
    (17.9390582, -76.7671692), #airport
    (18.05912872464319, -76.82104804840952), #solo pricemart
    (18.061493743046423, -76.80044868317515),
]

phone_app_screen = f"{setPath()}/phone_app_screen.jpg"

pip_packages = ["pywin32","geopy","pywebview","lorem-text","openrouteservice",
            "pillow","tk","tkintermapview","mysql-connector-python"]
