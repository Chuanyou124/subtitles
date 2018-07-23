#!/usr/bin/env python

from Tkinter import *
import Tkinter as tk

toggled = False
def action(event):
    global toggled
    if not toggled:
        toggled = True
        root.wm_attributes("-transparent", True)
        root.config(bg='systemTransparent')
    else:
        toggled = False
        root.wm_attributes("-transparent", False)
        root.config(bg='white')

root = Tk()
root.geometry('1500x60')
'''
t = Text(root, height=1, width=200, selectbackground='black', inactiveselectbackground='red')
t.pack()
t.insert(END, "Chuanyou's tool bar to hide Chinese subtitle and learn a foreign language".upper())

entry = tk.Entry(root)
entry.pack()
entry.insert("0", "Focus me!")
'''
c = tk.Canvas(root, width=20, height=20)
c.pack()
r = c.create_rectangle((7, 0, 19, 20), fill='white')
c.tag_bind(r, '<ButtonPress-1>', action)
c.focus_set()
c.bind('<space>', action)

root.wm_attributes("-topmost", 1)
root.title('subtitle hider')
root.mainloop()
