from collections import defaultdict, deque

class Component:
    def __init__(self, id, type, inputs, outputs):
        self.id = id
        self.type = type # AND, OR, NOT
        self.inputs = {name: False for name in inputs}
        self.outputs = {name: False for name in outputs}
        self.connections = {name: [] for name in outputs}

    def compute(self):
        pass

class InputPin(Component):
    def __init__(self, id, output_pin):
        super().__init__(id, "INPUT", [], output_pin)

    def set_output(self, pin, value):
        self.outputs[pin] = value

    def compute(self):
        pass

class OutputPin(Component):
    def __init__(self, id, input_pin):
        super().__init__(id, "OUTPUT", input_pin, [])

    def compute(self):
        print(f"[{self.id}] Output: {self.inputs}")
        

class Wire:
    def __init__(self, src_comp_id, src_pin, dst_comp_id, dst_pin):
        self.src_comp_id = src_comp_id
        self.src_pin = src_pin
        self.dst_comp_id = dst_comp_id
        self.dst_pin = dst_pin


class Circuit:
    def __init__(self):
        self.components = {}
        self.wires = []

    def add_component(self, component):
        self.components[component.id] = component
    
    def connect(self, wire):
        self.wires.append(wire)
        src = self.components[wire.src_comp_id]
        dst = self.components[wire.dst_comp_id]
        src.connections[wire.src_pin].append((dst.id, wire.dst_pin))

    def print_topological_order(self):

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

        if len(sorted_order) < len(self.components):
            print("Circuit contains a cycle (not a valid DAG).")
            return

        print("Circuit Topological Order:")
        for cid in sorted_order:
            comp = self.components[cid]
            print(f"  • {comp.id} [{comp.type}] inputs: [{comp.inputs}], outputs: [{comp.outputs}], connections: [{comp.connections}]")



class ComponentIDGenerator:
    def __init__(self):
        self.counter = 0

    def gen_id(self):
        cid = f"comp_{self.counter}"
        self.counter += 1
        return cid