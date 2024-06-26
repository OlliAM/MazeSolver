import random
from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Window")
        self.__canvas = Canvas()
        self.__canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close())

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def get_background_color(self):
        return self.__canvas["background"]


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x:{self.x}, y:{self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False


class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, win: Window, left=True, right=True, top=True, bottom=True):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0
        self.i = 0
        self.j = 0
        self.win = win
        self.visited = False

    def __repr__(self):
        return f"cell at ({Point(self._x1, self._y1)}, {Point(self._x2, self._y2)})"

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (
                    self._x1 == other._x1 and
                    self._x2 == other._x2 and
                    self._y1 == other._y1 and
                    self._y2 == other._y2 and
                    self.i == other.i and
                    self.j == other.j and
                    self.has_top_wall == other.has_top_wall and
                    self.has_bottom_wall == other.has_bottom_wall and
                    self.has_right_wall == other.has_right_wall and
                    self.has_left_wall == other.has_left_wall)
        else:
            return False

    def draw(self, p1: Point = None, p2: Point = None):
        if p1 is not None:
            self._x1 = p1.x
            self._y1 = p1.y
        if p2 is not None:
            self._x2 = p2.x
            self._y2 = p2.y
        bg_color = self.win.get_background_color()
        if not self.has_left_wall:
            line = Line(Point(self._x1, self._y1 + 1), Point(self._x1, self._y2 - 1))
            self.win.draw_line(line, bg_color)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self.win.draw_line(line)
        if not self.has_right_wall:
            line = Line(Point(self._x2, self._y1 + 1), Point(self._x2, self._y2 - 1))
            self.win.draw_line(line, bg_color)
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self.win.draw_line(line)
        if not self.has_top_wall:
            line = Line(Point(self._x1 + 1, self._y1), Point(self._x2 - 1, self._y1))
            self.win.draw_line(line, bg_color)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self.win.draw_line(line)
        if not self.has_bottom_wall:
            line = Line(Point(self._x1 + 1, self._y2), Point(self._x2 - 1, self._y2))
            self.win.draw_line(line, bg_color)
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self.win.draw_line(line)

    def center(self):
        return Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = self.win.get_background_color()
        self.win.draw_line(Line(self.center(), to_cell.center()), color)

    def get_position(self):
        return Point(self._x1, self._y1), Point(self._x2, self._y2)

    def get_ij(self):
        return self.i, self.j


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
