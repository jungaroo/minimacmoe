$( function() {

  // Cache common buttons
  const $board = $("#board");
  const $cardBody = $(".card-body");
  const $game = $("#game");
  const $mmmImage = $("#mmm-image");
  const $trashTalk = $("#trash-talk");

  // Global positioning constants
  const [HUMAN, ROBOT] = ['X', 'O'];
  const TRASH_TALK = [
    "....",
    "HAHAHA",
    "What kinda move is that?",
    "Oh, you're in big trouble",
    "WHAT IS THAT",
    "hmmm....",
    "WOW!",
    "LOOOOOSERR"
  ]

  let game = new TicTacToe(HUMAN, ROBOT);
  
  // Event listeners
  $cardBody.on("click", ".fight", function() {
    $game.slideToggle();
  })

  // Sending over a move to the server.
  $board.on("click", ".square", async function() {
    
    // Check if the move is playable
    let idx = $(this).index();
    if (!game.hasNotPlayed(idx) || game.gameOver) return;
  
    // Process that human played
    game.markPlayed(idx, HUMAN);
    updateUIPlay(idx, HUMAN);
    console.log("You play:", idx);

    let response = await playToServer(idx, "minnie")
    if (response.robot_move !== undefined) {
      console.log("Robot: ", response.robot_move)
      game.markPlayed(response.robot_move, ROBOT);
      updateUIPlay(response.robot_move, ROBOT);
    } else {
      console.log("server didn't get a robot move");
      console.log(response);
    }

    if (response.winner) {
      endGame();
    }
    
  });

  /** Updates the UI for play */
  function updateUIPlay(idx, player) {

    let mark = (player === 'X') ? "../static/img/X.png" : "../static/img/O.png";
    $board.children(`:nth-child(${idx+1})`).html($(`<img src="${mark}">`)); 

    if (player === 'X') {
      let n = Math.floor(Math.random() * 8 + 1);
      $mmmImage.attr('src', `../static/img/minmacmoe/mmm${n}.PNG`);
      $trashTalk.text(TRASH_TALK[n-1]);
    }
  }


  /** Sends a play to server */
  async function playToServer(human_move, option) {

    let response = await $.post('/move', {
      human_move : human_move,
      option : option
    });
    return response;
  }

  function endGame() {
    $mmmImage.attr('src', `../static/img/minmacmoe/loser.PNG`);
    game.gameOver = true;
  }

  
});