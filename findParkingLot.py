from tkintermapview import TkinterMapView
from tkinter import Tk, mainloop, CENTER, Canvas, Label, Scrollbar, Button
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
root_tk.title("Find FMP Parking Lots")
root_tk.resizable(False,False)


map_widget = TkinterMapView(root_tk, width = width, height = height, corner_radius = 2)
map_widget.pack(fill = "both")
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22)
#map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

car_pos = (17.9394675, -76.7665624)  #airport                 || squares: 116 | 1.31 seconds | total available_lots found: 5
#car_pos = (18.012265695689663, -76.79800557291115) #hwt       || squares: 26  | 1.46 seconds | total available_lots found: 55
#car_pos = (17.966814698972417, -76.80206888632081) #downtown  || squares: 71  | 1.36 seconds | total available_lots found: 19

#map_widget.set_position(18.012265695689663, -76.79800557291115, marker = False)
#map_widget.set_position(17.9432311, -76.7466463, marker = False)
map_widget.set_position(car_pos[0], car_pos[1], marker = False)
#map_widget.set_marker(car_pos[0], car_pos[1], text = "car")
#map_widget.set_position(39.0437, -77.4875, marker = True)

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
    #'darkpurple',
    'lightgray',
    'black'
]

def create_squares(car_pos: tuple):
    map_widget.set_position(car_pos[0], car_pos[1], marker = False)
    global count, colour
    colour = 0
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
    
    if len(available_lots) > 0:
        print(f"close available FMP lots: {len(available_lots)}")
        
        for name in available_lots.keys():            
            calculate_route_distance(car_pos, name, (available_lots[name][0][0], available_lots[name][0][1]),)# draw = True)

        if not exclude:
            exclude_already_added(car_pos, weight, second_weight_const)
            print(f"other available FMP lots: {len(more_available_lots)}")
            
            cap = 5
            for lot in islice(more_available_lots.items(), cap):
                calculate_route_distance(car_pos, lot[0], (lot[1][0], lot[1][1]),)
                map_widget.set_marker(lot[1][0], lot[1][1], text = lot[0], text_color = "red")

            print(f"total available FMP lots found: {len(available_lots) + len(more_available_lots)}")
    else:
        print(f"There are {len(available_lots)} FMP parking lots close by.")
    
    #WORK STARTS HERE
    drawSideWidget(car_pos, available_lots)

def drawSideWidget(car_pos: tuple, available_lots: dict): # width, height = 1200, 800
    global width, height, sideWidget
    sideWidget = Canvas(map_widget, bg = "#ffffff")
    sideWidget.place(x = width - 300, y = 0, width = 300, height = height)
    
    sideWidgetHeader = Label(sideWidget, text = f"Location: ({car_pos[0]:.3f} , {car_pos[1]:.3f})", font = ("calibri", 18, 'bold',), bg = "#ffffff", justify = "center")
    sideWidgetHeader.place(x = 15, y = 25)
    sideWidget.create_line(0, 70, width, 70, activefill = "black", smooth = False, width = 2)
    sideWidget.create_line(0, 80, width, 80, activefill = "black", smooth = False, width = 2)
    sideWidget.create_text(55, 110, text = "Results", font = ("calibri", 18, 'bold'), justify = "left")
        
    sideWidgetDataPanel = Canvas(sideWidget, bg = "lightblue")
    sideWidgetDataPanel.place(x = 0, y = 140, width = 300, height = height - 180)
    
    create_scroll(sideWidgetDataPanel)
    
    sideWidget.create_text(295, height - 35, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")

    global frame
    for name, data_list in available_lots.items():# name: str, data_list: list
        #data_list[coods: tuple, straight:float, route_coord: list]
        c = Canvas(frame, bg="azure", width= frame.winfo_reqwidth() - 4, height= 140,)
        c.pack(fill="both", expand=True, )
        #c.bind("<Button-1>", printer)
        
        route_distance, start, end = 0, 0, 1
        while end < len(data_list[2]):
            route_distance += distance.distance(data_list[2][start], data_list[2][end]).km
            start += 1
            end += 1
        
        c.create_text(int(c.winfo_reqwidth()/2) , 25, text = name, font = ('bold', 15, 'underline'), justify = "center", anchor = "center", tags = 'text')
        c.create_text(int(c.winfo_reqwidth()/5), 50, text = "No Reviews", font = ('bold', 13), justify = "left", anchor = "n", fill= "lightgray", tags = 'text')        
        c.create_text(int(c.winfo_reqwidth()/4), 70, text = f"Distance: {route_distance:.2f} kms", font = ('bold', 12), justify = "left", anchor = "n", tags = 'text')
        c.create_text(int(c.winfo_reqwidth()/5), 90, text = "Public Parking", font = ('bold', 12), justify = "center", anchor = "n", tags = 'text') 
        c.create_text(int(c.winfo_reqwidth()/4), 115, text = "Open. Closes 6PM ", font = ('bold', 12), justify = "center", anchor = "n", fill= "green", tags = 'text')
        #292 , 144
        b1 = Button(c, text = "Select", font = ('bold', 15), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")
        b1.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 85, width = 80, height = 30)
        
        b2 = setButton(c, name, data_list[2])
        b2.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 45, width = 80, height = 30)
        
