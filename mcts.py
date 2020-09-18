from node import Node
from Preprocessing import convert_to_int

import copy, random, math, sys
import numpy as np
import chess

class MonteCarloTreeSearch:

    def __init__(self, board, model,depth=5):
        self.board = board
        self.tree = Node(state=board)
        self.depth = depth
        self.model = model

    def choose(self, node):
        unexplored = [child for child in node.children if not child.expanded]

        if len(unexplored) > 0:
            selected_node = random.choice(unexplored)
        else:
            ucts = [self.uct(node, child) for child in node.children]

            selected_node = node.children[ucts.index(max(ucts))]

        return selected_node

    def expand(self, board, node):
        for move in board.get_legal_moves():
            temp_board = copy.deepcopy(board)

            temp_board.make_move(str(move), format='uci')
            node.add_child(move=str(move), state=temp_board, parent=node)

    def simulate(self, node, board, depth=None):

        if depth == 0 or board.is_game_over():
            return
        temp_board = copy.deepcopy(board)

        move = random.choice(list(temp_board.get_legal_moves()))

        temp_board.make_move(str(move), format='uci')

        child = node.add_child(move=str(move), state=board, parent=node)

        # NN softmax output
        board_state = self.process_board(child, temp_board.get_pychess_board())
        prediction = self.model.predict(np.reshape(board_state, (1, 7, 8, 8)))

        if prediction.index(max(prediction)) == 0:
            reward = prediction[0]
        elif prediction.index(max(prediction)) == 1:
            reward = prediction[1]
        else:
            reward = prediction[2]

        self.back_propagate(child, reward)
        
        self.simulate(child, temp_board, depth - 1)

    def back_propagate(self, node, reward):
        if node.parent is None:
            node.reward += reward
            return
        node.reward += reward
        self.back_propagate(node=node.parent, reward=reward)

    def uct(self, parent, child):

        return (child.reward + 1) * (math.sqrt(math.log(parent.visits) / child.visits))

    def run_mcts(self, max_iter):

        self.expand(node=self.tree, board=self.board)

        for _ in range(max_iter):
            best_node = self.choose(self.tree)
            if best_node.visits != 1:
                self.expand(node=best_node, board=self.board)
                # Accounts for the node that was visited to be expanded
                # No longer "best_node" for the rest of the code block
                best_node.visits += 1

                best_node = self.choose(node=best_node)

            self.simulate(node=best_node, board=self.board, depth=self.depth)
            best_node.expanded = True
            best_node.visits += 1

            self.tree.visits += 1

        overall_best_node = self.choose(self.tree)

        print([l.reward for l in self.tree.children])

        return str(overall_best_node.move)

    def process_board(self, node, board):
        white_kcastle = False
        black_kcastle = False
        white_qcastle = False
        black_qcastle = False

        move = chess.Move.from_uci(node.move)

        if board.is_kingside_castling(move):
            if board.turn:
                white_kcastle = True
            else:
                black_kcastle = True

        if board.is_queenside_castling(move):
            if board.turn:
                white_qcastle = True
            else:
                black_qcastle = True

        return convert_to_int(board, white_kcastle, black_kcastle, white_qcastle, black_qcastle)
