# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Code was created by @mp035 https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
# The onMouseWheel function was modified to use an improvement by @adam-jw-casey https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01?permalink_comment_id=4512797#gistcomment-4512797

import platform
import tkinter as tk
from tkinter import ttk


# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(ttk.Frame):
    def __init__(self, parent, background='#ffffff', borderwidth=0, usettk=False, **kwargs):
        super().__init__(parent, **kwargs)

        if usettk:
            background = ttk.Style().lookup("TFrame", "background", default="white")
            self.viewPort = tk.Frame(self.canvas, background=background)
        else:
            self.viewPort = ttk.Frame(self.canvas)

        self.canvas = tk.Canvas(self, borderwidth=borderwidth, background=background, **kwargs)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.viewPort.bind('<Enter>', self.onEnter)
        self.viewPort.bind('<Leave>', self.onLeave)
        
        self.canvas.bind("<Motion>", self.onTouchScroll)  
        self.canvas.bind("<ButtonPress-1>", self.onTouchStart)
        self.canvas.bind("<B1-Motion>", self.onTouchMove)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width - 2)            #whenever the size of the canvas changes alter the window region respectively.
    
    def resetCanvasScroll(self):
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0.5)

def onMouseWheel(self, event: tk.Event):
    """Scroll in computer"""
    canvas_height = self.canvas.winfo_height()
    rows_height = self.canvas.bbox("all")[3]

    if rows_height > canvas_height:  # Chỉ cuộn nếu có nội dung dư
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

def onTouchScroll(self, touch):
    """Scroll in Android"""
    if touch.dy:
        self.canvas.yview_scroll(-int(touch.dy / 10), "units")

def onEnter(self, event):
    """Enable scrolling when mouse enters frame (desktop only)"""
    if platform.system() == 'Linux':
        self.canvas.bind_all("<Button-4>", self.onMouseWheel)
        self.canvas.bind_all("<Button-5>", self.onMouseWheel)
    else:
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

def onLeave(self, event):
    """Disable scrolling when mouse leaves frame (desktop only)"""
    if platform.system() == 'Linux':
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
    else:
        self.canvas.unbind_all("<MouseWheel>")

def on_touch_down(self, touch):
    """Bật cuộn khi người dùng chạm vào màn hình trên Android"""
    self.canvas.bind("<Motion>", self.onTouchScroll)