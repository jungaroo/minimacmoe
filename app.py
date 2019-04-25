from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask import jsonify
from minimax import robot
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
CURRENT_NODE = robot.root
HUMAN = 'X'
ROBOT = 'O'

@app.route("/")
def home():
  """Routing for the home page. """
  
  # Refresh the CURRENT_NODE to be back 
  global CURRENT_NODE
  CURRENT_NODE = robot.root
  return render_template("home.html")

@app.route("/battle")
def battle():
  """Routing for the battle arena. """
  global CURRENT_NODE
  CURRENT_NODE = robot.root
  return render_template("battle.html")


@app.route("/move", methods=["POST"])
def move():
  """Routing to receive the human's move """

  # Grab data from the request forms
  human_move = int(request.form['human_move'])
  option = request.form['option']

  print("Server recieved:", human_move)
  # Process the move
  process_move(human_move)

  # Check if the player won (impossible btw)
  if CURRENT_NODE.player_won(HUMAN):
    return jsonify({"winner": HUMAN})

  # If not, let the robot move
  if option == "random":
    robot_move = get_random_move()
  elif option == "minnie":
    robot_move = get_robot_move(human_move)
  elif option == "maxi":
    robot_move = get_robot_move(human_move, minnie=False)
  
  # Process robot move and check if robot won
  process_move(robot_move)

  if CURRENT_NODE.player_won(ROBOT):
    return jsonify({"winner": ROBOT, "robot_move": robot_move})

  return jsonify({"robot_move": robot_move})
  
def get_robot_move(human_move, minnie=True):
  """Gets a player move and returns the move the robot will play.
  
  human_move -- An int (0 - 8), for which position the human played
  computer_move -- An int (0 - 8), for computer's play in response
  minnie -- A boolean (default True) if you want to play against Minnie (the smart robot)
  
  """
  
  global CURRENT_NODE

  process_move(human_move)
  if minnie:
    computer_move = CURRENT_NODE.max_move 
  else:
    computer_move = CURRENT_NODE.min_move

  process_move(computer_move)

  return computer_move


def process_move(move):
  """Updates the global CURRENT_NODE when the move is played. 

  move -- An int (0-8) specifying the move either the robot or human played.
  """
  global CURRENT_NODE

  for i, child in enumerate(CURRENT_NODE.children):
    if child.move == move:
      CURRENT_NODE = CURRENT_NODE.children[i]
      break

def get_random_move():
  """Selects a random choice move from the children """
  global CURRENT_NODE

  random_move_node = choice(CURRENT_NODE.children)
  return random_move_node.move

