from tkintermapview import TkinterMapView
from tkinter import Tk, mainloop, CENTER
from geopy.geocoders import Nominatim
from parkingLots import _parkingLots
import openrouteservice as ors
from itertools import islice
from geopy import distance
from time import time


client = ors.Client(key = '5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')
distanceService = Nominatim(user_agent = "geoapiExercises")


width, height = 1200, 800

root_tk = Tk()
root_tk.geometry(f"{width}x{height}")
root_tk.title("Find Parking Lot")

map_widget = TkinterMapView(root_tk, width = width, height = height, corner_radius = 2)
map_widget.pack(fill = "both")
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22)
#map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

#car_pos = (17.9394675, -76.7665624)  #airport                 || squares: 116 | 1.31 seconds | total available_lots found: 5
#car_pos = (18.012265695689663, -76.79800557291115) #hwt       || squares: 26  | 1.46 seconds | total available_lots found: 55
#car_pos = (17.966814698972417, -76.80206888632081) #downtown  || squares: 71  | 1.36 seconds | total available_lots found: 19

map_widget.set_position(18.012265695689663, -76.79800557291115, marker = False)
#map_widget.set_position(car_pos[0], car_pos[1], marker = False)
#map_widget.set_marker(car_pos[0], car_pos[1], text = "car")
#map_widget.set_marker(17.9393675, -76.7664624, text = "offs")

available_lots = {}
more_available_lots = {}
count = 1
left_click = False
first_weight_const = 0.000001
colours = ["purple","gray","cadetblue","orange","pink",
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'lightgray',
    'black'
]

def create_squares(car_pos):
    global count
    second_weight_const = 0.02
    draw_square(car_pos, second_weight_const, "pink")
    exclude = False
    weight = first_weight_const
    while len(available_lots) != 8 :
        for name, coord in _parkingLots.items():
            check_if_in_range(car_pos, name, coord, weight)
        weight += first_weight_const
        count += 1
        if weight >= second_weight_const:
            exclude = True
            break
        
    print(f"final weight: {weight:.4f}, squares: {count}")
        
    print(f"close available_lots: {len(available_lots)}")
    
    for name in available_lots.keys():
        calculate_route_distance(car_pos, name, (available_lots[name][0], available_lots[name][1]), draw = True)

    if not exclude:
        exclude_already_added(car_pos, weight, second_weight_const)
        print(f"other available_lots: {len(more_available_lots)}")
        
        cap = 5
        for lot in islice(more_available_lots.items(), cap):
            calculate_route_distance(car_pos, lot[0], (lot[1][0], lot[1][1]),)
            map_widget.set_marker(lot[1][0], lot[1][1], text = lot[0], text_color = "red")

        print(f"total available_lots found: {len(available_lots) + len(more_available_lots)}")
        
def check_if_in_range(car_pos, name, coord, weight):    
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight > lat and lon > car_pos[1] - weight:
        if car_pos[0] + weight > lat and lon < car_pos[1] + weight:
            if car_pos[0] - weight < lat and lon < car_pos[1] + weight:
                if car_pos[0] - weight < lat and lon > car_pos[1] - weight:
                    add_to_map(car_pos, name, coord, weight)                    

def add_to_map(car_pos, name, coord, weight):
    if name not in available_lots.keys():
        available_lots[name] = coord
        draw_square(car_pos, weight, "darkred")
        try:
            map_widget.set_marker(coord[0],coord[1], text = name, text_color = "green")
        except Exception:
            print(f"error @ {name} with {coord}")
        #print(f"{count}: {name} @ weight: {weight}")

def draw_square(car_pos, weight, colour):
    map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                            (car_pos[0] + weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] - weight),],
                            outline_color = colour, border_width = 2)
        
def exclude_already_added(car_pos, weight2, final_weight):
    while weight2 <= final_weight:
        for name, coord in _parkingLots.items():
            if name not in available_lots.keys():
                check_for_others(car_pos, name, coord, weight2)
            weight2 += first_weight_const       
           
        
def check_for_others(car_pos, name, coord, weight2):
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight2 > lat and lon > car_pos[1] - weight2:
        if car_pos[0] + weight2 > lat and lon < car_pos[1] + weight2:
            if car_pos[0] - weight2 < lat and lon < car_pos[1] + weight2:
                if car_pos[0] - weight2 < lat and lon > car_pos[1] - weight2:
                    if name not in more_available_lots.keys():
                        more_available_lots[name] = coord
                        #print(f"{count}: {name} @ weight: {weight2}")                        
                        
def calculate_route_distance(car_pos, name, found_lot, draw = False): 
    global colour
    global colours
    route = client.directions(coordinates = [[car_pos[1], car_pos[0]], [found_lot[1], found_lot[0]]],
                              profile = 'driving-car', format = 'geojson',)
    route_coordinates = [tuple(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
    route_coordinates.insert(0, tuple(car_pos))
    route_coordinates.insert(len(route_coordinates), (found_lot[0], found_lot[1]))
    if draw:
        map_widget.set_path(position_list = route_coordinates, color = colours[colour], width = 2)
        colour += 1
        
    print(f"car to ***{name}*** has {len(route_coordinates)} points")
    
    route_distance, start, end = 0, 0, 1
    while end < len(route_coordinates):
        route_distance += distance.distance(route_coordinates[start], route_coordinates[end]).km
        start += 1
        end += 1
    
    print(f"Roadway : {route_distance:.2f} kms")
    print(f"Straight: {distance.distance(car_pos, found_lot).km:.2f} kms")
    
def left_click_event(coordinates_tuple):
    global left_click
    if not left_click:
        global colour
        colour = 0
        left_click = True
        start = time()
        print("Finding Parking for Coordinates:", coordinates_tuple)
        map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text = f"CAR IS HERE", text_color = "blue")
        create_squares(coordinates_tuple)
        end = time()
        print(f'Execution time: {(end - start):.2f} seconds')
        print("------------------------------------------------------------------------------------------")

def right_click_event():
    try:
        map_widget.delete_all_polygon()
    except Exception:
        pass
    try:
        map_widget.delete_all_marker()
    except Exception:
        pass
    try:
        map_widget.delete_all_path()
    except Exception:
        pass
    try:
        available_lots.clear()
        more_available_lots.clear()
    except Exception:
        pass
    #print("------------------------------------------------------------------------------------------")
    global left_click
    left_click = False
    
map_widget.add_left_click_map_command(left_click_event)
map_widget.add_right_click_menu_command(label = "Restart", command = right_click_event, pass_coords = False)

mainloop()


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