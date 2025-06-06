"""
Filename: wire.py
Description: Wire GUI elements

Author: Toby Mallon
Created: 4-28-2025
"""

import window_helpers as wh


class GUICanvasWire:
    """
    Represents the GUI representation of a wire

    Attributes:
        canvas (tk.Canvas): Canvas to draw wire on
        src_comp_id (str): String representing id of the input component
        src_pin (str): String representing name of the input pin
        dst_comp_id (str): String representing id of the output component
        dst_pin (str): String representing name of the output pin
        line_segs (list[tk.Line]): list of tkinter lines
        curr_wire (tk.Line): id of the current wire being drawn
        wire_pos (tuple(x, y)): Tuple representing the x and y position of 
        the start of the current line segment
    """

    def __init__(self, canvas, src_pin, dst_pin):
        self.canvas = canvas
        self.src_pin = src_pin
        self.dst_pin = dst_pin
        self.line_segs = []
        self.path = []
        self.curr_wire = None
        self.wire_pos = (None, None)

    def to_dict(self):
        """ Serialize wire to json format
        """
        line_points = []
        for line in self.line_segs:
            x1, y1, x2, y2 = self.canvas.coords(line)
            if (x1, y1) not in line_points:
                line_points.append((x1, y1))
            if (x2, y2) not in line_points:
                line_points.append((x2, y2))
        return line_points

    def create_wire(self, x, y):
        """
        Initialize wire line and starting position

        Args:
            x (int): X-position of line start
            y (int): Y-position of line start

        Returns:
            None
        """
        self.wire_pos = (x, y)
        self.curr_wire = wh.draw_line(
            self.canvas, self.wire_pos[0], self.wire_pos[1], x, y, fill="black", width=3
        )
        self.path.append((x, y))
        self.canvas.tag_lower(self.curr_wire)

    def end_wire(self, x, y):
        """
        End wire line and add to line segments

        Args:
            x (int): X-position of line end
            y (int): Y-position of line end

        Returns:
            None
        """
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], self.wire_pos[0], y
            )
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], x, self.wire_pos[1]
            )
            self.canvas.tag_lower(self.curr_wire)

        self.line_segs.append(self.curr_wire)
        self.path.append((x, y))
        self.curr_wire = None
        self.wire_pos = (None, None)

    def draw_wire(self, x, y):
        """
        Continuously change line end coordinates while drawing

        Args:
            x (int): X-position of line end
            y (int): Y-position of line end

        Returns:
            None
        """
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], self.wire_pos[0], y
            )
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], x, self.wire_pos[1]
            )
            self.canvas.tag_lower(self.curr_wire)

    def curve_wire(self, x, y):
        """
        Start new line when line gets curved

        Args:
            x (int): X-position of line end
            y (int): Y-position of line end

        Returns:
            None
        """
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], self.wire_pos[0], y
            )
            self.wire_pos = (self.wire_pos[0], y)
            self.line_segs.append(self.curr_wire)
            self.path.append((self.wire_pos[0], y))
            self.curr_wire = wh.draw_line(
                self.canvas,
                self.wire_pos[0],
                self.wire_pos[1],
                self.wire_pos[0],
                y,
                fill="black",
                width=3,
            )
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(
                self.curr_wire, self.wire_pos[0], self.wire_pos[1], x, self.wire_pos[1]
            )
            self.wire_pos = (x, self.wire_pos[1])
            self.line_segs.append(self.curr_wire)
            self.path.append((x, self.wire_pos[1]))
            self.curr_wire = wh.draw_line(
                self.canvas,
                self.wire_pos[0],
                self.wire_pos[1],
                x,
                self.wire_pos[1],
                fill="black",
                width=3,
            )
            self.canvas.tag_lower(self.curr_wire)

    def update_color(self, state):
        """ Updates color of all line segments based on state
        """
        for segment in self.line_segs:
            self.canvas.itemconfig(segment, fill="green" if state else "gray")

    def update_wire(self):
        """ update wire positions of needed wire segments
        """
        x0, y0 = self.src_pin.get_pin_position()
        x_n, y_n = self.dst_pin.get_pin_position()

        if not self.path:
            if self.line_segs:
                self.canvas.coords(self.line_segs[0], x0, y0, x_n, y_n)

        dx = x0 - self.path[0][0]
        dy = y0 - self.path[0][1]

        shifted = []
        for px, py in self.path:
            shifted.append((px + dx, py + dy))
        shifted[-1] = (x_n, y_n)

        seg_needed = len(shifted) - 1

        while len(self.line_segs) < seg_needed:
            seg_id = wh.draw_line(self.canvas, 0, 0, 0, 0, fill="black", width=3)
            self.line_segs.append(seg_id)
            self.canvas.tag_lower(seg_id)

        for i in range(seg_needed):
            xa, ya = shifted[i]
            xb, yb = shifted[i + 1]
            self.canvas.coords(self.line_segs[i], xa, ya, xb, yb)

        for seg_id in self.line_segs[seg_needed:]:
            self.canvas.delete(seg_id)
        self.line_segs = self.line_segs[:seg_needed]

        self.path = shifted
