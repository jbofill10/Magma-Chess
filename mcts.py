from node import Node
import copy, random, math


class MonteCarloTreeSearch:

    def __init__(self, board, depth=5):
        self.board = board
        self.tree = Node(state=board)
        self.depth = depth

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
        reward = random.uniform(0.00, 1.00)

        self.back_propagate(child, reward)
        self.simulate(child, temp_board, depth - 1)

        node.reward += reward

    def back_propagate(self, node, reward):
        node.reward += reward

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

        return str(overall_best_node.move)
