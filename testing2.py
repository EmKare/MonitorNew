from getParkingLot import ParkingLotInfo, GetLot
from Parking import ParkingLot
from files import rel_path
from random import choice

g = GetLot() 
p = ParkingLotInfo(rel_path, g.listOfFolders[2])
print(p.ParkingLot_name)
spot = choice(p.ParkingLot_availableSpots)
print(spot)
index = ""
if spot[2] < 10:
    index = f'0{spot[2]}'
else:
    index = spot[2]
enter = ParkingLot(p.ParkingLot_mapcontents, p.ParkingLot_sides, "E", index, 1, spot[0],p.path+"image.png", p.ParkingLot_number)
enter.output_image()

exit = ParkingLot(p.ParkingLot_mapcontents, p.ParkingLot_sides, index, "X", 0, spot[0],p.path+"image1.png", p.ParkingLot_number)
exit.output_image()