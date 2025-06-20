"""
Controller for selecting canvas items.
"""

# TODO Maybe create Controller class that defines the init and registration

from __future__ import annotations
from tkinter import Canvas
from controller.event_bus import event_bus

class SelectController: # pylint: disable=too-few-public-methods
  """
  Manager selection highlighting for canvas items.
  """

  def __init__(self, canvas: Canvas) -> None:
    self.canvas: Canvas = canvas
    self.selected: int | None = None

    event_bus.subscribe("register_selectable", self._register)

  # -----------------------------------------------------------------------

  def _register(self, payload):
    item_id = payload.get("item") if isinstance(payload, dict) else payload
    if item_id:
      self.make_selectable(item_id)

  # -----------------------------------------------------------------------

  def make_selectable(self, item_id: int) -> None:
    """
    Bind mouse event so the item can be selected
    """
    self.canvas.tag_bind(item_id, "<Button-1>", self._on_select)

  # -----------------------------------------------------------------------

  def _on_select(self, _event):
    item = self.canvas.find_withtag("current")[0]
    self.select(item)

  def select(self, item: int) -> None:
    """
    Select Item
    """
    if self.selected is not None:
      self.canvas.itemconfig(self.selected, width=1)
    self.selected = item
    self.canvas.itemconfig(item, width=2)
    event_bus.publish("item_selected", {"item": item})

  def clear(self) -> None:
    """
    Clear selection
    """
    if self.selected is None:
      return
    self.canvas.itemconfig(self.selected, width=1)
    event_bus.publish("selection_cleared", {"item": self.selected})
    self.selected = None
