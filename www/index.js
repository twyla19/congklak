//board start
var board_current = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0];

//player one start
var player_turn = 1;

//reset default state
const reset_state = () => {
  board_current = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0];
  player_turn = 1;
}

//player var
const players = ['one', 'two'];

//default player agents
var player_states = ['Human', 'Human'];


const human_turn = () => player_states[player_turn - 1] == 'Human';

const update_progress = (player, agent, status, ms = 1000) => {
  return new Promise((resolve, reject) => {
    $(`#progress-${player == 1 ? 'one' : 'two'}-${agent}`).velocity({
      width: `${status}%`
    }, {
        duration: ms,
        complete: () => {
          resolve();
        }
      });
    });
  };
  
  //play speed
  const speed_slider = document.getElementById("agent_speed");
  const count_down_progress = (player, agent) => {
    return update_progress(player, agent, 100)
    .then(x => update_progress(player, agent, 0))
  }
  



  //player form input
const generate_inputs = (player, types) => {
  return R.pipe(
    R.map(type =>
      `
        <div>
          <div class="space-y-4">
            <div class="flex items-center">
              <input id="option-${player}-${type}" name="option-${player}" type="radio" class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300" value="${type}" ${type == "Human" ? "checked" : ""} >
              <label class="ml-3 block text-sm font-medium"> ${type} </label>
            </div>     
          </div>
          <div>
            <div id="progress-${player}-${type}" class="progress-bar class="m-4""></div>
          </div>
        </div>
      `
    ),
    R.values,
    R.join('\n'),
    html => `${html}`
  )(types);
};



var latest_url = '';
const fetch = (url) => {
  latest_url = url;
  return new Promise((resolve, reject) => {
    $.ajax({
      url,
      error: reject,
      success: (data) => {
        if (url != latest_url) {
          reject(false);
        } else {
          resolve(data);
        }
      }
    });
  });
};

const update_state_on_response = (e) => {
  if (!e) {
    return;
  }
  board_current = e.board;
  player_turn = e.player_turn;
  render_player(e);
  render_board(board_current);
  return !e.game_over;
};

const get_move = (url) => {
  return fetch(url)
    .catch(e => {
      if (e === false) {
        console.log('Caught failure');
        return false;
      }
      console.error(e);
      $('#server-message').html(e.responseJSON.error);
      return false;
    })
}

const cell_click = move => {
  if (!human_turn()) {
    console.log('Ignoring click');
    return;
  }
  // Send request
  return get_move(`/play/${board_to_str(board_current)}/${player_turn}/${move}`)
    .then(update_state_on_response)
    .then(kick_again);
};



//text color middle
const player_color = is_player_one => is_player_one ? 'rgba(37, 99, 235, 1)' : 'rgba(220, 38, 38, 1)';
const player_color_hex = is_player_one => is_player_one ? '#2563eb' : '#dc2626';


const player_one_score = $('#player_one_score');
const player_two_score = $('#player_two_score');
const auto_restart = $('#auto-restart');
const render_player = (game_state) => {
  const turn_elm = $('#player_turn');
  if (game_state.game_over) {
    const player_one_win = game_state.score[0] > game_state.score[1];
    const player_elm = player_one_win ? player_one_score : player_two_score;
    player_elm.html(+player_elm.html() + 1);
    turn_elm.html(`Pemain ${player_one_win ? 'Satu' : 'Dua'} Menang!`);
    turn_elm.css('color', player_color(player_one_win));

    if (game_state.score[0] == game_state.score[1]) {
      turn_elm.html('Permainan Seri!');
      turn_elm.css('color', '#009900');
    }

    const player_scoreboard = player_one_win ? player_one_score : player_two_score;
    pulse_score(player_scoreboard, player_color_hex(player_one_win))
      .then(x => pulse_score(player_scoreboard))

    if (auto_restart.prop('checked')) {
      restart_game();
      console.log('Auto restarting...');
    }
  } else {
    turn_elm.html(`${game_state.player_turn == 1 ? '⇐ ' : '⇒ '}Giliran Pemain ${game_state.player_turn == 1 ? 'Satu (1-7) ⇐' : 'Dua (9-15) ⇒'}`);
    turn_elm.css('color', player_color(game_state.player_turn == 1));
  }
}

// pulse scoreboard animation
const pulse_score = (elm, color = "#000000", fontSize = '200%', duration = 500) => {
  return new Promise((resolve, reject) => {
    elm.velocity({color}, {duration, easing: "easeInOutCubic", 
    complete: () => { resolve();}
    });
  });
};

// convert integer to string and if less than 10, add a zero
const i_to_str = i => i >= 10 ? `${i}` : `0${i}`;
const board_to_str = R.pipe(
  R.map(i_to_str),
  R.join('')
);
const over_cells = (cb) => {
  R.pipe(
    R.range(0),
    R.forEach(cb)
  )(16);
};


const render_cell = Number.prototype.toString.call(0);
const cell_from_id = i => $(`#cell-${i_to_str(i)}`);
const render_board = (board) => {
  over_cells(i => {
    const cell = $(`#cell-${i_to_str(i)}`);
    const cell_value = board[i];
    cell.html(cell_value);
  }
  );
}


// IF USING THE DOT
// const render_cell = R.pipe(
  //   R.repeat('⚫'),
  //   R.join('')
  // );
// const render_board = (board) => over_cells(i => cell_from_id(i).html(render_cell(board[i])));
  


const kick_again = (again) => {
  if (again) {
    kick_turn();
  }
}

const kick_turn = () => {
  // if human, do nothing (wait for click)
  if (human_turn()) {
    return;
  }
  // if not human, kick off the paired wait, of move request/slide down
  // console.log(`Computer's turn!`);
  Promise.all([
    get_move(`/agent/${board_to_str(board_current)}/${player_turn}/${player_states[player_turn - 1]}`),
   
    count_down_progress(player_turn, player_states[player_turn - 1]),
  ])
    .then(R.nth(0))
    .then(update_state_on_response)
    .then(kick_again);
}

// game restart
$(`#btn-restart-game`).on('touchstart click', evt => {
  console.log('Restart');
  evt.preventDefault();
  restart_game();
});
const restart_game = () => {
  reset_state();
  render_board(board_current);
  render_player({ game_over: false, player_turn });

  const player_one_type = $("input[name=option-one]:checked").val();
  const player_two_type = $("input[name=option-two]:checked").val();
  player_states = [player_one_type, player_two_type];
  kick_turn();
}



// fetch list of available agents
fetch("/agents")
  .then((agents_available) => {
    console.log(agents_available);
    // concatentate human player to the agent list
    const agents = R.concat(['Human'], agents_available.agents);

    // map list of agents to radio buttons
    R.map((player) => {
      $(`#player_${player}_choices`).html(generate_inputs(player, agents));
    }, players);

    over_cells(i => cell_from_id(i).on('touchstart click', evt => cell_click(i)));
    // render the board
    render_board(board_current);
    // render the player
    render_player({ game_over: false, player_turn });
  })
