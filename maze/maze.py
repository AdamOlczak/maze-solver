import random
import threading
from time import sleep
from typing import Optional

from graphics import Point, Window
from maze.cell import Cell


class Maze:
    def __init__(self, p1: Point, num_rows: int, num_cols: int, cell_size: int, window: Optional[Window] = None,
                 seed: int = None):
        self._p1 = p1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size = cell_size
        self._win = window
        if seed is not None:
            random.seed(seed)
        self.animate = False
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def solve(self) -> bool:
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        right_cell = left_cell = top_cell = bottom_cell = None

        if i < self._num_cols - 1:
            right_cell = self._cells[i + 1][j]
        if i > 0:
            left_cell = self._cells[i - 1][j]
        if j < self._num_rows - 1:
            bottom_cell = self._cells[i][j + 1]
        if j > 0:
            top_cell = self._cells[i][j - 1]

        if left_cell and not cell.has_left_wall and not left_cell.visited:
            cell.draw_move(left_cell)
            if self._solve_r(i - 1, j):
                return True
            cell.draw_move(left_cell, undo=True)
        if right_cell and not cell.has_right_wall and not right_cell.visited:
            cell.draw_move(right_cell)
            if self._solve_r(i + 1, j):
                return True
            cell.draw_move(right_cell, undo=True)
        if top_cell and not cell.has_top_wall and not top_cell.visited:
            cell.draw_move(top_cell)
            if self._solve_r(i, j - 1):
                return True
            cell.draw_move(top_cell, undo=True)
        if bottom_cell and not cell.has_bottom_wall and not bottom_cell.visited:
            cell.draw_move(bottom_cell)
            if self._solve_r(i, j + 1):
                return True
            cell.draw_move(bottom_cell, undo=True)

        return False

    def _create_cells(self):
        self._cells = [
            [
                Cell(
                    Point(self._p1.x + x * self._cell_size, self._p1.y + y * self._cell_size),
                    Point(self._p1.x + self._cell_size + x * self._cell_size,
                          self._p1.y + self._cell_size + y * self._cell_size),
                    window=self._win
                ) for y in range(self._num_rows)
            ] for x in range(self._num_cols)
        ]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                self._draw_cell(col, row)

    def _break_entrance_and_exit(self):
        cell = self._cells[0][0]
        cell.has_top_wall = False
        self._draw_cell(0, 0)

        cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_visit: list[tuple[tuple[int, int], Cell]] = []
            # cell at top
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append(((i, j - 1), self._cells[i][j - 1]))
            # cell to the right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append(((i + 1, j), self._cells[i + 1][j]))
            # cell at bottom
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append(((i, j + 1), self._cells[i][j + 1]))
            # cell to the left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append(((i - 1, j), self._cells[i - 1][j]))

            if len(to_visit) == 0:
                return

            location: tuple[int, int]
            next_cell: Cell
            location, next_cell = random.choice(to_visit)
            cell.break_wall_between_cell(next_cell)
            self._draw_cell(i, j)

            self._break_walls_r(*location)

    def _reset_cells_visited(self):
        for cols in self._cells:
            for cell in cols:
                cell.visited = False

    def _draw_cell(self, i: int, j: int):
        if self._win is None:
            return
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        if self.animate:
            sleep(0.1)
