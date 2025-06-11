"""
component.py
"""

from typing import Dict


class Component:
    """Component base class"""

    id: str
    type: str
    inputs: Dict[str, bool]
    outputs: Dict[str, bool]

    def __init__(
        self,
        cid: str,
        type: str, # pylint: disable=redefined-builtin
        inputs: Dict[str, bool] | None = None,
        outputs: Dict[str, bool] | None = None,
    ):

        self.id = cid
        self.type = type
        self.inputs = inputs or {}
        self.outputs = outputs or {}

    def compute(self) -> None:
        """Base compute function overide in subclasses"""
        raise NotImplementedError

    def to_dict(self):
        """Torn object into json serializable format"""
        return {
            "cid": self.id,
            "type": self.type,
            "inputs": self.inputs,
            "outputs": self.outputs,
        }


class AndComponent(Component):
    """
    And Component
    """

    def __init__(self, cid):
        super().__init__(cid, "AND", {"A": False, "B": False}, {"OUT": False})

    def compute(self):
        self.outputs["OUT"] = self.inputs["A"] and self.inputs["B"]


class OrComponent(Component):
    """
    And Component
    """

    def __init__(self, cid):
        super().__init__(cid, "OR", {"A": False, "B": False}, {"OUT": False})

    def compute(self):
        self.outputs["OUT"] = self.inputs["A"] or self.inputs["B"]


class NotComponent(Component):
    """
    Not Component
    """

    def __init__(self, cid):
        super().__init__(cid, "NOT", {"IN": False}, {"OUT": True})

    def compute(self):
        self.outputs["OUT"] = not self.inputs["IN"]


class InputComponent(Component):
    """
    Input Component
    """

    def __init__(self, cid):
        super().__init__(cid, "INPUT", {}, {"OUT": False})

    def compute(self):
        pass


class OutputComponent(Component):
    """
    Output Component
    """

    def __init__(self, cid):
        super().__init__(cid, "OUTPUT", {"IN": False}, {})

    def compute(self):
        return self.inputs["IN"]


class SubcircuitComponent(
    Component
):  # pylint: disable=missing-class-docstring, abstract-method
    # TODO implement this at some point

    def __init__(
        self, cid, sub_circuit, interface_map
    ):  # pylint: disable=useless-parent-delegation
        super().__init__(cid, "SUBCIRCUIT")
        self.sub_circuit = sub_circuit
        self.interface_map = interface_map  # eg {"A": ("node_1", "OUT"), ...}

    def compute(self):
        for ext_pin, (int_id, int_pin) in self.interface_map["inputs"].items():
            self.sub_circuit.components[int_id].inputs[int_pin].value = self.inputs[
                ext_pin
            ].value

        self.sub_circuit.evaluate()

        for ext_pin, (int_id, int_pin) in self.interface_map["outputs"].items():
            self.outputs[ext_pin].value = (
                self.sub_circuit.components[int_id].outputs[int_pin].value
            )
