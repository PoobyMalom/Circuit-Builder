"""
Controller handling dragging of canvas items.
"""

from __future__ import annotations
from tkinter import Canvas
from controller.event_bus import event_bus

class DragController: # pylint: disable=too-few-public-methods
  """
  Simple drag controller for tk.Canvas items
  """

  def __init__(self, canvas: Canvas) -> None:
    self.canvas: Canvas = canvas
    self._drag_item: int | None = None
    self._start_x = 0
    self._start_y = 0

    event_bus.subscribe("register_draggable", self._register)

  # -----------------------------------------------------------------------

  def _register(self, payload):
    """
    Subscribe callback allowing widgets to be registered for dargging.
    """

    item_id = payload.get("item") if isinstance(payload, dict) else payload
    if item_id:
      self.make_dragable(item_id)

  # -----------------------------------------------------------------------

  def make_dragable(self, item_id: int):
    """
    Bind mouse event so the item can be dragged.
    """

    self.canvas.tag_bind(item_id, "<ButtonPress-1>", self._on_press)
    self.canvas.tag_bind(item_id, "<B1-Motion>", self._on_drag)
    self.canvas.tag_bind(item_id, "<ButtonRelease-1>", self._on_release)

  # -----------------------------------------------------------------------

  def _on_press(self, event):
    self._drag_item = self.canvas.find_withtag("current")[0]
    self._start_x, self._start_y = event.x, event.y
    event_bus.publish("drag_start", {"item": self._drag_item})

  def _on_drag(self, event):
    if self._drag_item is None:
      return
    dx = event.x - self._start_x
    dy = event.y - self._start_y
    self._start_x, self._start_y = event.x, event.y
    self.canvas.move(self._drag_item, dx, dy)
    event_bus.publish(
      "drag_move",
      {"item": self._drag_item, "dx": dx, "dy": dy},
    )

  # -----------------------------------------------------------------------

  def _on_release(self, _event):
    if self._drag_item is None:
      return
    event_bus.publish("drag_end", {"item": self._drag_item})
    self._drag_item = None
