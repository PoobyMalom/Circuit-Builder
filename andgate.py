import window_helpers as wh
from circuit import Component, Wire
from gui_pin import GUIPin

class AndGate:
    def __init__(self, canvas, window, circuit, id_generator, x, y):
        self.canvas = canvas
        self.window = window
        self.circuit= circuit
        self.id_generator = id_generator
        self.id = id_generator.gen_id()
        self.x = x
        self.y = y
        self.component_shapes = [] # List to keep track of all tkinter objects that make up the and gate
        self.components = []

        self.width = 50
        self.height = 30

        self.pin_radius = 5

        # Base Rectangle

        self.base = wh.draw_rect(canvas, x - self.width/2, y - self.height/2, self.width, self.height, fill="#247ec4")
        self.component_shapes.append(self.base)
        self.components.append("")

        self.andgate = Component(self.id, "AND", {"A": False, "B": False}, {"OUT": False})
        self.circuit.add_component(self.andgate)

        self.input1 = GUIPin(canvas, window, circuit, x - self.width/2, y + self.height/4, self.pin_radius, self.andgate.id, "A", is_input=True, draggable=False)
        self.input2 = GUIPin(canvas, window, circuit, x - self.width/2, y - self.height/4, self.pin_radius, self.andgate.id, "B", is_input=True, draggable=False)
        self.component_shapes += [self.input1.id, self.input2.id]
        self.components += [self.input1, self.input2]

        self.output1 = GUIPin(canvas, window, circuit, x + self.width/2, y, self.pin_radius, self.andgate.id, "OUT", is_input=False, draggable=False)  #wh.draw_circle(canvas, x + self.width/2, y, self.pin_radius, fill="black")
        self.component_shapes.append(self.output1.id)
        self.components.append(self.output1)

        self.text = wh.draw_text(self.canvas, x, y, "AND", fill="#ffffff")
        self.component_shapes.append(self.text)
        self.components.append("")


        
        # print(self.input1.output_pin.id)
        # print(self.input2.output_pin.id)
        # print(self.andgate.id)
        # self.circuit.connect(Wire(self.input1.output_pin.id, "OUT", self.andgate.id, "A"))

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

        for i in range(len(self.component_shapes)):
            canvas.addtag_withtag(f"AND_{self.id}", self.component_shapes[i])
            if self.components[i] == "":
                canvas.addtag_withtag(f"AND_{self.id}_CLICKABLE", self.component_shapes[i])

        canvas.tag_bind(f"AND_{self.id}_CLICKABLE", "<Enter>", self.handle_hover_enter)
        canvas.tag_bind(f"AND_{self.id}_CLICKABLE", "<Leave>", self.handle_hover_leave)


    def start_drag(self, event):
        """
        Function to intiate gui element dragging

        Args:
            event (tk.Event): tkinter event

        Returns:
            none
        """
        self.dragging = True
        self.drag_started = False  # Reset
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event):
        """
        Function to change output position in the y direction. Also moves wire segments connected to the output

        Args:
            event (tk.Event): tkinter event

        Returns:
            none
        """
        self.input1.x, self.input1.y = event.x - self.width/2, event.y + self.height/4
        self.input2.x, self.input2.y = event.x - self.width/2, event.y - self.height/4
        self.output1.x, self.output1.y = event.x + self.width/2, event.y

        if self.dragging:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            # If moved enough pixels, mark as a real drag
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
        """
        Function to stop dragging

        Args:
            None

        Returns:
            None
        """
        if not self.drag_started:
            # It was a click, not a drag
            pass
        self.dragging = False
        self.drag_started = False
        
    def handle_hover_enter(self, event):
        self.window.hovered_component = self

    def handle_hover_leave(self, event):
        self.window.hovered_component = None