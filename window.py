import tkinter as tk
from tkinter import ttk
import window_helpers as wh
from dropdown import Dropdown
from circuit import Circuit, ComponentIDGenerator, Wire
from wire import GUICanvasWire

class Window:
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.width = width
        self.height = height

        self.circuit = Circuit()
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

        self.dropdown = Dropdown(self.root, self, self.frame, self.canvas, self.circuit, self.id_generator)

        # Bottom toolbar (overlaps input/output bars)
        self.toolbar = tk.Frame(root, height=30, bg="darkgray")
        self.toolbar.place(x=0, rely=1.0, anchor='sw', relwidth=1.0)

        self.root.bind("<Configure>", self.resize_window)
        #self.root.lift()
        self.root.attributes("-topmost", True)

        self.rect_id = wh.draw_rect(self.canvas, 30, 10, self.width - 60, self.height - 50, outline="#444444", width=2)

        self.wire_start = None
        self.drawing_wire = False
        self.curr_wire = None


    def resize_window(self, event):
        if event.widget == self.root:
            self.height = event.height
            self.width = event.width

            if self.rect_id is not None:
                self.canvas.coords(self.rect_id, 30, 10, self.width - 30, self.height - 50)


    def handle_right_click(self, event):
        x, y = event.x, event.y

        if (0 <= x < 30 or self.width - 30 <= x < self.width) and 0 <= y <= self.height - 50:
            self.dropdown.show_context_menu(event)

    def print_circuit(self, event):
        print(self.circuit.print_topological_order())

    def handle_wire_click(self, comp, comp_id, pin, x, y):
        if (not self.drawing_wire) and (pin == "OUT"):
            self.wire_start = (comp_id, pin, x, y)
            self.curr_wire = GUICanvasWire(self.canvas, comp_id, pin, None, None)
            comp.wire = self.curr_wire
            self.curr_wire.create_wire(x, y)
            self.drawing_wire = True
        else:
            src_id, src_pin, x0, y0 = self.wire_start
            dst_id, dst_pin = comp_id, pin

            self.curr_wire.dst_pin = dst_id
            self.curr_wire.dst_pin = dst_pin
            self.curr_wire.end_wire(x, y)
            comp.wire = self.curr_wire

            wire = Wire(src_id, src_pin, dst_id, dst_pin)
            self.circuit.connect(wire)

            self.drawing_wire = False
            self.curr_wire = None
            self.wire_start = None

    def draw_wire(self, event):
        if self.drawing_wire and self.curr_wire:
            self.curr_wire.draw_wire(event.x, event.y)

    def curve_wire(self, event):
        if self.drawing_wire and self.curr_wire:
            self.curr_wire.curve_wire(event.x, event.y)