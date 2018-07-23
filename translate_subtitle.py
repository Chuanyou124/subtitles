from tkinter import *
import tkinter as tk
from mss import mss
import pyautogui
import numpy as np
from pyscreenshot import grab
import pytesseract
from googletrans import Translator
from PIL import Image
from time import sleep

def bwfy(img, th=200, lonly=False):
    l = img.convert('L')
    if lonly:
        return l
    bw = np.asarray(l).copy()
    bw[bw < th] = 0    # Black
    bw[bw >= th] = 255 # White
    # Now we put it back in Pillow/PIL land
    return Image.fromarray(bw)

def stop_ss():
    root.after_cancel(ss_id)

def ss():
    root.after(1000, ss)
    global x1, y1, x2, y2
    if x2 - x1 >= 10 and y2 - y1 >= 10:
        if app.maximized:
            app.recover_size()
        im = bwfy(grab(bbox=(x1, y1, x2-x1, y2-y1)), th=200)
        text = pytesseract.image_to_string(im, lang='kor')
        print(text)
        stext = fanyi.translate(text, src='ko', dest='zh-CN').text
        print(stext)
        lbl_text.set(' '.join(stext.split()))
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

def jieping():
    global app, ss_id, btn_text
    btn_txt = btn_text.get()
    print('ss id', ss_id)
    if btn_txt == 'Select Screen':
        app = MaxApp(root)
        ss_id = root.after(1000, ss)
        btn_text.set('Stop')
    else:
        root.after_cancel(ss_id)
        sleep(2)
        btn_text.set('Select Screen')
    print('ss id', ss_id)

class MaxApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        self.pad=3
        self._geom='1000x90+500+0'
        #master.bind('<Escape>',self.toggle_geom)
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth()-self.pad, self.master.winfo_screenheight()-self.pad))
        self.master.update()
        self.maximized = True
        master.wm_attributes("-transparent", True)
        master.config(bg='systemTransparent')

    def maximize(self):
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth()-self.pad, self.master.winfo_screenheight()-self.pad))
        self.maximized = True

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        #print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        self.maximized = False

    def recover_size(self):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom
        self.maximized = False


x1, y1, x2, y2 = 0,0,0,0
ss_id = None
fanyi = Translator()

root = tk.Tk(); root.bind('<Button 1>', ul_pos); root.bind('<ButtonRelease-1>', br_pos)
app = None
lbl_text = tk.StringVar()
entry = tk.Label(root, textvariable=lbl_text, width = 100, height=2, font=("Helvetica", 15))
entry.grid(row=0,column=0)

btn_text = tk.StringVar()
btn_text.set('Select Screen')
button1 = tk.Button(root, textvariable=btn_text, width=15, height=2, command=jieping)
button1.grid(row=1, column=0)

root.wm_attributes("-topmost", 1)
root.mainloop()
