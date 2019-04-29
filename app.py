from flask import Flask, request, render_template, jsonify, session
from flask import redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension

from tictactoerobot import TicTacToeRobot
from random import choice
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

HUMAN = 'X'
ROBOT = 'O'

@app.route("/")
def home():
  """Routing for the home page. """
  
  session["move_history"] = []
    
  return render_template("home.html")

@app.route("/battle")
def battle():
  """Routing for the battle arena. """
  
  session["move_history"] = []
  return render_template("battle.html")


@app.route("/move", methods=["POST"])
def move():
  """Routing to receive the human's move """

  # Build the robot from history
  robot = TicTacToeRobot(session['move_history'])

  # Grab data from the request forms
  human_move = int(request.form['human_move'])
  client_history = json.loads(request.form['client_history'])

  # If the client opened multiple tabs or is trying to cheat through the client
  if not robot.is_valid_history(client_history):
    return jsonify({"error": "invalid"})

  # Create the robot's move, and update the history
  robot_move = robot.get_robots_move(human_move)
  session['move_history'] = robot.history

  return jsonify({"robot_move": robot_move})


