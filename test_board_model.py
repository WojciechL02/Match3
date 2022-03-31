from board_model import Colors, Cell, Board


RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
BLUE = Colors.BLUE
WHITE = Colors.WHITE
ORANGE = Colors.ORANGE
PINK = Colors.PINK

r = Cell(RED, 1, 1)
g = Cell(GREEN, 1, 1)
y = Cell(YELLOW, 1, 1)
b = Cell(BLUE, 1, 1)
w = Cell(WHITE, 1, 1)
o = Cell(ORANGE, 1, 1)
p = Cell(PINK, 1, 1)


def test_check_row():
    board = Board(4)
    case = [[g, g, g, b],
            [p, o, w, y],
            [y, w, o, p],
            [g, y, y, y]]
    assert board._check_row(case) == ([(0, 0), (0, 1), (0, 2), (3, 1), (3, 2), (3, 3)], 6)


def test_check_column():
    board = Board(4)
    case = [[y, b, o, p],
            [y, o, g, w],
            [y, w, b, g],
            [y, b, y, o]]
    assert board._check_column(case) == ([(0, 0), (1, 0), (2, 0), (3, 0)], 4)


def test_find_cells_to_delete_typical():
    board4 = Board(4)
    case1 = [[g, g, g, g],
             [y, g, b, p],
             [b, y, g, o],
             [o, o, w, w]]
    board3 = Board(3)
    case2 = [[g, b, y],
             [g, y, b],
             [g, b, b]]
    assert board4.find_cells_to_delete(case1) == ([(0, 0), (0, 1), (0, 2), (0, 3)], 4)
    assert board3.find_cells_to_delete(case2) == ([(0, 0), (1, 0), (2, 0)], 3)


def test_find_cells_to_delete_no_lines():
    board = Board(4)
    case = [[g, y, b, w],
            [o, p, g, b],
            [w, b, y, g],
            [g, o, p, o]]
    assert board.find_cells_to_delete(case) == ([], 0)


def test_find_cells_to_delete_all_board():
    board = Board(4)
    case = [[g, g, g, g],
            [g, g, g, g],
            [g, g, g, g],
            [g, g, g, g]]
    assert board.find_cells_to_delete(case) == ([(0, 0), (0, 1), (0, 2), (0, 3),
                                                 (1, 0), (1, 1), (1, 2), (1, 3),
                                                 (2, 0), (2, 1), (2, 2), (2, 3),
                                                 (3, 0), (3, 1), (3, 2), (3, 3)], 32)


def test_find_cells_to_delete_L():
    board = Board(4)
    case1 = [[y, y, y, b],
             [y, b, g, w],
             [y, w, b, p],
             [y, o, w, y]]
    case2 = [[w, w, b, y],
             [g, b, g, y],
             [o, w, b, y],
             [b, y, y, y]]
    assert board.find_cells_to_delete(case1) == ([(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (3, 0)], 7)
    assert board.find_cells_to_delete(case2) == ([(3, 1), (3, 2), (3, 3), (0, 3), (1, 3), (2, 3)], 7)


def test_find_cells_to_delete_T():
    board = Board(4)
    case1 = [[b, b, b, y],
             [o, b, y, g],
             [w, b, p, o],
             [y, b, o, w]]
    case2 = [[w, y, o, y],
             [o, b, y, g],
             [w, b, p, o],
             [b, b, b, w]]
    case3 = [[b, p, o, y],
             [b, b, b, b],
             [b, y, p, o],
             [b, b, o, w]]
    case4 = [[b, w, b, y],
             [o, b, y, g],
             [g, g, g, g],
             [y, b, o, g]]
    assert board.find_cells_to_delete(case1) == ([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1), (3, 1)], 7)
    assert board.find_cells_to_delete(case2) == ([(3, 0), (3, 1), (3, 2), (1, 1), (2, 1)], 6)
    assert board.find_cells_to_delete(case3) == ([(1, 0), (1, 1), (1, 2), (1, 3), (0, 0), (2, 0), (3, 0)], 8)
    assert board.find_cells_to_delete(case4) == ([(2, 0), (2, 1), (2, 2), (2, 3), (1, 3), (3, 3)], 7)


