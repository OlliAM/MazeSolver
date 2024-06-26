import random
import time

from cell import Cell
from utiliity import Window, Point


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = Window(1000, 1000)
        self._cells = []
        self.seed = None
        if self.num_cols > 0 and self.num_rows > 0:
            self._create_cells()
            self._break_entrance_and_exit()
        else:
            raise ValueError("Number of row or number of columns is less than 1")
        self._break_walls_r(0, 0, self.seed)
        self._reset_visited()
        self._solve_r(0, 0)


    def get_cells(self):
        return self._cells

    def _create_cells(self):
        for i in range(self.num_rows):
            col = []
            for j in range(self.num_cols):
                cell = Cell(self.window)
                cell.i = i
                cell.j = j
                col.append(cell)
            self._cells.append(col)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self.x1 + self.cell_size_x * j
        x2 = x1 + self.cell_size_x
        y1 = self.y1 + self.cell_size_y * i
        y2 = y1 + self.cell_size_y
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        self._cells[i][j].draw(p1, p2)
        self._animate()

    def _animate(self):
        self.window.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        maze_exit = self._cells[self.num_rows - 1][self.num_cols - 1]
        entrance.has_top_wall = False
        maze_exit.has_bottom_wall = False
        entrance.draw(entrance.get_position()[0], entrance.get_position()[1])
        maze_exit.draw(maze_exit.get_position()[0], maze_exit.get_position()[1])

    def _break_walls_r(self, i, j, seed=None):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if seed is not None:
            random.seed(seed)
        while True:
            to_visit = []
            for cell in self.adjacent_cells(i, j):
                if not cell.visited:
                    to_visit.append(cell)
            if not to_visit:
                current_cell.draw()
                break
            else:
                rand = 0
                if len(to_visit) > 1:
                    rand = random.randrange(0, len(to_visit))
                to_cell = self._cells[to_visit[rand].get_ij()[0]][to_visit[rand].get_ij()[1]]
                connector_wall = self.connected(current_cell, to_cell)
                match connector_wall:
                    case "top":
                        current_cell.has_top_wall = False
                        to_cell.has_bottom_wall = False
                    case "right":
                        current_cell.has_right_wall = False
                        to_cell.has_left_wall = False
                    case "bottom":
                        current_cell.has_bottom_wall = False
                        to_cell.has_top_wall = False
                    case "left":
                        current_cell.has_left_wall = False
                        to_cell.has_right_wall = False
                    case _:
                        raise Exception("You dun goof'd")
                self._draw_cell(i, j)
                self._animate()
                self._break_walls_r(to_cell.get_ij()[0], to_cell.get_ij()[1])

    def adjacent_cells(self, i, j):
        adjacents = []
        if j > 0:
            adjacents.append(self._cells[i][j - 1])
        if j < self.num_cols - 1:
            adjacents.append(self._cells[i][j + 1])
        if i > 0:
            adjacents.append(self._cells[i - 1][j])
        if i < self.num_rows - 1:
            adjacents.append(self._cells[i + 1][j])
        return adjacents

    def connected(self, cell1: Cell, cell2: Cell):
        connector_wall = "none"
        if cell2 in self.adjacent_cells(cell1.get_ij()[0], cell1.get_ij()[1]):
            # cell1 top wall is connected
            if cell1.get_position()[0] == Point(cell2.get_position()[0].x, cell2.get_position()[1].y):
                connector_wall = "top"
            # cell1 right wall is connected
            if cell1.get_position()[1] == Point(cell2.get_position()[0].x, cell2.get_position()[1].y):
                connector_wall = "right"
            # cell1 bottom wall is connected
            if cell1.get_position()[1] == Point(cell2.get_position()[1].x, cell2.get_position()[0].y):
                connector_wall = "bottom"
            # cell1 left wall is connected
            if cell1.get_position()[0] == Point(cell2.get_position()[1].x, cell2.get_position()[0].y):
                connector_wall = "left"
        return connector_wall

    def has_wall(self, cell1: Cell, cell2: Cell):
        match self.connected(cell1, cell2):
            case "top":
                return cell1.has_top_wall and cell2.has_bottom_wall
            case "right":
                return cell1.has_right_wall and cell2.has_left_wall
            case "bottom":
                return cell1.has_bottom_wall and cell2.has_top_wall
            case "left":
                return cell1.has_left_wall and cell2.has_right_wall
            case _: raise Exception("cell ain't connected son")

    def _solve_r(self, i, j):
        current_cell = self._cells[i][j]
        current_i = current_cell.get_ij()[0]
        current_j = current_cell.get_ij()[1]
        end_cell = self._cells[self.num_rows-1][self.num_cols-1]
        self._animate()
        current_cell.visited = True
        if current_cell == end_cell:
            return True
        for cell in self.adjacent_cells(current_i, current_j):
            if not self.has_wall(current_cell, cell) and not cell.visited:
                current_cell.draw_move(cell)
                if self._solve_r(cell.get_ij()[0], cell.get_ij()[1]):
                    return True
                else:
                    current_cell.draw_move(cell, True)
        return False



    def _reset_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False