def setButton(c, name, route_coordinates):
    return Button(c, text="Route", font = ('bold',15), command = lambda : drawSpecificRoute(name, route_coordinates), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")    

def drawSpecificRoute(name, route_coordinates):
    #print(f"clicked {name}")
    middle = route_coordinates[int(len(route_coordinates)/2)]
    map_widget.set_position(middle[0], middle[1], marker = False)
    try:
        map_widget.delete_all_path()
    except Exception:
        pass
    map_widget.set_path(position_list = route_coordinates, color = "purple", width = 5)
    
def create_scroll(canvas_frame: Canvas):
    main = Canvas(canvas_frame, )
    main.pack(side="left", fill="both", expand=True)
    #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
    canvas = Canvas(main, bg = "green", borderwidth=0, width=canvas_frame.winfo_reqwidth(), height=100)#canvas_frame.winfo_reqheight())
    ##create a new 'frame' canvas in the 'canvas' canvas, preset with the width and height of 'mainCanvas'
    global frame
    frame = Canvas(canvas, bg = "red", borderwidth=0, width = canvas_frame.winfo_reqwidth() - 94, height = canvas_frame.winfo_reqheight() - 200)
    #'vsb' is a Scrollbar event, and it is placed on self
    vsb = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    #sets a yscrollcommand for the 'canvas' widget
    canvas.configure(yscrollcommand=vsb.set)
    #places the scrollbar off screen
    vsb.place(x = canvas_frame.winfo_reqwidth()+30, y = 0)
    #packs the 'camvas' widet into the 'main' widget
    canvas.pack(side="left", fill="both", expand=True)
    #sets the 'frame' widget as a window of the 'canvas' widget
    canvas.create_window((4,4), window=frame, anchor="nw",tags="frame",)
    #binds 2 functions to the canvas, and 1 to the frame
    frame.bind("<Configure>", lambda event, canvas = canvas: onFrameConfigure(event, canvas))
    canvas.bind_all("<MouseWheel>", lambda event, canvas = canvas: _on_mousewheel(event, canvas))
    #canvas.bind_all("<Double-Button-1>", backtoHome)

#this function configues the 'canvas' canvas
def onFrameConfigure(event, canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

#this function configues the 'canvas' canvas scroll type
def _on_mousewheel(event, canvas):
    try:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    except Exception:
        pass   
    
def check_if_in_range(car_pos: tuple, name: str, coord: tuple, weight: float):    
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight > lat and lon > car_pos[1] - weight:
        if car_pos[0] + weight > lat and lon < car_pos[1] + weight:
            if car_pos[0] - weight < lat and lon < car_pos[1] + weight:
                if car_pos[0] - weight < lat and lon > car_pos[1] - weight:
                    add_to_map(car_pos, name, coord, weight)                    

def add_to_map(car_pos: tuple, name: str, coord: tuple, weight: float):
    if name not in available_lots.keys():
        variables = []
        variables.append(coord)
        available_lots[name] = variables
        draw_square(car_pos, weight, "darkred")
        try:
            map_widget.set_marker(coord[0],coord[1], text = name, text_color = "green")
        except Exception:
            print(f"error @ {name} with {coord}")
        #print(f"{count}: {name} @ weight: {weight}")

def draw_square(car_pos: tuple, weight: float, colour: str):
    map_widget.set_polygon([(car_pos[0] + weight, car_pos[1] - weight),
                            (car_pos[0] + weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] + weight),
                            (car_pos[0] - weight, car_pos[1] - weight),],
                            outline_color = colour, border_width = 2)
        
def exclude_already_added(car_pos: tuple, weight2: float, final_weight: float):
    while weight2 <= final_weight:
        for name, coord in _parkingLots.items():
            if name not in available_lots.keys():
                check_for_others(car_pos, name, coord, weight2)
            weight2 += first_weight_const       
                
def check_for_others(car_pos: tuple, name: str, coord: tuple, weight2: float):
    lat = coord[0]
    lon = coord[1]
    if car_pos[0] + weight2 > lat and lon > car_pos[1] - weight2:
        if car_pos[0] + weight2 > lat and lon < car_pos[1] + weight2:
            if car_pos[0] - weight2 < lat and lon < car_pos[1] + weight2:
                if car_pos[0] - weight2 < lat and lon > car_pos[1] - weight2:
                    if name not in more_available_lots.keys():
                        more_available_lots[name] = coord
                        #print(f"{count}: {name} @ weight: {weight2}")                        

def calculate_route_distance(car_pos: tuple, name: str, found_lot: tuple, draw: bool = False): 
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
    """    
    print(f"car to ***{name}*** has {len(route_coordinates)} points")
    
    route_distance, start, end = 0, 0, 1
    while end < len(route_coordinates):
        route_distance += distance.distance(route_coordinates[start], route_coordinates[end]).km
        start += 1
        end += 1
    """ 
    available_lots[name].append(distance.distance(car_pos, found_lot).km)
    available_lots[name].append(route_coordinates)
    
def left_click_event(coordinates_tuple: tuple):
    global left_click
    if not left_click:
        global colour
        colour = 0
        left_click = True
        start = time()
        print("Finding FMP parking for coordinates:", coordinates_tuple)
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
    try:
        global sideWidget
        sideWidget.destroy()
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