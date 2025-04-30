import tkinter as tk
from tkinter import ttk
import window_helpers as wh
from dropdown import Dropdown
from circuit import Circuit, ComponentIDGenerator
from wire import GUICanvasWire

class Window:
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.width = width
        self.height = height

        self.circuit = Circuit()
        self.id_generator = ComponentIDGenerator()

        self.root.title("Circuit Builder")
        self.root.geometry(f"{width}x{height}")
    

         # Main canvas frame
        self.frame = tk.Frame(root)
        self.frame.place(x=0, y=0, relwidth=1.0, relheight=1.0, anchor='nw')  # Leaves 30px space on each side

        self.drawing_wire = False
        self.curr_wire = None
        self.wire_pos = (None, None)

        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.create_wire)
        self.canvas.bind("<Motion>", self.draw_wire)
        self.canvas.bind("b", self.curve_wire)

        self.root.bind("<Configure>", self.resize_window)
        #self.root.lift()
        self.root.attributes("-topmost", True)

        self.rect_id = wh.draw_rect(self.canvas, 30, 10, self.width - 60, self.height - 50, outline="#444444", width=2)


    def resize_window(self, event):
        if event.widget == self.root:
            self.height = event.height
            self.width = event.width

            if self.rect_id is not None:
                self.canvas.coords(self.rect_id, 30, 10, self.width - 30, self.height - 50)

    def create_wire(self, event):
        if self.drawing_wire == False:
            self.curr_wire = GUICanvasWire(self.canvas, None, None, None, None)
            self.circuit.connect(self.curr_wire)
            self.curr_wire.create_wire(event)
            self.drawing_wire = True

        elif self.drawing_wire == True:
            self.curr_wire.end_wire(event)
            self.curve_wire = None
            self.drawing_wire = False
            self.curr_wire = None

        # if self.drawing_wire == False:
        #     self.wire_pos = (event.x, event.y)
        #     self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], event.x, event.y, fill="black", width=2)
        #     self.drawing_wire = True
        # elif self.drawing_wire == True:
        #     if abs(self.wire_pos[0] - event.x) < abs(self.wire_pos[1] - event.y):
        #         self.canvas.coords(self.curr_wire,
        #                         self.wire_pos[0], self.wire_pos[1],
        #                         self.wire_pos[0], event.y)
        #     else:
        #         self.canvas.coords(self.curr_wire,
        #                        self.wire_pos[0], self.wire_pos[1],
        #                        event.x, self.wire_pos[1])
            
        #     self.drawing_wire = False
        #     self.curr_wire = None
        #     self.wire_pos = (None, None)

    def draw_wire(self, event):
        if self.drawing_wire == True:
            self.curr_wire.draw_wire(event)
            # if abs(self.wire_pos[0] - event.x) < abs(self.wire_pos[1] - event.y):
            #     self.canvas.coords(self.curr_wire, 
            #                        self.wire_pos[0], self.wire_pos[1],
            #                        self.wire_pos[0], event.y)
            # else:
            #     self.canvas.coords(self.curr_wire, 
            #                        self.wire_pos[0], self.wire_pos[1],
            #                        event.x, self.wire_pos[1])
            
    def curve_wire(self, event):
        if self.drawing_wire == True:
            self.curr_wire.curve_wire(event)
            # if abs(self.wire_pos[0] - event.x) < abs(self.wire_pos[1] - event.y):
            #     self.canvas.coords(self.curr_wire,
            #                     self.wire_pos[0], self.wire_pos[1],
            #                     self.wire_pos[0], event.y)
            #     self.wire_pos = (self.wire_pos[0], event.y)
            #     self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], self.wire_pos[0], event.y, fill="black", width=2)
            # else:
            #     self.canvas.coords(self.curr_wire,
            #                     self.wire_pos[0], self.wire_pos[1],
            #                     event.x, self.wire_pos[1])
            #     self.wire_pos = (event.x, self.wire_pos[1])
            #     self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], event.x, self.wire_pos[1], fill="black", width=2)
            
    


root = tk.Tk()
window = Window(root, 800, 600)
root.mainloop()