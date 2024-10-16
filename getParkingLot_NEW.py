from files import rel_path
                
class ParkingLotInfo:
    def __init__(self, lotname:str, rel_path = rel_path,):
        self.path = rel_path + lotname + "/"  #sets class path
        file_type = ".txt" #to be appended to future file paths
        self.spots = f"{self.path}{lotname}{file_type}" #file with all spots in parking lot
        self.map = f"{self.path}{lotname}_map{file_type}" #file with parking lot map layout
        self.sides = f"{self.path}{lotname}_sides{file_type}" #file with parking lot's rows and lot numbers
        self.type = f"{self.path}{lotname}_type{file_type}" #file with parking lot columns and lot numbers
        self.name = f"{self.path}{lotname}_name{file_type}"
        self.imagepath = f"{self.path}{lotname}_logo.png"
        
        self.newsize = (350, 300)
        
        #self.ParkingLot_name = self.getName() #name of the parking lot
        self.ParkingLot_mapcontents = self.getContents() #gets the map layout for the parking lot
        self.ParkingLot_sides = [] #list for parking lot's rows and lot numbers
        self.ParkingLot_spotsStatuses = [] #list for all spots in parking lot
        self.ParkingLot_availableSpots = [] #list for all available spots in parking lot
        self.ParkingLot_amountAvailable = 0 #amount of available spots in parking lot
        self.ParkingLot_number = self.getType() #gets the parking lot number
        
        self.getSides() #gets parking lot's rows and lot numbers
        self.getSpots() #gets all spots in parking lot
        self.getAvailableSpots() #gets all available spots in parking lot
        self.getImage() #gets logo image for parking lot
    
    def getType(self):
        with open(self.type) as f: #this file only has 1 number in it
            return int((f.read().strip()))
        
    def getName(self):
        with open(self.name) as f: #this file contains the map of the parking lot
            return f.read()
    
    def getContents(self):
        with open(self.map) as f: #this file contains the map of the parking lot
            return f.read()
        
    def getImage(self):
        from PIL import ImageTk, Image
        self.image = ImageTk.PhotoImage(Image.open(f"{self.imagepath}").resize((self.newsize), Image.Resampling.LANCZOS))
                
    def getSides(self):
        import re
        with open(self.sides) as f: #this file contains the parking lot's rows and lot numbers
            for line in f:
                word = line.rstrip().split(",")
                spots = []
                pos = re.sub(r"[\([{'""'})\]]", "", word[0])
                spots.append(str(pos.strip("\""))) #row letter
                spots.append(int(word[1].strip(")"))) #highest number in row
                spots.append(int(word[2].strip(")"))) #lowest number in row
                self.ParkingLot_sides.append(spots) 

    def getSpots(self):
        with open(self.spots) as f: #this file contains all the spots in the parking lot
            for line in f:
                word = line.rstrip().split('#')
                spots = []
                spots.append(word[1].strip()) #name
                spots.append(word[2].strip()) #status
                spots.append(int(word[0].strip())) #index
                self.ParkingLot_spotsStatuses.append(spots)
    
    def getAvailableSpots(self):
        for spot in self.ParkingLot_spotsStatuses: #from the list of all spots in parking lot...
            if spot[1] == "A": #if the spot is marked with an "A", meaning available...
                self.ParkingLot_availableSpots.append(spot) #add that spot to the available spots list 
        self.ParkingLot_amountAvailable = len(self.ParkingLot_availableSpots)