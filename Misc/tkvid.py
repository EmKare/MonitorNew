from tkinter import Tk, Canvas, NW
from tkvideo import tkvideo

root = Tk()
my_label = Canvas(root, width = 500, height=500)
my_label.pack()
player = tkvideo(r"C:/Users/DELL/Desktop/MyJourney/Python/Parking/New folder/carPark.mp4", my_label, loop = 1, size = (500,281))
my_label.create_image(0,0,image = player, anchor = NW)
player.play()

root.mainloop()