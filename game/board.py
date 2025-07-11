from random import randrange

from .custom_types import Board
from .cell import Cell

class MinesweeperBoard:
    """
    Represents the game board for Minesweeper.
    """

    def __init__(self, row_size: int, col_size: int, mine_percent: float) -> None:
        self.row_size: int = row_size
        self.col_size: int = col_size
        self.mine_percent: float = mine_percent
        self._cell_count: int = row_size * col_size
        self._mine_cell_count: int = int(self.cell_count * self.mine_percent)
        self._non_mine_cell_count: int = self.cell_count - self.mine_cell_count
        self._revealed_non_mine_cell_count: int = 0
        self._grid: Board = self._initialize_grid()
        self._deploy_mines()
        self._update_adjacent_mine_counts()

    @property
    def row_size(self) -> int:
        return self._row_size
    
    @property
    def col_size(self) -> int:
        return self._col_size
    
    @property
    def mine_percent(self) -> float:
        return self._mine_percent
    
    @property
    def cell_count(self) -> int:
        return self._cell_count
    
    @property
    def mine_cell_count(self) -> int:
        return self._mine_cell_count
    
    @property
    def non_mine_cell_count(self) -> int:
        return self._non_mine_cell_count

    @property
    def revealed_non_mine_cell_count(self) -> int:
        return self._revealed_non_mine_cell_count
    
    @property
    def grid(self) -> Board:
        return self._grid
    
    @row_size.setter
    def row_size(self, size: int) -> None:
        if not isinstance(size, int):
            raise TypeError(
                f"Invalid type for `row_size` in {self.__class__.__name__}"
                f": expected int, got {type(size).__name__}")
        
        if size < 1:
            raise ValueError(
                f"Invalid value for `size` in {self.__class__.__name__}"
                f": must be `size` >= 1, got {size}")
        
        if not hasattr(self, "_row_size"):
            self._row_size = size

    @col_size.setter
    def col_size(self, size: int) -> None:
        if not isinstance(size, int):
            raise TypeError(
                f"Invalid type for `size` in {self.__class__.__name__}"
                f": expected int, got {type(size).__name__}")
        
        if size < 1:
            raise ValueError(
                f"Invalid value for `size` in {self.__class__.__name__}"
                f": must be `size` >= 1, got {size}")
        
        if not hasattr(self, '_col_size'):
            self._col_size = size
    
    @mine_percent.setter
    def mine_percent(self, percent: float) -> None:
        if not isinstance(percent, float):
            raise TypeError(
                f"Invalid type for `percent` in {self.__class__.__name__}"
                f": expected float, got {type(percent).__name__}")
        
        if percent < 0.1 or percent > 0.9:
            raise ValueError(
                f"Invalid value for `percent` in {self.__class__.__name__}"
                f": must be 0.1 <= `percent` <= 0.9, got {percent}")
        
        if not hasattr(self, "_mine_percent"):
            self._mine_percent = percent

    def _initialize_grid(self) -> Board:
        """
        Creates a 2D grid (list of lists) initialized with Cell objects.
    
        Each element in the grid represents a Cell.
    
        Returns:
            Board: A 2D list representing the grid.
        """
        return [
            [Cell() for _ in range(self._col_size)] 
            for _ in range(self._row_size)]

    def _deploy_mines(self) -> None:
        """
        Places mines randomly on the grid based on a mine percentage.

        Each mine is represented by -1.
        """
        deployed_mine_count: int = 0

        while deployed_mine_count < self._mine_cell_count:
            row_idx: int = randrange(self._row_size)
            col_idx: int = randrange(self._col_size)

            if self._grid[row_idx][col_idx].value != -1:
                self._grid[row_idx][col_idx].value = -1
                deployed_mine_count += 1

    def _get_adjacent_cell_positions(self, row_idx: int, col_idx: int) -> tuple[tuple[int, int]]:
        """
        Returns the positions of all adjacent cells around a given cell in a grid.
    
        Includes all eight neighboring positions: horizontal, vertical, and diagonal.
    
        Args:
            row_idx (int): The row index of the current cell.
            col_idx (int): The column index of the current cell.
    
        Returns:
            tuple[tuple[int, int]]: A list of (row, column) positions for all adjacent cells (8 neighbors).
        """
        if not isinstance(row_idx, int):
            raise TypeError(
                f"Invalid type for `row_idx` in {self.__class__.__name__}._get_adjacent_cell_positions"
                f": expected int, got {type(row_idx).__name__}")

        if not isinstance(col_idx, int):
            raise TypeError(
                f"Invalid type for `col_idx` in {self.__class__.__name__}._get_adjacent_cell_positions"
                f": expected int, got {type(col_idx).__name__}")
        
        return ( 
            (row_idx - 1, col_idx),
            (row_idx + 1, col_idx),
            (row_idx, col_idx - 1),
            (row_idx, col_idx + 1),
            (row_idx - 1, col_idx - 1),
            (row_idx - 1, col_idx + 1),
            (row_idx + 1, col_idx - 1),
            (row_idx + 1, col_idx + 1)
        )

    def _update_adjacent_mine_counts(self) -> None:
        """
        Updates each non-mine cell on the grid with the count of adjacent mines.
        """
        for row_idx in range(self._row_size):
            for col_idx in range(self._col_size):
                if self._grid[row_idx][col_idx].value == -1:
                    continue
    
                adjacent_mine_count: int = 0
                adjacent_cell_positions: tuple[tuple[int, int]] = self._get_adjacent_cell_positions(row_idx, col_idx)
    
                for _row_idx, _col_idx in adjacent_cell_positions:
                    if 0 <= _row_idx < self._row_size and \
                        0 <= _col_idx < self._col_size and \
                        self._grid[_row_idx][_col_idx].value == -1:
                        adjacent_mine_count += 1
                    
                self._grid[row_idx][col_idx].value = adjacent_mine_count

    def reveal_non_mine_cells(self, row_idx: int, col_idx: int) -> None:
        """
        Recursively reveals all connected non-mine cells starting from the given position.
    
        Expands outward until it reaches cells that are adjacent to at least one mine
        (i.e., cells with a non-zero value). Only hidden, non-mine cells are revealed.
    
        Args:
            row_idx (int): Starting row index. Must be in range [0, row_size).
            col_idx (int): Starting column index. Must be in range [0, col_size).
        """
        if not isinstance(row_idx, int):
            raise TypeError(
                f"Invalid type for `row_idx` in {self.__class__.__name__}.reveal_non_mine_cells"
                f": expected int, got {type(row_idx).__name__}")

        if not isinstance(col_idx, int):
            raise TypeError(
                f"Invalid type for `col_idx` in {self.__class__.__name__}.reveal_non_mine_cells"
                f": expected int, got {type(col_idx).__name__}")
        
        if 0 > row_idx >= self._row_size or \
            0 > col_idx >= self._col_size or \
            self._grid[row_idx][col_idx].visible:
            return None
        
        self._grid[row_idx][col_idx].visible = True
        self._revealed_non_mine_cell_count += 1
    
        if self._grid[row_idx][col_idx].value != 0:
            return None
        
        adjacent_cell_positions: tuple[tuple[int, int]] = self._get_adjacent_cell_positions(row_idx, col_idx)
    
        for _row_idx, _col_idx in adjacent_cell_positions:
            self.reveal_non_mine_cells(_row_idx, _col_idx)

    def reveal_mine_cells(self) -> None:
        """
        Reveals all mine cells on the board by setting their 'visible' flag to True.
        """
        for row in self._grid:
            for cell in row:
                if cell.value == -1:
                    cell.visible = True

