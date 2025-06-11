"""
serializer.py
"""

from typing import Dict, Any
from model.circuit import Circuit
from model.wire import Wire
from model.component import Component


def circuit_to_json(circuit: Circuit) -> Dict[str, Any]:
    """
    serialize circuit data into json format
    """
    # TODO maybe include the file saving logic in here?

    return circuit.to_dict()


def circuit_from_json(data: Dict) -> Circuit:
    """
    process json data into circuit object
    """
    components = data["components"]
    wires = data["wires"]

    circuit = Circuit()

    for component in components:
        circuit.add_component(Component(**component))

    for wire in wires:
        circuit.wires.append(Wire(**wire))

    return circuit
