"""
Filename: dropdown.py
Description: Dropdown window class file 

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
from circuit import InputPin, OutputPin
from gui_pin import GUIPin

class Dropdown():
    """
    Represents a dropdown menu created by right clicking on the canvas

    Attributes:
        root (tk.TK): root of the tkinter program
        window (Window): window that the dropdown menu is currently on
        frame (tk.Frame): canvas frame the dropdown menu interacts with
        canvas (tk.Canvas): canvas the the dropdown menu resides in
        circuit (Circuit): circuit that the program is working in
        id_generator (ComponentIDGenerator): id generator for new components
        context_menu (tk.Menu): dropdown menu constructor
        last_event (tk.Event): last event performed on the dropdown menu
    """
    def __init__(self, root, window, frame, canvas, circuit, id_generator):
        self.root = root
        self.window = window
        self.frame = frame
        self.canvas = canvas
        self.circuit = circuit
        self.id_generator = id_generator

        self.context_menu = tk.Menu(self.root, tearoff=0)

        self.last_event = None

    def show_context_menu(self, event):
        """
        Shows dropdown menu with different options depending on where the mouse was clicked

        Args:
            event (tk.Event): Event that caused this function to be called

        Returns:
            None
        """
        self.last_event = event

        self.context_menu.delete(0, tk.END)

        if event.x < 30:
            self.context_menu.add_command(label="Place Input", command=self.place_input)

        if event.x > self.frame.winfo_width() - 50:
            self.context_menu.add_command(label="Place Output", command=self.place_output)
        if self.window.hovered_component:
            if self.window.hovered_component.type == "AND":
                self.context_menu.add_command(label="Delete Component", command=self.delete_component)

        self.context_menu.tk_popup(event.x_root, event.y_root)

    def place_input(self):
        """
        Adds a new input to the canvas and the circuit

        Args:
            None

        Return:
            None
        """
        if self.last_event:
            comp_id = self.id_generator.gen_id()
            logic_input = InputPin(comp_id, ["OUT"])
            self.circuit.add_component(logic_input)
            GUIPin(self.canvas, 
                   self.window, 
                   self.circuit, 
                   x=30, 
                   y=self.last_event.y, 
                   radius=15, 
                   component_id=comp_id,
                   pin_name="OUT",
                   is_input=False,
                   draggable=True
                   )

    def place_output(self):
        """
        Adds a new output to the canvas and the circuit

        Args:
            None

        Return:
            None
        """
        if self.last_event:
            comp_id = self.id_generator.gen_id()
            logic_output = InputPin(comp_id, ["IN"])
            self.circuit.add_component(logic_output)
            GUIPin(self.canvas, 
                   self.window, 
                   self.circuit, 
                   x=self.frame.winfo_width() - 30, 
                   y=self.last_event.y, 
                   radius=15, 
                   component_id=comp_id,
                   pin_name="IN",
                   is_input=True,
                   draggable=True
                   )
            
    def delete_component(self):
        self.canvas.delete(f"{self.window.hovered_component.type}_{self.window.hovered_component.id}")
        self.circuit.delete_component(self.window.hovered_component)
        self.window.hovered_component = None