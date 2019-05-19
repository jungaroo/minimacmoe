import numpy as np
from .gametree import GameTree, GameNode
import pickle


def minimax(node):
    """Minimax algorithm. Store both min and move for every level for two versions of the robot. """
    if node.score is not None:  # hit a leaf
        return node.score
    else:
        scores = [minimax(child) for child in node.children.values()]

        min_score, max_score = min(scores), max(scores)

        moves = node.get_available_positions()
        node.min_move = moves[np.argmin(scores)]
        node.max_move = moves[np.argmax(scores)]
    
        if (node.depth % 2) == 1: # Odd depth is for computer's turn
            score = max_score
        elif (node.depth % 2) == 0: # Even depth for human's turn
            score = min_score
        return score


def build_minimax_tree():
    """Function to be only run once, in order to build the full minimax tree. """
    grid = list(range(9))
    tree = GameTree.create_game_tree(grid)
    minimax(tree.root)
    return tree


def prune(tree_node):
    """Runs once, will remove all children that is not the max or min move for
    the moves that are on the robot's turn. 
    It is 32x smaller """
    
    if tree_node.depth % 2 == 1: # robot's turn
        important = [tree_node.max_move, tree_node.min_move]
        keys = list(tree_node.children.keys())
        for i in keys:
            if i not in important:
                del tree_node.children[i]
    
    for children in tree_node.children.values():
        prune(children)