# ******************** old code ********************  

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


def reveal_non_mine_cells(board: list[list[dict[str, bool | int]]], row_size: int,
                        col_size: int, row_idx: int, col_idx: int) -> None:
    """
    Recursively reveals all connected non-mine cells starting from the given position.

    Expands outward until it reaches cells that are adjacent to at least one mine
    (i.e., cells with a non-zero value). Only hidden, non-mine cells are revealed.

    Args:
        board (list[list[dict[str, bool | int]]]): A 2D list representing the game board.
        row_size (int): Number of rows in the board. Must be >= 1.
        col_size (int): Number of columns in the board. Must be >= 1.
        row_idx (int): Starting row index. Must be in range [0, row_size).
        col_idx (int): Starting column index. Must be in range [0, col_size).

    Returns:
        None
    """
    if row_idx < 0 or row_idx >= row_size or \
        col_idx < 0 or col_idx >= col_size or \
        board[row_idx][col_idx]["visible"]:
        return None
    
    board[row_idx][col_idx]["visible"] = True

    if board[row_idx][col_idx]["value"] != 0:
        return None
    
    adjacent_cell_positions: tuple[tuple[int, int]] = \
        get_adjacent_cell_positions(row_idx, col_idx)

    for _row_idx, _col_idx in adjacent_cell_positions:
        reveal_non_mine_cells(board, row_size, col_size,_row_idx, _col_idx)


def get_visible_cell_count(board: list[list[dict[str, bool | int]]]) -> int:
    """
    Counts and returns the number of visible cells on the board.

    Args:
        board (list[list[dict[str, bool | int]]]): A 2D list representing the game board.

    Returns:
        int: The total number of visible (revealed) cells.
    """
    visible_cell_count = 0

    for row in board:
        for col in row:
            if col["visible"]:
                visible_cell_count += 1
    
    return visible_cell_count


def reveal_mine_cells(board: list[list[dict[str, bool | int]]]) -> None:
    """
    Reveals all mine cells on the board by setting their 'visible' flag to True.

    Args:
        board (list[list[dict[str, bool | int]]]): A 2D list representing the game board.
    """
    for row in board:
        for cell in row:
            if cell["value"] == -1:
                cell["visible"] = True
