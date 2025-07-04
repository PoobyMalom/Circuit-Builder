"""
Filename: window.py
Description: Main functionality of program and main program window

Author: Toby Mallon
Created: 4-28-2025
"""

import tkinter as tk
import window_helpers as wh
from dropdown import Dropdown
from circuit import Circuit, ComponentIDGenerator, Wire
from wire import GUICanvasWire, WireController
from andgate import AndGate
from notgate import NotGate
from toolbar import Toolbar
from ghost import Ghost


class Window:  # pylint: disable=too-many-instance-attributes
    # TODO Clean up instance attributes. distribute into objects.
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
        self.frame.place(x=0, y=0, relwidth=1.0, relheight=1.0, anchor="nw")
        # Leaves 30px space on each side

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

        self.dropdown = Dropdown(
            self.root, self, self.frame, self.canvas, self.circuit, self.id_generator
        )

        # Bottom toolbar (overlaps input/output bars)
        self.toolbar = Toolbar(self.frame, self)

        self.root.bind("<Configure>", self.resize_window)
        # self.root.lift()
        self.root.attributes("-topmost", True)
        self.rect_id = wh.draw_rect(
            self.canvas,
            30,
            10,
            self.width - 60,
            self.height - 50,
            outline="#444444",
            width=2,
        )

        self.wire_lookup = {}
        self.gui_lookup = {}
        self.pin_lookup = {}

        self.wire_start = None
        self.drawing_wire = False
        self.curr_wire = None

        self.hovered_component = None
        self.placing_type = None
        self.ghost = None

        self.wire_ctrl = WireController(self.canvas, self.circuit, self)

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
                self.canvas.coords(
                    self.rect_id, 30, 10, self.width - 30, self.height - 50
                )

    def handle_right_click(self, event):
        """
        Shows the context menu when right-clicking on input/output zones.

        Args:
            event (tk.Event): The mouse click event.
        """
        self.dropdown.show_context_menu(event)

    def print_circuit(self, _):
        """
        Prints the current circuit's topological order to the console.

        Args:
            event (tk.Event): The keypress event triggering the print.
        """
        print(self.circuit)

    def handle_pin_click(self, pin):
        """
        Handles logic for beginning or completing a wire connection between components.

        Args:
            comp: The component instance clicked.
            comp_id (str): The component's unique ID.
            pin (str): The pin name ("OUT" or "IN").
            x (int): X-coordinate of the click.
            y (int): Y-coordinate of the click.
        """
        if self.wire_ctrl.active:
            self.wire_ctrl.commit(pin)
        else:
            self.wire_ctrl.start(pin)

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

    # TODO Delete all these stupid ass functions

    def test_and(self, event):
        """Test function for placing and gates"""
        AndGate(self, self.canvas, self.id_generator.gen_id(), event.x, event.y)

    def test_eval(self, _):
        """Test function for evaluating circuits"""
        self.circuit.evaluate()

    def test_not(self, event):
        """Test function for testing not gates"""
        NotGate(self, self.canvas, self.id_generator.gen_id(), event.x, event.y)

    def print_hovered(self, _):
        """Test function for prints connected wires"""
        for _, value in self.circuit.components.items():
            print(value.connected_wires)

    def remove_gui_wire(self, src_id, dst_id):
        """Function to remove gui wires from the canvas"""
        # TODO delete this i think nothing uses it anymore
        key = (src_id, dst_id)
        if key in self.wire_lookup:
            for wire in self.wire_lookup.pop(key):
                for seg in wire.line_segs:
                    self.canvas.delete(seg)

    def test_wire_bullshit(self, _):
        """Prints wire lookup????"""
        # TODO DELETE BULLSHIT
        print(self.wire_lookup)

    def refresh_gui_from_logic(self):
        """Refreshes gui based on updated logic"""
        # TODO this is outdated fairly sure this is implemented in the circuit now
        for comp_id, comp in self.circuit.components.items():
            if comp.type == "INPUT":
                logic_value = comp.inputs["IN"]
                gui_pin = self.pin_lookup[(comp_id, "IN")]
                gui_pin.set_state_color(logic_value)

    def add_component(self, comp_type):
        """Adds ghost component and bindings"""
        self.canvas.focus_set()
        self.placing_type = comp_type
        self.canvas.config(cursor="crosshair")

        x, y = self.canvas.winfo_pointerxy()
        self.ghost = self.draw_ghost_gate(comp_type, x, y)
        print(self.ghost)

        self._ghost_move_id = self.canvas.bind("<Motion>", self._ghost_move, add="+")
        self._ghost_click_id = self.canvas.bind(
            "<Button-1>", self._ghost_place, add="+"
        )

    def _ghost_move(self, event):
        if not self.placing_type:
            return

        print("moving")
        new_x, new_y = event.x, event.y
        self.ghost.move(new_x, new_y)

    def _ghost_place(self, event):
        if not self.placing_type:
            return

        if self.placing_type == "AND":
            gate = AndGate(
                self,
                self.canvas,
                component_id=self.id_generator.gen_id(),
                x=event.x,
                y=event.y,
            )
        elif self.placing_type == "NOT":
            gate = NotGate(
                self,
                self.canvas,
                component_id=self.id_generator.gen_id(),
                x=event.x,
                y=event.y,
            )

        self.ghost.delete()

        self.placing_type = None
        self.ghost = None
        self.canvas.config(cursor="")
        self.canvas.unbind("<Motion>", self._ghost_move_id)
        self.canvas.unbind("<Button-1>", self._ghost_click_id)

    def draw_ghost_gate(self, comp_type, x, y):
        """Draws ghost gate"""
        if comp_type == "AND":
            return Ghost(self, self.canvas, x, y, 50, 30, "#247ec4")
        if comp_type == "NOT":
            return Ghost(self, self.canvas, x, y, 50, 30, "#a0241c")
        return TypeError("UH you fucked up this implementation")
