from tkinter import Tk, mainloop, CENTER
from tkintermapview import TkinterMapView
#import openrouteservice as ors

#client = ors.Client(key='5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')



# create tkinter window
root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = TkinterMapView(root_tk, width=800, height=600, corner_radius=2)
map_widget.pack(fill="both")

# example tile sever:
#map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

map_widget.set_position(18.007943,-76.781315, marker=False)  #google map 
#map_widget.set_marker(18.007943,-76.781315, text="Ja")





marker_2 = map_widget.set_marker(18.0118757, -76.7968643, text="start")
marker_3 = map_widget.set_marker(18.0072864, -76.7812398, text="end")

#coords = [[-76.7968643, 18.0118757], [-76.7812398, 18.0072864]]
#route = client.directions(coordinates=coords,
#                          profile='driving-car',
#                          format='geojson',)

#route_list = [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
#for x in route_list:
#    print(f"[{x[0]},{x[1]}],")
#print(len(route_list))

route_coordinates = [
(18.0118757, -76.7968643),
(18.011877,-76.796858),
(18.011164,-76.79674),
(18.010999,-76.796697),
(18.011139,-76.796194),
(18.011197,-76.796033),
(18.011383,-76.7956),
(18.011621,-76.795018),
(18.011639,-76.794968),
(18.011825,-76.794418),
(18.011999,-76.79386),
(18.012404,-76.792816),
(18.012902,-76.791672),
(18.013198,-76.791069),
(18.012514,-76.790775),
(18.011941,-76.790359),
(18.011916,-76.790335),
(18.011779,-76.7902),
(18.011685,-76.790023),
(18.011547,-76.789819),
(18.011334,-76.789378),
(18.011285,-76.789274),
(18.011195,-76.789072),
(18.010801,-76.788153),
(18.010492,-76.787431),
(18.010272,-76.786879),
(18.010169,-76.78666),
(18.009479,-76.785368),
(18.00945,-76.785312),
(18.009008,-76.784394),
(18.008812,-76.783866),
(18.00879,-76.783789),
(18.008371,-76.78253),
(18.008078,-76.78168),
(18.007943,-76.781315),
(18.007935,-76.78129),
(18.007831,-76.781321),
(18.007662,-76.78138),
(18.007414,-76.78151),
(18.0072864, -76.7812398),
]

path_1 = map_widget.set_path(route_coordinates)
 
map_widget.set_zoom(16) 

mark = 1

def add_marker_event(coords):
    global mark
    print("Add marker:", coords)
    map_widget.set_marker(coords[0], coords[1], text=f"marker {mark}")
    mark += 1
    
def left_click_event(coordinates_tuple):
    global mark
    print("Left click event with coordinates:", coordinates_tuple)
    map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text=f"marker {mark}")
    mark += 1
    
map_widget.add_left_click_map_command(left_click_event)

map_widget.add_right_click_menu_command(label="Add Marker", command=add_marker_event, pass_coords=True)

mainloop()