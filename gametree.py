from typing import List

ROBOT_O = 'O'
HUMAN_X = 'X'

class GameTree:
    """Class to represent the entire game tree of 9! moves """
    def __init__(self, move, grid):
        self.root = GameNode(move=move, grid=grid)
        GameTree._populate_game_tree(self.root)

    @staticmethod  # Private
    def _populate_game_tree(curr: 'GameNode'):
        """ Builds the entire game tree """
        if curr.playerWon(ROBOT_O):
            curr.setScore(1)
        elif curr.playerWon(HUMAN_X):
            curr.setScore(-1)
        elif (curr.isTied()):
            curr.setScore(0)
        elif curr.depth > 8:
            return
        else:
            # Create all the children (all moves)
            for move in curr.getAvailablePositions():
                next_grid = curr.make_move(move)
                child = GameNode(move=move, grid=next_grid, children=[], depth=curr.depth+1)
                curr.children.append(child)

            # Populate the rest of the children
            for child_node in curr.children:
                GameTree._populate_game_tree(child_node)

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
        self.children = children if children else []
        self.depth = depth # Also the turn count

        # Minimax moves
        self.max_move = None
        self.min_move = None

    def playerWon(self, player):
        """Returns whether the player won """

        def three_in_a_row(indices): return all(
            self.grid[i] == player for i in indices)
        return any(three_in_a_row(indices) for indices in GameNode.win_positions)

    def aboutToWin(self, player):
        """Returns whether someone is about to win """
        def score(
            spot): return GameNode.mark_score[spot] if spot in mark_score else 0

        def two_and_free(indices):
            """Player wins if it sums to 2, robot wins if it sums to -2 """
            total_score = sum([score(self.grid[i]) for i in indices])
            return abs(total_score) == 2

        return any(two_and_free(indices) for indices in win_positions)

    def isLeaf(self):
        return not self.children 

    def isTied(self):
        return all(type(pos) != int for pos in self.grid)

    def setScore(self, score):
        self.score = score

    def getAvailablePositions(self):
        return [position for position in self.grid if position not in ['O', 'X']]

    def make_move(self, move):
        next_grid = self.grid[:]
        assert type(next_grid[move]) == int, "That move is not valid"
        next_grid[move] = ROBOT_O if self.depth % 2 == 1 else HUMAN_X
        return next_grid

    def __repr__(self):
        """User friendly print of the board """
        b = self.grid
        board = f"""{b[0]} {b[1]} {b[2]}\n{b[3]} {b[4]} {b[5]}\n{b[6]} {b[7]} {b[8]}"""
        return f"{board}\n c={len(self.children)}"
