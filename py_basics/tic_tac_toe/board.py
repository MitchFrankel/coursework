"""
All functions associated with the game board
"""

__author__ = "Mitch Frnakel"
__version__ = "0.0.0"


def init_board():
    """
    Initialize the game_board

    Parameters
    -=--------
    None

    Returns
    -------
    board : list
        List of 3 lists with each of 3 positions in sublist set to " "
    """

    return [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


def display_board(board):
    """
    Display the tic tac toe board.

    Parameters
    ----------
    board : list
        List of value to display on a tic tac toe board. Requires a list of 3 lists with a single character in
        each of 3 positions

    Returns
    -------
    None
    """
    print("\n " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print("-----------")
    print(" " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print("-----------")
    print(" " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n")


def get_open_pos(game_board):
    """
    Get all open positions on the board and create an open choice board

    Parameters
    ----------
    game_board : list
        List of value to display on a tic tac toe board. Requires a list of 3 lists with a single character in
        each of 3 positions

    Returns
    -------
    choice_board : list
        Similar to board but with open positions instead of markers

    valid_pos : list
        List of all open positions
    """

    choice_board = init_board()
    valid_pos = []

    for row in range(3):
        for col in range(3):
            if game_board[row][col] not in "XO":
                pos = row * 3 + col
                choice_board[row][col] = str(pos + 1)
                valid_pos.append(pos + 1)

    return choice_board, valid_pos


def update_game_board(game_board, choice, marker):
    """
    Update the game board based on choice and marker

    Parameters
    ----------
    game_board : list
        List of value to display on a tic tac toe board. Requires a list of 3 lists with a single character in
        each of 3 positions

    choice : int
        Position to update

    marker : str
        string to place at choice position

    Returns
    -------
    game_board : list
        Updated game_board
    """
    choice -= 1
    game_board[choice // 3][choice % 3] = marker

    return game_board



