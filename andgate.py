"""Class to handle gui and logic for logical and gate"""

import window_helpers as wh
from pin import GUIPin
from component import GUIComponent


class AndGate(GUIComponent):
    """Class to define gui component for logical and gate"""

    def __init__(
        self, window, canvas, component_id, x, y
    ):  # pylint: disable=too-many-arguments, too-many-positional-arguments
        super().__init__(window, canvas, component_id, x, y)

        self.width = 50
        self.height = 30
        self.pin_radius = 5

        self.draw()
        self.add_component(window, component_id, "AND", x, y)

        canvas.tag_bind(self.component_shapes[0], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[0], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[0], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(self.component_shapes[-1], "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.component_shapes[-1], "<B1-Motion>", self.drag)
        canvas.tag_bind(self.component_shapes[-1], "<ButtonRelease-1>", self.stop_drag)

        canvas.tag_bind(
            f"AND_{self.component_id}_CLICKABLE", "<Enter>", self.handle_hover_enter
        )
        canvas.tag_bind(
            f"AND_{self.component_id}_CLICKABLE", "<Leave>", self.handle_hover_leave
        )

    def draw(self):
        body = wh.draw_rect(
            self.canvas,
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
            fill="#247ec4",
        )
        text = wh.draw_text(self.canvas, self.x, self.y, "AND", fill="#ffffff")

        self.canvas.addtag_withtag(f"AND_{self.component_id}_CLICKABLE", body)
        self.canvas.addtag_withtag(f"AND_{self.component_id}_CLICKABLE", text)

        a = GUIPin(
            self.window,
            self.canvas,
            self.component_id,
            self.x - self.width / 2,
            self.y + self.height / 4,
            self.pin_radius,
            "A",
            is_input=True,
            draggable=False,
        )
        b = GUIPin(
            self.window,
            self.canvas,
            self.component_id,
            self.x - self.width / 2,
            self.y - self.height / 4,
            self.pin_radius,
            "B",
            is_input=True,
            draggable=False,
        )
        out = GUIPin(
            self.window,
            self.canvas,
            self.component_id,
            self.x + self.width / 2,
            self.y,
            self.pin_radius,
            "OUT",
            False,
        )

        self.inputs["A"] = a
        self.window.pin_lookup[(self.component_id, "A")] = a
        self.inputs["B"] = b
        self.window.pin_lookup[(self.component_id, "B")] = b
        self.outputs["OUT"] = out
        self.window.pin_lookup[(self.component_id, "OUT")] = out

        self.component_shapes += [body, a.body, b.body, out.body, text]
