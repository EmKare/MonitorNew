from tkinter import Tk, ttk, Button, LabelFrame, Canvas, Label, NW, Checkbutton, BooleanVar, \
    Scrollbar, Frame, RIGHT, LEFT, BOTH, Y, Listbox, END, INSERT, Text, CENTER,\
        Entry, ARC
from PIL import Image, ImageTk
from lorem_text import lorem
import phonefiles as files
from random import randint, choice
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from parkingLots import _parkingLots
import openrouteservice as ors
from itertools import islice
from geopy import distance
from time import time

class EditCanvas(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.width, self.height = 400, 750 
        self.geometry(f'{self.width}x{self.height}+10+10')
        self.resizable(False, False)
        
        self.labelFrame = LabelFrame(self, width = self.width-10, height = self.height-10)
        self.labelFrame.place(x = 5, y = 5)
        
        self.mainCanvas = Canvas(self.labelFrame, width = self.width - 20, height = self.height - 20, bg = "#ffffff")
        self.mainCanvas.place(x = 0, y = 0)       
        
        self.client = ors.Client(key = '5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')
        self.distanceService = Nominatim(user_agent = "geoapiExercises")
        
        self.shapes = []
        
        self.mainCanvas.create_rectangle(3, 3, 381, 731, outline = "black", width = 2, tags="main-rectangle")
        self.decorate()
        self.create_rectangle(2,2, 382, 731, fill='snow', alpha=.6, tags = "blur")
        self.termsAgreed, self.canvasCleared  = False, False
        
        self.available_lots = {}
        self.more_available_lots = {}
        self.COUNT = 1
        self.left_click = False
        self.first_weight_const = 0.000001
        self.colours = ['purple', 'gray', 'cadetblue', 'orange', 'pink', 'beige', 'green', 'darkgreen',
                        'lightgreen', 'darkblue', 'lightblue', 'purple', 'lightgray', 'black']
        
        #self.termsAndConditions()
        self.createButtons()
        self.mainloop()
        
    def decorate(self):
        self.mainCanvas.create_polygon([4, 4, (self.width - 20)/2, self.height-20, 4, self.height-20], fill='light sea green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), self.height-20 ,(self.width - 20)/2 , self.height-20], fill='spring green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) * 2, (self.width - 20), self.height-20], fill='medium spring green', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), (self.height - 20) / 3, (self.width - 20), ((self.height - 20) / 3) * 2], fill='aquamarine', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), ((self.height - 20) / 3) / 2, (self.width - 20), (self.height - 20) / 3], fill='SpringGreen2', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2, (self.width - 20), ((self.height - 20) / 3) / 2], fill='PaleGreen1', tags="shapes")
        self.mainCanvas.create_polygon([4, 4, (self.width - 20), 4, (self.width - 20), (((self.height - 20) / 3) / 2) / 2], fill='azure', tags="shapes")
        self.mainCanvas.create_oval(0-30,0-30,0+80,0+80, fill = "yellow2", tags="shapes")
        self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")
    
    def create_rectangle(self, x1:int, y1:int, x2:int, y2:int, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            tags = kwargs.pop('tags')
            fill = self.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.shapes.append(ImageTk.PhotoImage(image))
            self.mainCanvas.create_image(x1, y1, image=self.shapes[-1], anchor='nw', tags = tags)
        self.mainCanvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    
    def createUserButton(self):
        self.userLabelButton = Button(self.mainCanvas, bg = "white", highlightthickness=0, relief="flat", borderwidth=0, )
        image = Image.open(files.no_user)
        image = image.resize((50,50), Image.Resampling.LANCZOS)
        self.userLabel_image = ImageTk.PhotoImage(image)
        self.userLabelButton.config(image = self.userLabel_image, state = "normal")
        self.userLabelButton.place(x = self.mainCanvas.winfo_reqwidth() - self.userLabelButton.winfo_reqwidth() - 4, y = 4,)
    
    def createButtons(self):
        self.createUserButton()
        self.freeUseButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Find Close-By", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white", command = self.appMap)
        self.freeUseButton.config(width = 15, height = 2)
        self.freeUseButton.place(x = int((self.width) / 2) - int(self.freeUseButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) - 60)
        
        self.reserveSpotButton = Button(self.mainCanvas, bg = "forest green", fg = "white", highlightthickness=0, relief="flat", borderwidth=0, text = "Reserve Parking", font = ('bold', 20), activebackground = "lightgreen", activeforeground = "white")
        self.reserveSpotButton.config(width = 15, height = 2)
        self.reserveSpotButton.place(x = int((self.width) / 2) - int(self.reserveSpotButton.winfo_reqwidth() / 2), y = int((self.height - 100) / 2) + 60)
    
    def appMap(self):
        self.clearCanvasToLayMap()
        self.userLabelButton.destroy()
        self.freeUseButton.place_forget()
        self.reserveSpotButton.place_forget()
        self.map_widget = TkinterMapView(self.mainCanvas, width = self.mainCanvas.winfo_reqwidth() - 8, height = self.mainCanvas.winfo_reqheight() - 8, corner_radius = 2)
        self.map_widget.place(x = 4, y = 4)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom = 22,)
        coordinates_tuple = (18.012265695689663, -76.79800557291115)#17.9432311, -76.7466463
        self.map_widget.set_position(coordinates_tuple[0], coordinates_tuple[1], marker = False,)
        
        self.map_widget.set_zoom(16)
        self.map_widget.add_left_click_map_command(self.left_click_event)
        
        self.left_click_event(coordinates_tuple)
        
        #0.005, 
        #if self.canvasCleared:
            #self.createUserButton()
            #self.mainCanvas.create_text(375, self.height - 32, text = 'Capstone Group 3', font = ('bold', 6), anchor = "ne", tags = 'group', activefill = "black")
            
    def create_squares(self, car_pos: tuple):
        self.map_widget.set_position(car_pos[0], car_pos[1], marker = False)
        self.map_widget.set_marker(car_pos[0], car_pos[1], text = "YOU", text_color = "black")
        FIRST_LIMIT = 8
        
        global COUNT, COLOUR
        btn_width, btn_height = 30, 30
        COLOUR = 0
        second_weight_const = 0.02
        EXCLUDE = False
        WEIGHT = self.first_weight_const
        
        doubleup = "\u21EE"
        up = "\u21E7"
        #down = "\u21E9"
        
        self.map_widget.add_right_click_menu_command(label = "Restart", pass_coords = False, command = lambda: self.right_click_event(btn_width, btn_height, up, doubleup), )
        
        while len(self.available_lots) != FIRST_LIMIT :
            for name, coord in _parkingLots.items():
                self.check_if_in_range(car_pos, name, coord, WEIGHT)
            WEIGHT += self.first_weight_const
            self.COUNT += 1
            if WEIGHT >= second_weight_const:
                EXCLUDE = True
                break

        show_more = False        
        if len(self.available_lots) > 0:
            
            for name in self.available_lots.keys():            
                self.calculate_route_distance(car_pos, name, (self.available_lots[name][0][0], self.available_lots[name][0][1]), self.available_lots)
            
            if not EXCLUDE:
                self.exclude_already_added(car_pos, WEIGHT, second_weight_const)
                show_more = True
                
                cap = 5
                for lot in islice(self.more_available_lots.items(), cap):
                    self.calculate_route_distance(car_pos, lot[0], (lot[1][0][0], lot[1][0][1]), self.more_available_lots)

        self.addSearch_andResults(car_pos, up, doubleup, btn_width, btn_height, show_more)
        
    def check_if_in_range(self, car_pos: tuple, name: str, coord: tuple, weight: float):    
        lat = coord[0]
        lon = coord[1]
        if car_pos[0] + weight > lat and lon > car_pos[1] - weight:
            if car_pos[0] + weight > lat and lon < car_pos[1] + weight:
                if car_pos[0] - weight < lat and lon < car_pos[1] + weight:
                    if car_pos[0] - weight < lat and lon > car_pos[1] - weight:
                        self.add_to_map(car_pos, name, coord, weight)                    

    def add_to_map(self, car_pos: tuple, name: str, coord: tuple, weight: float):
        if name not in self.available_lots.keys():
            variables = []
            variables.append(coord)
            self.available_lots[name] = variables

    def calculate_route_distance(self, car_pos: tuple, name: str, found_lot: tuple, lots_dict: dict, draw_marker: bool = False, draw_route: bool = False,): 
        route = self.client.directions(coordinates = [[car_pos[1], car_pos[0]], [found_lot[1], found_lot[0]]],
                                profile = 'driving-car', format = 'geojson',)
        route_coordinates = [tuple(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
        route_coordinates.insert(0, tuple(car_pos))
        route_coordinates.insert(len(route_coordinates), (found_lot[0], found_lot[1]))
        if draw_marker:
            self.map_widget.set_marker(found_lot[0],found_lot[1], text = name, text_color = "green")
        if draw_route:
            self.map_widget.set_path(position_list = route_coordinates, color = self.colours[COLOUR], width = 2)
            COLOUR += 1
            
        route_distance, start, end = 0, 0, 1
        while end < len(route_coordinates): # <<<<<<<<< HERESO
            route_distance += distance.distance(route_coordinates[start], route_coordinates[end]).km
            start += 1
            end += 1

        lots_dict[name].append(distance.distance(car_pos, found_lot).km)
        lots_dict[name].append(route_coordinates)
        lots_dict[name].append(route_distance)

    def exclude_already_added(self, car_pos: tuple, weight2: float, final_weight: float):
        while weight2 <= final_weight:
            for name, coord in _parkingLots.items():
                if name not in self.available_lots.keys():
                    self.check_for_others(car_pos, name, coord, weight2)
                weight2 += self.first_weight_const       
                    
    def check_for_others(self, car_pos: tuple, name: str, coord: tuple, weight2: float):
        lat = coord[0]
        lon = coord[1]
        if car_pos[0] + weight2 > lat and lon > car_pos[1] - weight2:
            if car_pos[0] + weight2 > lat and lon < car_pos[1] + weight2:
                if car_pos[0] - weight2 < lat and lon < car_pos[1] + weight2:
                    if car_pos[0] - weight2 < lat and lon > car_pos[1] - weight2:
                        if name not in self.more_available_lots.keys():
                            variables = []
                            variables.append(coord)
                            self.more_available_lots[name] = variables

    def addSearch_andResults(self, car_pos:tuple, up:str, doubleup:str, btn_width:int, btn_height:int, show_more:bool = False,):

        self.entry_width = 220
        search_colour = "gray78"
        self.results_canvas_mini_height = 50
        self.results_canvas_mid_height = 380
        self.results_canvas_full_height = 710
        
        canvas_height = self.results_canvas_mini_height       
        
        self.searchFrame = Frame(self.mainCanvas, bd = 0, bg = search_colour, width = self.mainCanvas.winfo_reqwidth() - 100, height = 32)
        self.searchFrame.place(x = 50, y = 20,)
        
        self.findLocation = Entry(self.searchFrame, bd = 0, bg = search_colour, font = ('bold',15), relief = "flat", highlightthickness = 0, border = 0, fg = "gray18")
        self.findLocation.place(x = 10, y = 1, width = self.entry_width, height = 30)
        
        self.clearButton = Button(self.searchFrame, text = "x", relief = "flat", bg = search_colour, activebackground = "#ffffff", bd = 0, highlightthickness = 0, border = 0, activeforeground = "red", command = lambda : self.clearEntry(),)
        self.clearButton.place(x = self.entry_width + 10 , y = 1, width = 20, height = 30)
        
        self.searchButton = Button(self.searchFrame, text = "find", relief = "flat", bg = "lightgray", fg = "green", activebackground = "lightgray", activeforeground = "green", bd= 0, highlightthickness = 0, border = 0,)# command = lambda : self.searchMap())
        self.searchButton.place(x = self.searchFrame.winfo_reqwidth() - 36, y = 1, width = 35, height = 30)
        
        self.resultsCanvas = Canvas(self.mainCanvas, bg = search_colour, bd= 0, highlightthickness = 0, border = 0,)
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        #self.can_it_curve(self.resltsCanvas, self.mainCanvas.winfo_reqwidth() - 20, canvas_height, "#ffffff",topleft=True, topright=True)
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        self.resultsLabel = Label(self.resultsCanvas, text = f"Results:  {len(self.available_lots)}", font = ("calibri", 18, 'bold'), bg = search_colour)
        self.resultsLabel.place(x = 10, y = 7)        
        
        #self.resultsCanvas.create_line(int(self.resultsCanvas.winfo_reqwidth()/2),0,int(self.resultsCanvas.winfo_reqwidth()/2),100, width = 5, activefill = "red")
        
        self.resultsCanvas.create_line(159,10,221,10, width = 5, fill = "gray64")
        
        self.results_halfScreen = Canvas(self.resultsCanvas, relief = "flat", bg = search_colour, borderwidth = 0, bd = 0, highlightthickness = 0, border = 0,)
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = up, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = up,
                                     e = doubleup,
                                     #f = results_canvas_mini_height,
                                     #g = results_canvas_full_height
                                     : 
                                     self.midimize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_halfScreen.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief = "flat"))
        self.results_halfScreen.place(x = 159, y = 15, width = btn_width, height = btn_height)     
        
        self.results_fullScreen = Canvas(self.resultsCanvas, relief = "flat", bg = search_colour, borderwidth = 0, bd = 0, highlightthickness = 0, )
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = doubleup, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = up,
                                     e = doubleup,
                                     #f = results_canvas_mini_height,
                                     #g = results_canvas_mid_height
                                     : 
                                     self.maximize_resultsCanvas(event, a, b, c, d, e,))
        self.results_fullScreen.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief = "flat"))
        self.results_fullScreen.place(x = 191, y = 15, width = btn_width, height = btn_height)
        
        self.sideWidgetDataPanel = Canvas(self.resultsCanvas, bg = "lightblue", bd= 0, highlightthickness = 0, border = 0,)
        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 18, height = canvas_height - 60 )
        
        self.populate_scroll(car_pos)
        
        if show_more:
            ADDITIONAL = 5
            self.show_more_button = Button(self.resultsCanvas, text = "Show More", bg = search_colour, font = ("calibri", 10, 'bold', 'underline'), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black", command = lambda: self.show_more_lots(car_pos, ADDITIONAL))
            self.show_more_button.place(x = self.resultsCanvas.winfo_reqwidth() - 120, y = 13, width = 80, height = 30)
        
        self.closeResults = Button(self.resultsCanvas, text = "X", font = ("calibri", 10, 'normal',), relief = "flat", fg = "#ffffff", bg = "gray64", activeforeground = "black", activebackground = "gray64", bd = 0, highlightthickness = 0, border = 0, command = lambda: self.right_click_event(btn_width, btn_height, up, doubleup))
        self.closeResults.place(x = self.resultsCanvas.winfo_reqwidth() - 40, y = 7, width = 20, height = 20)

    def show_more_lots(self, car_pos:tuple, additional:int,):    
        count = 0
        keys_to_remove = []

        for key in self.more_available_lots:
            if count < additional:
                keys_to_remove.append(key)
                count += 1
            else:
                break

        for key in keys_to_remove:
            self.calculate_route_distance(car_pos, key, (self.more_available_lots[key][0][0], self.more_available_lots[key][0][1]), self.more_available_lots, draw_marker = False)
            self.available_lots[key] = self.more_available_lots[key]
            del self.more_available_lots[key]
        
        self.resultsLabel.config(text = f"Results:  {len(self.available_lots)}")
        
        self.populate_scroll(car_pos)
        
    def minimize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str, ):
        self.map_widget.set_position(car_pos[0] , car_pos[1], marker = False,)
        canvas_height = self.results_canvas_mini_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height3
                                     : 
                                     self.midimize_resultsCanvas(event, a, b, c, d, e, ))

        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height2
                                     : 
                                     self.maximize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow2, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 18, height = canvas_height - 60,)

    def midimize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str,):
        self.map_widget.set_position(car_pos[0] - 0.004, car_pos[1], marker = False,)
        canvas_height = self.results_canvas_mid_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height, 
                                     #g = canvas_height3
                                     : 
                                     self.minimize_resultsCanvas(event, a, b, c, d, e,))
        
        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height,
                                     #g = canvas_height2,
                                     : 
                                     self.maximize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 18, height = canvas_height - 60,)
    
    def maximize_resultsCanvas(self, event, car_pos:tuple, btn_width:int, btn_height:int, arrow1:str, arrow2:str, ):
        canvas_height = self.results_canvas_full_height
        event.widget.configure(relief="sunken", border = 1,)
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.resultsCanvas.delete("results-rect")
        
        self.resultsCanvas.create_rectangle(0,0,self.mainCanvas.winfo_reqwidth()-21,canvas_height+1, width = 1, tags = "results-rect")
        
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        
        self.results_halfScreen.bind("<ButtonPress-1>", 
                                     lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height2, 
                                     #g = canvas_height
                                     : 
                                     self.midimize_resultsCanvas(event, a, b, c, d, e, ))
        
        self.results_fullScreen.bind("<ButtonPress-1>", lambda event, 
                                     a = car_pos, 
                                     b = btn_width, 
                                     c = btn_height, 
                                     d = arrow1,
                                     e = arrow2,
                                     #f = canvas_height3,
                                     #g = canvas_height,
                                     : 
                                     self.minimize_resultsCanvas(event, a, b, c, d, e,))
        
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow1, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "180", anchor = "center", text = arrow2, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        
        self.sideWidgetDataPanel.place(x = 2, y = 60, width = self.resultsCanvas.winfo_reqwidth() - 18, height = canvas_height - 60,)

    def populate_scroll(self, car_pos:tuple,):
        try:
            self.frame.destroy()
        except Exception:
            pass        
        try:
            self.main.destroy() 
        except Exception:
            pass
        
        fullstar = "\u2605"
        nullstar = "\u2606"
        parking_types = ["Public Parking", "Private Parking", "Paid Parking"]
        
        self.create_scroll(self.sideWidgetDataPanel)

        for name, data_list in sorted(self.available_lots.items(), key = lambda item: item[1][3]):

            c = Canvas(self.frame, bg="azure", width = self.sideWidgetDataPanel.winfo_reqwidth() - 22, height = 140,)
            c.pack(fill="both", expand=True, )
            
            title = Label(c, text = name, font = ('bold', 15, 'underline'), bg = "azure")
            title.place(x = int(c.winfo_reqwidth()/2) - int(title.winfo_reqwidth()/2), y = 5)
            
            review = Label(c, text = self.getReview(fullstar, nullstar), font = ('bold', 13), bg = "azure", fg= "lightgray")
            review.place(x = 20, y = 50)
            
            distance = Label(c, text = f"Distance: {data_list[3]:.2f} kms", font = ('bold', 12), bg = "azure", )
            distance.place(x = 20, y = 70)    
            
            parking = Label(c, text = choice(parking_types), font = ('bold', 12), bg = "azure", )
            parking.place(x = 20, y = 90)
            
            open = Label(c, text = self.opening_hours(), font = ('bold', 12), bg = "azure", fg= "green")
            open.place(x = 20, y = 115)

            b1 = Button(c, text = "Select", font = ('bold', 15), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")
            b1.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 85, width = 80, height = 30)
            
            b2 = self.setButton(c, name, data_list[0], car_pos, data_list[2])
            b2.place(x = c.winfo_reqwidth() - 100, y = c.winfo_reqheight() - 45, width = 80, height = 30)
    
    def opening_hours(self):
        type = randint(0,1)
        if type:
            return "Open 24 Hours"
        else:
            closing_times = [6,7,8,9,10]
            return f"Open. Closes {choice(closing_times)}PM "
    
    def getReview(self, fullstar:str, nullstar:str):
        max = 5
        rating = randint(0, max)
        if rating == 0:
            return "No Reviews"
        elif rating == max:
            review = ""
            while rating > 0:
                review = review + fullstar
                rating-=1
            return review
        else:
            review = ""
            extra = max - rating
            while rating > 0:
                review = review + fullstar
                rating-=1
            while extra > 0:
                review = review + nullstar
                extra-=1
            return review           

    def create_scroll(self, canvas_frame:Canvas):
        self.main = Canvas(canvas_frame, bd = 0, highlightthickness = 0, border = 0,)
        self.main.pack(side="left", fill="both", expand=True)
        #create a new 'canvas' canvas in the 'main canvas, preset with the width and height of 'mainCanvas'
        canvas = Canvas(self.main, bg = "#ffffff", borderwidth=0, width=canvas_frame.winfo_reqwidth(), height=100, bd= 0, highlightthickness = 0, border = 0,)#canvas_frame.winfo_reqheight())
        ##create a new 'frame' canvas in the 'canvas' canvas, preset with the width and height of 'mainCanvas' ♠
        self.frame = Canvas(canvas, bg = "#ffffff", borderwidth=0, width = canvas_frame.winfo_reqwidth(), height = canvas_frame.winfo_reqheight() - 200, bd= 0, highlightthickness = 0, border = 0,)
        #'vsb' is a Scrollbar event, and it is placed on self
        vsb = Scrollbar(self, orient="vertical", command=canvas.yview)
        #sets a yscrollcommand for the 'canvas' widget
        canvas.configure(yscrollcommand=vsb.set)
        #places the scrollbar off screen
        vsb.place(x = canvas_frame.winfo_reqwidth()+30, y = 0)
        #packs the 'camvas' widet into the 'main' widget
        canvas.pack(side="left", fill="both", expand=True)
        #sets the 'frame' widget as a window of the 'canvas' widget
        canvas.create_window((0,0), window= self.frame, anchor="nw",tags="frame",)
        #binds 2 functions to the canvas, and 1 to the frame
        self.frame.bind("<Configure>", lambda event, canvas = canvas: self.onFrameConfigure(event, canvas))
        canvas.bind_all("<MouseWheel>", lambda event, canvas = canvas: self._on_mousewheel(event, canvas))
        #canvas.bind_all("<Double-Button-1>", backtoHome)
        
    #this function configues the 'canvas' canvas
    def onFrameConfigure(self, event, canvas:Canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    #this function configues the 'canvas' canvas scroll type
    def _on_mousewheel(self, event, canvas:Canvas):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
        
    def setButton(self, c:Canvas, name:str, coord:tuple, car_pos:tuple, route_coordinates:list):
        return Button(c, text="Route", font = ('bold',15), command = lambda : self.drawSpecificRoute(car_pos, coord, name, route_coordinates), highlightthickness = 0, relief = "flat", borderwidth = 0, fg = "black")
    
    def drawSpecificRoute(self, car_pos:tuple, coord:tuple, name:str, route_coordinates:list):
        #middle = route_coordinates[int(len(route_coordinates)/2)]
        #self.map_widget.set_position(middle[0], middle[1], marker = False) (18.0073643 -76.7982349)
        try:
            self.map_widget.delete_all_path()
        except Exception:
            pass
        try:
            self.map_widget.delete_all_marker()
        except Exception:
            pass
        self.map_widget.set_path(position_list = route_coordinates, color = "purple", width = 5)
        self.map_widget.set_marker(coord[0],coord[1], text = name, text_color = "green")
        self.map_widget.set_marker(car_pos[0], car_pos[1], text = "YOU", text_color = "black")

    def clearEntry(self):
        #self.hasRoute = False
        self.findLocation.delete(0, END)
        
    def clearCanvasToLayMap(self):
        self.mainCanvas.delete("shapes")
        self.mainCanvas.delete("group")
        self.canvasCleared = True
        
    def left_click_event(self, coordinates_tuple: tuple):
        if not self.left_click:
            self.COLOUR = 0
            self.left_click = True
            start = time()
            print("Finding FMP parking for coordinates:", coordinates_tuple)
            self.map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1], text = "YOU", text_color = "blue")
            self.create_squares(coordinates_tuple)
            end = time()
            print(f'Execution time: {(end - start):.2f} seconds')
            print("------------------------------------------------------------------------------------------")

    def right_click_event(self, btn_width:int, btn_height:int, up:str, doubleup:str):
        canvas_height = self.results_canvas_mini_height
        try:
            self.map_widget.delete_all_polygon()
        except Exception:
            pass
        try:
            self.map_widget.delete_all_marker()
        except Exception:
            pass
        try:
            self.map_widget.delete_all_path()
        except Exception:
            pass
        try:
            self.available_lots.clear()
            self.more_available_lots.clear()
        except Exception:
            pass
        try:
            self.frame.destroy()
        except Exception:
            pass        
        try:
            self.main.destroy() 
        except Exception:
            pass
        try:
            self.results_halfScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass        
        try:
            self.results_fullScreen.unbind("<ButtonPress-1>")
        except Exception:
            pass
        self.show_more_button.destroy()
        self.results_halfScreen.delete("arrow")
        self.results_fullScreen.delete("arrow")
        self.results_halfScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = up, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")        
        self.results_fullScreen.create_text((btn_width/2, btn_height/2), angle = "0", anchor = "center", text = doubleup, font = ("calibri", 20, 'normal',), fill="SystemButtonText", tags = "arrow")
        self.resultsLabel.config(text = "No Results")
        self.resultsCanvas.place(x = 10, y = self.mainCanvas.winfo_reqheight() - canvas_height - 4, width = self.mainCanvas.winfo_reqwidth() - 20, height = canvas_height,)
        self.left_click = False

    def termsAndConditions(self):
        self.mainCanvas.create_text(50, 130, text = "->", activefill = "red", tags = "terms")
               
        self.termsAndConditionsBox = Text(self.mainCanvas, width = 32, height = 19, font = ("calibri", 12), relief = "flat", )
        self.termsAndConditionsBox.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight()) + 150)
        self.termsAndConditionsBox.insert(INSERT, "\n\n")
        self.termsAndConditionsBox.insert(INSERT, self.getText())
        
        self.headerLabel = Label(self.mainCanvas, text = "TERMS AND CONDITIONS", font = ("calibri", 14, 'underline'), bg = "#ffffff")
        self.headerLabel.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = 132, width = self.termsAndConditionsBox.winfo_reqwidth(), height = 30)
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) - int(self.termsAndConditionsBox.winfo_reqheight()) - int(self.headerLabel.winfo_reqheight()) + 158, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 243, 
        outline = "black", width = 2, tags = "terms")
        
        self.check_variable = BooleanVar()
        self.agree_disagree = Checkbutton(self.mainCanvas, text = "   I accept these Terms and Conditions  ", onvalue = 1, offvalue = 0, font = ('bold', 10), bg = "#ffffff", variable = self.check_variable, command = self.toggle_button_state, )
        self.agree_disagree.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2), y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 242,)        
        
        self.mainCanvas.create_rectangle(
            int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2,
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 244, 
            int(self.mainCanvas.winfo_reqwidth() / 2) + int(self.termsAndConditionsBox.winfo_reqwidth() / 2) + 2, 
            int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 214, 
        outline = "black", width = 2, tags = "terms")
        
        self.acceptTermsAndConditionButton = Button(self.mainCanvas, text = "continue", font = ('bold', 12), relief = "flat", state = "disabled", command = self.termsAndContidionsAgreed)
        self.acceptTermsAndConditionButton.place(x = int(self.mainCanvas.winfo_reqwidth() / 2) - int(self.termsAndConditionsBox.winfo_reqwidth() / 2) - 2, y = int(self.mainCanvas.winfo_reqheight() / 2) + int(self.termsAndConditionsBox.winfo_reqheight()) + int(self.headerLabel.winfo_reqheight()) - 213, width = int(self.termsAndConditionsBox.winfo_reqwidth() + 4))

    def termsAndContidionsAgreed(self):
        self.termsAgreed = True
        self.mainCanvas.delete("terms")
        self.mainCanvas.delete("blur")
        self.agree_disagree.destroy()
        self.headerLabel.destroy()
        self.termsAndConditionsBox.destroy()
        self.acceptTermsAndConditionButton.destroy()
        self.createButtons()
        
    def getText(self):
        text = lorem.words(15) + "\n\n" + lorem.paragraph()
        cap = 0
        while cap <= 12:
            text = f"{text}\n\n{cap+1})     {lorem.paragraph()}"
            cap += 1
        return text + "\n\nNB:     " + lorem.words(15)
    
    def toggle_button_state(self):
        if self.check_variable.get():
            self.acceptTermsAndConditionButton.config(state = "normal")
        else:
            self.acceptTermsAndConditionButton.config(state = "disabled")

    def can_it_curve(self, canvas: Canvas, width: int, height: int, bg_color: str, topleft: bool = False, topright: bool = False, bottomleft: bool = False, bottomright: bool = False):
        radius = 25
        pos_corr = -1
        if bottomright:
            canvas.create_arc(width - 2 * radius + 5 + pos_corr, height - 2 * radius + 5 + pos_corr, width + 5 + pos_corr, height + 5 + pos_corr, style=ARC, tag="corner", width=10, outline=bg_color, start=-90) #bottom right
        if bottomleft:
            canvas.create_arc(2 * radius - 5, height - 2 * radius + 5 + pos_corr, -5, height + 5 + pos_corr, style=ARC, tag="corner", width=10, outline=bg_color, start=180) #bottom left
        if topleft:
            canvas.create_arc(-5, -5, 2 * radius - 5, 2 * radius - 5, style=ARC, tag="corner", width=10, outline=bg_color, start=-270) #top left
        if topright:
            canvas.create_arc(width - 2 * radius + 5 + pos_corr, -5, width + 5 + pos_corr, 2 * radius - 5, style=ARC, tag="corner", width=10, outline=bg_color, start=0) #top right
  
EditCanvas()