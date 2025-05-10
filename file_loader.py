import json
import tkinter as tk
from circuit import Wire
from andgate import AndGate    
from pin import GUIPin
from wire import GUICanvasWire
import window_helpers as wh

class FileLoader:
    def __init__(self, file_name, circuit, canvas, window):
        self.file_name = file_name
        self.circuit = circuit
        self.canvas = canvas
        self.window = window

        with open(f"components/{file_name}", "r") as f:
            data = json.load(f)

        self.circuit_name = data["name"]
        self.components = data["components"]
        self.wires = data["wires"]

        self.component_lookup = {d["id"]: d for d in self.components}

        for component_data in self.components:
            self.instantiate_component(component_data, self.circuit, self.canvas, self.window)

        for wire_data in self.wires:
            src_id = wire_data["src_id"]
            src_pin = wire_data["src_pin"]
            dst_id = wire_data["dst_id"]
            dst_pin = wire_data["dst_pin"]

            wire = Wire(src_id, src_pin, dst_id, dst_pin)
            circuit.connect(wire)

            gui_wire = GUICanvasWire(canvas, src_id, src_pin, dst_id, dst_pin)
            window.wire_lookup[(src_id, dst_id)] = gui_wire



    def instantiate_component(self, comp_data, circuit, canvas, window):
        id = comp_data["id"]
        type = comp_data["type"]
        x, y = comp_data["pos"]

        if type == "INPUT":
            print("input")
            GUIPin(window, canvas, id, x, y, 15, "OUT", False, True)
        elif type == "OUTPUT":
            print("output")
            GUIPin(window, canvas, id, x, y, 15, "IN", True, True)
        elif type == "AND":
            print("and")
            AndGate(window, canvas, id, x, y)
        elif type == "NOT":
            pass
        elif type == "SUBCIRCUIT":
            pass
        else:
            raise LookupError(type)
