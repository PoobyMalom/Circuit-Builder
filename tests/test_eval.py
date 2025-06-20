"""
test_eval.py

Test module for circuit evaluation.
"""

import unittest
from typing import List
from model.wire import Wire
from model.circuit import Circuit
from model.component import AndComponent, OutputComponent, InputComponent, Component
from utils.id_generator import ComponentIDGenerator


class TestCircuitEvaluation(unittest.TestCase):
    def setUp(self):
        self.circuit: Circuit = Circuit()
        self.cid_gen: ComponentIDGenerator = ComponentIDGenerator()

        self.input1: InputComponent = InputComponent(self.cid_gen.gen_id())
        self.input2: InputComponent = InputComponent(self.cid_gen.gen_id())
        self.and1: AndComponent = AndComponent(self.cid_gen.gen_id())
        self.output1: OutputComponent = OutputComponent(self.cid_gen.gen_id())

        wire1: Wire = Wire(self.input1.id, "OUT", self.and1.id, "A")
        wire2: Wire = Wire(self.input2.id, "OUT", self.and1.id, "B")
        wire3: Wire = Wire(self.and1.id, "OUT", self.output1.id, "IN")

        components: List[Component] = [self.input1, self.input2, self.and1, self.output1]
        wires: List[Wire] = [wire1, wire2, wire3]

        self.circuit.wires += wires
        for component in components:
            self.circuit.add_component(component)

    def test_and_gate_evaluation(self):
        self.input1.outputs["OUT"] = True
        self.input2.outputs["OUT"] = True

        self.circuit.evaluate()

        self.assertTrue(self.output1.inputs["IN"])