def test_find_cells_to_delete_plus_shape():
    board = Board(4)
    case = [[g, y, b, o],
            [y, y, y, w],
            [w, y, o, p],
            [p, b, g, b]]
    assert board.find_cells_to_delete(case) == ([(1, 0), (1, 1), (1, 2), (0, 1), (2, 1)], 6)


def test_find_cells_to_delete_I():
    board = Board(3)
    case1 = [[y, y, y],
             [b, y, w],
             [y, y, y]]
    case2 = [[w, y, w],
             [w, w, w],
             [w, y, w]]
    assert board.find_cells_to_delete(case1) == ([(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2), (1, 1)], 9)
    assert board.find_cells_to_delete(case2) == ([(1, 0), (1, 1), (1, 2), (0, 0), (2, 0), (0, 2), (2, 2)], 9) # noqa


def test_point_in_range_typical():
    board = Board(8)
    assert board._point_in_range((1, 4)) is True


def test_point_in_range_corners():
    board = Board(8)
    assert board._point_in_range((0, 0)) is True
    assert board._point_in_range((0, 7)) is True
    assert board._point_in_range((7, 0)) is True
    assert board._point_in_range((7, 7)) is True


def test_point_in_range_x_outside():
    board = Board(8)
    assert board._point_in_range((10, 4)) is False
    assert board._point_in_range((-1, 4)) is False


def test_point_in_range_y_outside():
    board = Board(8)
    assert board._point_in_range((2, 15)) is False
    assert board._point_in_range((6, -2)) is False


def test_point_in_range_both_outside():
    board = Board(8)
    assert board._point_in_range((-2, 10)) is False
    assert board._point_in_range((50, -8)) is False
    assert board._point_in_range((-4, -8)) is False
    assert board._point_in_range((50, 15)) is False


def test_check_lost_defeat():
    board = Board(4)
    case = [[g, g, y, y],
            [y, o, p, p],
            [w, w, g, b],
            [b, b, y, w]]
    assert board.check_lost(case) is True


def test_check_lost_possible_connection_first_type():
    board = Board(4)
    """
    for example:
                (blue)(RED)(green)
                (RED)(green)(RED)
                (purple)(blue)(green)
    """
    case1 = [[o, y, g, b],
             [y, p, y, g],
             [w, b, b, y],
             [g, o, p, p]]
    case2 = [[p, b, g, b],
             [o, y, p, g],
             [y, b, y, y],
             [g, o, p, p]]
    case3 = [[g, y, g, b],
             [o, g, y, g],
             [w, y, b, y],
             [g, o, p, p]]
    case4 = [[y, w, y, b],
             [o, p, y, g],
             [w, y, b, o],
             [g, o, y, p]]
    assert board.check_lost(case2) is False
    assert board.check_lost(case1) is False
    assert board.check_lost(case3) is False
    assert board.check_lost(case4) is False


def test_check_lost_possible_connection_second_type_rows():
    board = Board(4)
    """
    for example:
                (blue)(purple)(RED)
                (RED)(RED)(yellow)
                (purple)(blue)(green)
    """
    case1 = [[y, y, g, b],
             [o, p, y, g],
             [w, b, b, y],
             [g, o, p, p]]
    case2 = [[w, b, g, b],
             [o, p, y, g],
             [y, y, b, w],
             [g, o, p, p]]
    case3 = [[y, o, g, b],
             [o, p, y, g],
             [w, w, b, w],
             [g, o, p, p]]
    case4 = [[y, y, g, b],
             [o, p, o, g],
             [b, w, b, b],
             [g, o, p, p]]
    case5 = [[y, y, g, b],
             [o, b, o, g],
             [y, w, b, b],
             [g, o, p, p]]
    case6 = [[y, y, g, b],
             [o, p, o, g],
             [b, w, g, g],
             [g, g, p, p]]
    assert board.check_lost(case1) is False
    assert board.check_lost(case2) is False
    assert board.check_lost(case3) is False
    assert board.check_lost(case4) is False
    assert board.check_lost(case5) is False
    assert board.check_lost(case6) is False


