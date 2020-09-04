from chess_interface.Game import ChessGame
import sys


def game():

    board = ChessGame()
    board.show_board()
    player_color = 1 if sys.argv[1] else 0
    while not board.is_game_over():
        print()
        if board.curr_turn() == player_color:
            move = input(f"Enter a move as {'White' if board.curr_turn() else 'Black'}: ")
            try:
                board.make_move(move)
                board.show_board()
            except Exception as error:
                print("Unable to make move!")
                print(error)
        else:
            # Pass to neural network
            pass


if __name__ == '__main__':
    game()
