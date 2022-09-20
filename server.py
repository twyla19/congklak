import datetime
import os
from flask import Flask, jsonify
from flask import send_from_directory
from dakon.utility import split_string
from dakon.game import Game
# from dakon.agents.random import AgentRandom
# from dakon.agents.max import AgentMax
from dakon.agents.mcts import AgentMonteCarlo
from dakon.agents.easy import AgentEasy
from dakon.agents.medium import AgentMedium
from dakon.agents.hard import AgentHard 



FLASKAPP = Flask(__name__)
FLASKAPP.config.from_object(__name__)

# Define agents
# AGENT_RANDOM = AgentRandom(454)
# AGENT_MAX = AgentMax(454)
AGENT_EASY = AgentEasy(454)
AGENT_MEDIUM = AgentMedium(454)
AGENT_HARD = AgentHard(454, 3)
AGENT_MCTS = AgentMonteCarlo(454, 3)



def board_str_to_game(board, player_turn):
    """Turns parameters into game or error tuple"""
    board_arr = split_string(board, 2)

    if len(board_arr) != 16:
        return jsonify({"error": "Invalid Board"}), 400

    if player_turn != 1 and player_turn != 2:
        return jsonify({"error": "Invalid Player"}), 400

    game = Game(board_arr, player_turn)
    return game


def agent_play(game, agent_str):
    """Play a game, based on agent string. Or no move."""
    # if agent_str == "random":
    #     game.move(AGENT_RANDOM.move(game))
    # elif agent_str == 'max':
    #     game.move(AGENT_MAX.move(game))
    if agent_str == 'easy':
        game.move(AGENT_EASY.move(game))
    elif agent_str == 'medium':
        game.move(AGENT_MEDIUM.move(game))
    elif agent_str == 'hard':
        game.move(AGENT_HARD.move(game))

    # elif agent_str == 'montecarlo':
    #     game.move(AGENT_MCTS.move(game))
    return game


@FLASKAPP.route('/time')
def time():
    """Returns current time"""
    return jsonify({'current_time': datetime.datetime.utcnow().isoformat()})


@FLASKAPP.route('/agents')
def agents():
    """Returns available agent strings"""
    agents = [ 'easy', 'medium', 'hard']
    return jsonify({'agents': agents})



@FLASKAPP.route('/play/<string:board>/<int:player_turn>/<int:move>')
def play_board(board, player_turn, move):
    """Make a move based on a player and a board"""

    if move < 0 or move > 15:
        return jsonify({"error": "Invalid move"}), 400

    game = board_str_to_game(board, player_turn)
    if not isinstance(game, Game):
        return game

    game.move(move)
    print("Human Choose= " +str(move))
    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'game_over': game.over(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })


@FLASKAPP.route('/agent/<string:board>/<int:player_turn>/<string:agent>/')
def play_agent(board, player_turn, agent):
    """Make a move based on a player and a board"""

    game = board_str_to_game(board, player_turn)
    if not isinstance(game, Game):
        return game

    # game.move(move)
    game = agent_play(game, agent)

    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'game_over': game.over(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })


@FLASKAPP.route('/')
def serve_index():
    """Serve index"""
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, 'index.html')


@FLASKAPP.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, filename)


FLASKAPP.run()