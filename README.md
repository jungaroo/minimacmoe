# Mini Mac Moe
Combination of Tic Tac Toe and minimax. The "chat" thing is just a randomly generated [Markov Text Chain](https://en.wikipedia.org/wiki/Markov_chain)

Deployment:
https://minimacmoe.herokuapp.com/battle

# To develop/test
```
pip3 install -r requirements.txt
flask run
```
Unit tests
```
python3 -m unittest discover
```

# About
Built in Python and JS.
flask, jQuery, AJAX

The robot is actually unbeatable! The entire game tree is built with the minimax algorithm, and pruned for only the robot's optimal moves. 

