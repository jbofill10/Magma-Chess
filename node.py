class Node:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.reward = 0
        self.children = []
        self.parent = parent
        self.visits = 1
        self.move = move
        self.expanded = False

    def add_child(self, move, state, parent):
        child = Node(move=move, state=state, parent=parent)

        self.children.append(child)

        return child

    def is_expanded(self):
        return self.expanded
