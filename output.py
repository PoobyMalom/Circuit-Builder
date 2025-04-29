import tkinter as tk
import window_helpers as wh

class Output:
    def __init__(self, canvas, x, y):
        self.state = 0
        self.radius = 15
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_started = False  # New flag
        self.start_x = 0
        self.start_y = 0

        self.id = self.create_output(x, y, self.radius)

        canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.stop_drag)
    
    def create_output(self, x, y, radius):
        return wh.draw_circle(self.canvas, x, y, radius, fill='red', outline='black')

    def start_drag(self, event):
        self.dragging = True
        self.drag_started = False  # Reset
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event):
        if self.dragging:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            # If moved enough pixels, mark as a real drag
            if abs(dx) > 2 or abs(dy) > 2:
                self.drag_started = True

                # Actually move the object
                self.y = event.y
                self.canvas.coords(
                    self.id, 
                    self.x - self.radius, event.y - self.radius,
                    self.x + self.radius, event.y + self.radius
                )

    def stop_drag(self, event):
        if not self.drag_started:
            # It was a click, not a drag
            self.change_state()
        self.dragging = False
        self.drag_started = False

    def change_state(self):
        if self.state == 0:
            self.canvas.itemconfig(self.id, fill="green")
            self.state = 1
        elif self.state == 1:
            self.canvas.itemconfig(self.id, fill="red")
            self.state = 0