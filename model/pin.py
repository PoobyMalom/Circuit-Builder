"""
pin.py
"""

from dataclasses import dataclass


@dataclass
class Pin:
  """
    Pin class
    """

  pid: str
  pin_name: str
  value: bool
  is_input: bool
