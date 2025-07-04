"""Module to load circuit based on json file"""

import json
import re

import window_helpers as wh
from andgate import AndGate
from circuit import Wire
from pin import GUIPin
from wire import GUICanvasWire


class FileLoader:
    """Class to handle reading and reconstructing circuit data"""

    def __init__(
        self, file_name, circuit, canvas, window
    ):  # pylint: disable=too-many-locals
        # TODO for the love of god move most of this from init into their own functions
        self.file_name = file_name
        self.circuit = circuit
        self.canvas = canvas
        self.window = window

        # Open json save file
        with open(f"components/{file_name}", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Instatiate highest level json elements
        self.circuit_name = data["name"]
        self.components = data["components"]
        self.wires = data["wires"]

        # Create component lookup dictionary
        self.component_lookup = {d["id"]: d for d in self.components}

        # create each gui component replace placeholder in lookup table
        for component_data in self.components:
            self.instantiate_component(component_data, self.canvas, self.window)

        print("----------------")
        self.window.circuit.print_topological_order()
        print("----------------")

        # create each wire
        for wire_data in self.wires:
            src_id = wire_data["src_id"]
            src_pin = wire_data["src_pin"]
            dst_id = wire_data["dst_id"]
            dst_pin = wire_data["dst_pin"]
            path = wire_data["path"]

            print(
                f"src_id: {src_id}, src_pin: {src_pin}, dst_id: {dst_id}, dst_pin: {dst_pin}"
            )

            # Create logical wire
            wire = Wire(src_id, src_pin, dst_id, dst_pin, path)
            circuit.connect(wire)

            src_id_obj = self.window.pin_lookup[(src_id, src_pin)]
            dst_id_obj = self.window.pin_lookup[(dst_id, dst_pin)]

            # Create Gui Wire
            gui_wire = GUICanvasWire(canvas, src_id_obj, dst_id_obj)
            for i in range(len(path) - 1):
                x0, y0 = path[i]
                x1, y1 = path[i + 1]
                line = wh.draw_line(canvas, x0, y0, x1, y1, fill="black", width=3)
                self.canvas.tag_lower(line)
                gui_wire.line_segs.append(line)
                self.canvas.tag_bind(line, "<Button-1>", gui_wire.add_ghost_node)
                gui_wire.path.append((x0, y0))

            gui_wire.path.append(path[-1])

            src_id_obj.wire.append(gui_wire)
            dst_id_obj.wire.append(gui_wire)

            window.wire_lookup.setdefault((src_id, dst_id), []).append(gui_wire)
            window.gui_lookup[src_id].wire = gui_wire

        # Set focus back on canvas
        self.window.canvas.focus_set()

        # Set id generator to start after highest number in json ids
        comp_nums = [
            list(map(int, re.findall(r"\d+", num)))[0]
            for num in self.window.gui_lookup.keys()
        ]
        self.window.id_generator.counter = max(comp_nums) + 1

    def instantiate_component(self, comp_data, canvas, window):
        """Instatiates given component based on its component data"""
        comp_id = comp_data["id"]
        comp_type = comp_data["type"]
        x, y = comp_data["pos"]

        gui: GUIPin | AndGate

        if comp_type == "INPUT":
            gui = GUIPin(window, canvas, comp_id, x, y, 15, "IN", True, True)
        elif comp_type == "OUTPUT":
            gui = GUIPin(window, canvas, comp_id, x, y, 15, "OUT", False, True)
        elif comp_type == "AND":
            gui = AndGate(window, canvas, comp_id, x, y)
        elif comp_type == "NOT":
            pass
        elif comp_type == "SUBCIRCUIT":
            pass
        else:
            raise LookupError(comp_type)

        window.gui_lookup[comp_id] = gui
