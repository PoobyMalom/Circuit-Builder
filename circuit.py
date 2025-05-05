"""
Filename: circuit.py
Description: Contains circuit element classes and circuit logic

Author: Toby Mallon
Created: 4-28-2025
"""

from collections import defaultdict, deque

class Component:
    """
    Represents a basic circuit component (AND, OR, NOT, INPUT, OUTPUT)

    Attributs:
        id (str): string representing component id
        type (str): string representing component type
        inputs (str[]): logic inputs into the component
        outputs (str[]): logic outputs into the component
        connections (str[]): list of connections to other components
    """
    def __init__(self, id, type, inputs, outputs):
        self.id = id
        self.type = type # AND, OR, NOT
        self.inputs = {name: False for name in inputs}
        self.outputs = {name: False for name in outputs}
        self.connections = {name: [] for name in outputs}
        self.connected_wires = []

    def compute(self):
        """
        TODO Implement computing circuit logic
        """
        if self.type == "AND":
            self.outputs["OUT"] = self.inputs["A"] and self.inputs["B"]

        elif self.type == "OR":
            self.outputs["OUT"] = self.inputs["A"] or self.inputs["B"]

        elif self.type == "NOT":
            self.outputs["OUT"] = not self.inputs["IN"]

        elif self.type == "INPUT":
            pass

        elif self.type == "OUTPUT":
            pass

    def __str__(self):
        return f"  • {self.id} [{self.type}] inputs: [{self.inputs}], outputs: [{self.outputs}], connections: [{self.connections}]"

class InputPin(Component):
    """
    Represents an input pin in the circuit

    Inherits from:
        Component: Base class for all logic components

    Adds ability to change input pin output values
    """
    def __init__(self, id, output_pin):
        super().__init__(id, "INPUT", [], output_pin)

    def set_output(self, pin, value):
        self.outputs[pin] = value


class OutputPin(Component):
    """
    Represents an output pin in the circuit

    Inherits from:
        Component: Base class for all logic components
    """
    def __init__(self, id, input_pin):
        super().__init__(id, "OUTPUT", input_pin, [])


class Wire:
    """
    Represents a wire drawn on the canvas connecting two components.

    Attributes:
        canvas (tk.Canvas): The canvas the wire is drawn on.
        src_comp_id (str): ID of the source component.
        src_pin (str): Name of the source pin.
        dst_comp_id (str): ID of the destination component.
        dst_pin (str): Name of the destination pin.
    """
    def __init__(self, src_comp_id, src_pin, dst_comp_id, dst_pin):
        self.src_comp_id = src_comp_id
        self.src_pin = src_pin
        self.dst_comp_id = dst_comp_id
        self.dst_pin = dst_pin


class Circuit:
    """
    Represents the whole circuit

    Attributs:
        components (dict): represents a dictionary of component id, component pairs
        wire (list): represents a list of all wires in the circuit
    """
    def __init__(self, window):
        self.window = window
        self.components = {}
        self.wires = []

    def add_component(self, component):
        """
        Adds component to the circuit

        Args:
            component (Component): component to be added to the circuit

        Returns:
            None
        """
        self.components[component.id] = component

    def delete_component(self, component):
        for src_pin, targets in component.connections.items():
            for (dst_id, dst_pin) in targets:
                if dst_id in self.components:
                    self.components[dst_id].inputs[dst_pin] = False

                self.window.remove_gui_wire(component.id, dst_id)

        for other_id, other_comp in self.components.items():
            for out_pin, connections in other_comp.connections.items():
                other_comp.connections[out_pin] = [
                    (dst_id, dst_pin) for (dst_id, dst_pin) in connections
                    if dst_id != component.id
                ]
                
                self.window.remove_gui_wire(other_id, component.id)

        del self.components[component.id]

        self.wires = [
            wire for wire in self.wires
            if wire.src_comp_id != component.id and wire.dst_comp_id != component.id
        ]
    
    def connect(self, wire):
        """
        Connects two components based on a wire

        Args:
            wire (Wire): wire object storing start and end point ids and pins

        Returns:
            None
        """
        self.wires.append(wire)
        src = self.components[wire.src_comp_id]
        dst = self.components[wire.dst_comp_id]
        src.connections[wire.src_pin].append((dst.id, wire.dst_pin))
        

    def print_topological_order(self):
        """
        Prints the circuit in a toplogically sorted order for readability

        Args:
            None

        Returns:
            None
        """

        # Build the adjacency list and in-degree count
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # Initialize in-degrees to 0 for all components
        for comp_id in self.components:
            in_degree[comp_id] = 0

        print(in_degree)

        # Populate graph and in-degree based on wires
        for wire in self.wires:
            graph[wire.src_comp_id].append(wire.dst_comp_id)
            in_degree[wire.dst_comp_id] += 1

        print(graph)

        # Kahn's algorithm: start with nodes with in-degree 0
        queue = deque([cid for cid, deg in in_degree.items() if deg == 0])
        sorted_order = []

        while queue:
            cid = queue.popleft()
            sorted_order.append(cid)

            for neighbor in graph[cid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) < len(self.components):
            print("Circuit contains a cycle (not a valid DAG).")
            return

        print("Circuit Topological Order:")
        print(sorted_order)
        for cid in sorted_order:
            comp = self.components[cid]
            print(f"  • {comp.id} [{comp.type}] inputs: [{comp.inputs}], outputs: [{comp.outputs}], connections: [{comp.connections}]")

    def topological_sort(self):
         # Build the adjacency list and in-degree count
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # Initialize in-degrees to 0 for all components
        for comp_id in self.components:
            in_degree[comp_id] = 0

        # Populate graph and in-degree based on wires
        for wire in self.wires:
            graph[wire.src_comp_id].append(wire.dst_comp_id)
            in_degree[wire.dst_comp_id] += 1

        # Kahn's algorithm: start with nodes with in-degree 0
        queue = deque([cid for cid, deg in in_degree.items() if deg == 0])
        sorted_order = []

        while queue:
            cid = queue.popleft()
            sorted_order.append(cid)

            for neighbor in graph[cid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return sorted_order
    
    def evaluate(self):
        for cid in self.topological_sort():
            component = self.components[cid]
            component.compute()
            print(component)

            for pin, output_value in component.outputs.items():
                for (dst_id, dst_pin) in component.connections[pin]:
                    self.components[dst_id].inputs[dst_pin] = output_value

                    if self.window.wire_lookup is not None:
                        key = (component.id, dst_id)
                        gui_wire = self.window.wire_lookup.get(key)
                        if gui_wire:
                            gui_wire.update_color(output_value)

        print("------------------------------------------------------------------- \n")


class ComponentIDGenerator:
    """
    Simple class to keep track of component id numbers to not accidently create 
    components with duplicate ids

    Attributes:
        counter (int): used to increment id numbers
    """
    def __init__(self):
        self.counter = 0

    def gen_id(self):
        """
        Creates a new id based on counter

        Args:
            None

        Returns:
            cid: string of id including new id number
        """
        cid = f"comp_{self.counter}"
        self.counter += 1
        return cid