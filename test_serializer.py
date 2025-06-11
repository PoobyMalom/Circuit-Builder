"""
test_serializer.py

test module for json serialization
"""

from typing import List, Dict, Any
import json
from model.wire import Wire
from model.circuit import Circuit
from model.component import AndComponent, OutputComponent, InputComponent, Component
from model.serializer import circuit_to_json, circuit_from_json
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

serialized_data: Dict[str, Any] = circuit_to_json(circuit)

print(json.dumps(serialized_data, indent=3, default=str))

deserialized_circuit: Circuit = circuit_from_json(serialized_data)

print(deserialized_circuit)
