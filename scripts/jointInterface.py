from jointRos import*
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#import numpy as np
Offset = [512,512,512,512,512]
DEGS=[[0, 0, 0, 0, 0],
      [-20, 20, -20, 20, 0],
      [30,-30, 30, -30, 0],
      [-90, 15, -55, 17, 0],
      [ -90, 45, -55, 45, 10]]
def printMessage():
    return messagebox.showinfo("Hola")

if __name__ =='__main__':
    listener()
    global Goal
    WIDTH,HEIGHT= 1440,1080
    W=100
    H=50
    window=tk.Tk()
    window.title('Dynamixel Interface')
    
    #Home and Teach
    window.geometry('%sx%s' % (WIDTH,HEIGHT))
    Goal=tk.IntVar()
    def getGoal(value):
        print(value)
        return
    
    def moveGoal(value):
        moveRobot(DEGS[value-1],0.5)
        return

    Teach=ttk.Button(window,text="Teach",command=lambda:moveGoal(Goal.get())).place(x=W,y=H*7)
    Preview=ttk.Button(window,text="Preview",command=lambda:getGoal(Goal.get())).place(x=W,y=H*8)

    #Radio
    Pos1=tk.Radiobutton(window,text="1",variable=Goal,value=1).place(x=W,y=H*2)
    Pos2=tk.Radiobutton(window,text="2",variable=Goal,value=2).place(x=W,y=H*3)
    Pos3=tk.Radiobutton(window,text="3",variable=Goal,value=3).place(x=W,y=H*4)
    Pos4=tk.Radiobutton(window,text="4",variable=Goal,value=4).place(x=W,y=H*5)
    Pos5=tk.Radiobutton(window,text="5",variable=Goal,value=5).place(x=W,y=H*6)

    window.mainloop()

