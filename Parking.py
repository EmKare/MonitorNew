
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class ParkingLot():
    def __init__(self, contents,lot_sides,start,goal,typer,spot,imagename,lotnumber):
        self.typer = typer
        self.spot = spot
        self.imagename = imagename
        self.lot_sides = lot_sides
        self.lotnumber = int(lotnumber)
        #START OF MY TING
        self.spots_before = []
        start_spot = str(start)
        end_spot = str(goal)
        #This will work when the goal is a parking spot/ populates "self.spots_before"
        try:
            self.getPreviousLots(int(goal)) 
        except Exception:
            pass
        # Read file and set height and width of maze  
        self.contents = contents
        #print(self.contents)
        # Validate start and goal
        if self.contents.count(start_spot) != 1:
             raise Exception("maze must have exactly one start point")
        if self.contents.count(end_spot) != 1:
            raise Exception("maze must have exactly one goal")
        #sets paramaeters depending on the type of map needed
        self.extendDrawing(start_spot,end_spot)
        self.checkParam(start_spot,"A")
        self.checkParam(end_spot,"B")
        check = 1
        for prev in self.spots_before:    
            self.checkPreviousSpots(str(prev[1]),"@")
            check += 1
        #END OF MY TING
        # Determine height and width of maze
        self.contents = self.contents.splitlines()
        self.height = len(self.contents)
        self.width = max(len(line) for line in self.contents)
        # Keep track of walls
        self.walls = []
        self.specificspots = []
        for i in range(self.height):
            row = []
            passSpots = []
            for j in range(self.width):
                try:                    
                    if self.contents[i][j] == "A":
                        self.start = (i, j) 
                        row.append(False)
                    elif self.contents[i][j] == "B":
                        self.goal = (i, j) 
                        row.append(False)
                    elif self.contents[i][j] == "-":
                        passSpots.append((i,j))
                        row.append(False)
                    elif self.contents[i][j] == "@":
                        passSpots.append((i,j))
                        row.append(False)
                    elif self.contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)                            
                except IndexError:
                    row.append(False)
                if len(passSpots) > 0 and passSpots not in self.specificspots:
                    self.specificspots.append(passSpots)
            self.walls.append(row)
        self.solution = None
        self.solve()
    
    def getPreviousLots(self,goal):
        #uses preset lot information: row letter, 'row highest', 'row lowest'
        for i, values in enumerate(self.lot_sides):
            #if the 'row highest' is greater than the goal AND 'row lowest' is lower than the goal
            if values[1] >= goal and values[2] <= goal:
                #diff is the 'row highest'
                diff = values[1]
                #num is the amount of lots in the row before the goal: the 'row highest' - the goal
                num = values[1] - goal
                for i in range(num):
                    #if the 'row highest' is less' than 10, append a zero
                    if diff < 10:
                        self.spots_before.append((i,f'0{diff}',f'{values[0]}{values[1] - diff}'))
                    elif diff == 10:
                        self.spots_before.append((i,f'{diff}',f'{values[0]}{values[1] - diff}'))
                    else:
                        self.spots_before.append((i,f'{values[1] - i}',f'{values[0]}{values[1] - (values[1] - (i + 1))}'))
                    #decrement diff
                    diff -= 1
    
    def extendDrawing(self,start_spot,end_spot):
        if start_spot == "E" and end_spot == "X":
            pass
        if start_spot == "X" and end_spot == "E":
            pass
        if start_spot == "E" and end_spot != "X":
            self.contents = self.contents.replace("X" , " ")
        if start_spot == "X" and end_spot != "E":
            self.contents = self.contents.replace("E" , " ")
        if start_spot != "E" and end_spot == "X":
            self.contents = self.contents.replace("E" , " ")
        if start_spot != "X" and end_spot == "E":
            self.contents = self.contents.replace("X" , " ")
        
    def checkParam(self,spot,letter):
        import re
        if len(spot) == 2:            
                #searches for the 'spot' in the uploaded parking lot file
                match = (re.search(spot, self.contents))
                x, y = match.span()
                #print(f"({match.span()})")                
                slot = f'{self.contents[x]}{self.contents[y-1]}'
                #[("A",68,57),("B",56,45),("C",44,34),("D",33,23),("E",22,11),("F",10,0)]
                if self.lotnumber == 1:
                    if int(slot) <= 10 or int(slot) <= 33 and int(slot) > 22 or int(slot) <= 56 and int(slot) > 44:
                        self.contents = self.contents.replace(slot , f"{letter} ")
                    else:
                        self.contents = self.contents.replace(slot , f" {letter}")
                #[("A",9,0),("B",19,10),("C",29,20),("D",39,30),("E",49,40)]
                elif self.lotnumber == 2:
                    if int(slot) <= 19 and int(slot) > 9 or int(slot) <= 39 and int(slot) > 29:
                        self.contents = self.contents.replace(slot , f"{letter} ")
                    else:
                        self.contents = self.contents.replace(slot , f" {letter}")
                #[("A",5,0),("B",15,6)]
                elif self.lotnumber == 3:
                    if int(slot) <= 5 and int(slot) >= 0:                 
                        self.contents = self.contents.replace(slot , f"{letter} ")
                    else:
                        self.contents = self.contents.replace(slot , f" {letter}") 
                elif self.lotnumber == 4:
                #[("A",7,0),("B",15,8),("C",23,16),("D",29,24),("E",35,30),("F",41,36),("G",46,42)]     
                    if int(slot) <= 7 or int(slot) <= 23 and int(slot) > 15 or int(slot) <= 35 and int(slot) > 29 or int(slot) <= 46 and int(slot) > 41:
                        self.contents = self.contents.replace(slot , f"{letter} ")
                    else:
                        self.contents = self.contents.replace(slot , f" {letter}")             
        if len(spot) == 1:
            self.contents = self.contents.replace(spot , letter)            

    def checkPreviousSpots(self,spot,letter):
        import re
        if len(spot) == 2: #self.checkParam(start_spot,"A") = (spot=09,letter="A")
            try:
                match = (re.search(spot, self.contents))
                x, y = match.span()
                slot = f'{self.contents[x]}{self.contents[y-1]}'
                if len(letter) == 2:
                        self.contents = self.contents.replace(slot , f"{letter}")
                else:
                    if self.lotnumber == 1:
                    #1  [("A",68,57),("B",56,45),("C",44,34),("D",33,23),("E",22,11),("F",10,0)]
                        if int(slot) <= 10 or int(slot) <= 33 and int(slot) > 22 or int(slot) <= 56 and int(slot) > 44:
                            self.contents = self.contents.replace(slot , f"-{letter}")
                        else:
                            self.contents = self.contents.replace(slot , f"{letter}-")
                    elif self.lotnumber == 2:
                    #2  [("A",9,0),("B",19,10),("C",29,20),("D",39,30),("E",49,40)]
                        if int(slot) <= 19 and int(slot) > 9 or int(slot) <= 39 and int(slot) > 29:
                            self.contents = self.contents.replace(slot , f"-{letter}")
                        else:
                            self.contents = self.contents.replace(slot , f"{letter}-")
                    elif self.lotnumber == 3:
                    #3  [("A",5,0),("B",15,6)]
                        if int(slot) <= 5 and int(slot) >= 0:
                            self.contents = self.contents.replace(slot , f"-{letter}")
                        else:
                            self.contents = self.contents.replace(slot , f"{letter}-")
                    elif self.lotnumber == 4:
                    #4  [("A",7,0),("B",15,8),("C",23,16),("D",29,24),("E",35,30),("F",41,36),("G",46,42)]
                        if int(slot) <= 7 or int(slot) <= 23 and int(slot) > 15 or int(slot) <= 35 and int(slot) > 29 or int(slot) <= 46 and int(slot) > 41:
                            self.contents = self.contents.replace(slot , f"-{letter}")
                        else:
                            self.contents = self.contents.replace(slot , f"{letter}-")           
            except Exception:
                pass
        if len(spot) == 1:
            self.contents = self.contents.replace(spot , letter)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print(u"\u2588", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""
        # Keep track of number of states explored
        self.num_explored = 0
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)
        # Initialize an empty explored set
        self.explored = set()
        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            # Mark node as explored
            self.explored.add(node.state)
            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw, ImageFont
        newsize = (400, 300)
        toORfrom = ""
        starting_point = ""
        ending_point = ""
        if self.typer == 0:
            toORfrom = "Leaving"
            starting_point = f'from {self.spot}'
            ending_point = "to EXIT"
        else:
            toORfrom = "Finding"
            starting_point = "ENTRANCE"
            ending_point = f'   to {self.spot}'        
        cell_size = 50 
        cell_border = 2
        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black")
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                # Walls
                if col:
                    fill = (0,0,0)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size )]),
                    fill=fill)
                # Start
                elif (i, j) == self.start:
                    fill = (0, 171, 28)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size )]),
                    fill=fill)
                # Goal
                elif (i, j) == self.goal: 
                    fill = (0, 171, 28)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size )]),
                    fill=fill)                  
                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (0, 171, 28)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size )]),
                    fill=fill)
                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (255,0,0)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size)]),
                    fill=fill)
                # Empty cell
                else:
                    fill = (255, 0, 0)
                    draw.rectangle(
                    ([(j * cell_size , i * cell_size ),
                      ((j + 1) * cell_size , (i + 1) * cell_size )]),
                    fill=fill)                
        # Draw white for other parking spaces in the same row       
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                for item in self.specificspots:
                    if (i, j) == item[0] or (i, j) == item[1]:
                        fill = (255, 255, 255)
                        draw.rectangle(
                        ([(j * cell_size , i * cell_size + cell_border),
                        ((j + 1) * cell_size , (i + 1) * cell_size - cell_border)]),
                        fill=fill)
        # Draw the text for entrance/goal and goal/exit
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):                
                if (i, j) == self.start: 
                    draw.text(((j * cell_size) + 2, (i * cell_size) + 7), starting_point, (255,255,255),font = ImageFont.load_default(size=27),stroke_fill="white")
                if (i, j) == self.goal: 
                    draw.text(((j * cell_size) - 105, (i * cell_size) + 5), ending_point, (255,255,255),font = ImageFont.load_default(size=30),stroke_fill="white")
        # Draw names of previos parking spots in the same row
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                for k, item in enumerate(self.specificspots):
                    if (i,j) == item[0]:
                        thisSpot = self.spots_before[k]
                        draw.text(((j * cell_size) + 10, (i * cell_size) + 10), thisSpot[2], (0, 0, 0),font = ImageFont.load_default(size=30))
        # Draw map heading        
        draw.text((40, 0),f"Guide Map For {toORfrom} {self.spot}",(255,255,255),font = ImageFont.load_default(size=50))
        img.resize(newsize, Image.Resampling.LANCZOS)
        #img.save(self.imagename)
        return img