$(function () {

  // Choose the images
  const X_IMG = "../static/img/redx.svg.png";
  const O_IMG = "../static/img/o.svg.png";
  
  // Cache common buttons
  const $board = $("#board");
  const $mmmImage = $("#mmm-image");
  const $trashTalk = $("#trash-talk");
  const $squares = $(".square");
  const $chatForm = $("#chat-form");
  const $chatMessages = $("#chat-messages");

  // Global positioning constants
  const [HUMAN, ROBOT] = ['X', 'O'];
  let CHAT_MSG_COUNTER = 1;

  const game = new TicTacToe(HUMAN, ROBOT);

  // Event listeners
  $("#game").on("click", ".restart", function(evt) {
    evt.preventDefault();
    window.location.reload();
  });


  // Sending over a move to the server.
  $board.on("click", ".square", async function () {

    // Check if the move is playable
    let idx = $(this).index();
    if (!game.hasNotPlayed(idx) || game.gameOver) return;

    // Send the move to server, with the game history for validation
    let response = await playToServer(idx, game.history);

    if (response.robot_move !== undefined) {

      // Record player's move
      game.markPlayed(idx, HUMAN);
      updateUIPlay(idx, HUMAN);

      // Record robot's move
      game.markPlayed(response.robot_move, ROBOT);
      updateUIPlay(response.robot_move, ROBOT);
    } else {
      window.location.reload();
    }

    // Check win conditions
    checkWin();

  });
  
  function checkWin() {

    const winningPositions = game.checkForWin(ROBOT);
    if (winningPositions) {
      highlightWin(winningPositions);
      endGame();
    } else if (game.isTied()) {
      endGame();
    }
    
  }

  /** Updates the UI for play */
  function updateUIPlay(idx, player) {

    const mark = (player === 'X') ? X_IMG || "../static/img/X.png" :  O_IMG || "../static/img/O.png";
    $board.children(`:nth-child(${idx + 1})`).html($(`<img style="height: 90px; width: 90px" src="${mark}">`));

    // Change 
    if (player === 'X') changeRobotImg();
    
  }
  
  function changeRobotImg() {
    const n = Math.floor(Math.random() * 6);
    $mmmImage.attr('src', `../static/img/minmacmoe/mmm${n}.PNG`);
  }

  /** Sends a play to server */
  async function playToServer(human_move, client_history) {

    const data = {
      human_move: human_move,
      client_history: JSON.stringify(client_history)
    };
    const response = await $.post('/move', data);
    return response;
  }

  function endGame() {
    $mmmImage.attr('src', `../static/img/minmacmoe/loser.PNG`);
    $trashTalk.text(RANDOM_MESSAGES[7]);
    game.gameOver = true;
  }

  function highlightWin(winningPositions) {
    // Find out win position
    for (let i of winningPositions) {
      $squares.eq(i)
        .children(0)
        .addClass("spinner-border")
        .addClass("text-primary");
    }

  }

  $chatForm.on("submit", async function(evt) {
    evt.preventDefault();
    
    CHAT_MSG_COUNTER++;
    CHAT_MSG_COUNTER %= 5;
    if (CHAT_MSG_COUNTER === 0) $chatMessages.empty();

    const $textField = $("#btn-input");
    
    const text = $textField.val();
    const userText = $(`<li class=list-group-item"></li>`).text(`> ${text}`); // sanitize to prevent
    $chatMessages.append(userText);
    $textField.val('');

    
    const computerReply = await $.post("/chat", {text});
    const { reply } = computerReply;
    $chatMessages.append(`<li class="list-group-item-danger"><b>Mini:</b> ${reply} </li>`);
    

  });

});