from tkinter import Tk, mainloop, CENTER
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from geopy import distance 

import openrouteservice as ors
client = ors.Client(key='5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')

distanceService = Nominatim(user_agent="geoapiExercises")

root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Find Parking Lot")

map_widget = TkinterMapView(root_tk, width=800, height=600, corner_radius=2,)
map_widget.pack(fill="both")
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22)

car_pos = (18.012265695689663, -76.79800557291115)#(17.9394675, -76.7665624) 

map_widget.set_position(car_pos[0], car_pos[1], marker=False,)
map_widget.set_marker(car_pos[0], car_pos[1], text="car")

weight = 0.02
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="red", border_width=2)

weight = 0.01
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="darkgreen", border_width=2)
weight = 0.005
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="black", border_width=2)
weight = 0.0116
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="purple", border_width=2)
toadd = 0.001
weight += toadd
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="orange", border_width=2)
weight += toadd
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="gray", border_width=2)
weight += toadd
map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                        (car_pos[0] + weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] + weight),
                        (car_pos[0] - weight, car_pos[1] - weight),],
                       outline_color="blue", border_width=2)

car = 1
def left_click_event(coordinates_tuple):
    global car
    print("Left click event with coordinates:", coordinates_tuple)
    map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text=f"marker {car}")
    print(f"Straight: {distance.distance(car_pos, coordinates_tuple).km:.2f} kms")
    car += 1
    
def showLocations():
    from parkingLots import _parkingLots    
    for x, y in _parkingLots.items():
        map_widget.set_marker(y[0], y[1], text = x, text_color = "green")
    
map_widget.add_left_click_map_command(left_click_event)

showLocations()
mainloop()