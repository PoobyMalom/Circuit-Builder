import tkinter as tk
import window_helpers as wh

class Input:
    def __init__(self, canvas, x, y):
        self.state = 0
        self.radius = 15
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dragging = False

        self.id = self.create_input(x, y, self.radius)
        
        canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.stop_drag)
    
    def create_input(self, x, y, radius):
        return wh.draw_circle(self.canvas, x, y, radius, fill='red', outline='black')

    def start_drag(self, event):
        self.dragging = True

    def drag(self, event):
        if self.dragging:
            self.y = event.y
            self.canvas.coords(
                self.id, 
                self.x - self.radius, event.y - self.radius,
                self.x + self.radius, event.y + self.radius
            )

    def stop_drag(self, event):
        self.dragging = False