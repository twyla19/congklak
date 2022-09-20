# -*- coding: utf-8 -*-

"""
Easy Difficulty Agent for the a dakon AI using random moves
"""

import random
from .agent import Agent


class AgentEasy(Agent):
    """Random Player Class for play dakon."""

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    def _move(self, game):
        """Return a random valid move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        options = Agent.valid_indices(game)
        if len(options) < 1:
            return 0

        return random.choice(options)
