from .cell import Cell
from .custom_types import Board

def print_column_numbers(col_size: int, digit_count: int) -> None:
    """
    Prints the column headers (numbers) aligned with the game board.

    Args:
        col_size (int): Number of columns in the board.
        digit_count (int): Width for formatting numbers based on the largest index.
    """
    print(" " * (digit_count + 3), end="")

    for i in range(1, col_size + 1):
        n = digit_count - len(str(i))
        print(f" {' ' * n}{i}  ", end="")
    print()


def print_horizontal_partition(col_size: int, digit_count: int) -> None:
    """
    Prints a horizontal line separator between rows of the board.

    Args:
        col_size (int): Number of columns in the board.
        digit_count (int): Width for formatting based on index length.
    """
    print(" " * (digit_count + 2) + "+", end="")

    for i in range(col_size):
        print("-" * (digit_count + 2) + "+", end="")
    print()


def print_horizontal_cells(board_row: list[Cell], row_idx: int, digit_count: int) -> None:
    """
    Prints the contents of a single row of the board.

    Args:
        board_row (list): A list of cell object for each cell in the row, each containing:
            - `visible` (bool): Whether the cell is revealed.
            - `value` (int): -1 for a mine, or number of adjacent mines.
        row_idx (int): The index of the current row (0-based).
        digit_count (int): Width for formatting row numbers and cells.
    """
    print(f" {' ' * (digit_count - len(str(row_idx + 1)))}{row_idx + 1} |", end="")  

    for col_idx, cell in enumerate(board_row):
        n: int = digit_count - len(str(col_idx))

        print(f" {' ' * n}", end="")

        if cell.visible and cell.value == -1:
            print("@ |", end="")
        elif cell.visible:
            print(f"{cell.value} |", end="")
        else:
            print("  |", end="")
    print()


def print_board(board: Board, row_size: int, col_size: int) -> None:
    """
    Prints the entire game board with row and column headers.

    Each cell is represented as a cell object with:
        - `visible` (bool): Whether the cell has been revealed.
        - `value` (int): The cell's value (-1 for a mine, or 0-8 for adjacent mine counts).

    Args:
        board (list): A 2D list of dictionaries representing the board state.
        row_size (int): Total number of rows in the board.
        col_size (int): Total number of columns in the board.
    """
    digit_count: int = len(str(max(row_size, col_size)))

    print(end="\n\n")
    print_column_numbers(col_size, digit_count)

    for row_idx, board_row in enumerate(board):
        print_horizontal_partition(col_size, digit_count)
        print_horizontal_cells(board_row, row_idx, digit_count)
    print_horizontal_partition(col_size, digit_count)
