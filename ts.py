from tkinter import *
import tkinter as tk
from mss import mss
import pyautogui
import numpy as np
from pyscreenshot import grab
import pytesseract
from googletrans import Translator
from PIL import Image

def bwfy(img, th=200, lonly=False):
    l = img.convert('L')
    if lonly:
        return l
    bw = np.asarray(l).copy()
    bw[bw < th] = 0    # Black
    bw[bw >= th] = 255 # White
    # Now we put it back in Pillow/PIL land
    return Image.fromarray(bw)

def ss():
    root.after(50, ss)
    global x1, y1, x2, y2, im
    if x2 - x1 >= 10 and y2 - y1 >= 10:
        if app.maximized:
            app.toggle()
        im = bwfy(grab(bbox=(x1, y1, x2-x1, y2-y1)), th=100)
        text = pytesseract.image_to_string(im, lang='kor')
        print(text)
        stext = fanyi.translate(text, src='ko', dest='zh-CN').text
        print(stext)
        lbl_text.set(stext)
        entry.update_idletasks()


def ul_pos(event):
    global x1
    global y1
    x1 = root.winfo_pointerx()
    y1 = root.winfo_pointery()
    print('x1', 'y1', x1, y1)


def br_pos(event):
    global x2
    global y2
    x2 = root.winfo_pointerx()
    y2 = root.winfo_pointery()
    print('x2', 'y2', x2, y2)


x1, y1, x2, y2 = 0,0,0,0
fanyi = Translator()
app = None
task_id = None

def jieping():
    global app, task_id
    if task_id is not None:
        root.after_cancel(task_id)
    app = MaxApp(root)
    task_id = root.after(50, ss)

class MaxApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x50+1000+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.wm_attributes("-transparent", True)
        master.config(bg='systemTransparent')
        master.wm_attributes("-topmost", 1)
        self.maximized = True
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
    def toggle(self):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom
        self.maximized = False


root = tk.Tk(); root.bind('<Button 1>', ul_pos); root.bind('<ButtonRelease-1>', br_pos)
lbl_text = tk.StringVar()
button1 = tk.Button(root, textvariable = 'select screen', width = 25, command = jieping)
button1.pack()
entry = tk.Label(root, textvariable=lbl_text, width = 100, height=2, font=("Helvetica", 20))
entry.grid(row=0,column=0)
entry.pack()
root.mainloop()
