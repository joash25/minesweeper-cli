from random import randrange

def create_board(row_size: int, col_size: int) -> list[list[dict[str, bool | int]]] | None:
    """
    Creates a 2D board (list of lists) initialized with {"visible": False, "value": 0}.

    Each element in the board represents a cell.

    Args:
        row_size (int): Number of rows in the board. Must be >= 1.
        col_size (int): Number of columns in the board. Must be >= 1.

    Returns:
        list[list[dict[str, bool | int]]] | None: A 2D list representing the board,
        or None if the input dimensions are invalid (less than 1).
    """
    if row_size < 1 or col_size < 1:
        return None
    
    board: list[list[dict[str, bool | int]]] = [
        [{"visible": False, "value": 0} for _ in range(col_size)] 
        for _ in range(row_size)]

    return board


def deploy_mines_on_board(board: list[list[dict[str, bool | int]]], 
        row_size: int, col_size: int, mines_percent: int) -> int | None:
    """
    Places mines randomly on the board based on a percentage.

    Each mine is represented by -1. The board is modified in-place.

    Args:
        board (list[list[dict[str, bool | int]]]): A 2D list representing the game board.
        row_size (int): Number of rows in the board. Must be >= 1.
        col_size (int): Number of columns in the board. Must be >= 1.
        mines_percent (int): Percentage of cells to be filled with mines.
        
    Returns:
        int | None: The total number of mines deployed, or None if the input is invalid.
    """
    if row_size < 1 or col_size < 1:
        return None
    
    total_mines: int = int((row_size * col_size) * (mines_percent / 100))
    deployed_mines_count: int = 0

    while deployed_mines_count < total_mines:
        row_idx: int = randrange(row_size)
        col_idx: int = randrange(col_size)
        if board[row_idx][col_idx]["value"] != -1:
            board[row_idx][col_idx]["value"] = -1
            deployed_mines_count += 1

    return deployed_mines_count


def update_cells_with_adjacent_mine_counts(board: list[list[dict[str, bool | int]]],
                                            row_size: int, col_size: int) -> None:
    """
    Updates each non-mine cell on the board with the count of adjacent mines.

    Args:
        board (list[list[dict[str, bool | int]]]): A 2D list representing the game board.
        row_size (int): Number of rows in the board. Must be >= 1.
        col_size (int): Number of columns in the board. Must be >= 1.

    Returns:
        None
    """
    for row_idx in range(row_size):
        for col_idx in range(col_size):
            if board[row_idx][col_idx]["value"] == -1:
                continue

            adjacent_mines_count: int = 0
            adjacent_cell_positions: tuple[tuple[int, int]] = \
                get_adjacent_cell_positions(row_idx, col_idx)

            for _row_idx, _col_idx in adjacent_cell_positions:
                if _row_idx >= 0 and _row_idx < row_size and \
                    _col_idx >= 0 and _col_idx < col_size and \
                    board[_row_idx][_col_idx]["value"] == -1:
                    adjacent_mines_count += 1
                
            board[row_idx][col_idx]["value"] = adjacent_mines_count


def get_adjacent_cell_positions(row_idx: int, col_idx: int) -> tuple[tuple[int, int]]:
    """
    Returns the positions of all adjacent cells around a given cell in a grid.

    Includes all eight neighboring positions: horizontal, vertical, and diagonal.

    Args:
        row_idx (int): The row index of the current cell.
        col_idx (int): The column index of the current cell.

    Returns:
        tuple[tuple[int, int]]: A list of (row, column) positions for all adjacent cells (8 neighbors).
    """
    adjacent_cell_positions: tuple[tuple[int, int]] = ( 
        (row_idx - 1, col_idx),
        (row_idx + 1, col_idx),
        (row_idx, col_idx - 1),
        (row_idx, col_idx + 1),
        (row_idx - 1, col_idx - 1),
        (row_idx - 1, col_idx + 1),
        (row_idx + 1, col_idx - 1),
        (row_idx + 1, col_idx + 1)
    )

    return adjacent_cell_positions