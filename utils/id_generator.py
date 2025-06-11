"""
id_generator.py
"""

# TODO maybe use uuids for component ids


class ComponentIDGenerator:  # pylint: disable=too-few-public-methods
    """
    Generates IDs
    """

    def __init__(self):
        self.counter = 0

    def gen_id(self):
        """
        creates a new id
        """
        cid = f"comp_{self.counter}"
        self.counter += 1
        return cid
