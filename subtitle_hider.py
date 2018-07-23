#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
from mss import mss
import pyautogui
import numpy as np
from pyscreenshot import grab
import pytesseract
from googletrans import Translator
from PIL import Image

orig_trans = False
fanyi = Translator()
stbox = None

def bwfy(img, th=200, lonly=False):
    l = img.convert('L')
    if lonly:
        return l
    bw = np.asarray(l).copy()
    bw[bw < th] = 0    # Black
    bw[bw >= th] = 255 # White
    # Now we put it back in Pillow/PIL land
    return Image.fromarray(bw)

class Hidden_ST:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.btn_text = tk.StringVar()
        self.lbl_text = tk.StringVar()
        self.btn_text.set('original subtitle box')
        self.button1 = tk.Button(self.frame, textvariable = self.btn_text, width = 25, command = self.new_window)
        self.button1.pack()
        #self.entry = tk.Text(root, width = 100, height=2, font=("Helvetica", 20))
        #self.entry = tk.Entry(root, width = 100, justify='center')#font=("Helvetica", 20))
        self.entry = tk.Label(root, textvariable=self.lbl_text, width = 100, height=2, font=("Helvetica", 20))
        #self.entry.tag_configure('tag-center', justify='center')
        self.entry.grid(row=0,column=0)
        self.entry.pack()
        self.frame.pack()
        print(self.master.geometry())

    def new_window(self):
        self.btn_text.set('Translated subtitle')
        self.newWindow = tk.Toplevel(self.master)
        self.orig_w = Orig_ST(self.newWindow)
        def detect_st():
            self.master.after(500, detect_st)
            if orig_trans:
                (x, y, w, h, dy) = stbox
                #print(x, y, dy, w, h)
                im = bwfy(grab(bbox=(x, y-dy, w, h+2*dy)), lonly=False, th=200)
                #im.show()
                text = pytesseract.image_to_string(im, lang='chi_sim')
                print(text)
                stext = fanyi.translate(text, src='zh-CN', dest='en').text
                print(stext)
                #self.entry.delete("1.0", tk.END)
                #self.entry.insert(tk.END, stext, 'tag-center')
                self.lbl_text.set(stext)
                #self.master.update()
                self.entry.update_idletasks()
                #self.entry.delete(0, 'end')
                #self.entry.insert('0', stext)
                '''
                if len(text) < 3:
                    self.master.withdraw()
                    #self.master.wm_attributes("-transparent", True)
                    #self.master.config(bg='systemTransparent')
                else:
                    #self.master.wm_attributes("-transparent", False)
                    #self.master.config(bg='white')
                    self.master.wm_deiconify()
                '''

        self.master.after(500, detect_st)

class Orig_ST:
    def __init__(self, master):
        self.master = master
        self.master.wm_attributes("-topmost", 1)
        self.master.bind('<ButtonRelease-1>', self.ss)
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Close', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        global orig_trans
        global stbox
        #self.master.withdraw()
        orig_trans = True
        x = self.master.winfo_x()
        y = self.frame.winfo_rooty()
        w = self.master.winfo_width()
        h = self.frame.winfo_height()
        dy = y - self.master.winfo_y()
        stbox = (x, y, w, h, dy)
        self.master.destroy()
        #self.master.overrideredirect(True)
        #self.master.wm_attributes("-transparent", True)
        #self.master.config(bg='systemTransparent')
        #self.frame.pack_forget()

    def ss(self, event):
        x = self.frame.winfo_rootx()
        y = self.frame.winfo_rooty()
        w = self.frame.winfo_width()
        h = self.frame.winfo_height()
        print(x, y, w, h)

root = tk.Tk()
root.wm_attributes("-topmost", 1)
app = Hidden_ST(root)
root.mainloop()

'''
toggled = False
sct = mss()

def ss(event):
    g = root.geometry()
    a, x, y = g.split('+')
    w, h = [int(e) for e in a.split('x')]
    x, y = int(x), int(y)
    print(x,y,w,h)
    #im = pyautogui.screenshot(region=(x,y+20,w,h-20))
    #monitor = {'top': 40, 'left': 0, 'width': 80, 'height': 70}
    #img = sct.grab(monitor)
    #print(img)
    #print(im.size)
    im = grab(bbox=(x, y, w, h))
    print(im.size)
    #im.show()

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
root.bind('<ButtonRelease-1>', ss)
root.bind('<space>', action)
#t = Text(root, height=1, width=200, selectbackground='black', inactiveselectbackground='red')
#t.pack()
#t.insert(END, "Chuanyou's tool bar to hide Chinese subtitle and learn a foreign language".upper())
#
#entry = tk.Entry(root)
#entry.pack()
#entry.insert("0", "Focus me!")
#c = tk.Canvas(root, width=20, height=20)
#c.pack()
#r = c.create_rectangle((7, 0, 19, 20), fill='white')
#c.tag_bind(r, '<ButtonPress-1>', action)
#c.focus_set()

root.wm_attributes("-topmost", 1)
#root.title("李传猷的可协变量子引力波-人工智能区块链APP以挡住中文字幕来学习外语,就问你怕不怕; just ask you are te or not terrified")
root.mainloop()
'''