def test_check_lost_possible_connection_second_type_columns():
    board = Board(4)
    """
    for example:
                (blue)(RED)(green)
                (green)(RED)(purple)
                (RED)(blue)(green)
    """
    case1 = [[y, w, g, b],
             [w, p, y, g],
             [w, b, b, y],
             [g, o, p, p]]
    case2 = [[y, w, g, b],
             [o, p, w, g],
             [w, b, w, y],
             [g, o, p, p]]
    case3 = [[y, w, g, b],
             [o, w, y, g],
             [w, b, b, y],
             [g, o, p, p]]
    case4 = [[y, w, g, b],
             [o, w, y, g],
             [b, b, w, y],
             [g, o, p, p]]
    case5 = [[y, w, g, b],
             [o, w, o, g],
             [b, y, b, b],
             [g, w, p, p]]
    case6 = [[y, y, p, b],
             [o, g, o, g],
             [b, w, p, b],
             [g, o, p, p]]
    assert board.check_lost(case1) is False
    assert board.check_lost(case2) is False
    assert board.check_lost(case3) is False
    assert board.check_lost(case4) is False
    assert board.check_lost(case5) is False
    assert board.check_lost(case6) is False


def test_generate_grid_1_level():
    board = Board(8)
    cells_types = []
    for row in board.get_grid():
        for cell in row:
            cells_types.append(cell.get_color())
    assert len(set(cells_types)) == 4


def test_generate_grid_2_level():
    board = Board(8)
    cells_types = []
    for row in board.generate_grid(2):
        for cell in row:
            cells_types.append(cell.get_color())
    assert len(set(cells_types)) == 5


def test_generate_grid_3_level():
    board = Board(8)
    cells_types = []
    for row in board.generate_grid(3):
        for cell in row:
            cells_types.append(cell.get_color())
    assert len(set(cells_types)) == 6


def test_generate_grid_higher_levels_v1():
    board = Board(8)
    cells_types = []
    for row in board.generate_grid(4):
        for cell in row:
            cells_types.append(cell.get_color())
    assert len(set(cells_types)) == 7


def test_generate_grid_higher_levels_v2():
    board = Board(8)
    cells_types = []
    for row in board.generate_grid(152):
        for cell in row:
            cells_types.append(cell.get_color())
    assert len(set(cells_types)) == 7


def test_generate_grid_less_than_8():
    board = Board(4)
    assert len(board.get_grid()) == 4
    for i in range(4):
        assert len(board.get_grid()[i]) == 4


def test_generate_grid_8():
    board = Board(8)
    assert len(board.get_grid()) == 8
    for i in range(8):
        assert len(board.get_grid()[i]) == 8


def test_generate_grid_more_than_8():
    board = Board(10)
    assert len(board.get_grid()) == 10
    for i in range(10):
        assert len(board.get_grid()[i]) == 10


def test_change_jewels():
    board = Board(3)
    grid = [[y, w, g],
            [w, p, y],
            [w, b, b]]
    new_grid = board._change_jewels(grid, [(0, 0), (0, 1)])
    assert new_grid[0][0].get_color() == Colors.WHITE.value
    assert new_grid[0][1].get_color() == Colors.YELLOW.value


def test_handle_selected_jewels_rows():
    board = Board(4)
    y1 = Cell(YELLOW, 1, 1)
    case = [[y, y, w, y],
            [o, p, y1, o],
            [p, b, g, r],
            [g, b, o, p]]
    assert board.handle_selected_jewels([(0, 2), (1, 2)], case) ==\
        ([[y, y, y1, y],
          [o, p, w, o],
          [p, b, g, r],
          [g, b, o, p]], [(0, 0), (0, 1), (0, 2), (0, 3)], 4)


def test_handle_selected_jewels_not_in_neighbours():
    board = Board(4)
    case = [[y, y, w, y],
            [o, p, y, o],
            [p, b, g, r],
            [g, b, o, p]]
    assert board.handle_selected_jewels([(0, 0), (0, 2)], case) ==\
        ([[y, y, w, y],
          [o, p, y, o],
          [p, b, g, r],
          [g, b, o, p]], [], 0)


