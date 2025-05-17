"""
Filename: window.py
Description: Main functionality of program and main program window

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
from tkinter import ttk
import window_helpers as wh
from dropdown import Dropdown
from circuit import Circuit, ComponentIDGenerator, Wire
from wire import GUICanvasWire
from andgate import AndGate 
from notgate import NotGate
from toolbar import Toolbar

class Window:
    """
    Main GUI window for the circuit builder application.

    Manages the canvas, circuit data structure, dropdown context menus,
    and interactive wire placement between input and output components.
    """
    def __init__(self, root, width=800, height=600):
        """
        Initializes the main application window, canvas, and layout.

        Args:
            root (tk.Tk): The root Tkinter window.
            width (int): The initial width of the window.
            height (int): The initial height of the window.
        """
        self.root = root
        self.width = width
        self.height = height

        self.circuit = Circuit(self)
        self.id_generator = ComponentIDGenerator()

        self.root.title("Circuit Builder")
        self.root.geometry(f"{width}x{height}")
    

         # Main canvas frame
        self.frame = tk.Frame(root)
        self.frame.place(x=0, y=0, relwidth=1.0, relheight=1.0, anchor='nw')  # Leaves 30px space on each side


        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()
        self.canvas.bind("<Button-2>", self.handle_right_click)
        self.canvas.bind("c", self.print_circuit)
        self.canvas.bind("<Motion>", self.draw_wire)
        self.canvas.bind("b", self.curve_wire)
        self.canvas.bind("a", self.test_and)
        self.canvas.bind("e", self.test_eval)
        self.canvas.bind("n", self.test_not)
        self.canvas.bind("t", self.print_hovered)
        self.canvas.bind("d", self.test_wire_bullshit)
        

        self.dropdown = Dropdown(self.root, self, self.frame, self.canvas, self.circuit, self.id_generator)

        # Bottom toolbar (overlaps input/output bars)
        self.toolbar = Toolbar(self.frame, self)
       
        

        self.root.bind("<Configure>", self.resize_window)
        #self.root.lift()
        self.root.attributes("-topmost", True)
        self.rect_id = wh.draw_rect(self.canvas, 30, 10, self.width - 60, self.height - 50, outline="#444444", width=2)

        self.wire_lookup = {}
        self.gui_lookup = {}

        self.wire_start = None
        self.drawing_wire = False
        self.curr_wire = None

        self.hovered_component = None

    def resize_window(self, event):
        """
        Handles resizing of the main window and updates the canvas boundary box.

        Args:
            event (tk.Event): The window resize event.
        """
        if event.widget == self.root:
            self.height = event.height
            self.width = event.width

            if self.rect_id is not None:
                self.canvas.coords(self.rect_id, 30, 10, self.width - 30, self.height - 50)


    def handle_right_click(self, event):
        """
        Shows the context menu when right-clicking on input/output zones.

        Args:
            event (tk.Event): The mouse click event.
        """
        x, y = event.x, event.y

        self.dropdown.show_context_menu(event)

    def print_circuit(self, _):
        """
        Prints the current circuit's topological order to the console.

        Args:
            event (tk.Event): The keypress event triggering the print.
        """
        print(self.circuit.print_topological_order())

    def handle_wire_click(self, comp, comp_id, pin, x, y):
        """
        Handles logic for beginning or completing a wire connection between components.

        Args:
            comp: The component instance clicked.
            comp_id (str): The component's unique ID.
            pin (str): The pin name ("OUT" or "IN").
            x (int): X-coordinate of the click.
            y (int): Y-coordinate of the click.
        """
        if not self.drawing_wire:
            if not comp.is_input:
                self.wire_start = (comp_id, pin, x, y)
                self.curr_wire = GUICanvasWire(self.canvas, comp_id, pin, None, None)
                
                comp.wire = self.curr_wire
                self.curr_wire.create_wire(x, y)
                self.drawing_wire = True
            else:
                print("Cannot end a wire on an output pin.")
                return

        else:
            if comp.is_input:
                src_id, src_pin, _, _ = self.wire_start
                dst_id, dst_pin = comp_id, pin

                self.curr_wire.dst_pin = dst_id
                self.curr_wire.dst_pin = dst_pin
                self.curr_wire.end_wire(x, y)
                comp.wire = self.curr_wire
                #self.circuit.components[comp.component_id].connected_wires += self.curr_wire.to_dict()

                wire = Wire(src_id, src_pin, dst_id, dst_pin, comp.wire.path)
                self.circuit.connect(wire)
                self.wire_lookup[(src_id, dst_id)] = self.curr_wire

                self.drawing_wire = False
                self.curr_wire = None
                self.wire_start = None
            else:
                print("Cannot end a wire on an input pin.")
                return

    def draw_wire(self, event):
        """
        Updates the visual line segment to follow the mouse as the wire is being drawn.

        Args:
            event (tk.Event): The mouse motion event.
        """
        if self.drawing_wire and self.curr_wire:
            self.curr_wire.draw_wire(event.x, event.y)

    def curve_wire(self, event):
        """
        Adds a curved segment to the currently drawn wire at the mouse location.

        Args:
            event (tk.Event): The keypress event ('b') and current mouse position.
        """
        if self.drawing_wire and self.curr_wire:
            self.curr_wire.curve_wire(event.x, event.y)

    def test_and(self, event):
        AndGate(self, self.canvas, self.id_generator.gen_id(), event.x, event.y)

    def test_eval(self, event):
        self.circuit.evaluate()

    def test_not(self, event):
        NotGate(self, self.canvas, self.id_generator.gen_id(), event.x, event.y)

    def print_hovered(self, event):
        for _, value in self.circuit.components.items():
            print(value.connected_wires)

    def remove_gui_wire(self, src_id, dst_id):
        key = (src_id, dst_id)
        if key in self.wire_lookup:
            wire = self.wire_lookup.pop(key)
            for seg in wire.line_segs:
                self.canvas.delete(seg)

    def test_wire_bullshit(self, event):
        print(self.gui_lookup)
        for component in self.gui_lookup.values():
            print(component.wire)