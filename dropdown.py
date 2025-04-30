"""
Filename: dropdown.py
Description: Dropdown window class file 

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
from input import Input
from output import Output
from circuit import InputPin, OutputPin

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
            new_id = self.id_generator.gen_id()
            input_pin = InputPin(new_id, ["OUT"])
            self.circuit.add_component(input_pin)

            Input(self.canvas, self.window, self.circuit, new_id, 30, self.last_event.y)

    def place_output(self):
        """
        Adds a new output to the canvas and the circuit

        Args:
            None

        Return:
            None
        """
        if self.last_event:
            new_id = self.id_generator.gen_id()
            output_pin = OutputPin(new_id, ["IN"])
            self.circuit.add_component(output_pin)

            Output(self.canvas, self.window, self.circuit, new_id, self.frame.winfo_width() - 30, self.last_event.y)
