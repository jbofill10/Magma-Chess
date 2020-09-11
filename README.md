# Magma-Chess
Chess AI using supervised learning techniques

# How it works
* Converted many FIDE games + other games (On the board and online) from Elos > 2000 into a numerical 7x8x8 3D matrix representation of the board with the 9th column used to represent who's turn it is. 

* Using python-chess for chess game state

* Get's softmax evaluation for which move/lines out of all legal moves is best

# Model's Decision Making Process
* Python-chess get's all possible legal moves and uses them to create an expansion in the Monte Carlo Tree Search
* The Policy network will evaulate these lines to a certain depth which will in turn lead to a move being made
