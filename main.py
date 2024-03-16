from time import sleep

from graphics import Window, Line, Point
from maze.cell import Cell
from maze.maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(Point(50, 50), num_rows=20, num_cols=20, cell_size=20, window=win)
    maze.animate = True
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
