from tkinter import *

def raise_frame(num, check):
    global here, there    
    list_of_frames[num].tkraise()
    if check:
        here +=1 
    else:
        here -= 1
    check_btn(here, there)
    
def check_btn(here, there):
    if here == 0:
        backbtn.config(state="disabled")
    else:
        backbtn.config(state="normal")
    if here == there:
        nextbtn.config(state="disabled")
    else:
        nextbtn.config(state="normal")

main_win = Tk()
main_win.geometry('500x500')
main_win.title("Registration Form")

frm_list = ["A", "B", "C", "D", "E"]
list_of_frames = {}

for i, nm in enumerate(frm_list):
    frame = Frame(main_win, bg = "blue")
    frame.place(x=50, y=50, width=400, height=200)
    
    label_8 = Label(frame, text=f"Welcome to {i}-{nm}",font=("bold", 10))
    label_8.place(x=200, y = 100)
    
    list_of_frames[i] = frame

global here, there
here = 0
there = len(list_of_frames) - 1

backbtn = Button(main_win, text='back',width=20,bg='brown',fg='white', command=lambda:raise_frame(here-1,False))
backbtn.place(x=90,y=380)

nextbtn = Button(main_win, text="next",width=20,bg='brown',fg='white', command=lambda:raise_frame(here+1,True))
nextbtn.place(x=270,y=380)

list_of_frames[0].tkraise()
check_btn(here, there)

main_win.mainloop()