"""
circuit.py
"""

from collections import defaultdict, deque
from typing import Dict, List, DefaultDict
from model.component import Component
from model.wire import Wire


class Circuit:
  """
    logical circuit
    """

  components: Dict[str, Component]
  wires: List[Wire]

  def __init__(self):
    self.components = {}
    self.wires = []

  def __str__(self):
    print_out = "-------------------------------------- \n"
    for key, comp in self.components.items():
      print_out += (
          f"{key}: component type: {comp.type}, component inputs: {comp.inputs},"
          f" component outputs: {comp.outputs} \n")
      print_out += "-------------------------------------- \n"

    return print_out

  def to_dict(self) -> Dict:
    """
        Turn object into json serializable format
        """
    return {
        "components": [comp.to_dict() for comp in self.components.values()],
        "wires": [wire.to_dict() for wire in self.wires],
    }

  def add_component(self, component: Component) -> None:
    """
        Adds component to circuit
        """
    self.components[component.id] = component

  def delete_component(self, component: Component) -> None:
    """
        Deletes a component
        """
    del self.components[component.id]

  def _topological_sort(self) -> List:
    """
        Basic topological sort
        """
    # TODO figure out better thing than topo sort this shit doodoo

    graph: DefaultDict[List] = defaultdict(list)
    in_degree: DefaultDict[int] = defaultdict(int)

    for cid in self.components:
      in_degree[cid] = 0

    for wire in self.wires:
      graph[wire.src_comp_id].append(wire.dst_comp_id)
      in_degree[wire.dst_comp_id] += 1

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
    """
        evaluate a circuit logically
        """
    # TODO figure out how I want to update the guis based on these

    for comp in self.components.values():
      if comp.type != "INPUT":
        for pin in comp.inputs.values():
          pin.value = False

    for cid in self._topological_sort():
      self.components[cid].compute()

    for wire in self.wires:
      src_comp_id, src_pin_name = wire.src_pin_id.split(".")
      dst_comp_id, dst_pin_name = wire.dst_pin_id.split(".")

      value = self.components[src_comp_id].outputs[src_pin_name].value

      dst_pin = self.components[dst_comp_id].inputs[dst_pin_name]
      dst_pin.value = dst_pin.value or value
