import window_helpers as wh

class Ghost:
    def __init__(self, window, canvas, x, y, width, height, color):
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
        self.body = wh.draw_rect(self.canvas, self.x - self.width/2, self.y - self.height/2, self.width, self.height, fill=self.color)

    def move(self, x, y):
        self.canvas.coords(self.body, x - self.width/2, y - self.height/2, x + self.width/2, y + self.height/2)

    def delete(self):
        self.canvas.delete(self.body)