ROBOT_O = 'O'
HUMAN_X = 'X'

class Player:
  def __init__(self, mark):
    self.mark = mark

class Robot(Player):
  def __init__(self):
    super().__init__(ROBOT_O)

class Human(Player):
  def __init__(self):
    super().__init__(HUMAN_X)

