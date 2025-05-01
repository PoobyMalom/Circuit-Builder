import window_helpers as wh
from circuit import Component
from input import Input
from output import Output

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

        self.width = 50
        self.height = 30

        self.pin_radius = 5

        # Base Rectangle

        self.base = wh.draw_rect(canvas, x - self.width/2, y - self.height/2, self.width, self.height, fill="#247ec4")
        self.component_shapes.append(self.base)

        self.input1 = Output(canvas, window, circuit, x - self.width/2, y + self.height/4, self.pin_radius, id_generator, False) #wh.draw_circle(canvas, x - self.width/2, y - self.height/4, self.pin_radius, fill="black")
        self.input2 = Output(canvas, window, circuit, x - self.width/2, y - self.height/4, self.pin_radius, id_generator, False) #wh.draw_circle(canvas, x - self.width/2, y + self.height/4, self.pin_radius, fill="black")
        self.component_shapes += [self.input1.id, self.input2.id]

        self.output1 = Input(canvas, window, circuit, x + self.width/2, y, self.pin_radius, id_generator, False)  #wh.draw_circle(canvas, x + self.width/2, y, self.pin_radius, fill="black")
        self.component_shapes.append(self.output1.id)

        self.text = wh.draw_text(self.canvas, x, y, "AND", fill="#ffffff")
        self.component_shapes.append(self.text)

        self.andgate = Component(self.id, "AND", {"A": False, "B": False}, {"OUT": False})
        self.circuit.add_component(self.andgate)

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
                for item in self.component_shapes:
                    self.canvas.move(item, -dx, -dy)

                self.output1.update_wires(event)
                self.input1.update_wires(event)
                self.input2.update_wires(event)
                    

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
        