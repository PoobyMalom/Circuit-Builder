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
  value: bool
  is_input: bool
