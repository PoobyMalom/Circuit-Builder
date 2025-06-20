"""
Wire widget module.
"""

from __future__ import annotations
from typing import Tuple
from tkinter import Canvas
from controller.event_bus import event_bus
from utils.draw_utils import draw_line

class WireWidget:
  """
  Drawn representation of a wire between two points.
  """

  def __init__(self, canvas: Canvas, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    self.canvas = canvas
    self.start = start
    self.end = end
    self.line_id: int | None = None
    self.draw()

  # -----------------------------------------------------------------------

  def draw(self) -> None:
    """
    Draw the wire
    """
    x1, y1 = self.start
    x2, y2 = self.end
    self.line_id = draw_line(self.canvas, x1, y1, x2, y2, fill="black", width=2)
    event_bus.publish("wire_drawn", {"wire": self})

  def update(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
    """
    Update wire points
    """

    self.start = start
    self.end = end
    self.canvas.coords(self.line_id, start[0], start[1], end[0], end[1]) # type: ignore
    event_bus.publish(
      "wire_updated",
      {"wire": self, "start": start, "end": end}
    )

  def delete(self) -> None:
    """
    Delete Wire
    """
    self.canvas.delete(self.line_id) # type: ignore
