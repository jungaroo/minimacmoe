$(function() {
  const $board = $("#board");
  const $button = $(".btn");


  let human = new Human('O');
  let robot = new Robot('X');
  let game = new TicTacToe(human, robot);

  $board.on("click", ".button", function() {
    let col = $(this).index();
    let row = $(this).parent().index();

    if (game.hasNotPlayed(row, col)) {
      game.play(row, col, human);
      updatePlay(row, col, human);
      console.log(game.getAvailablePositions());
      toggleButtons();

      if (game.checkForWin()) {
        alert("You won!");
        return;
      } else if (game.isTied()) {
        alert("Tied!");
        return;
      }

      let [r, c] = game.computerPlays(row, col);
      console.log("Robot plays at", r, c);
      updatePlay(r, c, robot);

      if (game.checkForWin()) {
        alert("You lost!");
        return;
      }

      toggleButtons();
      

    } else {
      console.log("rejected", row, col);
    }

  });

  function updatePlay(row, col, player) {
    $board.children(`:nth-child(${row+1})`).children(`:nth-child(${col+1})`).text(player.symbol); ;
  }

  function toggleButtons() {
    $button.toggleClass("button");
  }


  let gameTree = new GameTree(game.board, 0);
  
  function populateGameTree(root) {

    if (game.checkForWin(root.board)) {
      return;
    }
    if (root.board.every(isNaN)) {
      return;
    }
    for (position of game.getAvailablePositions(root.board)) {
      let copyBoard = [...root.board];
      let depth = root.depth + 1;
      copyBoard[position] = (depth % 2 == 0) ? 'O' : 'X';
      root.addPosition(position);
      root.addChild(copyBoard);
    }

    for (child of root.children) {
      populateGameTree(child);
    }
  }

  populateGameTree(gameTree);
  console.log("Done iwth game tree.", gameTree);
  
});