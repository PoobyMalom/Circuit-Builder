"""
Command.py
"""

from typing import Tuple, List
from model.circuit import Circuit
from model.component import Component
from model.pin import Pin
from model.wire import Wire
from utils.component_factory import build_component

class Command:
  """
  Basic command base class
  """
  def __init__(self):
    pass

  def execute(self) -> None:
    """
    base execute function to be written over by subclasses
    """
    raise NotImplementedError

  def undo(self) -> None:
    """
    base undo function to be written over by subclasses
    """
    raise NotImplementedError

  def redo(self) -> None:
    """
    base redo function to be writtem over by subclasses
    """

class AddGateCommand(Command):
  """
  Adds a gate to the canvas and add its to the logical circuit
  """

  def __init__(self, gate_type: str, position: Tuple[int, int], gate_id: str, circuit: Circuit):
    self.gate_type: str = gate_type
    self.position: Tuple[int, int] = position
    self.gate_id: str = gate_id
    self.circuit: Circuit = circuit
    self.component = None

  def execute(self) -> None:
    self.component = build_component(self.gate_type, self.position, self.gate_id)
    self.circuit.add_component(self.component)
    # TODO add gui component as well, tie it to logic component

  def undo(self):
    self.circuit.delete_component(self.component)
    # TODO add gui component

  def redo(self):
    self.circuit.add_component(self.component)
    # TODO add gui component


class MoveCommand(Command):
  """
  Moves a gate to a new position
  """

  def __init__(self, gate_id: str):
    self.gate_id: str = gate_id
    self.old_position: Tuple[int, int] = None
    self.new_position: Tuple[int, int] = None

  def execute(self):
    """
    Move a gate
    """

    # TODO implement gui logic
    print("moved")

  def undo(self):
    """
    Undo gate move
    """

    # TODO implement gui logic
    print("undid move")

  def redo(self):
    """
    Redo gate move
    """

    # TODO implement gui logic
    print("redid move")


class DeleteCommand(Command):
  """
  Delete a component
  """
  def __init__(self, component: Component, circuit: Circuit):
    self.component: Component = component
    self.connections: List = None # TODO implement find wire connections to the component
    self.circuit: Circuit = circuit

  def execute(self):
    """
    Delete a component
    """
    # TODO add gui component as well, tie it to logic component
    # TODO delete connected wires gui and logic
    self.circuit.delete_component(self.component)

  def undo(self):
    """
    Undo deletion of a component
    """
    # TODO add gui component as well, tie it to logic component
    self.circuit.add_component(self.component)

  def redo(self):
    """
    Redelete a component
    """
    # TODO add gui component as well, tie it to logic component
    self.execute()


class AddWireCommand(Command):
  """
  Add a wire from one pin to another
  """

  def __init__(self, src_pin: Pin, wire_id: str, circuit: Circuit):
    self.src_pin: Pin = src_pin
    self.dst_pin: Pin = None
    self.wire_id: str = wire_id
    self.circuit: Circuit = circuit
    self.wire: Wire = None
    # TODO implement gui wire

  def execute(self):
    """
    Add wire to circuit and draw
    """
    # TODO implement wire drawing
    # TODO implement adding wires to src pin and dst pin components
    self.circuit.wires.append(self.wire)

  def undo(self):
    """
    Remove wire from circuit and canvas
    """
    # TODO remove wire from components
    print("undid wire drawing/connection")

  def redo(self):
    """
    Redo removing wire
    """

    # TODO all this bullshit
    print("redid wire connection")
