import window_helpers as wh
from circuit import Component, Wire
from gui_pin import GUIPin

class NotGate:
    def __init__(self, canvas, window, circuit, id_generator, x, y):
        self.canvas = canvas
        self.window = window
        self.circuit = circuit
        self.id_generator = id_generator
        self.id = id_generator.gen_id()
        self.x = x
        self.y = y
        self.component_shapes = []
        self.components = []

        self.width = 50
        self.height = 30

        self.pin_radius = 5

        self.base = wh.draw_rect(canvas, x - self.width/2, y - self.height/2, self.width, self.height, fill="#a0241c")
        self.component_shapes.append(self.base)
        self.components.append("")

        self.notgate = Component(self.id, "NOT", {"IN": False}, {"OUT", False})
        self.circuit.add_component(self.notgate)
        self.components.append("")

        self.input = GUIPin(canvas, window, circuit, x - self.width/2, y, self.pin_radius, self.notgate.id, "IN", is_input=True, draggable=False)
        self.component_shapes.append(self.input.id)
        self.components.append(self.input)

        self.output = GUIPin(canvas, window, circuit, x + self.width/2, y, self.pin_radius, self.notgate.id, "OUT", is_input=False, draggable=False)
        self.component_shapes.append(self.output.id)
        self.components.append(self.output)

        self.text = wh.draw_text(self.canvas, x, y, "NOT", fill='#ffffff')
        self.component_shapes.append(self.text)
        self.components.append("")

        self.dragging = False
        self.drag_started = False
        self.start_x = 0
        self.start_y = 0

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(self.component_shapes[-1], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[-1], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[-1], "<ButtonRelease-1>", self.stop_drag)

    def start_drag(self, event):
        self.dragging = True
        self.drag_started = False
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event):
        self.input.x, self.input.y = event.x - self.width/2, event.y
        self.output.x, self.output.x = event.x + self.width/2, event.y

        if self.dragging:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            if abs(dx) > 2 or abs(dy) > 2:
                self.drag_started = True

                dx = self.x - event.x
                dy = self.y - event.y

                self.x = event.x
                self.y = event.y

                for i in range(len(self.component_shapes)):
                    self.canvas.move(self.component_shapes[i], -dx, -dy)
                    if hasattr(self.components[i], "update_wires"):
                        self.components[i].update_wires(event)

    def stop_drag(self, _):
        if not self.drag_started:
            pass
        self.dragging = False
        self.drag_started = False