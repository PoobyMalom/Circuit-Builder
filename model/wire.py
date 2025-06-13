"""
wire.py
"""


class Wire:  # pylint: disable=too-few-public-methods
  """
    Class for logical wire
    """

  src_id: str
  src_pin: str
  dst_id: str
  dst_pin: str

  def __init__(self, src_id: str, src_pin: str, dst_id: str, dst_pin: str):
    self.src_id = src_id
    self.src_pin = src_pin
    self.dst_id = dst_id
    self.dst_pin = dst_pin

  def to_dict(self):
    """Turns object into json serializable format"""
    return {
        "src_id": self.src_id,
        "src_pin": self.src_pin,
        "dst_id": self.dst_id,
        "dst_pin": self.dst_pin,
    }
