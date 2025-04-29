import tkinter as tk
from tkinter import ttk
import window_helpers as wh
from dropdown import Dropdown
from test import Circuit, ComponentIDGenerator

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


        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-2>", self.handle_right_click)

        self.dropdown = Dropdown(self.root, self.frame, self.canvas, self.circuit, self.id_generator)

        # Bottom toolbar (overlaps input/output bars)
        self.toolbar = tk.Frame(root, height=30, bg="darkgray")
        self.toolbar.place(x=0, rely=1.0, anchor='sw', relwidth=1.0)

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

    def place_input(self, event):
        # print(event.x)
        # wh.draw_circle(self.canvas, event.x, event.y, 20, fill="blue", outline="black", tag="input_circ")
        # self.canvas.tag_raise("input_circ")
        pass
    

    def handle_right_click(self, event):
        x, y = event.x, event.y

        if (0 <= x < 30 or self.width - 30 <= x < self.width) and 0 <= y <= self.height - 50:
            self.dropdown.show_context_menu(event)
        

