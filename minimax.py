import numpy as np
from gametree import GameTree, GameNode


def minimax(node):
    """minimax"""
    if node.score is not None:  # hit a leaf
        return node.score
    else:
        scores = [minimax(child) for child in node.children]

        min_score = min(scores)
        max_score = max(scores)

        moves = node.getAvailablePositions()
        node.min_move = moves[np.argmin(scores)]
        node.max_move = moves[np.argmax(scores)]
    
        if (node.depth % 2) == 1:
            score = max_score
        elif (node.depth % 2) == 0:
            score = min_score
        return score

# grid = list(range(9))
# grid = ['X', 'X', 'X', 3, 4, 5, 'O', 'O', 'O']

# tree = GameTree(move=None,grid=grid)
# minimax(tree.root)

# robot = tree

# print(tree.root)
# print(tree.root.children[0], tree.root.children[1], sep='\n\n')
import pickle
# with open("gametree.obj", "wb") as pickle_file:
#     pickle.dump(tree, pickle_file, pickle.HIGHEST_PROTOCOL) 
#     print("done dumping")

with open("gametree.obj", "rb") as pickle_file:
    robot = pickle.load(pickle_file) 
    print("done loading")



