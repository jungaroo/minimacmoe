#! ../venv/bin/python

import unittest
from gametree import ROBOT_O, HUMAN_X
from gametree import GameTree, GameNode


class TestGameNodeMethods(unittest.TestCase):

    def test_player_wins(self):
        """Check if player_wins method is working """

        # Horizontal human match
        board1 = ['X', 'X', 'X',
                  'O', 'O', 5,
                  6, 'O', 8]
                  
        board1_node = GameNode(move=None, grid=board1)
        self.assertTrue(board1_node.player_won(HUMAN_X))
        self.assertFalse(board1_node.player_won(ROBOT_O))

        # Diagonal robot match
        board2 = ['O', 'X', 'X',
                  3, 'O', 5,
                  6, 'X', 'O']

        board2_node = GameNode(move=None, grid=board2)
        self.assertTrue(board2_node.player_won(ROBOT_O))
        self.assertFalse(board2_node.player_won(HUMAN_X))

    def test_about_to_win(self):
        """Test if it can succesfully detect if any player is about to win in the next move """

        board1 = ['X', 1, 'X',
                  'O', 4, 'O',
                  6, 7, 8]

        board1_node = GameNode(move=None, grid=board1)
        self.assertTrue(board1_node.about_to_win(ROBOT_O))
        self.assertTrue(board1_node.about_to_win(HUMAN_X))

        board2 = ['X', 1, 'X',
                  'O', 'X', 'O',
                  6, 7, 8]

        board2_node = GameNode(move=None, grid=board2)
        self.assertFalse(board2_node.about_to_win(ROBOT_O))
        self.assertTrue(board2_node.about_to_win(HUMAN_X))

        board3 = ['X', 'O', 'X',
                  3, 4, 'O',
                  6, 7, 8]

        board3_node = GameNode(move=None, grid=board3)
        self.assertFalse(board3_node.about_to_win(ROBOT_O))
        self.assertFalse(board3_node.about_to_win(HUMAN_X))

    # Test the basic methods

    def test_is_leaf(self):
        """Tests if the leaf is working properly """

        kwargs = {
            "move": None,
            "grid": None
        }

        node = GameNode(**kwargs)
        self.assertTrue(node.is_leaf())

        node_with_children = GameNode(
            **kwargs, children={1: GameNode(**kwargs), 2: GameNode(**kwargs)})
        self.assertFalse(node_with_children.is_leaf())

    def test_is_tied(self):
        """Tests to see if ties are detected correctly """

        board1 = ['X', 'X', 'O',
                  'O', 'O', 'X',
                  'X', 'O', 'X']

        self.assertTrue(GameNode(move=None, grid=board1).is_tied())

        board1[3] = 'X'  # Make the X win
        self.assertFalse(GameNode(move=None, grid=board1).is_tied())

        board1[3] = 3  # Make the board not yet complete
        self.assertFalse(GameNode(move=None, grid=board1).is_tied())

    def test_get_available_positions(self):
        """Tests to see if available positions function correctly gets the moves """

        board1 = ['X', 'O', 'X',
                  3, 4, 'O',
                  6, 7, 8]

        avail = [3, 4, 6, 7, 8]
        self.assertEqual(
            GameNode(move=None, grid=board1).get_available_positions(), avail)

        # No moves left:
        board1 = ['X', 'O', 'X',
                  'O', 'X', 'O',
                  'X', 'O', 'X']

        self.assertListEqual(
            GameNode(move=None, grid=board1).get_available_positions(), [])

    def test_make_moves(self):
        """Tests to see if it makes moves correctly, and alternates correctly"""

        board1 = list(range(9))
        start_node = GameNode(move=None, grid=board1)
        second_node = GameNode.make_next_move_node(start_node, 1)
        self.assertListEqual(second_node.grid, [0, 'X', 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(second_node.depth, 1)

        third_node = GameNode.make_next_move_node(second_node, 2)
        self.assertListEqual(third_node.grid, [0, 'X', 'O', 3, 4, 5, 6, 7, 8])
        self.assertEqual(third_node.depth, 2)


class TestGameTreeMethods(unittest.TestCase):

    def test_create_game_tree(self):
        """Check if it builds trees correctly """

        board1 = ['O', 'X', 'X',
                  3, 'O', 5,
                  6, 'X', 'O']

        # player won, so it should not have any children
        tree = GameTree.create_game_tree(board1)
        self.assertDictEqual(tree.root.children, {})

        # Should have four children
        board2 = ['O', 'X', 'X',
                  3, 'O', 5,
                  6, 'X', 8]

        tree2 = GameTree.create_game_tree(board2)
        self.assertListEqual([3, 5, 6, 8], list(tree2.root.children.keys()))

        # Check if traversing deeper is good
        tree_node3 = tree2.root.children[3]
        self.assertListEqual([5, 6, 8], list(tree_node3.children.keys()))

        tree_node4 = tree_node3.children[6]
        self.assertListEqual([5, 8], list(tree_node4.children.keys()))

        tree_node5 = tree_node4.children[8]
        self.assertListEqual([5], list(tree_node5.children.keys()))

        terminal_node = tree_node5.children[5]
        self.assertListEqual([], list(terminal_node.children.keys()))

    def test_terminal_node_scoring(self):
        """Test if the scoring base cases work correctly """
        board1 = ['O', 'X', 'X',
                  'X', 'O', 'O',
                  'O', 'X', 'X']

        # tie
        tree = GameTree.create_game_tree(board1)
        self.assertEqual(tree.root.score, 0)

        # human win
        board1[0] = 'X'
        tree = GameTree.create_game_tree(board1)
        self.assertEqual(tree.root.score, -1)

        # robo win
        board1[0] = 'O'
        board1[3] = 'O'
        tree = GameTree.create_game_tree(board1)
        self.assertEqual(tree.root.score, 1)


if __name__ == "__main__":
    unittest.main()
