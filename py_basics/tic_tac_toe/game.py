"""
Functions and Classes related to the game
"""

__author__ = "Mitch Frankel"
__version__ = "0.0.0"


# Imports
import board
from time import sleep as t_sleep


def start_game():
    """
    Initialize the game

    Returns
    -------
    p1_x: bool
        Whether p1's marker is X (true) or O (false)
    """

    print("Welcome to Tic Tac Doh!\n")
    t_sleep(1)

    # Get Player 1 marker
    marker = input("Player 1: Enter Marker Choice X or O: ")
    while not(marker == "X" or marker == "O"):
        print("\nNow now Player 1, that was not a valid choice!\n")
        t_sleep(1)
        marker = input("\tPlayer 1: Enter Marker Choice X or O: ")

    return True if marker == "X" else False


def move(choice_board, valid_pos, p1_turn):
    """
    Return the choice of move by player

    Parameters
    ----------
    choice_board : list
        List of values to display on a tic tac toe board. Requires a list of 3 lists with a single character in
        each of 3 positions

    valid_pos : list
        List of all open positions

    p1_turn : bool
        Whether it is player 1 or 2's turn

    Returns
    -------
    choice : int
        The choice of move
    """
    board.display_board(choice_board)

    player = get_player(p1_turn)
    choice = input("Player {}: Choose an open position above from {}: ".format(player, valid_pos))
    while choice not in [str(x) for x in valid_pos]:
        print("\nNow now Player {}, that's not a valid choice!".format(player))
        choice = input("\tPlayer {}: Choose an open position above from {}: ".format(player, valid_pos))

    return int(choice)


def get_marker(p1_turn, p1_x):
    """
    Determine the current marker based on whose turn and what marker

    Parameters
    ----------
    p1_turn : bool
        Is it Player 1's turn

    p1_x : bool
        Is Player 1 X marker

    Returns
    -------
    marker : str
        "X" or "O"
    """
    return "X" if (p1_turn and p1_x) or (not p1_turn and not p1_x) else "O"


def get_status(game_board, marker):
    """
    Get the status of the current game

    Parameters
    ----------
    game_board : list
        List of values to display on a tic tac toe game_board. Requires a list of 3 lists with a single character in
        each of 3 positions

    marker : str
        "X" or "O" for current marker

    Returns
    -------
    status : str
        Status of current game - "winner", "stalemate", "ongoing"
    """

    # Check rows for winner
    for row in range(3):
        if game_board[row][0] == marker and game_board[row][1] == marker and game_board[row][2] == marker:
            return "winner"

    # Check columns for winner
    for col in range(3):
        if game_board[0][col] == marker and game_board[1][col] == marker and game_board[2][col] == marker:
            return "winner"

    # Check diagonals for winner
    if (game_board[0][0] == marker and game_board[1][1] == marker and game_board[2][2] == marker) or \
            (game_board[2][0] == marker and game_board[1][1] == marker and game_board[0][2] == marker):
        return "winner"

    # Check for stalemate
    if " " not in set(x for y in game_board for x in y):
        return "stalemate"

    # Otherwise we're still going
    return "ongoing"


def set_replay(status, p1_turn):
    """

    Based on win or stalemate see if they want to continue with a new game

    Parameters
    ----------
    status : str
        "winner" or "stalemate

    p1_turn : bool
        If it's player 1's turn

    Returns
    -------
    again : bool
        Whether to play again or quit
    """

    if status == "winner":
        print("Congratulations Player {}, YOU'VE WON!!!".format(get_player(p1_turn)))
    else:
        print("Dang, it's a stalemate!")

    again = input("Would you like to play again? Y or N: ")
    while not (again.upper() == "Y" or again.upper() == "N"):
        print("C'mon player, that's not a valid answer!")
        again = input("\tWould you like to play again? Y or N: ")

    return True if again.upper() == "Y" else False


def get_player(p1_turn):
    """
    Return the string of which player is up

    Parameters
    ----------
    p1_turn : bool
        If it's player 1's turn

    Returns
    -------
    player : str
        "1" or "2" depending on whose turn it is
    """
    return "1" if p1_turn else "2"


def reset_game(p1_turn):
    """
    Reset the game_board and who goes first (opposite of who went first last time).

    Parameters
    ----------
    p1_turn : bool
        Whether or not it is player 1's turn

    Returns
    -------
    game_board : list
        Reset game_board to initial status

    p1_turn : bool
        Whether or not it is player 1's turn
    """

    return board.init_board(), not p1_turn
