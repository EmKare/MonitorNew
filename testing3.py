from getParkingLot import GetLot
from Parking import ParkingLot
from files import rel_path
from random import choice

g = GetLot()
for lot in g.ParkingLots:
    #contents,lot_sides,start,goal,typer,spot,imagename,lotnumber
    spot = choice(lot.ParkingLot_availableSpots)
    print(f'{lot.ParkingLot_name}: #{lot.ParkingLot_number}: Spot({spot[0]}) Index({spot[2]})')
    index = ""
    if spot[2] < 10:
        index = f'0{spot[2]}'
    else:
        index = spot[2]
    entrance = ParkingLot(lot.ParkingLot_mapcontents, lot.ParkingLot_sides, "E", index, 1, spot[0], f"{lot.path}{spot[0]}_Entrance.png", lot.ParkingLot_number)
    entrance.output_image()
    exit = ParkingLot(lot.ParkingLot_mapcontents, lot.ParkingLot_sides, index, "X", 0, spot[0], f"{lot.path}{spot[0]}_Exit.png", lot.ParkingLot_number)
    exit.output_image()