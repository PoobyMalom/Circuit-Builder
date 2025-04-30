"""
Filename: output.py
Description: Output component logic and gui elements

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
import window_helpers as wh

class Output:
    """
    Represent an output component

    Attributes:
        window (Window): window to place output component in
        state (bool): state of the output (on/off)
        radius (int): static radius of the output circle
        canvas (tk.Canvas): canvas to place output component in 
        circuit (Circuit): circuit the program is working in
        output_id (string): Component id
        x (int): X-coordinate of the output
        y (int): Y-coordinate of the output
        dragging (bool): variable to track if output is being dragged
        drag_started (bool): variable to track if the output has started to be dragged 
                             (used for click debouncing)
        start_x (int): X-coordinate of output when dragging starts
        start_y (int): Y-coordinate of output when dragging starts
        wire (Wire): wire object connecting output to component
        id (tk.oval): gui oval id
    """
    def __init__(self, canvas, window, circuit, id, x, y):
        self.window = window
        self.state = 0
        self.radius = 15
        self.canvas = canvas
        self.circuit = circuit
        self.output_id = id
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_started = False 
        self.start_x = 0
        self.start_y = 0

        self.wire = None

        self.id = self.create_output(x, y, self.radius)

        canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.id, "<Button-2>", self.place_wire)
    
    def create_output(self, x, y, radius):
        """
        Creates the gui element for the output

        Args:
            x (int): X-coordinate of the output circle
            y (int): Y-coordinate of the output circle
            radius (int): Radius of the output circle

        Returns:
            Tkinted oval object representing our output
        """
        return wh.draw_circle(self.canvas, x, y, radius, fill='red', outline='black')

    def start_drag(self, event):
        """
        Function to intiate gui element dragging

        Args:
            event (tk.Event): tkinter event

        Returns:
            none
        """
        self.dragging = True
        self.drag_started = False  # Reset
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event):
        """
        Function to change output position in the y direction. Also moves wire segments connected to the output

        Args:
            event (tk.Event): tkinter event

        Returns:
            none
        """
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
                
                if self.wire:
                    x1, y1, _, _ = self.canvas.coords(self.wire.line_segs[-1])
                    self.canvas.coords(
                        self.wire.line_segs[-1],
                        x1, self.y,
                        self.x, self.y
                    )
                    if len(self.wire.line_segs) > 2:
                        x1_1, y1_1, _, _ = self.canvas.coords(self.wire.line_segs[-2])
                        self.canvas.coords(
                            self.wire.line_segs[-2],
                            x1_1, y1_1,
                            x1, y1        
                        )

    def stop_drag(self, _):
        """
        Function to stop dragging

        Args:
            None

        Returns:
            None
        """
        if not self.drag_started:
            # It was a click, not a drag
            self.change_state()
        self.dragging = False
        self.drag_started = False

    def change_state(self):
        """
        Changes state of output and updates gui accordingly

        Args:
            None
        
        Returns:
            None
        """
        if self.state == 0:
            self.canvas.itemconfig(self.id, fill="green")
            self.circuit.components[self.output_id].inputs['IN'] = True
            self.state = 1
        elif self.state == 1:
            self.canvas.itemconfig(self.id, fill="red")
            self.circuit.components[self.output_id].inputs['IN'] = False
            self.state = 0

    def place_wire(self, _):
        """
        Handles wire placement from inside output but raises it above

        Args:
            None

        Returns:
            None
        """
        self.window.handle_wire_click(self, self.output_id, "IN", self.x, self.y)