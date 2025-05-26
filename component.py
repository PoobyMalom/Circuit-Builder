""" Module for generic gui component construction
"""
from circuit import Component

class GUIComponent: # pylint: disable=too-many-instance-attributes
    """ Class to define generic varaibles and functions for gui components
    """
    def __init__(self, window, canvas, component_id, x, y): # pylint: disable=too-many-arguments, too-many-positional-arguments
        self.window = window
        self.canvas = canvas
        self.component_id = component_id
        self.logic_component = None
        self.x = x
        self.y = y

        self.component_shapes = []
        self.inputs = {}
        self.outputs = {}

        self.dragging = False
        self.drag_started = False
        self.start_x = 0
        self.start_y = 0

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
        Function to change output position in the y direction. Also moves wire segments 
        connected to the output

        Args:
            event (tk.Event): tkinter event

        Returns:
            none
        """

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

                for component in self.component_shapes:
                    self.canvas.move(component, -dx, -dy)

                for pin in {**self.inputs, **self.outputs}.values():
                    pin.x -= dx
                    pin.y -= dy
                    if pin.wire:
                        for wire in pin.wire:
                            wire.update_wire()

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

    def handle_hover_enter(self, _):
        """ change global hovered variable
        """
        self.window.hovered_component = self

    def handle_hover_leave(self, _):
        """ change global hovered variable
        """
        self.window.hovered_component = None

    def draw(self):
        """
        Subclasses implement this to draw the component on the canvas.
        Should add all canvas IDs to self.shapes.
        """
        raise NotImplementedError

    def delete(self):
        """ Delete gui elements from canvas
        """
        for item in self.component_shapes:
            self.canvas.delete(item)

    def update_outputs(self, outputs: dict):
        """ Updates color of output pins based on circuit logic
        """
        for pin, value in outputs.items():
            if pin in self.outputs:
                circle_id = self.outputs[pin]
                color = "green" if value else "black"
                self.canvas.itemconfig(circle_id, fill=color)

    def get_pin_position(self, pin_name):
        """ Gets pin position using specific pin object
        """
        pin_id = self.outputs.get(pin_name) or self.inputs.get(pin_name)
        return self._get_center_of(pin_id)

    def _get_center_of(self, canvas_id):
        coords = self.canvas.coords(canvas_id)
        x0, y0, x1, y1 = coords
        return (x0 + x1) / 2, (y0 + y1) / 2

    def add_component(self, window, comp_id, comp_type, x, y):
        """ Add logical component to circuit
        """
        self.logic_component = Component(comp_id, comp_type, self.inputs, self.outputs, (x, y))
        window.circuit.add_component(self.logic_component)
