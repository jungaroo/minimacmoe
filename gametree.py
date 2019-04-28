from typing import List

ROBOT_O = 'O'
HUMAN_X = 'X'

class GameTree:
    """Class to represent the entire game tree of 9! moves """
    
    def __init__(self, root: 'GameNode'):
        self.root = root

    @classmethod
    def create_game_tree(cls, grid=None):
        """Class method to create the gametree from the passed in grid as the root. """
        
        if grid is None:
            grid = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        root = GameNode(move=None, grid=grid)
        tree = cls(root)
        tree._populate_game_tree(tree.root)
        return tree

    @staticmethod  #
    def _populate_game_tree(curr: 'GameNode'):
        """ Builds the entire game tree """
        if curr.player_won(ROBOT_O):
            curr.set_score(1)
        elif curr.player_won(HUMAN_X):
            curr.set_score(-1)
        elif (curr.is_tied()):
            curr.set_score(0)
        elif curr.depth > 8:
            return
        else:
            # Create all the children (all moves)
            for move in curr.get_available_positions():
                child = GameNode.make_next_move_node(curr, move)
                curr.children[move] = child
                GameTree._populate_game_tree(child)

            # # Populate the rest of the children
            # for child_node in curr.children:
            #     GameTree._populate_game_tree(child_node)

class GameNode:
    """GameNode for minimax functions """

    win_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # row wins
                     [0, 3, 6], [1, 4, 7], [2, 5, 8],  # column wins
                     [0, 4, 8], [2, 4, 6]]  # diagonal wins

    mark_score = {  # Scoring system
        ROBOT_O: 1,
        HUMAN_X: -1,
    }

    def __init__(self, move: int, grid: List, children=None, depth: int = 0):
        """ Move is the most recently played move to get to that Node. """
        self.score = None # Score for this node (if it is terminal)
        self.move = move # Move played to get to this spot 
        
        self.grid = grid # [0, 1, 2 ... 8]
        self.children = children if children else {}
        self.depth = depth # Also the turn count

        # Minimax moves
        self.max_move = None
        self.min_move = None

    def player_won(self, player):
        """Returns whether the player won """

        three_in_a_row = lambda indices : all(self.grid[i] == player for i in indices)

        return any(three_in_a_row(indices) for indices in GameNode.win_positions)

    def about_to_win(self, player):
        """Returns whether someone is about to win """
        
        get_score = lambda spot : GameNode.mark_score[spot] if spot in GameNode.mark_score else 0

        def two_and_free(indices):
            """Player wins if it sums to 2, robot wins if it sums to -2 """
            total_score = sum(get_score(self.grid[i]) for i in indices)
            return total_score == 2 * GameNode.mark_score[player] # -2 if robot, +2 if human

        return any(two_and_free(indices) for indices in GameNode.win_positions)

    def is_leaf(self):
        """Returns whether a node is a leaf node without any children """

        return not self.children 

    def is_tied(self):
        """ Returns whether a board is a tie or not """

        robot_won = self.player_won(ROBOT_O)
        human_won = self.player_won(HUMAN_X)
        board_is_filled = all(type(pos) != int for pos in self.grid)
        # Neither player/robot won and board is full
        return not (robot_won or human_won) and board_is_filled

    def set_score(self, score):
        """Sets the score for that node """
        
        self.score = score


    def get_available_positions(self):
        """Returns all the available positions that can be played as a list """

        return [position for position in self.grid if position not in ['O', 'X']]

    @classmethod
    def make_next_move_node(cls, current_node, move):
        """Makes a move on that board, returning the new GameNode based off that move """

        next_grid = current_node.grid[:]
        next_grid[move] = ROBOT_O if current_node.depth % 2 == 1 else HUMAN_X
        return cls(move=move, grid=next_grid, depth=current_node.depth + 1)

    def __str__(self):
        """User friendly print of the board """

        b = self.grid
        board = f"""{b[0]} {b[1]} {b[2]}\n{b[3]} {b[4]} {b[5]}\n{b[6]} {b[7]} {b[8]}"""
        return f"{board}\n c={len(self.children)}"

    def __repr__(self):
        """Object information representation """

        return f"<GameNode @ {self.grid}. Depth: {self.depth}>"
