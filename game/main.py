from pyfiglet import figlet_format

from .minesweeper_board import MinesweeperBoard
from .print_board import print_board
from .player_move import get_player_move

ROW_SIZE: int = 3 # Number of rows on the board
COL_SIZE: int = 3 # Number of columns on the board
MINE_PERCENT: float = 0.25 # Percentage of cells that contain mines

def _game_loop() -> None:
    """
    Runs the main game loop for Minesweeper.
    """
    print(figlet_format("Minesweeper"), end="")
    print(f"Game Board Size: {ROW_SIZE} rows and {COL_SIZE} columns")

    minesweeper_board: MinesweeperBoard = MinesweeperBoard(ROW_SIZE, COL_SIZE, MINE_PERCENT)

    while minesweeper_board.revealed_non_mine_cell_count != minesweeper_board.non_mine_cell_count:
        print_board(minesweeper_board.grid, ROW_SIZE, COL_SIZE)

        row_idx, col_idx = get_player_move(ROW_SIZE, COL_SIZE)
        
        if minesweeper_board.grid[row_idx][col_idx].value == -1:
            minesweeper_board.reveal_mine_cells()
            break

        minesweeper_board.reveal_non_mine_cells(row_idx, col_idx)

    print_board(minesweeper_board.grid, ROW_SIZE, COL_SIZE)
    
    if minesweeper_board.revealed_non_mine_cell_count == minesweeper_board.non_mine_cell_count:
        print(figlet_format("You won!"))
    else:
        print(figlet_format("You lose!"))


def play() -> None:
    """
    Starts and manages the main loop of the Minesweeper game.

    Repeatedly calls the core game logic (`_game_loop`) and prompts the user
    to play again or exit.
    """
    prompt: str = (
        "\nWould you like to play again?\n"
        " • Type any key and press Enter to play again\n"
        " • Press Enter to quit\n > ")

    while True:
        _game_loop()
        
        try:
            response: str = input(prompt)
            if response.strip() == "":
                break
        except KeyboardInterrupt:
            exit(1)
    