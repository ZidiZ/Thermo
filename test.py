from Tkinter import *
#import tkinter

win = Tk()
win.title("xinghaohan")
win.geometry("400x400+200+20")
 
label = Label(win,text="good good study", bg="red")

label.focus_set()
label.pack()
 
def func(event):
    print("event.char =", event.char)
    print("event.keycode =", event.keycode)
 

label.bind("<Key>",func)
 

#def func(event):
#    print("event.char =", event.char)
#    print("event.keycode =", event.keycode)
#
#win.bind("<Key>",func)
 
win.mainloop()