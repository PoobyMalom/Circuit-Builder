"""
Filename: input.py
Description: Input component logic and gui elements

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
import window_helpers as wh

class Input:
    """
    Represent an input component

    Attributes:
        window (Window): window to place input component in
        state (bool): state of the input (on/off)
        radius (int): static radius of the input circle
        canvas (tk.Canvas): canvas to place input component in 
        circuit (Circuit): circuit the program is working in
        input_id (string): Component id
        x (int): X-coordinate of the input
        y (int): Y-coordinate of the input
        dragging (bool): variable to track if input is being dragged
        drag_started (bool): variable to track if the input has started to be dragged 
                             (used for click debouncing)
        start_x (int): X-coordinate of input when dragging starts
        start_y (int): Y-coordinate of input when dragging starts
        wire (Wire): wire object connecting input to component
        id (tk.oval): gui oval id
    """
    def __init__(self, canvas, window, circuit, id, x, y):
        self.state = 0
        self.window = window
        self.radius = 15
        self.canvas = canvas
        self.circuit = circuit
        self.input_id = id
        self.x = x
        self.y = y
        self.dragging = False
        self.drag_started = False  # New flag
        self.start_x = 0
        self.start_y = 0

        self.wire = None

        self.id = self.create_input(x, y, self.radius)
        
        canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.id, "<Button-2>", self.place_wire)
    
    def create_input(self, x, y, radius):
        """
        Creates the gui element for the input

        Args:
            x (int): X-coordinate of the input circle
            y (int): Y-coordinate of the input circle
            radius (int): Radius of the input circle

        Returns:
            Tkinted oval object representing our input
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
        Function to change input position in the y direction. Also moves wire segments connected to the input

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
                    _, _, x2, y2 = self.canvas.coords(self.wire.line_segs[0])
                    self.canvas.coords(
                        self.wire.line_segs[0],
                        self.x, self.y,
                        x2, self.y
                    )
                    if len(self.wire.line_segs) > 2:
                        _, _, x2_1, y2_1 = self.canvas.coords(self.wire.line_segs[1])
                        self.canvas.coords(
                            self.wire.line_segs[1],
                            x2, y2,
                            x2_1, y2_1        
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
        Changes state of input and updates gui accordingly

        Args:
            None
        
        Returns:
            None
        """
        if self.state == 0:
            self.canvas.itemconfig(self.id, fill="green")
            self.circuit.components[self.input_id].outputs['OUT'] = True
            self.state = 1
        elif self.state == 1:
            self.canvas.itemconfig(self.id, fill="red")
            self.circuit.components[self.input_id].outputs['OUT'] = False
            self.state = 0

    def place_wire(self, event):
        """
        Handles wire placement from inside input but raises it above

        Args:
            None

        Returns:
            None
        """
        self.window.handle_wire_click(self, self.input_id, "OUT", self.x, self.y)