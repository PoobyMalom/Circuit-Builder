"""
wire_controller.py
"""

from tkinter import Event
from typing import Tuple
from model.pin import Pin
from model.circuit import Circuit
from model.wire import Wire
from controller.event_bus import event_bus

class WireController:
  """
  WireController
  """

  def __init__(self, circuit: Circuit):
    self.is_drawing: bool = False
    self.start_pin: Pin | None = None
    self.start_component_id: str | None = None
    self.circuit: Circuit = circuit
    self.current_preview_position: Tuple[int, int] | None = None

    event_bus.subscribe("pin_clicked", self.handle_pin_clicked)
    event_bus.subscribe("mouse_moved", self.update_preview)
    event_bus.subscribe("cancel_wire", self.cancel_wire)

  def handle_pin_clicked(self, payload):
    """
    Figure out whether its a wire end or wire begin
    """
    is_input: bool = payload['pin'].is_input
    if is_input and self.is_drawing:
      self.complete_wire(payload['pin'])
    elif not is_input and not self.is_drawing:
      self.start_wire(payload['pin'])
    else:
      print("not a valid starting point")

  def start_wire(self, start_pin: Pin):
    """
    Start wire
    """
    self.start_pin = start_pin
    self.is_drawing = True
    event_bus.publish("wire_started")

  def complete_wire(self, end_pin: Pin):
    """
    End wire
    """
    # TODO switch over to using commands for this

    wire = Wire(self.start_pin.pid, self.start_pin.pin_name, end_pin.pid, end_pin.pin_name) # type: ignore
    self.circuit.wires.append(wire)
    event_bus.publish("wire_committed")

  def update_preview(self, event: Event):
    """
    Updates wire preview
    """
    if self.is_drawing:
      event_bus.publish("wire_preview_updated", {
        "new_position": (event.x, event.x)})

  def cancel_wire(self):
    """
    Cancels wire
    """
    self.is_drawing = False
    self.start_pin = None
    self.start_component_id = None
    self.current_preview_position= None

    event_bus.publish("wire_cancelled")