def test_handle_selected_jewels_same_cell():
    board = Board(4)
    case = [[y, y, w, y],
            [o, p, y, o],
            [p, b, g, r],
            [g, b, o, p]]
    assert board.handle_selected_jewels([(0, 0), (0, 0)], case) ==\
        ([[y, y, w, y],
          [o, p, y, o],
          [p, b, g, r],
          [g, b, o, p]], [], 0)


def test_handle_selected_jewels_no_match():
    board = Board(4)
    case = [[y, y, w, y],
            [o, p, y, o],
            [p, b, g, r],
            [g, b, o, p]]
    assert board.handle_selected_jewels([(0, 0), (1, 0)], case) ==\
        ([[y, y, w, y],
          [o, p, y, o],
          [p, b, g, r],
          [g, b, o, p]], [], 0)


def test_delete_jewels_line_in_row_top(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(ORANGE, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(PINK, r, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(0, 0), (0, 1), (0, 2), (0, 3)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(WHITE, 1, 0), Cell(ORANGE, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
         [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(PINK, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_line_in_row_down(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(GREEN, 0, 1), Cell(ORANGE, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(ORANGE, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(PINK, 3, 1), Cell(PINK, 3, 2), Cell(PINK, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(3, 1), (3, 2), (3, 3)], 1) ==\
        [[Cell(YELLOW, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(WHITE, 1, 0), Cell(GREEN, 1, 1), Cell(ORANGE, 1, 2), Cell(YELLOW, 1, 3)],
         [Cell(RED, 2, 0), Cell(ORANGE, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(PINK, 3, 2), Cell(WHITE, 3, 3)]]


def test_delete_jewels_line_in_column(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(WHITE, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(ORANGE, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
                    [Cell(WHITE, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(WHITE, 3, 0), Cell(PINK, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(1, 0), (2, 0), (3, 0)], 1) ==\
        [[Cell(RED, 0, 0), Cell(WHITE, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
         [Cell(RED, 1, 0), Cell(ORANGE, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
         [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(PINK, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_L_down(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(ORANGE, 1, 0), Cell(WHITE, 1, 1), Cell(ORANGE, 1, 2), Cell(RED, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(WHITE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(3, 1), (3, 2), (3, 3), (2, 1), (1, 1)], 1) ==\
        [[Cell(YELLOW, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(ORANGE, 1, 0), Cell(RED, 1, 1), Cell(YELLOW, 1, 2), Cell(YELLOW, 1, 3)],
         [Cell(RED, 2, 0), Cell(RED, 2, 1), Cell(ORANGE, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(YELLOW, 3, 1), Cell(PINK, 3, 2), Cell(WHITE, 3, 3)]]


def test_delete_jewels_L_up(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(ORANGE, 1, 0), Cell(WHITE, 1, 1), Cell(WHITE, 1, 2), Cell(WHITE, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(3, 1), (2, 1), (1, 1), (1, 2), (1, 3)], 1) ==\
        [[Cell(YELLOW, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(ORANGE, 1, 0), Cell(RED, 1, 1), Cell(YELLOW, 1, 2), Cell(YELLOW, 1, 3)],
         [Cell(RED, 2, 0), Cell(RED, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(YELLOW, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_T_up(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(WHITE, 1, 1), Cell(WHITE, 1, 2), Cell(RED, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(1, 0), (3, 1), (2, 1), (1, 1), (1, 2)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(YELLOW, 0, 3)],
         [Cell(YELLOW, 1, 0), Cell(RED, 1, 1), Cell(YELLOW, 1, 2), Cell(RED, 1, 3)],
         [Cell(RED, 2, 0), Cell(RED, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(YELLOW, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_T_down(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(PINK, 1, 0), Cell(WHITE, 1, 1), Cell(ORANGE, 1, 2), Cell(RED, 1, 3)],
                    [Cell(RED, 2, 0), Cell(WHITE, 2, 1), Cell(PINK, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(WHITE, 3, 0), Cell(WHITE, 3, 1), Cell(WHITE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(3, 0), (3, 1), (3, 2), (3, 3), (1, 1), (2, 1)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(YELLOW, 1, 0), Cell(RED, 1, 1), Cell(YELLOW, 1, 2), Cell(YELLOW, 1, 3)],
         [Cell(PINK, 2, 0), Cell(RED, 2, 1), Cell(ORANGE, 2, 2), Cell(RED, 2, 3)],
         [Cell(RED, 3, 0), Cell(YELLOW, 3, 1), Cell(PINK, 3, 2), Cell(WHITE, 3, 3)]]


def test_delete_jewels_T_left(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(RED, 0, 2), Cell(ORANGE, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(PINK, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
                    [Cell(WHITE, 2, 0), Cell(WHITE, 2, 1), Cell(WHITE, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(WHITE, 3, 0), Cell(ORANGE, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(2, 0), (2, 1), (2, 2), (2, 3), (1, 0), (3, 0)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(RED, 1, 0), Cell(YELLOW, 1, 1), Cell(RED, 1, 2), Cell(ORANGE, 1, 3)],
         [Cell(RED, 2, 0), Cell(PINK, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(ORANGE, 3, 1), Cell(ORANGE, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_T_right(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(YELLOW, 0, 1), Cell(YELLOW, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(RED, 1, 1), Cell(RED, 1, 2), Cell(WHITE, 1, 3)],
                    [Cell(WHITE, 2, 0), Cell(WHITE, 2, 1), Cell(WHITE, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(PINK, 3, 1), Cell(ORANGE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(2, 0), (2, 1), (2, 2), (2, 3), (1, 3), (3, 3)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(YELLOW, 1, 0), Cell(YELLOW, 1, 1), Cell(YELLOW, 1, 2), Cell(RED, 1, 3)],
         [Cell(WHITE, 2, 0), Cell(RED, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(PINK, 3, 1), Cell(ORANGE, 3, 2), Cell(YELLOW, 3, 3)]]


def test_delete_jewels_plus_shape(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(RED, 0, 0), Cell(YELLOW, 0, 1), Cell(ORANGE, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(ORANGE, 1, 0), Cell(WHITE, 1, 1), Cell(RED, 1, 2), Cell(WHITE, 1, 3)],
                    [Cell(WHITE, 2, 0), Cell(WHITE, 2, 1), Cell(WHITE, 2, 2), Cell(RED, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(ORANGE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(2, 0), (2, 1), (2, 2), (1, 1), (3, 1)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(YELLOW, 0, 3)],
         [Cell(RED, 1, 0), Cell(RED, 1, 1), Cell(ORANGE, 1, 2), Cell(WHITE, 1, 3)],
         [Cell(ORANGE, 2, 0), Cell(RED, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(YELLOW, 3, 1), Cell(ORANGE, 3, 2), Cell(WHITE, 3, 3)]]


def test_delete_jewels_H(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(RED, 0, 0), Cell(YELLOW, 0, 1), Cell(ORANGE, 0, 2), Cell(YELLOW, 0, 3)],
                    [Cell(ORANGE, 1, 0), Cell(WHITE, 1, 1), Cell(RED, 1, 2), Cell(WHITE, 1, 3)],
                    [Cell(GREEN, 2, 0), Cell(WHITE, 2, 1), Cell(WHITE, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(YELLOW, 3, 0), Cell(WHITE, 3, 1), Cell(ORANGE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(2, 1), (2, 2), (2, 3), (1, 1), (3, 1), (1, 3), (3, 3)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(ORANGE, 1, 0), Cell(RED, 1, 1), Cell(ORANGE, 1, 2), Cell(RED, 1, 3)],
         [Cell(GREEN, 2, 0), Cell(RED, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(YELLOW, 3, 0), Cell(YELLOW, 3, 1), Cell(ORANGE, 3, 2), Cell(YELLOW, 3, 3)]]


def test_delete_jewels_H_sideways(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(RED, 0, 0), Cell(YELLOW, 0, 1), Cell(ORANGE, 0, 2), Cell(RED, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(WHITE, 1, 1), Cell(WHITE, 1, 2), Cell(PINK, 1, 3)],
                    [Cell(GREEN, 2, 0), Cell(WHITE, 2, 1), Cell(GREEN, 2, 2), Cell(ORANGE, 2, 3)],
                    [Cell(WHITE, 3, 0), Cell(WHITE, 3, 1), Cell(WHITE, 3, 2), Cell(YELLOW, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    assert board.delete_jewels([(1, 0), (1, 1), (1, 2), (3, 0), (3, 1), (3, 2), (2, 1)], 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(RED, 1, 0), Cell(RED, 1, 1), Cell(RED, 1, 2), Cell(PINK, 1, 3)],
         [Cell(RED, 2, 0), Cell(RED, 2, 1), Cell(ORANGE, 2, 2), Cell(ORANGE, 2, 3)],
         [Cell(GREEN, 3, 0), Cell(YELLOW, 3, 1), Cell(GREEN, 3, 2), Cell(YELLOW, 3, 3)]]


def test_delete_jewels_all_board(monkeypatch):
    def returnOne(f, t):
        return Colors.RED

    board = Board(4)
    board.set_grid([[Cell(WHITE, 0, 0), Cell(WHITE, 0, 1), Cell(WHITE, 0, 2), Cell(WHITE, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(WHITE, 1, 1), Cell(WHITE, 1, 2), Cell(WHITE, 1, 3)],
                    [Cell(WHITE, 2, 0), Cell(WHITE, 2, 1), Cell(WHITE, 2, 2), Cell(WHITE, 2, 3)],
                    [Cell(WHITE, 3, 0), Cell(WHITE, 3, 1), Cell(WHITE, 3, 2), Cell(WHITE, 3, 3)]])
    monkeypatch.setattr('board_model.random.randint', returnOne)
    delete_list = []
    for i in range(4):
        for j in range(4):
            delete_list.append((i, j))
    assert board.delete_jewels(delete_list, 1) ==\
        [[Cell(RED, 0, 0), Cell(RED, 0, 1), Cell(RED, 0, 2), Cell(RED, 0, 3)],
         [Cell(RED, 1, 0), Cell(RED, 1, 1), Cell(RED, 1, 2), Cell(RED, 1, 3)],
         [Cell(RED, 2, 0), Cell(RED, 2, 1), Cell(RED, 2, 2), Cell(RED, 2, 3)],
         [Cell(RED, 3, 0), Cell(RED, 3, 1), Cell(RED, 3, 2), Cell(RED, 3, 3)]]


def test_delete_jewels_no_matches():
    board = Board(4)
    board.set_grid([[Cell(YELLOW, 0, 0), Cell(WHITE, 0, 1), Cell(YELLOW, 0, 2), Cell(WHITE, 0, 3)],
                    [Cell(WHITE, 1, 0), Cell(YELLOW, 1, 1), Cell(WHITE, 1, 2), Cell(YELLOW, 1, 3)],
                    [Cell(PINK, 2, 0), Cell(ORANGE, 2, 1), Cell(GREEN, 2, 2), Cell(PINK, 2, 3)],
                    [Cell(ORANGE, 3, 0), Cell(PINK, 3, 1), Cell(RED, 3, 2), Cell(ORANGE, 3, 3)]])
    assert board.delete_jewels([], 1) ==\
        [[Cell(YELLOW, 0, 0), Cell(WHITE, 0, 1), Cell(YELLOW, 0, 2), Cell(WHITE, 0, 3)],
         [Cell(WHITE, 1, 0), Cell(YELLOW, 1, 1), Cell(WHITE, 1, 2), Cell(YELLOW, 1, 3)],
         [Cell(PINK, 2, 0), Cell(ORANGE, 2, 1), Cell(GREEN, 2, 2), Cell(PINK, 2, 3)],
         [Cell(ORANGE, 3, 0), Cell(PINK, 3, 1), Cell(RED, 3, 2), Cell(ORANGE, 3, 3)]]
