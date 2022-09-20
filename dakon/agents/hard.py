"""
Hard Difficulty Agent for the a dakon AI using MCTS
"""

import random
import sys
from dakon.game import Game
from .agent import Agent


class AgentHard(Agent):
    """Agent which picks a move by the next score"""

    def __init__(self, seed=451, depth=6):
        # seed for random.seed()
        self._seed = seed
        # idx for keeping track of moves
        self._idx = 0
        # depth of the tree search
        self._depth = depth

    @staticmethod
    def _score_of_move(move_test, game):
        game.move(move_test)
        return game.score()[0]

    @staticmethod
    def _evaluate_board(game):
        return game.score()[0]
    
    
    # selection
    def _move(self, game):
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()

        move_options = Agent.valid_indices(game_clone)
        # print(move_options)

        # expansion
        available_scores = list(
            map(lambda move_slot:
                AgentHard._hard(
                    self._depth,
                    game_clone,
                    move_slot,
                    -sys.maxsize,
                    sys.maxsize
                ),
                move_options))

        
        score_max = max(available_scores)
        final_options = [move for score, move in
                         zip(available_scores, move_options)
                         if score == score_max]

        final_move = Game.rotate_board(rot_flag, random.choice(final_options))
        # print("AGENT CHOOSE "+str(final_move))
        return final_move

    # simulation
    @staticmethod
    def _hard(depth, game, move, alpha, beta):

        clone = game.clone()
        clone.move(move)

        maximizer = clone.turn_player() == 1

        if depth == 0:
            return AgentHard._evaluate_board(clone)

        move_options = Agent.valid_indices(clone)
        best_move = -sys.maxsize if maximizer else sys.maxsize
        # print("MOVE OPTIONS: "+str(move_options))

        for move_slot in move_options:
            current_value = AgentHard._hard(
                depth - 1,
                clone,
                move_slot,
                alpha,
                beta
            )

            if maximizer:
                best_move = max(current_value, best_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(current_value, best_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move
