"""
component_factory.py
"""
from typing import Tuple, Dict
from model.component import AndComponent, NotComponent, OrComponent, SubcircuitComponent
from model.circuit import Circuit

def build_component(component_type: str, position: Tuple[int, int], comp_id: str, # pylint: disable=unused-argument
                    sub_circuit: Circuit = None, interface_map: Dict[str, Tuple[str, str]] = None):
  """
  Builds components based on type and id, arguments for subcircuits not neeeded
  """

  #TODO do something about position, either include it or something idk
  if component_type == "AND":
    return AndComponent(comp_id)
  if component_type == "NOT":
    return NotComponent(comp_id)
  if component_type == "OR":
    return OrComponent(comp_id)
  if component_type == "SUBCIRCUIT":
    return SubcircuitComponent(component_type, sub_circuit, interface_map)

  return None
