from mcts import MonteCarloTreeSearch
from chess_interface.Game import ChessGame
import sys


def game():

    board = ChessGame()
    board.show_board()
    player_color = 1 if sys.argv[1] else 0
    while not board.is_game_over():
        if board.curr_turn() == player_color:
            # move = input(f"Enter a move as {'White' if board.curr_turn() else 'Black'}: ")
            move='e4'
            try:
                # print(chr(27) + "[2J")
                board.make_move(move)
                board.show_board()
            except Exception as error:
                print("Unable to make move!")
                print(error)
        else:

            move = MonteCarloTreeSearch(board, depth=18).run_mcts(50)
            # print(chr(27) + "[2J")
            board.make_move(move, format='uci')
            board.show_board()
            sys.exit(0)


if __name__ == '__main__':
    game()
