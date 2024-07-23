from tkinter import Tk, Label
from tkinter import ttk
root = Tk()
root.title("Combobox Example")
root.geometry('350x300')
lisvalues = ["Option 0", "Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6", "Option 7", "Option 8", "Option 9",]
lisvalues_copy = lisvalues.copy()

# Combo 1 ------------------------------------------------
combo_1 = ttk.Combobox(root, )
combo_1['values'] = [x for x in lisvalues_copy]
combo_1.current(0)
combo_1_cur = combo_1.get()
combo_1.place(x = 10, y = 0)
# LAbel 1 ------------------------------------------------
label_1 = Label(root, bg = "red", text = combo_1_cur, font = ('bold', 15))
label_1.place(x = 10, y = 40, width = 140, height = 40,)
# Combo 2 ------------------------------------------------
combo_2 = ttk.Combobox(root,)
combo_2['values'] = [x for x in lisvalues_copy]
combo_2.current(1)
combo_2_cur = combo_2.get()
combo_2.place(x = 200, y = 0)
# LAbel 2 ------------------------------------------------
label_2 = Label(root, bg = "green", text = combo_2_cur, font = ('bold', 15))
label_2.place(x = 200, y = 40, width = 140, height = 40,)
# Combo 3 ------------------------------------------------
combo_3 = ttk.Combobox(root,)
combo_3['values'] = [x for x in lisvalues_copy]
combo_3.current(2)
combo_3_cur = combo_3.get()
combo_3.place(x = 10, y = 150)
# LAbel 3 ------------------------------------------------
label_3 = Label(root, bg = "blue", text = combo_3_cur, font = ('bold', 15))
label_3.place(x = 10, y = 190, width = 140, height = 40,)
# Combo 4 ------------------------------------------------
combo_4 = ttk.Combobox(root,)
combo_4['values'] = [x for x in lisvalues.copy()] #lisvalues_copy]
combo_4.current(3)
combo_4_cur = combo_4.get()
combo_4.place(x = 200, y = 150)
# LAbel 4 ------------------------------------------------
label_4 = Label(root, bg = "yellow", text = combo_4_cur, font = ('bold', 15))
label_4.place(x = 200, y = 190, width = 140, height = 40,)

