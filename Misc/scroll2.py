import tkinter as tk
class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width,)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")    


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)
        

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

root = tk.Tk()
root.geometry("300x310+100+10")
root.resizable(False,False)

header = tk.Frame(root)
body = tk.Frame(root)
footer = tk.Frame(root)
header.pack()
body.pack()
footer.pack()

tk.Label(header, text="The header").pack()
tk.Label(footer, text="The Footer").pack()


scrollable_body = Scrollable(body, width=32)

for i in range(30):
    tk.Label(scrollable_body, text=f"I'm button {i} in the scrollable frame").grid()

scrollable_body.update()

root.mainloop()