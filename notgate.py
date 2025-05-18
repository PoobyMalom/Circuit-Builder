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

        canvas.tag_bind(f"NOT_{self.component_id}_CLICKABLE", "<Enter>", self.handle_hover_enter)
        canvas.tag_bind(f"NOT_{self.component_id}_CLICKABLE", "<Leave>", self.handle_hover_leave)

    def draw(self):
        body = wh.draw_rect(self.canvas, self.x - self.width/2, self.y - self.height/2, self.width, self.height, fill="#a0241c")
        text = wh.draw_text(self.canvas, self.x, self.y, "NOT", fill="#ffffff")

        self.canvas.addtag_withtag(f"NOT_{self.component_id}_CLICKABLE", body)
        self.canvas.addtag_withtag(f"NOT_{self.component_id}_CLICKABLE", text)

        In = GUIPin(self.window, self.canvas, self.component_id, self.x - self.width/2, self.y, self.pin_radius, "IN", is_input=True, draggable=False)
        Out = GUIPin(self.window, self.canvas, self.component_id, self.x + self.width/2, self.y, self.pin_radius, "OUT", False)

        self.inputs["IN"] = In
        self.window.pin_lookup[(self.component_id, "IN")] = In
        self.outputs["OUT"] = Out
        self.window.pin_lookup[(self.component_id, "OUT")] = Out

        self.component_shapes += [body, In.body, Out.body, text]

    def add_component(self, window, id, x, y):
        self.logic_component = Component(id, "NOT", self.inputs, self.outputs, (x, y))
        window.circuit.add_component(self.logic_component)