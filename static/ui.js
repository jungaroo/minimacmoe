$( function() {

  // Cache common buttons
  const $board = $("#board");
  const $button = $(".btn");
  const $carousel = $("#carouselRobots");
  const $game = $("#game");

  // Global positioning constants
  const [HUMAN, ROBOT] = ['X', 'O'];

  let game = new TicTacToe(HUMAN, ROBOT);
  
  // Event listeners
  $carousel.on("click", ".fight", function() {
    $game.slideToggle();
  })

  // Sending over a move to the server.
  $board.on("click", ".square", async function() {
    
    // Check if the move is playable
    let idx = $(this).index();
    if (!game.hasNotPlayed(idx)) return;
  
    // Process that human played
    game.markPlayed(idx, HUMAN);
    updateUIPlay(idx, HUMAN);
    toggleButtons();
    sleep(checkForWinner);

    
    // Get robot's play
    // let {robot_move} = await playToServer(idx); // Plays minimax
  
    let robot_move = playRandom();
    game.markPlayed(robot_move, ROBOT);
    
    
    sleep(updateUIPlay, robot_move, ROBOT);
    setTimeout(()=>sleep(checkForWinner, 200));


  });

  /** Updates the UI for play */
  function updateUIPlay(idx, player) {
    let mark = (player === 'X') ? "../static/img/X.png" : "../static/img/O.png";
    $board.children(`:nth-child(${idx+1})`).html($(`<img src="${mark}">`)); 
  }

  /** Toggles button from being clicked for spots that are already played.  */
  function toggleButtons() {
    $button.toggleClass("button");
  }

  /** Sends a play to server */
  async function playToServer(human_move) {
    let response = $.post('/move', {human_move});
    return response;
  }

  function playRandom() {
    let availPositions = game.getAvailable();
    let randomIdx = Math.floor(Math.random() * availPositions.length);
    return availPositions[randomIdx];
  }

  function endGame(player) {
    if (player === ROBOT) {
      alert("Pwned");
    } else if (player === HUMAN) {
      alert("You win!");
    } else {
      alert("Tied!");
    }
    window.location.reload();
  }

  function checkForWinner() {
    if (game.checkForWin(ROBOT)) {
      endGame(ROBOT);
    } else if (game.checkForWin(HUMAN)) {
      endGame(HUMAN);
    } else  if (game.isTied()){
      endGame("tied");
    } else {
      toggleButtons();
    }
  }

  /** Function that forces a sleep in */
  async function sleep(fn, ...args) {
    function timeout(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
    await timeout(450);
    return fn(...args);
  }
  
});