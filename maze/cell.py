from typing import Self

from graphics import Window, Line
from graphics.point import Point


class Cell:
    def __init__(self, p1: Point, p2: Point, window: Window, has_left_wall=True, has_right_wall=True, has_top_wall=True,
                 has_bottom_wall=True):
        self._win = window
        self._p1 = p1
        self._p2 = p2
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._visited = False

    def draw(self):
        default_color = "white"
        color = default_color
        if self.has_top_wall:
            color = "black"
        line = Line(self._p1, Point(self._p2.x, self._p1.y))
        self._win.draw_line(line, color)

        color = default_color
        if self.has_bottom_wall:
            color = "black"
        line = Line(self._p2, Point(self._p1.x, self._p2.y))
        self._win.draw_line(line, color)

        color = default_color
        if self.has_left_wall:
            color = "black"
        line = Line(self._p1, Point(self._p1.x, self._p2.y))
        self._win.draw_line(line, color)

        color = default_color
        if self.has_right_wall:
            color = "black"
        line = Line(self._p2, Point(self._p2.x, self._p1.y))
        self._win.draw_line(line, color)

    def draw_move(self, to_cell: Self, undo=False):
        color = "red"
        if undo:
            color = "gray"
        self._win.draw_line(Line(self._midpoint(), to_cell._midpoint()), color)

    def break_wall_between_cell(self, other: Self):
        # other cell to the top
        if self._p1.y > other._p1.y:
            self.has_top_wall = False
            other.has_bottom_wall = False
        # other cell to the bottom
        elif self._p1.y < other._p1.y:
            self.has_bottom_wall = False
            other.has_top_wall = False
        # other cell to the right
        elif self._p1.x < other._p1.x:
            self.has_right_wall = False
            other.has_left_wall = False
        # other cell to the left
        elif self._p1.x > other._p1.x:
            self.has_left_wall = False
            other.has_right_wall = False

    def _midpoint(self) -> Point:
        return Point((self._p1.x + self._p2.x) / 2, (self._p1.y + self._p2.y) / 2)

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    def __str__(self):
        cell_size = self._p2.x - self._p1.x
        return f"Cell at pos: ({self._p1.x}, {self._p1.y}) idx: ({self._p1.x // cell_size - 1}, {self._p1.y // cell_size - 1})"