#lisvalues_copy
def combo_1_option_selected(event): #lisvalues_copy    
    lisvalues_copy = lisvalues.copy()
    comb1cur = combo_1.get() #gets combo 1 value

    if comb1cur == combo_2.get():
        to_set = lisvalues_copy.index(combo_1_cur) # noqa
        combo_2.current(to_set)
        label_2.config(text = f"{combo_2.get()}",)
    
    if comb1cur == combo_3.get():
        to_set = lisvalues_copy.index(combo_1_cur) # noqa
        combo_3.current(to_set)
        label_3.config(text = f"{combo_3.get()}",)
        
    if comb1cur == combo_4.get():
        to_set = lisvalues_copy.index(combo_1_cur) # noqa
        combo_4.current(to_set)
        label_4.config(text = f"{combo_4.get()}",)
    
    comb2cur = combo_2.get() #gets combo 2 value
    comb3cur = combo_3.get() #gets combo 3 value
    comb4cur = combo_4.get() #gets combo 4 value
    
    try:
        to_pop = lisvalues_copy.index(comb1cur) #locates combo 1 value in list
        lisvalues_copy.pop(to_pop) #pops combo 1 value from list at this index
    except Exception:
        pass    
    try:
        to_pop = lisvalues_copy.index(comb2cur) #locates combo 2 value in list
        lisvalues_copy.pop(to_pop) #pops combo 2 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb3cur) #locates combo 3 value in list
        lisvalues_copy.pop(to_pop) #pops combo 3 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb4cur) #locates combo 4 value in list
        lisvalues_copy.pop(to_pop) #pops combo 4 value from list at this index
    except Exception:
        pass
    
    label_1.config(text = f"{comb1cur}",)
    
    combo_1['values'] = [x for x in lisvalues_copy] #reassigns combo 1 values as those from list
    combo_2['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list
    combo_3['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list
    combo_4['values'] = [x for x in lisvalues_copy] #reassigns combo 4 values as those from list
    
def combo_2_option_selected(event): #lisvalues_copy
    lisvalues_copy = lisvalues.copy()
    comb2cur = combo_2.get() #gets combo 2 value
    
    if comb2cur == combo_3.get():
        to_set = lisvalues_copy.index(combo_2_cur) # noqa
        combo_3.current(to_set)
        label_3.config(text = f"{combo_3.get()}",)
        
    if comb2cur == combo_4.get():
        to_set = lisvalues_copy.index(combo_2_cur) # noqa
        combo_4.current(to_set)
        label_4.config(text = f"{combo_4.get()}",)
    
    if comb2cur == combo_1.get():
        to_set = lisvalues_copy.index(combo_2_cur) # noqa
        combo_1.current(to_set)
        label_1.config(text = f"{combo_1.get()}",)
    
    comb3cur = combo_3.get() #gets combo 3 value
    comb4cur = combo_4.get() #gets combo 4 value
    comb1cur = combo_1.get() #gets combo 1 value
    
    try:
        to_pop = lisvalues_copy.index(comb2cur) #locates combo 2 value in list
        lisvalues_copy.pop(to_pop) #pops combo 2 value from list at this index
    except Exception:
        pass    
    try:
        to_pop = lisvalues_copy.index(comb3cur) #locates combo 3 value in list
        lisvalues_copy.pop(to_pop) #pops combo 3 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb4cur) #locates combo 4 value in list
        lisvalues_copy.pop(to_pop) #pops combo 4 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb1cur) #locates combo 1 value in list
        lisvalues_copy.pop(to_pop) #pops combo 1 value from list at this index
    except Exception:
        pass
    
    label_2.config(text = f"{comb2cur}",)
    
    combo_2['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list
    combo_3['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list
    combo_4['values'] = [x for x in lisvalues_copy] #reassigns combo 4 values as those from list
    combo_1['values'] = [x for x in lisvalues_copy] #reassigns combo 1 values as those from list
    
def combo_3_option_selected(event): #lisvalues_copy
    lisvalues_copy = lisvalues.copy()    
    comb3cur = combo_3.get() #gets combo 3 value
    
    if comb3cur == combo_4.get():
        to_set = lisvalues_copy.index(combo_3_cur) # noqa
        combo_4.current(to_set)
        label_4.config(text = f"{combo_4.get()}",)
    
    if comb3cur == combo_1.get():
        to_set = lisvalues_copy.index(combo_3_cur) # noqa
        combo_1.current(to_set)
        label_1.config(text = f"{combo_1.get()}",)
    
    if comb3cur == combo_2.get():
        to_set = lisvalues_copy.index(combo_3_cur) # noqa
        combo_2.current(to_set)
        label_2.config(text = f"{combo_2.get()}",)
    
    comb4cur = combo_4.get() #gets combo 4 value
    comb1cur = combo_1.get() #gets combo 1 value
    comb2cur = combo_2.get() #gets combo 2 value
    
    try:
        to_pop = lisvalues_copy.index(comb3cur) #locates combo 3 value in list
        lisvalues_copy.pop(to_pop) #pops combo 3 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb4cur) #locates combo 4 value in list
        lisvalues_copy.pop(to_pop) #pops combo 4 value from list at this index
    except Exception:
        pass 
    try:
        to_pop = lisvalues_copy.index(comb1cur) #locates combo 1 value in list
        lisvalues_copy.pop(to_pop) #pops combo 1 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb2cur) #locates combo 2 value in list
        lisvalues_copy.pop(to_pop) #pops combo 2 value from list at this index
    except Exception:
        pass
    
    label_3.config(text = f"{comb3cur}",)
    
    combo_3['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list
    combo_4['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list
    combo_1['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list    
    combo_2['values'] = [x for x in lisvalues_copy] #reassigns combo 1 values as those from list

def combo_4_option_selected(event): #lisvalues_copy
    lisvalues_copy = lisvalues.copy()    
    comb4cur = combo_4.get() #gets combo 3 value
    
    if comb4cur == combo_1.get():
        to_set = lisvalues_copy.index(combo_4_cur) # noqa
        combo_1.current(to_set)
        label_1.config(text = f"{combo_1.get()}",)
    
    if comb4cur == combo_2.get():
        to_set = lisvalues_copy.index(combo_4_cur) # noqa
        combo_2.current(to_set)
        label_2.config(text = f"{combo_2.get()}",)
    
    if comb4cur == combo_3.get():
        to_set = lisvalues_copy.index(combo_4_cur) # noqa
        combo_3.current(to_set)
        label_3.config(text = f"{combo_3.get()}",)
        
    comb1cur = combo_1.get() #gets combo 1 value
    comb2cur = combo_2.get() #gets combo 2 value
    comb3cur = combo_3.get() #gets combo 4 value
    

    try:
        to_pop = lisvalues_copy.index(comb4cur) #locates combo 4 value in list
        lisvalues_copy.pop(to_pop) #pops combo 4 value from list at this index
    except Exception:
        pass 
    try:
        to_pop = lisvalues_copy.index(comb1cur) #locates combo 1 value in list
        lisvalues_copy.pop(to_pop) #pops combo 1 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb2cur) #locates combo 2 value in list
        lisvalues_copy.pop(to_pop) #pops combo 2 value from list at this index
    except Exception:
        pass
    try:
        to_pop = lisvalues_copy.index(comb3cur) #locates combo 3 value in list
        lisvalues_copy.pop(to_pop) #pops combo 3 value from list at this index
    except Exception:
        pass
    
    label_4.config(text = f"{comb4cur}",)
    
    combo_4['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list
    combo_1['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list    
    combo_2['values'] = [x for x in lisvalues_copy] #reassigns combo 1 values as those from list
    combo_3['values'] = [x for x in lisvalues_copy] #reassigns combo 3 values as those from list

combo_1.bind("<<ComboboxSelected>>", combo_1_option_selected)
combo_2.bind("<<ComboboxSelected>>", combo_2_option_selected)
combo_3.bind("<<ComboboxSelected>>", combo_3_option_selected)
combo_4.bind("<<ComboboxSelected>>", combo_4_option_selected)

root.mainloop()