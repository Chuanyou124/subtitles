from tkinter import *
import tkinter as tk
import pyautogui
import numpy as np
from pyscreenshot import grab
import pytesseract
from googletrans import Translator
import PIL
from PIL import Image
from PIL import ImageTk
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

def ss():
    global ss_id
    im = bwfy(grab(bbox=(x1, y1, x2-x1, y2-y1)), th=200)
    text = pytesseract.image_to_string(im, lang=L_img[tkvar.get()], config='--psm 7')
    print(text)
    stext = fanyi.translate(text, src=L_trans[tkvar.get()], dest=L_trans[tkvarTo.get()]).text
    print(stext)
    lbl_text.set(' '.join(stext.split()))
    entry.update_idletasks()
    ss_id = root.after(period, ss)

def ul_pos(event):
    global x1, y1
    x1 = root.winfo_pointerx()
    y1 = root.winfo_pointery()
    print('x1', 'y1', x1, y1)


def br_pos(event):
    global x2, y2
    x2 = root.winfo_pointerx()
    y2 = root.winfo_pointery()
    print('x2', 'y2', x2, y2)

def jieping():
    global app, ss_id, btn_text
    btn_txt = btn_text.get()
    print('ss id', ss_id)
    if btn_txt == 'Select Screen':
        app.maximize()
        btn_text.set('Stop')
    else:
        root.after_cancel(ss_id)
        btn_text.set('Select Screen')
    print('ss id', ss_id)

class DrawRectangle(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.canvas = Canvas(self, cursor="cross", width=1, height=1)
        self.maximized = False

        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.sbarv.grid(row=0,column=1,stick=N+S)
        self.sbarh.grid(row=1,column=0,sticky=E+W)

        self.canvas.bind("<Escape>", self.recover_size)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

    def maximize(self):
        root.wm_attributes('-alpha', 0.3)
        self.canvas.config(width=root.winfo_screenwidth()-3, height=root.winfo_screenheight()-3)
        self.maximized = True

    def recover_size(self):
        root.wm_attributes('-alpha', 1)
        self.canvas.config(width=1, height=1)
        self.maximized = False

    def on_button_press(self, event):
        global x1, y1
        x1 = root.winfo_pointerx()
        y1 = root.winfo_pointery()
        print('x1', 'y1', x1, y1)
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='green')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        global x2, y2
        x2 = root.winfo_pointerx()
        y2 = root.winfo_pointery()
        print('x2', 'y2', x2, y2)
        global ss_id
        if x2 - x1 > 100 and y2 - y1 > 10:
            self.recover_size()
            ss_id = root.after(period, ss)

x1, y1, x2, y2 = 0,0,0,0
ss_id = None
period = 100
fanyi = Translator()
L_img = {'Chinese':'chi_sim','English':'eng','Japanese':'jpn','Korean':'kor'}
L_trans = {'Chinese':'zh-CN','English':'en','Japanese':'ja','Korean':'ko'}

root = tk.Tk()# root.bind('<Button 1>', ul_pos); root.bind('<ButtonRelease-1>', br_pos)

app = DrawRectangle(root)
app.grid(row=0, column=0)

lbl_text = tk.StringVar()
entry = tk.Label(root, textvariable=lbl_text, width = 100, height=2, font=("Helvetica", 15))
entry.grid(row=1, column=0)

btn_text = tk.StringVar()
btn_text.set('Select Screen')
button1 = tk.Button(root, textvariable=btn_text, width=15, height=2, command=jieping)
button1.grid(row=1, column=1)

def action(*args):
    global ss_id, tkvarA
    if tkvarA.get() == 'Start':
        ss_id = root.after(period, ss)
    else:
        root.after_cancel(ss_id)

'''
tkvarA = StringVar(root)
choicesA = { 'Start','Stop'}
tkvarA.set('Stop') # set the default option
act = OptionMenu(root, tkvarA, *choicesA)
act.grid(row=2, column=1)
tkvarA.trace('w', action)
'''

# Create a Tkinter variable
tkvar = StringVar(root);tkvarTo = StringVar(root)
# Dictionary with options
choices = { 'Chinese','English','Japanese','Korean'}
tkvar.set('Chinese') # set the default option
langFrom = OptionMenu(root, tkvar, *choices)
langFrom.grid(row=1, column=3)
Label(root, text="From").grid(row=1, column=2)
tkvarTo.set('Chinese') # set the default option
langTo = OptionMenu(root, tkvarTo, *choices)
langTo.grid(row=2, column=3)
Label(root, text="To").grid(row=2, column=2)

root.wm_attributes("-topmost", 1)
root.mainloop()
