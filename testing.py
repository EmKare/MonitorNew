from ParkingLot import ParkingLot
import files as files

mySpot = 33
n = 'E3'
index = ""
folder = files.rel_path+"ParkingLot4/"
newsize = (350, 300)

if mySpot < 10:
    index = f'0{mySpot}'
else:
    index = mySpot

entrance = ParkingLot(folder + "ParkingLot4_map.txt", #text file
                                    "E", #starting point
                                    index, #goal
                                    1, #type of map
                                    n, #name of the spot
                                    folder + "Entrance4.png") #name of the image
                                    #f"Entrance_{self.mySpot[1]}.png") #name of the image
entrance.output_image()#.resize(newsize, Image.Resampling.LANCZOS)


exit = ParkingLot(folder + "ParkingLot4_map.txt", index, "X", 0, n, folder + "Exit4.png")
exit.output_image()#.resize(newsize, Image.Resampling.LANCZOS)
