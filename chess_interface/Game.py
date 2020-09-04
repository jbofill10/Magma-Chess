import chess


class ChessGame:
    board = None
    prev_turn = None

    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        self.prev_turn = 'white' if self.board.turn == chess.WHITE else 'black'
        self.board.push_san(move)
        print(self.prev_turn)

    def get_legal_moves(self):
        return list(self.board.legal_moves)

    def is_game_over(self):
        if self.board.is_stalemate() or self.board.can_claim_threefold_repetition() or self.board.can_claim_draw():
            return 0.5

        elif self.board.is_game_over(claim_draw=False):

            if self.prev_turn == 'white':
                return 1

            else:
                return -1

    def show_board(self):
        print(self.board)

    def get_fen(self):
        return self.board.fen()