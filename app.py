from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask import jsonify
from minimax import robot

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
CURRENT_NODE = robot.root

@app.route("/")
def home():
  """Routing for the home page. """
  
  # Refresh the CURRENT_NODE to be back 
  global CURRENT_NODE
  CURRENT_NODE = robot.root
  return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
  """Routing to receive the human's move """

  human_move = int(request.form['human_move'])
  process_move(human_move)
  robot_move = getRobotPlay(human_move)
  process_move(robot_move)
  return jsonify({"robot_move": robot_move})
  
def getRobotPlay(human_move, minnie=True):
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