import tkinter as tk # python3
root = tk.Tk()
myList = tk.Listbox(root)
myText = "A list item"
#for i in range(0,30):
#    myList.insert(i, myText)
myList.pack()
for i in range(0,30):
    #myList.insert(i, myText)
    lbl = tk.Label(myList, text=myText, anchor="w", font=("Helvetica", "24"))
    lbl.pack(side="top", fill="x", anchor="w")
root.mainloop()