import random
import copy
from typing import Tuple, Optional
from enum import Enum


class Colors(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    ORANGE = 4
    PINK = 5
    WHITE = 6
    YELLOW = 7


class Cell:
    def __init__(self, color, x: int, y: int):
        """
        Creates instance of cell.
        """
        self._color = color.value
        self._x = x
        self._y = y

    def get_color(self) -> int:
        return self._color

    def set_color(self, color):
        self._color = color.value

    def get_x(self) -> int:
        return self._x

    def set_x(self, x: int):
        self._x = x

    def get_y(self) -> int:
        return self._y

    def set_y(self, y: int):
        self._y = y

    def __eq__(self, other_cell: object) -> bool:
        return self.get_color() == other_cell.get_color()


class Board:
    def __init__(self, size: int):
        """
        Creates instance of board.
        """
        self._size = size
        self._colors_number = 7
        self._grid = self.generate_grid(1)

    def get_grid(self) -> list:
        return self._grid

    def set_grid(self, new_grid: list):
        self._grid = new_grid

    def get_size(self) -> int:
        return self._size

    def get_colors_number(self) -> int:
        return self._colors_number

    def generate_grid(self, level: int) -> list:
        """
        Generates random grid, which is not lost and there are not any matches.
        """
        size = self.get_size()
        if level <= 3:
            number_of_types = (3 + level % 4)
        else:
            number_of_types = self.get_colors_number()
        grid = [[Cell(Colors(random.randint(1, number_of_types)), x, y)
                for x in range(size)]
                for y in range(size)]
        while self.find_cells_to_delete(grid)[0] != []\
                or self.check_lost(grid):
            grid = [[Cell(Colors(random.randint(1, number_of_types)), x, y)
                    for x in range(size)]
                    for y in range(size)]
        return grid

    def find_cells_to_delete(self,
                             grid: Optional[list] = None) -> Tuple[list, int]:
        """
        Finds matches and counts score.
        """
        if grid is None:
            grid = self.get_grid()
        cells_to_delete = []
        # ROWS
        cells_list_row, rows_score = self._check_row(grid)
        for cell in cells_list_row:
            if cell not in cells_to_delete:
                cells_to_delete.append(cell)
        # COLUMNS
        cells_list_column, columns_score = self._check_column(grid)
        for cell in cells_list_column:
            if cell not in cells_to_delete:
                cells_to_delete.append(cell)
        return cells_to_delete, rows_score + columns_score

    def _check_row(self, grid: list) -> Tuple[list, int]:
        """
        Checks all rows if there are any matches, count rows-points.
        """
        cells_to_delete = []
        score = 0
        for row in range(self.get_size()):
            for column in range(self.get_size()):
                base = grid[row][column]
                to_delete_local = [(row, column)]
                field_count = 1
                for i in range(column+1, self.get_size()):
                    if grid[row][i] == base:
                        field_count += 1
                        to_delete_local.append((row, i))
                    if grid[row][i] != base or i == self.get_size() - 1:
                        if field_count >= 3 and\
                                to_delete_local[0] not in cells_to_delete:
                            cells_to_delete += to_delete_local
                            score += field_count
                        field_count = 1
                        break
        return cells_to_delete, score

    def _check_column(self, grid: list) -> Tuple[list, int]:
        """
        Checks all columns if there are any matches, count columns-points.
        """
        cells_to_delete = []
        score = 0
        for row in range(self.get_size()):
            for column in range(self.get_size()):
                base = grid[row][column]
                to_delete_local = [(row, column)]
                field_count = 1
                for i in range(row+1, self.get_size()):
                    if grid[i][column] == base:
                        field_count += 1
                        to_delete_local.append((i, column))
                    if grid[i][column] != base\
                            or i == self.get_size() - 1:
                        if field_count >= 3 and\
                                to_delete_local[0] not in cells_to_delete:
                            cells_to_delete += to_delete_local
                            score += field_count
                        field_count = 1
                        break
        return cells_to_delete, score

    def check_lost(self, grid: list) -> bool:
        """
        Checks the possibilities of matches.
        """
        for x in range(self.get_size()):
            for y in range(self.get_size()):
                base = grid[x][y]
                necessary = [(x, y+2), (x, y+1), (x+2, y), (x+1, y)]
                sufficient = [[(x-1, y+1), (x+1, y+1)],
                              [(x, y-2), (x, y+3), (x-1, y-1), (x+1, y-1), (x-1, y+2), (x+1, y+2)], # noqa
                              [(x+1, y-1), (x+1, y+1)],
                              [(x-2, y), (x+3, y), (x-1, y-1), (x-1, y+1), (x+2, y-1), (x+2, y+1)]] # noqa
                for i, case in enumerate(necessary):
                    if self._point_in_range(case) and\
                            grid[case[0]][case[1]] == base:
                        for prospect in sufficient[i]:
                            if self._point_in_range(prospect) and\
                                    grid[prospect[0]][prospect[1]] == base:
                                return False
        return True

    def _point_in_range(self, point: tuple) -> bool:
        """
        Checks if the given coordinates of the point fit on the board.
        """
        x, y = point
        x_case = True if x in range(self.get_size()) else False
        y_case = True if y in range(self.get_size()) else False
        return x_case and y_case

    def delete_jewels(self, matched: list, level: int) -> list:
        """
        Change all colors of matched cells. Randomize the top cell's colors.
        """
        number_of_types = (3 + level % 4) if level <= 3 else 7
        for cell in sorted(matched, key=lambda pair: pair[0]):
            x, y = cell
            while x > 0:
                new_color = self.get_grid()[x-1][y].get_color()
                self.get_grid()[x][y].set_color(Colors(new_color))
                x -= 1
            new_top_color = Colors(random.randint(1, number_of_types))
            self.get_grid()[x][y].set_color(new_top_color)
        return self.get_grid()

    def _change_jewels(self, grid: list, cells: list) -> list:
        """
        Change colors of given cells.
        """
        result = copy.deepcopy(grid)
        x1, y1 = cells[0]
        x2, y2 = cells[1]
        result[x1][y1]._color, result[x2][y2]._color =\
            result[x2][y2]._color, result[x1][y1]._color
        return result

    def handle_selected_jewels(self,
                               selected: list,
                               last_grid: Optional[list] = None) -> Tuple[list, list, int]: # noqa
        """
        Checks if the selection is valid.
        """
        if last_grid is None:
            last_grid = self.get_grid()
        x, y = selected[0]
        neighbours = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        if selected[1] not in neighbours:
            return last_grid, [], 0
        elif selected[1] == selected[0]:
            return last_grid, [], 0
        new_grid = self._change_jewels(last_grid, selected)
        match, score = self.find_cells_to_delete(new_grid)
        if match == []:
            return last_grid, [], 0
        return new_grid, match, score
