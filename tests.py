import unittest

from graphics import Point
from maze.maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10)
        self.assertEqual(len(m1._cells), num_cols)

        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_has_entrance(self):
        num_cols = 5
        num_rows = 4
        m = Maze(Point(0, 0), num_rows, num_cols, 10)
        self.assertFalse(m._cells[0][0].has_top_wall)

    def test_maze_has_exit(self):
        num_cols = 5
        num_rows = 4
        m = Maze(Point(0, 0), num_rows, num_cols, 10)
        self.assertFalse(m._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_cells_are_unvisited_after_maze_generation(self):
        num_cols = 5
        num_rows = 4
        m = Maze(Point(0, 0), num_rows, num_cols, 10)
        cells_visited = [m._cells[i][j].visited for i in range(num_cols) for j in range(num_rows)]
        self.assertNotIn(True, cells_visited, msg="There are cells in maze that haven't been marked as unvisited")


if __name__ == "__main__":
    unittest.main()
