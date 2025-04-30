import window_helpers as wh

class GUICanvasWire:
    def __init__(self, canvas, src_comp_id, src_pin, dst_comp_id, dst_pin):
        self.canvas = canvas
        self.src_comp_id = src_comp_id
        self.src_pin = src_pin
        self.dst_comp_id = dst_comp_id
        self.dst_pin = dst_pin
        self.line_segs = []
        self.curr_wire = None
        self.wire_pos = (None, None)

    def create_wire(self, x, y):
        self.wire_pos = (x, y)
        self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], x, y, fill="black", width=2)
        self.canvas.tag_lower(self.curr_wire)

    def end_wire(self, x, y):
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(self.curr_wire,
                            self.wire_pos[0], self.wire_pos[1],
                            self.wire_pos[0], y)
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(self.curr_wire,
                        self.wire_pos[0], self.wire_pos[1],
                        x, self.wire_pos[1])
            self.canvas.tag_lower(self.curr_wire)
            
        self.line_segs.append(self.curr_wire)
        self.curr_wire = None
        self.wire_pos = (None, None)

    def draw_wire(self, x, y):
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(self.curr_wire, 
                                self.wire_pos[0], self.wire_pos[1],
                                self.wire_pos[0], y)
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(self.curr_wire, 
                                self.wire_pos[0], self.wire_pos[1],
                                x, self.wire_pos[1])
            self.canvas.tag_lower(self.curr_wire)
        
    def curve_wire(self, x, y):
        if abs(self.wire_pos[0] - x) < abs(self.wire_pos[1] - y):
            self.canvas.coords(self.curr_wire,
                            self.wire_pos[0], self.wire_pos[1],
                            self.wire_pos[0], y)
            self.wire_pos = (self.wire_pos[0], y)
            self.line_segs.append(self.curr_wire)
            self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], self.wire_pos[0], y, fill="black", width=2)
            self.canvas.tag_lower(self.curr_wire)
        else:
            self.canvas.coords(self.curr_wire,
                            self.wire_pos[0], self.wire_pos[1],
                            x, self.wire_pos[1])
            self.wire_pos = (x, self.wire_pos[1])
            self.line_segs.append(self.curr_wire)
            self.curr_wire = wh.draw_line(self.canvas, self.wire_pos[0], self.wire_pos[1], x, self.wire_pos[1], fill="black", width=2)
            self.canvas.tag_lower(self.curr_wire)
        
    