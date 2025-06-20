"""
Gate widget module.
"""

from __future__ import annotations
from typing import Tuple
from tkinter import Canvas
from controller.event_bus import event_bus
from utils.draw_utils import draw_rect, draw_text

class GateWidget:
  """
  Simple drawn representation of a logical gate.
  """
  def __init__(self, canvas: Canvas, gid: str, position: Tuple[int, int], label: str) -> None:
    self.canvas: Canvas = canvas
    self.gid: str = gid
    self.x, self.y = position
    self.label = label

    self.width: int = 60
    self.height: int = 40

    self.body_id: int | None = None
    self.text_id: int | None = None

    self.draw()

  # -----------------------------------------------------------------------

  def draw(self) -> None:
    """
    Draw the gate on the canvas
    """

    self.body_id = draw_rect(
      self.canvas,
      self.x - self.width / 2,
      self.y - self.height /2,
      self.width,
      self.height,
      fill="#ccccccc",
      outline="black",
    )
    self.text_id = draw_text(self.canvas, self.x, self.y, self.label)

    event_bus.publish("grate_drawn", {"gate": self})

  # -----------------------------------------------------------------------

  def move(self, dx: int, dy: int) -> None:
    """
    Move the gate by specified delta
    """

    self.x += dx
    self.y += dy
    for item in (self.body_id, self.text_id):
      self.canvas.move(item, dx, dy)

  def move_to(self, x: int, y: int) -> None:
    """
    Move the gate to given coords
    """

    self.move(x - self.x, y - self.y)

  # -----------------------------------------------------------------------

  def delete(self) -> None:
    """
    Delete gate
    """
    for item in (self.body_id, self.text_id):
      self.canvas.delete(item) # type: ignore
