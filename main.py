from time import sleep
import random
import pygame as pg


class Circle:
    def __init__(self, color, position, radius):
        self.position = position
        self.color = color
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = max(value, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __gt__(self, other):
        return self.radius > other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __add__(self, other):
        if self >= other :
            return Circle(self.color, self.position, self.radius + other.radius)
        else:
            return Circle(other.color, other.position, self.radius + other.radius)
    def __sub__(self, other):
        if self < other:
            return Exception("First circle is less then seccond")
        return Circle(self.color, self.position, self.radius - other.radius)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.position, self.radius)

class Rectangle:
    def __init__(self, color, position, rect):
        self.position = position
        self.color = color
        self.rect = rect

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = (max(value[0], 0), max(value[1], 0))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __gt__(self, other):
        return self.rect[0] * self.rect[1] > other.rect[0] * other.rect[1]

    def __ge__(self, other):
        return self.rect[0] * self.rect[1] >= other.rect[0] * other.rect[1]

    def __lt__(self, other):
        return self.rect[0] * self.rect[1] < other.rect[0] * other.rect[1]

    def __le__(self, other):
        return self.rect[0] * self.rect[1] <= other.rect[0] * other.rect[1]

    def __add__(self, other):
        if self >= other :
            return Rectangle(self.color, self.position, (self.rect[0] + other.rect[0], self.rect[1] + other.rect[1]))
        else:
            return Circle(other.color, other.position, (self.rect[0] + other.rect[0], self.rect[1] + other.rect[1]))
    def __sub__(self, other):
        if self < other:
            return Exception("First rectangle is less then seccond")
        return Rectangle(self.color, self.position, (max(self.rect[0] - other.rect[0], 0), max(self.rect[1] - other.rect[1], 0)))

    def draw(self, screen):
        pg.draw.rect(screen, self.color, pg.Rect(
            self.position[0], self.position[1], self.rect[0], self.rect[1]
        ))



WINDOW_SIZE = (800, 600)
def run_game():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Game")

    rectangle = Rectangle("white", (300, 200), (200, 200))
    circle1 = Circle("green", (200,200), 100)
    circle2 = Circle("red", (100,100), 80)
    circle3 = circle1 - circle2
    circle3.color = "blue"
    print(circle2 > circle1)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        rectangle.draw(screen)
        circle1.draw(screen)
        circle2.draw(screen)
        circle3.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    run_game()