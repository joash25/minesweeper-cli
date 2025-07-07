from simple_chalk import chalk

def get_player_move(row_size: int, col_size: int) -> tuple[int, int]:
    """
    Prompt the player to enter a valid row and column within the board boundaries.
    
    This function repeatedly asks for input until valid integers within the
    specified range are provided.
    
    Args:
        row_size (int): Total number of rows on the board.
        col_size (int): Total number of columns on the board.
    
    Returns:
        tuple[int, int]: A tuple (row, column) representing the player's chosen
        coordinates, using 1-based indexing.
    """
    while True:
        coord: list[str] = input(chalk.blue(f"+ Please enter the row and column number: ")).strip().split(" ")
        if len(coord) > 1:
            row_num: str = coord[0] 
            col_num: str = coord[1]

            if row_num.isnumeric() and col_num.isnumeric():
                row_idx: int = int(row_num) - 1
                col_idx: int = int(col_num) - 1
        
                if row_idx >= 0 and row_idx < row_size and \
                    col_idx >= 0 and col_idx < col_size:
                    return (row_idx, col_idx)
            
        print(chalk.yellow("\nOops! It looks like something went wrong. Please try again."), end="\n\n")



