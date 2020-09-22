# Magma-Chess
Chess AI using supervised learning techniques

# How it works
* Converted many FIDE games + other games (On the board and online) from Elos > 2000 into a numerical 7x8x8 3D matrix representation of the board with the 9th column used to represent who's turn it is. 

* Using python-chess for chess game state

* Get's softmax evaluation for which move/lines out of all legal moves is best

# How it learns
* Learns by classifying whether that position is winning or not

# Model's Decision Making Process
* Python-chess get's all possible legal moves and uses them to create an expansion in the Monte Carlo Tree Search
* MCTS' "terminal node" in this case is a 18 deep node, since actually reaching a terminal state in a real chess game is too large of a search.
* MCTS iterates 200 times before deciding on the best move
* The Policy network will evaulate each move within the mcts tree and have the values backpropogated up to the first layer of child nodes.

# NN Architecture
* Convolutional Layer:
  * Filters: 256
  * Kernel Size: 3x3
* Convolutional Layer:
  * Filters: 256
  * Kernel Size: 3x3
* Flattening Layer
* Dense Layer:
  * Softmax Output of 3 classes
