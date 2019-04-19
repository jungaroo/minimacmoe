$(function() {
  const $board = $("#board");
  const $button = $(".btn");
  const $fight = $("#fight");
  const $game = $("#game");

  const [HUMAN, ROBOT] = ['X', 'O'];

  let game = new TicTacToe(HUMAN, ROBOT);
  
  $fight.on("click", function() {
    $game.slideToggle();
  })
  $board.on("click", ".square", async function() {
    let idx = $(this).index();
 
    if (!game.hasNotPlayed(idx)) return; // Already played
  
    // Process that human played
    game.markPlayed(idx, HUMAN);
    updateUIPlay(idx, HUMAN);
    toggleButtons();
    
    // Get robot's play
    let {robot_move} = await playToServer(idx);
    game.markPlayed(robot_move, ROBOT);
    setTimeout(() => {
      updateUIPlay(robot_move, ROBOT);
    }, 100);

    // Check for wins
    if (game.checkForWin(ROBOT)) {
      setTimeout( ()=> alert("Pwned") , 300);
    } else {
      toggleButtons();
    }

  });

  function updateUIPlay(idx, player) {
    $board.children(`:nth-child(${idx+1})`).text(player); ;
  }

  function toggleButtons() {
    $button.toggleClass("button");
  }

  async function playToServer(player_move) {
    let response = $.post('/move', {player_move});
    return response;
  }
  
});