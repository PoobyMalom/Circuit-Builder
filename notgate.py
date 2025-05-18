import window_helpers as wh
from circuit import Component, Wire
from pin import GUIPin
from component import GUIComponent

class NotGate(GUIComponent):
    def __init__(self, window, canvas, component_id, x, y):
        super().__init__(window, canvas, component_id, x, y)

        self.width = 50
        self.height = 30
        self.pin_radius = 5

        self.draw()
        self.add_component(window, component_id, x, y)

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(self.component_shapes[-1], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[-1], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[-1], "<ButtonRelease-1>", self.stop_drag)

    def draw(self):
        body = wh.draw_rect(self.canvas, self.x - self.width/2, self.y - self.height/2, self.width, self.height, fill="#a0241c")

        In = GUIPin(self.canvas, self.window, self.x - self.width/2, self.y, self.pin_radius, self.component_id, "IN", is_input=True, draggable=False)
        Out = GUIPin(self.canvas, self.window, self.x + self.width/2, self.y, self.pin_radius, self.component_id, "OUT", False)
        text = wh.draw_text(self.canvas, self.x, self.y, "NOT", fill="#ffffff")

        self.inputs["IN"] = In
        self.outputs["OUT"] = Out

        self.component_shapes += [body, In.id, Out.id, text]

    def add_component(self, window, id, x, y):
        comp = Component(id, "NOT", self.inputs, self.outputs, (x, y))
        window.circuit.add_component(comp)