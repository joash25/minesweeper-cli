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
