"""Module to handle gui and logic for logical not gate"""

import window_helpers as wh
from pin import GUIPin
from component import GUIComponent


class NotGate(GUIComponent):
    """Class to define gui component for logical and gate"""

    def __init__(self, window, canvas, component_id, x, y):
        super().__init__(window, canvas, component_id, x, y)

        self.width = 50
        self.height = 30
        self.pin_radius = 5

        self.draw()
        self.add_component(window, component_id, "NOT", x, y)

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(self.component_shapes[-1], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[-1], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[-1], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(
            f"NOT_{self.component_id}_CLICKABLE", "<Enter>", self.handle_hover_enter
        )
        canvas.tag_bind(
            f"NOT_{self.component_id}_CLICKABLE", "<Leave>", self.handle_hover_leave
        )

    def draw(self):
        body = wh.draw_rect(
            self.canvas,
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
            fill="#a0241c",
        )
        text = wh.draw_text(self.canvas, self.x, self.y, "NOT", fill="#ffffff")

        self.canvas.addtag_withtag(f"NOT_{self.component_id}_CLICKABLE", body)
        self.canvas.addtag_withtag(f"NOT_{self.component_id}_CLICKABLE", text)

        in_pin = GUIPin(
            self.window,
            self.canvas,
            self.component_id,
            self.x - self.width / 2,
            self.y,
            self.pin_radius,
            "IN",
            is_input=True,
            draggable=False,
        )
        out_pin = GUIPin(
            self.window,
            self.canvas,
            self.component_id,
            self.x + self.width / 2,
            self.y,
            self.pin_radius,
            "OUT",
            False,
        )

        self.inputs["IN"] = in_pin
        self.window.pin_lookup[(self.component_id, "IN")] = in_pin
        self.outputs["OUT"] = out_pin
        self.window.pin_lookup[(self.component_id, "OUT")] = out_pin

        self.component_shapes += [body, in_pin.body, out_pin.body, text]
