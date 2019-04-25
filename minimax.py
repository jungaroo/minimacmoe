import numpy as np
from gametree import GameTree, GameNode
import pickle


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
    
        if (node.depth % 2) == 1: # Odd depth is for computer's turn
            score = max_score
        elif (node.depth % 2) == 0: # Even depth for human's turn
            score = min_score
        return score


PICKLE_FILE = "gametree.obj"

def build_minimax_tree():
    """Function to be only run once, in order to build the full minimax tree. """
    grid = list(range(9))
    tree = GameTree(move=None, grid=grid)
    minimax(tree.root)
    return tree

def save_minimax_tree_to_pickle(tree):
    """Saves the tree to a pickle file """
    print("Dumping the minimax tree into a pickle file. ")
    with open(PICKLE_FILE, "wb") as pickle_file:
        pickle.dump(tree, pickle_file, pickle.HIGHEST_PROTOCOL) 
    
    print("Done dumping")

def load_minimax_tree_from_pickle():
    """Loads the minimax tree from the pickle file"""
    with open(PICKLE_FILE, "rb") as pickle_file:
        robot = pickle.load(pickle_file) 
    print("Done loading")
    return robot

robot = load_minimax_tree_from_pickle()
# robot = GameTree(move=None, grid=['X','X','X','O','O',,'X',7,8])


