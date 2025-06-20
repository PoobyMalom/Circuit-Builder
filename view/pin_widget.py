"""
pin_widget.py
"""

from tkinter import Canvas
from typing import Tuple
from model.pin import Pin
from controller.event_bus import event_bus
from utils.draw_utils import draw_circle

class GUIPin:
  """
  GUI Pin
  """

  def __init__(self, pin: Pin, canvas: Canvas, position: Tuple[int, int]):
    self.pin: Pin = pin
    self.canvas: Canvas = canvas
    self.position: Tuple[int, int] = position
    self.visual_id = self.draw_pin()

  def draw_pin(self):
    """
    Draw the pin on the canvas
    """
    x, y = self.position
    return draw_circle(self.canvas, x, y, 10, fill="black", outline="white")

  def update_color(self):
    """
    Update color based on state
    """
    color = "green" if self.pin.value else "black"
    self.canvas.itemconfig(self.visual_id, fill=color)

  def bind_events(self):
    """
    Bind events to the pin circle
    """
    self.canvas.tag_bind(self.visual_id, "<Button-1>", self.on_click)

  def on_click(self, event): # pylint: disable=unused-argument
    """
    publish on click of pin
    """
    event_bus.publish("pin_clicked", {
      "pin": self.pin,
      "position": self.position,
      "widget": self})
