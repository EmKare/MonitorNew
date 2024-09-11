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
#map_widget.place(relx=0.5, rely=0.5, anchor=CENTER)

# example tile sever:
#map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
#map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
#map_widget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
#map_widget.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")  # black and white
#map_widget.set_tile_server("https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png")  # detailed hiking
#map_widget.set_tile_server("https://tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png")  # no labels
#map_widget.set_tile_server("https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg")  # swisstopo map

# example overlay tile server
#map_widget.set_overlay_tile_server("http://tiles.openseamap.org/seamark//{z}/{x}/{y}.png")  # sea-map overlay
#map_widget.set_overlay_tile_server("http://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png")  # railway infrastructure


#map_widget.set_position(22.6927737, 114.2805821, marker=False)  #google map
#map_widget.set_marker(22.6927737, 114.2805821, text="Home")

map_widget.set_position(18.007943,-76.781315, marker=False)  #google map 
#map_widget.set_marker(18.007943,-76.781315, text="Ja")

marker_2 = map_widget.set_marker(18.0118757, -76.7968643, text="start")
marker_3 = map_widget.set_marker(18.0072864, -76.7812398, text="end")

#coords = [[-76.7968643, 18.0118757], [-76.7812398, 18.0072864]]
#route = client.directions(coordinates=coords,
#                          profile='driving-car',
#                          format='geojson',)

#waypoints = list(dict.fromkeys(reduce(operator.concat, list(map(lambda step: step['way_points'], route['features'][0]['properties']['segments'][0]['steps'])))))
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
#[18.011877,-76.796858],[18.011164,-76.79674],

#map_widget.set_address("Tokyo Japan", marker = False)
#map_widget.set_address("United States", marker = False)

# set current widget position and zoom
#map_widget.set_position(22.6962768, 114.2749194, marker=True)  #default map
 
map_widget.set_zoom(14) 

mainloop()