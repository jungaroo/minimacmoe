from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask import jsonify
from minimax import robot

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
currentNode = robot.root

@app.route("/")
def home():
  global currentNode
  currentNode = robot.root
  return render_template("index.html")

@app.route("/move", methods=["POST"])
def player():
  player_move = int(request.form['player_move'])
  move = getRobotPlay(player_move)
  return jsonify({"robot_move": move})
  
def getRobotPlay(player_move):
  global currentNode

  # Process player's move
  print("Player plays:", player_move)
  print("Here are the valid moves:", [child.move for child in currentNode.children])
  for i, child in enumerate(currentNode.children):
    if child.move == player_move:
      currentNode = currentNode.children[i]
      break
  
  computer_move = currentNode.max_move 
  print("Robot plays:", computer_move)
  # Process our move
  for i, child in enumerate(currentNode.children):
    if child.move == computer_move:
      currentNode = currentNode.children[i]
  print("Here are the valid moves:", [child.move for child in currentNode.children])

  return computer_move

    
