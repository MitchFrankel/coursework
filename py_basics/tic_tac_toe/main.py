"""
Tic Tac Doh main game script
"""

__author__ = "Mitch Frankel"
__version__ = "0.0.0"


# Imports
import board
import game
from time import sleep as t_sleep

# My Module Imports
import sys
sys.path.append("../../common")
from jupyter_helper import clear_display


def run_game():
    not_quit = True
    p1_turn  = False                # This will make sense below for who goes first
    p1_x     = game.start_game()

    while not_quit:
        
        # Clear the display
        clear_display()

        # Initialize the game
        game_board = board.init_board()

        status = game.get_status(game_board, game.get_marker(p1_turn, p1_x))

        # Take turns until game is won or lost or quit
        while status == "ongoing":

            # Change whose turn it is
            p1_turn = not p1_turn

            # Set current marker
            marker = game.get_marker(p1_turn, p1_x)

            # Get choice positions and valid positions and move
            print("\n----------------")
            print("\nOpen Options Board:")
            move_choice = game.move(*board.get_open_pos(game_board), p1_turn)

            # Update the board
            game_board = board.update_game_board(game_board, move_choice, marker)
            
            # Clear the display
            clear_display()

            # Display the Board
            print("\nGame Board:")
            board.display_board(game_board)

            # Check if game is won or stalemate
            status = game.get_status(game_board, marker)
            if status != "ongoing":
                break

            t_sleep(1)

        # See if they want to play again
        not_quit = game.set_replay(status, p1_turn)

    print("\nSorry to see you go, but I'll enjoy watching you walk away :)")


if __name__ == "__main__":
    run_game()
