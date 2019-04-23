
/** Class to represent the Tic Tac Toe game state. **/
class TicTacToe {
   
  /** Constructs the TicTacToe board, a 1D array with its elements as indice as available spots.
    * @params
    * human : string ('X' or 'O')
    * robot : string ('X' or 'O')
  */
  constructor(human, robot) {
    this.board = [0, 1, 2, 3, 4, 5, 6, 7, 8]; // Indices of the 3x3 
    
    // Strings for the symbols for human and count
    this.human = human; 
    this.robot = robot;

    // Count for ties
    this.turnCount = 0;

    this.checkForWin = this.checkForWin.bind(this);
    this.isTied = this.isTied.bind(this);
  }

  /** Returns whether or not someone has played at this position.
   * @params
   * index - just an int
   */
  hasNotPlayed(index) {
    return !isNaN(this.board[index])
  }

  /** Plays the mark at that position.
   * @params
   * index - and int of the index
   * player - string of either 'X' or 'O'
   */
  markPlayed(index, player) {
    this.board[index] = player;
    this.turnCount++;
  }

  /** Checks the board for the winner.
   * @params
   * winner: string of either 'X' or 'O'
   */
  checkForWin(winner) {

    let winPositions = [[0,1,2], [3,4,5], [6,7,8],  // row wins
                        [0,3,6], [1,4,7], [2,5,8],  // column wins
                        [0,4,8], [2,4,6]] // diagonal wins
                            
    return winPositions.some(positions => positions.every((i) => this.board[i] === winner));
  
  }

  isTied() {
    return this.turnCount === 9;
  }

  getAvailable() {
    let avails = this.board.filter((item)=>!isNaN(item));
    return avails;
  }
}
