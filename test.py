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


class ComponentIDGenerator:
    def __init__(self):
        self.counter = 0

    def gen_id(self):
        cid = f"comp_{self.counter}"
        self.counter += 1
        return cid
    

generator = ComponentIDGenerator()

c = Circuit()
a = Component(generator.gen_id(), "AND", ["A", "B"], ["OUT"])
i = InputPin("IN1", ["OUT"])
o = OutputPin("OUT1", ["IN"])

c.add_component(i)
c.add_component(o)

w = Wire("IN1", "OUT", "OUT1", "IN")
c.connect(w)

i.set_output("OUT", True)

print(c.components)
print(c.components["IN1"].id)
print(c.components["IN1"].type)
print(c.components["IN1"].inputs)
print(c.components["IN1"].outputs)
print(c.components["IN1"].connections)
