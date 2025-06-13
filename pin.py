"""Module to define gui and logic for input or output pin"""

from component import GUIComponent
from circuit import Pin
import window_helpers as wh


class GUIPin(GUIComponent):
    """Class to control logic and gui elements for a pin object"""

    def __init__(
        self,
        window,
        canvas,
        component_id,
        x,
        y,
        radius,
        pin_name,
        is_input,
        draggable=False,
    ):
        super().__init__(window, canvas, component_id, x, y)
        self.radius = radius
        self.pin_name = pin_name
        self.is_input = is_input
        self.draggable = draggable
        self.state = 0
        self.wire = []
        self.body = None

        self.draw()
        self.add_pin(window, component_id, x, y)

        window.pin_lookup[(component_id, pin_name)] = self

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.component_shapes[0], "<Button-2>", self.place_wire)

        if self.draggable:
            canvas.tag_bind(
                self.component_shapes[0], "<Enter>", self.handle_hover_enter
            )
            canvas.tag_bind(
                self.component_shapes[0], "<Leave>", self.handle_hover_leave
            )

    def draw(self):
        self.body = wh.draw_circle(
            self.canvas, self.x, self.y, self.radius, fill="black", outline="white"
        )

        if self.is_input:
            self.outputs["OUT"] = self
        else:
            self.inputs["IN"] = self

        self.component_shapes.append(self.body)

    def add_pin(self, window, comp_id, x, y):
        """Overide adding component due to this being a pin"""
        self.logic_component = Pin(
            comp_id, "INPUT" if self.is_input else "OUTPUT", [self.pin_name], (x, y)
        )
        window.circuit.add_component(self.logic_component)

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
                self.component_shapes[0],
                self.x - self.radius,
                self.y - self.radius,
                self.x + self.radius,
                self.y + self.radius,
            )

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
            self.canvas.itemconfig(self.component_shapes[0], fill="green")
            logic_pin.outputs[self.pin_name] = True
            self.state = 1
        else:
            self.canvas.itemconfig(self.component_shapes[0], fill="black")
            logic_pin.outputs[self.pin_name] = False
            self.state = 0

        self.window.circuit.evaluate()

    def set_state_color(self, logic_value):
        """Sets state color based on logic value"""
        self.canvas.itemconfig(
            self.component_shapes[0], fill=("green" if logic_value else "black")
        )

    def place_wire(self, event):
        """
        Trigger wire placement logic from Window.
        """
        if (event.x > 30) and (event.x < self.window.width - 30):
            self.window.handle_pin_click(self)

    def get_pin_position(self):
        x0, y0, x1, y1 = self.canvas.coords(self.body)
        return ((x0 + x1) / 2, (y0 + y1) / 2)
