"""
test_eval.oy

test module for circuit eval
"""

from typing import List
from model.wire import Wire
from model.circuit import Circuit
from model.component import AndComponent, OutputComponent, InputComponent, Component
from utils.id_generator import ComponentIDGenerator

circuit: Circuit = Circuit()
cid_gen: ComponentIDGenerator = ComponentIDGenerator()


input1: InputComponent = InputComponent(cid_gen.gen_id())
input2: InputComponent = InputComponent(cid_gen.gen_id())

and1: AndComponent = AndComponent(cid_gen.gen_id())

output1: OutputComponent = OutputComponent(cid_gen.gen_id())

wire1: Wire = Wire(input1.id, "OUT", and1.id, "A")
wire2: Wire = Wire(input2.id, "OUT", and1.id, "B")
wire3: Wire = Wire(and1.id, "OUT", output1.id, "IN")

components: List[Component] = [input1, input2, and1, output1]
wires: List[Wire] = [wire1, wire2, wire3]

circuit.wires += wires

for component in components:
    circuit.add_component(component)

input1.outputs["OUT"] = True
input2.outputs["OUT"] = True

circuit.evaluate()
assert output1.inputs["IN"] is True
