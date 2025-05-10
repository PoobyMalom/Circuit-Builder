import tkinter as tk
import window_helpers as wh
from circuit import InputPin, OutputPin

class GUIPin:
    """
    Represents a GUI pin that can act as either a logic source or sink.

    Attributes:
        canvas (tk.Canvas): Canvas to draw the pin on
        window (Window): Window reference to call wire logic
        circuit (Circuit): The logical circuit object
        x, y (int): Pin coordinates
        radius (int): Radius of the pin circle
        is_input (bool): True if sink (e.g., connects to gate input), False if source (e.g., toggleable input)
        component_id (str): ID of the logical component this pin connects to
        pin_name (str): Name of the logic pin ("A", "OUT", etc.)
        wire (GUICanvasWire): Currently attached GUI wire, if any
    """
    def __init__(self, canvas, window, x, y, radius, component_id, pin_name, is_input, draggable=False):
        self.canvas = canvas
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.is_input = is_input
        self.component_id = component_id
        self.pin_name = pin_name
        self.dragging = False
        self.drag_started = False
        self.wire = None
        self.draggable = draggable
        self.state = 0

        self.id = self.create_pin(x, y)

        canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.id, "<Button-2>", self.place_wire)

    def create_pin(self, x, y):
        color = "black"
        return wh.draw_circle(self.canvas, x, y, self.radius, fill=color, outline='white')

    def start_drag(self, event):
        if self.draggable:
            self.dragging = True
            self.drag_started = False
            self.start_x = event.x
            self.start_y = event.y

    def drag(self, event):
        if not self.dragging:
            return

        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if abs(dx) > 2 or abs(dy) > 2:
            self.drag_started = True
            self.y = event.y
            self.canvas.coords(
                self.id,
                self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius
            )

            # If connected, update wire end
            if self.wire:
                if self.is_input:
                    x1, y1, _, _ = self.canvas.coords(self.wire.line_segs[-1])
                    self.canvas.coords(self.wire.line_segs[-1], x1, self.y, self.x, self.y)
                    if len(self.wire.line_segs) > 2:
                        x1_1, y1_1, _, _ = self.canvas.coords(self.wire.line_segs[-2])
                        self.canvas.coords(self.wire.line_segs[-2], x1_1, y1_1, x1, y1)
                else:
                    _, _, x2, y2 = self.canvas.coords(self.wire.line_segs[0])
                    self.canvas.coords(self.wire.line_segs[0], self.x, self.y, x2, self.y)
                    if len(self.wire.line_segs) > 2:
                        _, _, x2_1, y2_1 = self.canvas.coords(self.wire.line_segs[1])
                        self.canvas.coords(self.wire.line_segs[1], x2, y2, x2_1, y2_1)

    def stop_drag(self, _):
        if not self.drag_started and not self.is_input:
            self.toggle_state()
        self.dragging = False
        self.drag_started = False

    def toggle_state(self):
        """
        Flip the logic value of the pin and trigger evaluation if source.
        """
        logic_pin = self.window.circuit.components[self.component_id]

        if self.state == 0:
            self.canvas.itemconfig(self.id, fill="green")
            logic_pin.outputs[self.pin_name] = True
            self.state = 1
        else:
            self.canvas.itemconfig(self.id, fill="black")
            logic_pin.outputs[self.pin_name] = False
            self.state = 0

        self.window.circuit.evaluate()

    def place_wire(self, event):
        """
        Trigger wire placement logic from Window.
        """
        direction = "IN" if self.is_input else "OUT"
        self.window.handle_wire_click(self, self.component_id, self.pin_name, self.x, self.y)

    def update_wires(self, event):
        if self.wire:
            print("found wire")
            if self.is_input:
                print("input")
                x1, y1, _, _ = self.canvas.coords(self.wire.line_segs[-1])
                self.canvas.coords(self.wire.line_segs[-1], x1, self.y, self.x, self.y)
                if len(self.wire.line_segs) > 2:
                    x1_1, y1_1, _, _ = self.canvas.coords(self.wire.line_segs[-2])
                    self.canvas.coords(self.wire.line_segs[-2], x1_1, y1_1, x1, y1)
            else:
                print("output")
                _, _, x2, y2 = self.canvas.coords(self.wire.line_segs[0])
                self.canvas.coords(self.wire.line_segs[0], self.x, self.y, x2, self.y)
                if len(self.wire.line_segs) > 2:
                    _, _, x2_1, y2_1 = self.canvas.coords(self.wire.line_segs[1])
                    self.canvas.coords(self.wire.line_segs[1], x2, y2, x2_1, y2_1)
