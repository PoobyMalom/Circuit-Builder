"""
Filename: window_helpers.py
Description: Contains helpful functions to draw tkinter shapes and lines

Author: Toby Mallon
Created: 4-28-2025
"""


def draw_circle(canvas, x, y, radius, **kwargs):
  """
    Draws a circle on given canvas

    Args:
        canvas (tk.Canvas): The canvas to draw on
        x (int): X-coordinate of the circle center
        y (int): Y-coordinate of the circle center
        radius (float): Radius of the circle
        **kwargs: Additional options passed to `canvas.create_oval` (e.g., fill, outline, width)

    Returns:
        Canvas oval object
    """
  return canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                            **kwargs)


def draw_rect(canvas, x, y, rect_width, rect_height, **kwargs):
  """
    Draws a rectangle on given canvas

    Args:
        canvas (tk.Canvas): The canvas to draw on
        x (int): X-coordinate of the rectangles top left point
        y (int): Y-coordinate of the rectangles top left point
        rect_width (int): Width of the rectangle in pixels
        rect_height (int): Height of the rectangle in pixels
        # **kwargs: Additional options `canvas.create_rectangle` (e.g., fill, outline, width)

    Returns:
        Canvas rectangle object
    """
  return canvas.create_rectangle(x, y, x + rect_width, y + rect_height,
                                 **kwargs)


def draw_line(canvas, x1, y1, x2, y2, **kwargs):
  """
    Draws a line on given canvas

    Args:
        canvas (tk.Canvas): The canvas to draw on
        x1 (int): X-coordinate of the first point of the line
        y1 (int): Y-coordinate of the first point of the line
        x2 (int): X-coordinate of the last point of the line
        y2 (int): Y-coordinate of the last point of the line
        **kwargs: Additional options passed to `canvas.create_line` (e.g., fill, width)

    Returns:
        Canvas line object
    """
  return canvas.create_line(x1, y1, x2, y2, **kwargs)


def draw_text(canvas, x, y, text, **kwargs):
  """
    Draws text on given canvas

    Args:
        canvas (tk.Canvas): The canvas to draw on
        x (int): X-coordinate of the center of the text
        y (int): Y-coordinate of the center of the text
        text (string): Text to be displayed on the canvas
        **kwargs: Additional options passed to `canvas.create_text` (e.g., fill, font, width)
    """
  return canvas.create_text(x, y, text=text, **kwargs)
