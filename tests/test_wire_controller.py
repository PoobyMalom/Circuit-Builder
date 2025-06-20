# from model.circuit import Circuit
# from controller.wire_controller import WireController
# from model.pin import Pin
# from view.pin_widget import GUIPin
# import tkinter as tk

# root = tk.Tk()
# frame = tk.Frame(root)
# canvas = tk.Canvas(frame, bg="white")
# canvas.pack(fill=tk.BOTH, expand=True)

# circuit = Circuit()

# wc = WireController(circuit)

# pin1 = Pin("pin_1", "OUT", False, False)
# pin2 = Pin("pin_1", "IN", False, True)

# gui_pin1 = GUIPin(pin1, canvas, (50, 50))
# gui_pin2 = GUIPin(pin2, canvas, (100, 100))

# gui_pin1.on_click(None)
# gui_pin2.on_click(None)

# print(circuit.wires)

# tests/test_wire_creation.py

import unittest
from model.circuit import Circuit
from model.pin import Pin
from controller.wire_controller import WireController
from controller.event_bus import event_bus

class TestWireCreation(unittest.TestCase):
  """
  Test creating a wire
  """
  def setUp(self):
    event_bus._subscribers.clear()
    self.circuit = Circuit()
    self.controller = WireController(self.circuit)

  def test_create_wire(self):
    """
    Test creating a wire
    """
    output_pin = Pin("comp1", "OUT", value=False, is_input=False)
    input_pin = Pin("comp2", "IN", value=False, is_input=True)

    self.controller.handle_pin_clicked({'pin': output_pin})
    self.controller.handle_pin_clicked({'pin': input_pin})

    self.assertEqual(len(self.circuit.wires), 1)
    wire = self.circuit.wires[0]
    self.assertEqual(wire.src_id, "comp1")
    self.assertEqual(wire.src_pin, "OUT")
    self.assertEqual(wire.dst_id, "comp2")
    self.assertEqual(wire.dst_pin, "IN")
  
class TestWireInvalidStart(unittest.TestCase):
  """
  Test an invalid start
  """
  def setUp(self):
    event_bus._subscribers.clear()
    self.circuit = Circuit()
    self.controller = WireController(self.circuit)

  def test_invalid_start_from_input(self):
    """
    Test an invalid connection
    """
    input_pin = Pin("comp1", "IN", value=False, is_input=True)

    self.controller.handle_pin_clicked({'pin': input_pin})

    self.assertEqual(len(self.circuit.wires), 0)
    self.assertFalse(self.controller.is_drawing)
    
class TestWireCancel(unittest.TestCase):
  """
  Test cancelling a wire
  """
  def setUp(self):
    event_bus._subscribers.clear()
    self.circuit = Circuit()
    self.controller = WireController(self.circuit)

  def test_cancel_wire(self):
    """
    Test cancelling a wire
    """
    output_pin = Pin("comp1", "OUT", value=False, is_input=False)
    self.controller.start_wire(output_pin)
    self.assertTrue(self.controller.is_drawing)

    self.controller.cancel_wire()
    self.assertFalse(self.controller.is_drawing)
    self.assertEqual(len(self.circuit.wires), 0)