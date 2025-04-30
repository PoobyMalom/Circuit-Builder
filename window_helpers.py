import tkinter as tk

def draw_circle(canvas, x, y, radius, **kwargs):
    return canvas.create_oval(x-radius, y-radius, x+radius, y+radius, **kwargs)

def draw_rect(canvas, x, y, rect_width, rect_height, **kwargs):
    return canvas.create_rectangle(x, y, x+rect_width, y+rect_height, **kwargs)

def draw_line(canvas, x1, y1, x2, y2, **kwargs):
    return canvas.create_line(x1, y1, x2, y2, **kwargs)