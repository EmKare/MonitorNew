from tkinter import Tk, Label
from tkinter import ttk
root = Tk()
root.title("Combobox Example")
root.geometry('400x300')
lisvalues = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5",]
lisvalues_copy = lisvalues.copy()
#["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6", "Option 7", "Option 8", "Option 8", "Option 10"]

combo_1_cur = 0
combo_1 = ttk.Combobox(root, )
combo_1['values'] = [x for x in lisvalues_copy]
combo_1.current(0)
combo_1.place(x = 10, y = 0)

label_1 = Label(root, bg = "red")
label_1.place(x = 10, y = 40, width = 140, height = 40,)

combo_2_cur = 0
combo_2 = ttk.Combobox(root,)
combo_2['values'] = [x for x in lisvalues_copy]
combo_2.current(1)
combo_2.place(x = 200, y = 0)

label_2 = Label(root, bg = "green")
label_2.place(x = 200, y = 40, width = 140, height = 40,)

combo_3_cur = 0
combo_3 = ttk.Combobox(root,)
combo_3['values'] = [x for x in lisvalues_copy]
combo_3.current(2)
combo_3.place(x = 10, y = 150)

label_3 = Label(root, bg = "blue")
label_3.place(x = 10, y = 190, width = 140, height = 40,)

combo_4_cur = 0
combo_4 = ttk.Combobox(root,)
combo_4['values'] = [x for x in lisvalues.copy()] #lisvalues_copy]
combo_4.current(3)
#combo_4.place(x = 200, y = 150)

label_4 = Label(root, bg = "yellow")
#label_4.place(x = 200, y = 190, width = 140, height = 40,)

def combo_1_option_selected(event): #lisvalues_copy
    comb4cur = combo_4.get() #gets combo 4 value
    comb3cur = combo_3.get() #gets combo 3 value
    comb2cur = combo_2.get() #gets combo 2 value
    comb1cur = combo_1.get() #gets combo 1 value
    comb1ind = combo_1.current()
    
    to_pop = lisvalues_copy.index(comb1cur) #locates combo 1 value in list
    lisvalues_copy.pop(to_pop) #pops combo 1 value from list at this index
    combo_2['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list
    combo_3['values'] = [x for x in lisvalues_copy] #reassigns combo 2 values as those from list
    #combo_4['values'] = [x for x in demo] #assigns combo 2 values as those from new list
    
    label_1.config(text = f"{combo_1.get()}", font = ('bold', 15))
    
    if comb1cur == comb2cur:
        if to_pop == 0: 
            combo_2.current(1) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_2.current(len(demo) - 1) #if 1st  value selected, choose 2nd
        else:
            combo_2.current(to_pop - 1)
    
    if comb1cur == comb3cur:
        if to_pop == 0: 
            combo_3.current(2) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_3.current(len(demo) - 2) #if 1st  value selected, choose 2nd
        else:
            combo_3.current(to_pop + 1)
    
def combo_2_option_selected(event):
    comb1cur = combo_1.get() #gets combo 1 value
    comb2cur = combo_2.get() #gets combo 2 value
    comb3cur = combo_3.get() #gets combo 4 value
    comb4cur = combo_4.get() #gets combo 3 value
    demo = lisvalues.copy() #creates copy of original list
    to_pop = demo.index(comb2cur) #locates combo 2 value in new list
    demo.pop(to_pop) #pops combo 2 value from new list at this index
    combo_1['values'] = [x for x in demo] #assigns combo 1 values as those from new list
    combo_3['values'] = [x for x in demo] #assigns combo 2 values as those from new list
    #combo_4['values'] = [x for x in demo] #assigns combo 2 values as those from new list
    
    label_2.config(text = f"{combo_2.get()}", font = ('bold', 15))
    
    if comb2cur == comb1cur:
        if to_pop == 0: 
            combo_1.current(1) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_1.current(len(demo) - 1) #if 1st  value selected, choose 2nd
        else:
            combo_1.current(to_pop - 1)
    
    if comb2cur == comb3cur:
        if to_pop == 0: 
            combo_3.current(2) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_3.current(len(demo) - 2) #if 1st  value selected, choose 2nd
        else:
            combo_3.current(to_pop + 1)
            
def combo_3_option_selected(event):
    comb1cur = combo_1.get() #gets combo 1 value
    comb2cur = combo_2.get() #gets combo 2 value
    comb3cur = combo_3.get() #gets combo 4 value
    comb4cur = combo_4.get() #gets combo 3 value
    demo = lisvalues.copy() #creates copy of original list
    to_pop = demo.index(comb3cur) #locates combo 2 value in new list
    demo.pop(to_pop) #pops combo 2 value from new list at this index
    combo_1['values'] = [x for x in demo] #assigns combo 1 values as those from new list
    combo_2['values'] = [x for x in demo] #assigns combo 2 values as those from new list
    #combo_4['values'] = [x for x in demo] #assigns combo 2 values as those from new list
    
    label_3.config(text = f"{combo_3.get()}", font = ('bold', 15))
    
    if comb3cur == comb1cur:
        if to_pop == 0: 
            combo_1.current(1) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_1.current(len(demo) - 1) #if 1st  value selected, choose 2nd
        else:
            combo_1.current(to_pop - 1)
    
    if comb3cur == comb2cur:
        if to_pop == 0: 
            combo_2.current(2) #if 1st  value selected, choose 2nd
        elif to_pop == len(demo):
            combo_2.current(len(demo) - 2) #if 1st  value selected, choose 2nd
        else:
            combo_2.current(to_pop + 1)

    
combo_1.bind("<<ComboboxSelected>>", combo_1_option_selected)
combo_2.bind("<<ComboboxSelected>>", combo_2_option_selected)
combo_3.bind("<<ComboboxSelected>>", combo_3_option_selected)
#combo_3.bind("<<ComboboxSelected>>", combo_3_option_selected)
root.mainloop()


"""
    if cur == topup:
        if topup == 0: 
            combo_1.current(1)
        elif topup == len(demo):
            combo_1.current(len(demo) - 1)
        else:
            combo_1.current(topup - 1)    
    """