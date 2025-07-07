from pyfiglet import figlet_format
from simple_chalk import chalk 

from .board import (
    create_board,
    deploy_mines_on_board,
    update_cells_with_adjacent_mine_counts,
    get_visible_cell_count,
    reveal_non_mine_cells,
    reveal_mine_cells
)
from .print_board import print_board
from .player_move import get_player_move

ROW_SIZE: int = 8 # Number of rows on the board
COL_SIZE: int = 8 # Number of columns on the board
TOTAL_CELLS: int = ROW_SIZE * COL_SIZE # Total number of cells on the board
MINES_PERCENT: int = 25 # Total number of percentage a mines should in a board 

def game_loop() -> None:
    print(figlet_format("Minesweeper"), end="")
    print(chalk.yellow(f"Game Board Size: {ROW_SIZE} rows and {COL_SIZE} columns"))

    board: list[list[dict[str, bool | int]]] = create_board(ROW_SIZE, COL_SIZE)
    total_mine_cells_count: int = deploy_mines_on_board(board, ROW_SIZE, COL_SIZE, MINES_PERCENT)
    total_non_mine_cells_count: int = TOTAL_CELLS - total_mine_cells_count
    update_cells_with_adjacent_mine_counts(board, ROW_SIZE, COL_SIZE)
    
    while get_visible_cell_count(board) != total_non_mine_cells_count:
        print_board(board, ROW_SIZE, COL_SIZE)

        row_idx, col_idx = get_player_move(ROW_SIZE, COL_SIZE)
        
        if board[row_idx][col_idx]["value"] == -1:
            break

        reveal_non_mine_cells(board, ROW_SIZE, COL_SIZE, row_idx, col_idx)

    if get_visible_cell_count(board) == total_non_mine_cells_count:
        print(figlet_format("You won!"))
    else:
        reveal_mine_cells(board)
        print_board(board, ROW_SIZE, COL_SIZE)
        print(figlet_format("You lose!"))


def play() -> None:
    while True:
        game_loop()
        
        prompt: str = "\nWould you like to play again?\n • Press Enter to play again\n • Type any key and press Enter to quit\n > "
        play_again: str = input(chalk.cyan(prompt)).lower()
        if play_again != "":
            break
    