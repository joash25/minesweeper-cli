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