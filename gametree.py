from typing import List
from player import Player, Robot, Human
from player import ROBOT_O, HUMAN_X


class GameTree:
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

            assert len(curr.children) == len(curr.getAvailablePositions())
            for child_node in curr.children:
                GameTree._populate_game_tree(child_node)

    def display(self):
        def display_helper(curr):

            if curr.isLeaf():
                return
            else:
                # print(' ' * curr.depth, curr.grid, sep='')
                for child in curr.children:
                    if child.playerWon(HUMAN_X):
                        print(' ' * child.depth, "HUMAN", child.grid)
                    elif child.playerWon(ROBOT_O):
                        print(' ' * child.depth, "ROBOT", child.grid)
                    elif child.isTied():
                        print(' ' * child.depth, "TIED", child.grid)
                    else:
                        pass
                        # print(' ' * child.depth, child.grid, sep='')
                    display_helper(child)
        display_helper(self.root)

class GameNode:

    win_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # row wins
                     [0, 3, 6], [1, 4, 7], [2, 5, 8],  # column wins
                     [0, 4, 8], [2, 4, 6]]  # diagonal wins

    mark_score = {  # Scoring system
        ROBOT_O: 1,
        HUMAN_X: -1,
    }

    def __init__(self, move: int, grid: List, children=None, depth: int = 0):
        """ Move is the most recently played move to get to that Node. """
        self.score = None
        self.move = move # Move played to get to this spot 
        self.grid = grid # [0, 1, 2 ... 8]
        self.children = children if children else []
        self.depth = depth # Also the turn count


        self.max_move = None
        self.min_move = None

    def playerWon(self, player: Player):
        """Returns whether the player won """

        def three_in_a_row(indices): return all(
            self.grid[i] == player for i in indices)
        return any(three_in_a_row(indices) for indices in GameNode.win_positions)

    def aboutToWin(self, player: Player):
        """Returns whether someone is about to win """
        def score(
            spot): return GameNode.mark_score[spot] if spot in mark_score else 0

        def two_and_free(indices):
            """Player wins if it sums to 2, robot wins if it sums to -2 """
            total_score = sum([score(self.grid[i]) for i in indices])
            return abs(total_score) == 2

        return any(two_and_free(indices) for indices in win_positions)

    def isLeaf(self):
        return not self.children  # No children

    def isTied(self):
        return all(type(pos) != int for pos in self.grid)

    def setScore(self, score):
        self.score = score

    def getAvailablePositions(self):
        return [position for position in self.grid if position not in ['O', 'X']]

    def make_move(self, move):
        next_grid = self.grid[:]
        assert type(next_grid[move]) == int
        next_grid[move] = ROBOT_O if self.depth % 2 == 1 else HUMAN_X
        return next_grid

    def __repr__(self):
        b = self.grid
        board = f"""{b[0]} {b[1]} {b[2]}\n{b[3]} {b[4]} {b[5]}\n{b[6]} {b[7]} {b[8]}"""
        return f"{board}\n c={len(self.children)}"


if __name__ == "__main__":
    s = GameNode(move=None, grid=[0,1,2,'X',4,5,6,7,8])
    print(s)