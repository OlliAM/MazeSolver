from utiliity import Window, Point, Line


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
