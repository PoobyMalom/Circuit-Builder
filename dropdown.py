import tkinter as tk
from input import Input
from output import Output
from circuit import InputPin, OutputPin

class Dropdown():
    def __init__(self, root, window, frame, canvas, circuit, id_generator):
        self.root = root
        self.window = window
        self.frame = frame
        self.canvas = canvas
        self.circuit = circuit
        self.id_generator = id_generator

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Place Input", command=self.place_input)
        self.context_menu.add_command(label="Say Goodbye", command=self.say_goodbye)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Exit", command=self.root.quit)

        self.last_event = None

    def show_context_menu(self, event):
        self.last_event = event

        self.context_menu.delete(0, tk.END)

        if event.x < 30:
            self.context_menu.add_command(label="Place Input", command=self.place_input)

        if event.x > self.frame.winfo_width() - 50:
            self.context_menu.add_command(label="Place Output", command=self.place_output)

        print(self.frame.winfo_width())

        self.context_menu.tk_popup(event.x_root, event.y_root)

    def place_input(self):
        if self.last_event:
            new_id = self.id_generator.gen_id()
            input_pin = InputPin(new_id, ["OUT"])
            self.circuit.add_component(input_pin)

            Input(self.canvas, self.window, self.circuit, new_id, 30, self.last_event.y)

    def place_output(self):
        if self.last_event:
            new_id = self.id_generator.gen_id()
            output_pin = OutputPin(new_id, ["IN"])
            self.circuit.add_component(output_pin)

            Output(self.canvas, self.window, self.circuit, new_id, self.frame.winfo_width() - 30, self.last_event.y)

    def say_goodbye(self):
        print("Goodbye!")