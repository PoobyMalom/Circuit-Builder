import tkinter as tk
from input import Input
from output import Output
from test import InputPin, OutputPin

class Dropdown():
    def __init__(self, root, frame, canvas, circuit, id_generator):
        self.root = root
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
            Input(self.canvas, 30, self.last_event.y)

            new_id = self.id_generator.gen_id()
            input_circuit = InputPin(new_id, ["OUT"])
            self.circuit.add_component(input_circuit)

    def place_output(self):
        if self.last_event:
            Output(self.canvas, self.frame.winfo_width() - 30, self.last_event.y)

            new_id = self.id_generator.gen_id()
            output_circuit = OutputPin(new_id, ["IN"])
            self.circuit.add_component(output_circuit)

    def say_goodbye(self):
        print("Goodbye!")