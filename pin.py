from component import GUIComponent
from circuit import Pin
import window_helpers as wh

class GUIPin(GUIComponent):
    def __init__(self, window, canvas, component_id, x, y, radius, pin_name, is_input, draggable=False):
        super().__init__(window, canvas, component_id, x, y)
        self.radius = radius
        self.pin_name = pin_name
        self.is_input = is_input
        self.draggable = draggable
        self.state = 0
        self.wire = None
        self.body = None

        self.draw()
        self.add_component(window, component_id, x, y)

        window.pin_lookup[(component_id, pin_name)] = self

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.component_shapes[0], "<Button-2>", self.place_wire)

    def draw(self):
        self.body = wh.draw_circle(self.canvas, self.x, self.y, self.radius, fill="black", outline="white")

        if self.is_input:
            self.outputs["OUT"] = self
        else:
            self.inputs["IN"] = self

        self.component_shapes.append(self.body)


    def add_component(self, window, id, x, y):
        comp = Pin(id, "INPUT" if self.is_input else "OUTPUT", [self.pin_name], (x, y))
        window.circuit.add_component(comp)

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
                self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius
            )

            # If connected, update wire end
            if self.wire:
                self.wire.update_wire()

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
        self.canvas.itemconfig(self.component_shapes[0], fill=("green" if logic_value else "black"))

    def place_wire(self, event):
        """
        Trigger wire placement logic from Window.
        """
        direction = "IN" if self.is_input else "OUT"
        self.window.handle_wire_click(self, self.component_id, self.pin_name, self.x, self.y)

    def get_pin_position(self):
        return self._get_center_of(self.body)