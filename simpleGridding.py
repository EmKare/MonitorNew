import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

# Create widgets and place them in the grid
# Ensuring only 4 columns are used
row = 0
col = 0
for i in range(10):
    label = tk.Label(frame, text=f"Label {i}")
    label.grid(row=row, column=col)

    col += 1
    if col > 3:
        col = 0
        row += 1

root.mainloop()