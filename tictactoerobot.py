from setup_mmt import load_minimax_tree_from_pickle

class TicTacToeRobot:
  """Class for the Robot that uses minimax algorithm. 
  The root of the entire tree is saved across all classes. 

  Each instance of a robot stores the history of moves used to traverse the tree.
  History of moves can be serialized and saved as a cookie.
  """
  
  minimax_root = load_minimax_tree_from_pickle().root

  def __init__(self, history):
    self.history = history
  
  
  def get_robots_move(self, human_move: int):
    """Takes in human_move (int), and returns robots corresponding move"""
    
    self.history.append(human_move)
    curr_node = self.traverse()
    robot_move = curr_node.max_move
    self.history.append(robot_move)
    return robot_move
      

  def traverse(self):
    """Traverses to the final node based on the history. """

    curr_node = TicTacToeRobot.minimax_root
    for move in self.history:
        curr_node = curr_node.children[move]
     
    return curr_node

  def is_valid_history(self, client_history):
    return self.history == client_history











