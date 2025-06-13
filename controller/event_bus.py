"""
EventBus.py
"""

class EventBus:
  """
    EventBus class
    """

  def __init__(self):
    self._subscribers = {}

  def subscribe(self, event_type, callback):
    """
        Adds event type and callback pair to subscribers
        """
    if event_type not in self._subscribers:
      self._subscribers[event_type] = []
    self._subscribers[event_type].append(callback)

  def unsubscribe(self, event_type, callback):
    """
        Removes event type and callback pair from subscribers
        """
    if event_type in self._subscribers:
      self._subscribers[event_type].remove(callback)

  def publish(self, event_type, payload=None):
    """
        run each callback with specified payload for event type given
        """
    for callback in self._subscribers.get(event_type, []):
      callback(payload)
