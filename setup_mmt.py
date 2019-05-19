"""Module for setting up pickle file for the tree
Run as a script to rebuild the pickle """

from minimaxtree.gametree import GameTree
from minimaxtree.minimax import minimax, prune
import pickle

PICKLE_FILE = "./tree_pickles/gametree_prune.obj"

def build_minimax_tree():
    """Function to be only run once, in order to build the full minimax tree. """
    grid = list(range(9))
    tree = GameTree.create_game_tree(grid)
    minimax(tree.root)
    return tree

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

if __name__ == "__main__":

    print("Attempting to rebuild the gametree from beginning. ")
    answer = input("Would you like to overwrite the current pickle file? [y/n]")
    while answer not in 'yn':
        answer = input("Would you like to overwrite the current pickle file? [y/n]")
    
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