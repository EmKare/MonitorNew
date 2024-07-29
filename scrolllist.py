from tkinter import *
import files
lotname = "ParkingLot1/ParkingLot1.txt"

path = files.rel_path + lotname 

sides = []

# Creating the root window 
root = Tk() 

sizex = 600
sizey = 400
posx  = 40
posy  = 20
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

def CurSelet(evt):
    v = listbox.get(listbox.curselection())
    label.config(text = f"You've selected {v}", justify = "center")
    #value=[v for v in sides if v[0] == listbox.get(listbox.curselection())]
    #value = value[0]
    #label.config(text = f"You've selected {value[0]} at index {value[2]}. Status '{value[1]}'", justify = "center")
    
def getSides():
        with open(path) as f: #this file contains the parking lot's rows and lot numbers
            for line in f:
                word = line.rstrip().split('#')
                spots = []
                spots.append(word[1].strip()) #name
                spots.append(word[2].strip()) #status
                spots.append(int(word[0].strip())) #index
                sides.append(spots)
getSides()

# Creating a Listbox and 
# attaching it to root window 
listbox = Listbox(root,font=('times',13)) 

# Adding Listbox to the left 
# side of root window 
listbox.place(x = 0, y = 0,width=50,height=400,) 
listbox.bind('<<ListboxSelect>>',CurSelet)

# Creating a Scrollbar and 
# attaching it to root window 
scrollbar = Scrollbar(root) 

# Adding Scrollbar to the right 
# side of root window 
scrollbar.place(x=52,y=0,width=0,height=0)

label = Label(root, font=('times',20),)
label.place(x = 80, y = 30,width=500,height=30,)

#itemsforlistbox=['one','two','three','four','five','six','seven']

##for items in itemsforlistbox:
#    mylistbox.insert(END,items) 

# Insert elements into the listbox 
#for values in sides: 
#	listbox.insert(END, values[0])
 
for values in range(200): 
    listbox.insert(END, values)
	
# Attaching Listbox to Scrollbar 
# Since we need to have a vertical 
# scroll we use yscrollcommand 
listbox.config(yscrollcommand = scrollbar.set) 

# setting scrollbar command parameter 
# to listbox.yview method its yview because 
# we need to have a vertical view 
scrollbar.config(command = listbox.yview) 


root.mainloop() 





