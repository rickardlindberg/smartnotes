import sys
import random

class App:

    def __init__(self):
        self.frames = Frames()

    def event(self, event):
        if event.key_down("ctrl+q"):
            sys.exit(0)
        else:
            self.frames.event(event)

    def update(self, elapsed_ms):
        self.frames.update(elapsed_ms)

    def draw(self, canvas):
        canvas.fill(color=(255, 0, 100))
        self.frames.draw(canvas.deflate(40))

class Frames:

    def __init__(self):
        self.frames = [Frame(x) for x in range(50)]
        self.rectangle = None
        self.position = self.find_position()

    def event(self, event):
        if event.mouse_motion():
            self.position = self.find_position(event.mouse_point())

    def update(self, elapsed_ms):
        self.before = []
        self.magnify = []
        self.after = []
        number_of_frames_to_magnify = 5
        for frame in self.frames:
            if frame.number < self.position - number_of_frames_to_magnify/2:
                frame.deflate_height = 20
                self.before.append(frame)
            elif frame.number > self.position + number_of_frames_to_magnify/2:
                frame.deflate_height = 20
                self.after.append(frame)
            else:
                frame.deflate_height = 0
                self.magnify.append(frame)

    def draw(self, canvas):
        self.rectangle = canvas.rectangle
        canvas.stroke(color=(25, 25, 25))
        canvas.columns([
            {
                "fn": self.draw_before,
                "proportion": len(self.before),
            },
            {
                "fn": self.draw_magnify,
                "size": 2 * len(self.magnify) * (self.rectangle.width / len(self.frames)),
            },
            {
                "fn": self.draw_after,
                "proportion": len(self.after),
            },
        ])

    def draw_before(self, canvas):
        canvas.columns([{"fn": frame.draw} for frame in self.before])

    def draw_magnify(self, canvas):
        canvas.columns([{"fn": frame.draw} for frame in self.magnify])

    def draw_after(self, canvas):
        canvas.columns([{"fn": frame.draw} for frame in self.after])

    def find_position(self, mouse_point=None):
        if self.rectangle:
            positions = []
            for frame in self.frames:
                if frame.rectangle.contains(mouse_point):
                    positions.append(
                        frame.number + frame.rectangle.percent(mouse_point).x
                    )
            if positions:
                return sum(positions) / len(positions)
        return len(self.frames) / 2

class Frame:

    def __init__(self, number):
        self.number = number
        self.rectangle = None
        self.deflate_height = 0

    def draw(self, canvas):
        self.rectangle = canvas.rectangle
        sub = canvas.deflate(height=self.deflate_height)
        sub.stroke(color=(20, 20, 100))
        sub.text(str(self.number))
