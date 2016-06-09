from tkinter import *
import time
root = Tk() 

w = Canvas(root, width = 500, height = 500, bg = 'white') 

r=60
x=150
a=9.8
global y
y=r

ball = w.create_oval(x-r, y-r, x+r, y+r, fill = 'Blue' , tags = 'ball')
w.pack() 
w.update()

def click_ball(event):
    if val.get() ==0:
        global x,y
        x = event.x
        y = event.y
        w.coords(ball, x-r, y-r, x+r, y+r)
    
def move_ball():
    w.tag_bind('ball', '<Button1-Motion>', click_ball)

def drop_ball():
    v = 0
    T0 = time.time()
    while val.get() ==1:
        time.sleep(0.05)
        global x,y
        if y<500-r:
            T1 = time.time()
            w.move(ball, 0, a*(T1-T0))
            y += a*(T1-T0)
        else: w.coords(ball, x-r, 500-2*r, x+r, 500)
        w.pack() 
        w.update()

val = IntVar()
val.set(0)

r0 = Radiobutton(text = 'move', variable = val, value = 0, command = move_ball)
r0.pack()
r1 = Radiobutton(text = 'drop', variable = val, value = 1, command = drop_ball)
r1.pack()

root.mainloop() 
