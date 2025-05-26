""" Module to draw a ghost component when dragging from toolbar
"""
import window_helpers as wh


class Ghost:
    """ Class to handle ghost intialization and movement
    """
    def __init__(self, window, canvas, x, y, width, height, color):
        # TODO maybe change how things like position, width, height, color are passed in
        self.window = window
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.body = None

        self.draw()

    def draw(self):
        """ Draw ghost on canvas
        """
        self.body = wh.draw_rect(
            self.canvas,
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
            fill=self.color,
        )

    def move(self, x, y):
        """ Move ghost to new coordinates
        """
        self.canvas.coords(
            self.body,
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
        )

    def delete(self):
        """ Deletes ghost off of the canvas
        """
        self.canvas.delete(self.body)
