
class TicTacToe {
  /** Human is a human object, Robot is the robot class */
  constructor(human, robot) {
    this.board = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    this.human = human; // i.e. 'O' or 'X
    this.robot = robot;
    this.turnCount = 0;

    this.checkForWin = this.checkForWin.bind(this);
    this.isTied = this.isTied.bind(this);
  }

  hasNotPlayed(row, col) {
    let index = this.coords2Idx(row, col);
    return !isNaN(this.board[index])
  }

  play(row, col, player) {
    let index = this.coords2Idx(row, col);
    this.board[index] = player.symbol;
    this.turnCount++;
  }

  coords2Idx(row, col) {
    return row * 3 + col;
  }

  idx2coors(i) {
    let row = Math.floor(i/3);
    let col = i % 3;
    return [row, col];
  }

  computerPlays() {
    let [row, col] = this.robot.analyzeAndPlay(this);
    this.play(row, col, this.robot);
    return [row, col];
  }

  checkForWin(bo) {
    let human = this.human;
    let robot = this.robot;
    let b = (bo === undefined) ? this.board : bo; // Option to call as argument

    let winPositions = [[0,1,2], [3,4,5], [6,7,8],  // row wins
                        [0,3,6], [1,4,7], [2,5,8],  // column wins
                        [0,4,8], [2,4,6]] // diagonal wins
    let someoneWon = winPositions.some(function(positions) {
      let humanWon = positions.every((i) =>  b[i] === human.symbol);
      let robotWon = positions.every((i) => b[i] === robot.symbol);
      return humanWon || robotWon;
    });

    return someoneWon;
  }

  getAvailablePositions(other) {
    let brd = (other === undefined) ? this.board : other;
    return brd.filter((item) => {
      return !isNaN(item);
    });
  }

  isTied() {
    return this.turnCount == 9;
  }
}

class Player {
  constructor(symbol) {
    this.symbol = symbol;
  }
}

class Human extends Player {
  constructor(symbol) {
    super(symbol);
  }
}

class Robot extends Player {
  constructor(symbol) {
    super(symbol);
  }

  analyzeAndPlay(game) {
    // Get available indices
    let possiblePositions = game.getAvailablePositions();
    let randIdx = Math.floor(Math.random() * possiblePositions.length);
    return game.idx2coors(possiblePositions[randIdx]);
  }
}