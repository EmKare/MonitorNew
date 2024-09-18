
from time import time
start = time()

from tkinter import Tk, mainloop, CENTER
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from geopy import distance
from parkingLots import _parkingLots
from itertools import islice

import openrouteservice as ors
client = ors.Client(key='5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')

distanceService = Nominatim(user_agent="geoapiExercises")

root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Find Parking Lot")

map_widget = TkinterMapView(root_tk, width=800, height=600, corner_radius=2)
map_widget.pack(fill="both")
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

#(18.0109438, -76.7972963)
#car_pos = (17.9394675, -76.7665624)  #airport                 || squares: 116 | 1.31 seconds | total available_lots found: 5
car_pos = (18.012265695689663, -76.79800557291115) #hwt       || squares: 26  | 1.46 seconds | total available_lots found: 55
#car_pos = (17.966814698972417, -76.80206888632081) #downtown  || squares: 71  | 1.36 seconds | total available_lots found: 19

map_widget.set_position(car_pos[0], car_pos[1], marker=False)
map_widget.set_marker(car_pos[0], car_pos[1], text="car")

#map_widget.set_marker(17.9393675, -76.7664624, text="offs")

parkingLots = {
    "NMIA Parking Lot A": (17.9386082, -76.7780145),
    "NMIA Parking Lot B": (17.9381959, -76.7760460),
    "NMIA Parking Lot C": (17.9398411, -76.7783603),
    "NMIA Parking Lot D": (17.9400975, -76.7761406),
    "NMIA Parking Lot E": (17.9402314, -76.7718813),
}
   
car = 1

"""
weight = 0.011
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="darkgreen", border_width=2)

weight = 0.01
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="black", border_width=2)
weight = 0.009
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="red", border_width=2)
weight = 0.008
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="purple", border_width=2)
weight = 0.007
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="orange", border_width=2)
weight = 0.006
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="blue", border_width=2)
weight = 0.005
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="lightgreen", border_width=2)
weight = 0.004
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="pink", border_width=2)
weight = 0.003
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="gray", border_width=2)
weight = 0.002
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="darkblue", border_width=2)
weight = 0.001
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),#-76.7667624
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="darkred", border_width=2)
"""

def add_marker_event(coords):
    global car
    print("Add marker:", coords)
    map_widget.set_marker(coords[0], coords[1], text=f"marker {car}")
    car += 1
    
def left_click_event(coordinates_tuple):
    global car
    print("Left click event with coordinates:", coordinates_tuple)
    map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text=f"marker {car}")
    print(f"Straight: {distance.distance(car_pos, coordinates_tuple).km:.2f} kms")
    car += 1
    
map_widget.add_left_click_map_command(left_click_event)

map_widget.add_right_click_menu_command(label="Add Marker", command=add_marker_event, pass_coords=True)
yes = 'yes'
no = 'no'

first_weight_const = 0.0001
#final =             0.0116
second_weight_const = 0.02 #0.0026
max = 0.015

available_lots = {}
more_available_lots = {}
count = 1

def create_squares():
    global count
    weight = first_weight_const
    while len(available_lots) != 4:
        for name, coord in _parkingLots.items():
            check_if_in_range(name, coord, weight)
        weight += first_weight_const
        count += 1
        
    print(f"final weight: {weight:.4f}, squares: {count}")  
    exclude_already_added(second_weight_const)
        
    print(f"close available_lots: {len(available_lots)}")
    for name in available_lots.keys():
        print(name)
        #map_widget.set_marker(coord[0],coord[1], text = name, text_color = "red")
    cap, amt = 5, 1
    print(f"other available_lots: {len(more_available_lots)}")
    
    for lot in islice(more_available_lots.items(), cap):
        print(f"{amt}: {lot[0]}")
        map_widget.set_marker(lot[1][0], lot[1][1], text = lot[0], text_color = "red")
        amt+=1

        
    print(f"total available_lots found: {len(available_lots) + len(more_available_lots)}")
        
def check_if_in_range(name, coord, weight):
    
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight > lat and lon > car_pos[1] - weight:
        if car_pos[0] + weight > lat and lon < car_pos[1] + weight:
            if car_pos[0] - weight < lat and lon < car_pos[1] + weight:
                if car_pos[0] - weight < lat and lon > car_pos[1] - weight:
                    add_to_map(name, coord, weight)
                    

def add_to_map(name, coord, weight):
    if name not in available_lots.keys():
        available_lots[name] = coord
        map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                            (car_pos[0] + weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] - weight),],
                            outline_color="darkred", border_width=2)
        map_widget.set_marker(coord[0],coord[1], text = name, text_color = "green")
        #print(f"{count}: {name} @ weight: {weight}")
        
def exclude_already_added(weight2):
    map_widget.set_polygon([(car_pos[0] + weight2, car_pos[1] - weight2),
                            (car_pos[0] + weight2, car_pos[1] + weight2),
                            (car_pos[0] - weight2, car_pos[1] + weight2),
                            (car_pos[0] - weight2, car_pos[1] - weight2),],
                            outline_color="pink", border_width=2)
    for name, coord in _parkingLots.items():
        if name not in available_lots.keys():
            check_for_others(name, coord, weight2)
        
def check_for_others(name, coord, weight2):
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight2 > lat and lon > car_pos[1] - weight2:
        if car_pos[0] + weight2 > lat and lon < car_pos[1] + weight2:
            if car_pos[0] - weight2 < lat and lon < car_pos[1] + weight2:
                if car_pos[0] - weight2 < lat and lon > car_pos[1] - weight2:
                    if name not in more_available_lots.keys():
                        more_available_lots[name] = coord
                        #print(f"{count}: {name} @ weight: {weight2}")

create_squares()

end = time()

print(f'Execution time: {(end - start):.2f} seconds') #1.22 seconds

mainloop()
    
"""
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["color"] = "red"
print(thisdict)





(17.939937031793168, -76.76703446878662),
(17.939967653388585, -76.76596158518066),
(17.9392021119137, -76.7660045005249),
(17.939171490185824, -76.76704519762268),


print(f"({(car_pos[0] + weight, car_pos[1] - weight)},\
{(car_pos[0] + weight, car_pos[1] + weight)},\
{(car_pos[0] - weight, car_pos[1] + weight),}\
{(car_pos[0] - weight, car_pos[1] - weight)})"
)
"""

