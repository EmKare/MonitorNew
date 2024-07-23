from getParkingLot import ParkingLotInfo, GetLot
from Parking import ParkingLot
from files import rel_path

g = GetLot() 
p = ParkingLotInfo(rel_path, g.listOfFolders[2])
print(p.ParkingLot_name)
#contents,lot_sides,start,goal,typer,spot,imagename,lottype,lotnumber):
spot = "A3"
enter = ParkingLot(p.ParkingLot_mapcontents, p.ParkingLot_sides, "E", "03", 1, spot,p.path+"image.png", p.ParkingLot_sides,p.ParkingLot_number)
enter.output_image()

exit = ParkingLot(p.ParkingLot_mapcontents, p.ParkingLot_sides, "03", "X", 0, spot,p.path+"image1.png", p.ParkingLot_sides,p.ParkingLot_number)
exit.output_image()