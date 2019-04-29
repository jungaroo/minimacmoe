$(function () {

  // Cache common buttons
  const $board = $("#board");
  const $cardBody = $(".card-body");
  const $game = $("#game");
  const $mmmImage = $("#mmm-image");
  const $trashTalk = $("#trash-talk");
  const $squares = $(".square");

  // Global positioning constants
  const [HUMAN, ROBOT] = ['X', 'O'];
  const RANDOM_MESSAGES = [
    "O_o",
    ":-]",
    "HAHAHA!",
    "uhhhhh...",
    "PFFFFT!",
    "AAAAAAAAAAAAAHHHH",
    "durrrrr",
    "LOOOOOSERR"
  ];

  let GAME_STARTED = false;

  let game = new TicTacToe(HUMAN, ROBOT);

  // Event listeners
  $cardBody.on("click", ".fight", function () {
    if (!GAME_STARTED) { // Start if not started
      $game.slideToggle();
      GAME_STARTED = true;
      $(this).text("Restart");
    } else { // Restart if did
      window.location.reload();
    }
  })


  // Sending over a move to the server.
  $board.on("click", ".square", async function () {

    // Check if the move is playable
    let idx = $(this).index();
    if (!game.hasNotPlayed(idx) || game.gameOver) return;

    // Send the move to server, with the game history for validation
    let response = await playToServer(idx, game.history)

    if (response.robot_move !== undefined) {

      game.markPlayed(idx, HUMAN);
      updateUIPlay(idx, HUMAN);

      game.markPlayed(response.robot_move, ROBOT);
      updateUIPlay(response.robot_move, ROBOT);
    } else {
      window.location.reload();
    }

    let winningPositions = game.checkForWin(ROBOT);
    if (winningPositions) {
      highlightWin(winningPositions);
      endGame();
    } else if (game.isTied()) {
      endGame();
    }

  });

  /** Updates the UI for play */
  function updateUIPlay(idx, player) {

    let mark = (player === 'X') ? "../static/img/X.png" : "../static/img/O.png";
    $board.children(`:nth-child(${idx + 1})`).html($(`<img src="${mark}">`));

    if (player === 'X') {
      let n = Math.floor(Math.random() * 6);
      $mmmImage.attr('src', `../static/img/minmacmoe/mmm${n}.PNG`);
      $trashTalk.text(RANDOM_MESSAGES[n]);
    }
  }


  /** Sends a play to server */
  async function playToServer(human_move, client_history) {

    let data = {
      human_move: human_move,
      client_history: JSON.stringify(client_history)
    }
    let response = await $.post('/move', data);
    return response;
  }

  function endGame() {
    $mmmImage.attr('src', `../static/img/minmacmoe/loser.PNG`);
    $trashTalk.text(RANDOM_MESSAGES[7]);
    game.gameOver = true;
  }

  function highlightWin(winningPositions) {
    // Find out win position
    console.log(winningPositions);
    for (let i of winningPositions) {
      $squares.eq(i).css("background-color", "red");
    }

  }


});