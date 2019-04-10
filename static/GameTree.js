class GameTree {
  constructor(board, depth) {
    this.board = board; // Value at that position (the state of the board)
    this.depth = depth || 0; // Used to calculate Min vs Max
    this.children = [];
    this.prevMove = null;
  }

  isLeaf() {
    return this.children.length === 0;
  }

  addChild(board) {
    this.children.push(new GameTree(board, this.depth +1));
  }

  addPosition(position) {
    this.prevMove = position;
  }
}


