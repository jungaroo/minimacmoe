import numpy as np
from gametree import GameTree, GameNode
import pickle


def minimax(node):
    """Minimax algorithm. Store both min and move for every level for two versions of the robot. """
    if node.score is not None:  # hit a leaf
        return node.score
    else:
        scores = [minimax(child) for child in node.children.values()]

        min_score = min(scores)
        max_score = max(scores)

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
    



def save_minimax_tree_to_pickle(tree):
    """Saves the tree to a pickle file """
    print("Dumping the minimax tree into a pickle file. ")
    with open(PICKLE_FILE, "wb") as pickle_file:
        pickle.dump(tree, pickle_file, pickle.HIGHEST_PROTOCOL) 
    
    print(f"Done dumping to '{PICKLE_FILE}'")

def load_minimax_tree_from_pickle():
    """Loads the minimax tree from the pickle file"""
    with open(PICKLE_FILE, "rb") as pickle_file:
        robot = pickle.load(pickle_file) 
    print("Done loading")
    return robot

PICKLE_FILE = "gametree_prune.obj"

if __name__ == "__main__":

    print("Attempting to rebuild the gametree from beginning. ")
    answer = input("Would you like to overwrite the current pickle file? [y/n]")
    while answer not in 'yn':
        input("Would you like to overwrite the current pickle file? [y/n]")
    
    if answer == 'y':
        
        print("Beginning to build the tree... ")
        tree = build_minimax_tree()
        print("Done builing! Starting the prune")
        prune(tree.root)
        print("Done pruning! Now saving...")
        save_minimax_tree_to_pickle(tree)
    else:
        import sys
        sys.exit()



