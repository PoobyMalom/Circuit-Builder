"""
CanvasView module.

Provides a simple wrapper around a tk.Canvas used to draw gate and wire
widgets. The view exposes helper methods for adding and removing widgets and
publishes mouse move events so controllers can react to them
"""

from __future__ import annotations
from typing import Dict, List
from tkinter import Canvas, BOTH
import tkinter as tk
from controller.event_bus import event_bus
from view.toolbar import Toolbar
from utils.draw_utils import draw_rect

class CanvasView: # pylint: disable=too-few-public-methods
  """
  Wrapper managing a tk.Canvas instance
  """

  def __init__(self, root: tk.Tk, width: int = 800, height: int = 630, bg: str = "white") -> None:
    
    self.root = root
    self.root.title("Circuit Builder")
    self.root.geometry(f"{width}x{height}")
    
    self.width = width
    self.height = height
    
    self.frame = tk.Frame(root)
    self.frame.place(x=0, y=0, relwidth=1.0, relheight=1.0, anchor="nw")
    self.canvas = Canvas(self.frame, width=width, height=height, bg=bg)
    self.canvas.pack(fill=BOTH, expand=True)
    
    self.rect_id = draw_rect(
      self.canvas,
      30,
      10,
      self.width - 60,
      self.height - 50,
      outline="#444444",
      width=2,
    )

    self.toolbar: Toolbar = Toolbar(self.frame)

    # These are the gui gates and wires
    self.gates: Dict[str, GateWidget] = {}
    self.wires: List[WireWidget] = []

    # Pass mouse movements to event bus
    self.canvas.bind("<Motion>", self._on_motion)
    self.root.bind("<Configure>", self.resize_window)

  # -----------------------------------------------------------------------
  # event handlers
  # -----------------------------------------------------------------------

  def _on_motion(self, event):
    event_bus.publish("mouse_moved", event)

  # -----------------------------------------------------------------------
  # helper functions
  # -----------------------------------------------------------------------

  def add_gate(self, gate: GateWidget) -> None:
    """
    Register a gate widget with the canvas
    """
    self.gates[gate.gid] = gate

  def remove_gate(self, gid: str):
    """
    Remove a gate widget from the canvas
    """
    gate = self.gates.pop(gid, None)
    if gate:
      gate.delete()

  def add_wire(self, wire: WireWidget) -> None:
    """
    Register a wire widget with the canvas
    """
    self.wires.append(wire)

  def remove_wire(self, wire: "WireWidget") -> None:
    """
    Remove a wire widget from the canvas
    """
    if wire in self.wires:
      self.wires.remove(wire)
      wire.delete()

  def clear(self) -> None:
    """
    Clear the whole canvas
    """
    for gate in list(self.gates.values()):
      gate.delete()

    for wire in list(self.wires):
      wire.delete()

    self.wires.clear()
    self.gates.clear()

  def resize_window(self, event):
    """
    Handles resizing of the main window and updates the canvas boundary box.

    Args:
        event (tk.Event): The window resize event.
    """
    if event.widget == self.root:
        self.height = event.height
        self.width = event.width

        if self.rect_id is not None:
            self.canvas.coords(
                self.rect_id, 30, 10, self.width - 30, self.height - 50
            )

from .gate_widget import GateWidget # noqa: E402  pylint: disable=wrong-import-position, relative-beyond-top-level
from .wire_widget import WireWidget # noqa: E402  pylint: disable=wrong-import-position, relative-beyond-top-level
