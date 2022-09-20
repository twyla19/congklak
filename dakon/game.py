class Game():
    _default_board = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0]

    # CLASS CONSTRUCTOR
    def __init__(
                # object created
                 self,
                # The board state.
                 board=None,
                #  The player whose turn it is.
                 player_turn=None,
                #  The moves that have been made.
                 moves=None,
                #  The history of the game.
                 history=None
                 ):

        # board created, 2 player with 7 holes each

        self._board = Game._default_board[:] if board is None else board
        # papan yang muncul seharusnya seperti 08 09 10 11 12 13 14
        #                                    07                    15
        #                                      06 05 04 03 02 01 00
        # skor player 1 ada di index 07 dan skor player 2 ada di index 15
        self._player_one = True if player_turn is None else (player_turn == 1)
        self._moves = [] if moves is None else moves
        self._history = [] if history is None else history

    def board(self):
        # board render
        return self._board[:]

    def history(self):
        # board render array
        return self._history[:]

    def moves(self):
        # player moves array
        return self._moves[:]

    def turn_player(self):
        # player turn
        return 1 if self._player_one else 2

    def score(self):
        # return current score
        return Game.score_board(self._board)  


    def winner(self):
        if not self.over():
            return 0
        return 1 if self.score()[0] > self.score()[1] else 2
    @staticmethod
    def score_board(board):
        # score of board
        return (board[7], board[15])

    def side_empty(self):
        stones_left_01 = sum(self._board[0:7])
        stones_left_02 = sum(self._board[8:15])
        return stones_left_01 == 0 or stones_left_02 == 0

    def over(self):
        return self.side_empty()

    def board_render(self):
        # menampilkan papan beserta biji pada tiap lubang

        # lubang player 2
        result = '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2} {6: >2}\n'.format(
            self._board[8], self._board[9], self._board[10],
            self._board[11], self._board[12], self._board[13], self._board[14])
        # lubang skor player 1 dan 2
        result += ' {0: >2}                     {1: >2} \n'.format(
            self._board[7], self._board[15])
        # lubang player 1
        result += '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2} {6: >2}'.format(
            self._board[6], self._board[5], self._board[4], self._board[3],
            self._board[2], self._board[1], self._board[0])
        return result

    @staticmethod
    def idx_player_1(idx):
        # player 1 zone
        return idx >= 0 and idx <= 6

    @staticmethod
    def idx_player_2(idx):
        # player 2 zone
        return idx >= 8 and idx <= 14

    @staticmethod
    def own_zone(idx, player):
        if player:
            return Game.idx_player_1(idx)
        else:
            return Game.idx_player_2(idx)
 
    def clone(self):
        return Game(
            self.board(),
            self.turn_player(),
            self.moves(),
            self.history()
        )

    def clone_turn(self):
        if self.turn_player() == 1:
            return self.clone(), False
        else:
            rot_board = self.board()[8:16] + self.board()[0:8]
            return Game(rot_board, 1), True

    @staticmethod
    # rotate the board
    def rotate_board(rot_flag, move):
        if rot_flag:
            return move + 8
        else:
            return move

    # def verify_move(self, idx):
    #     if self._player_one and not Game.idx_player_1(idx):
    #         return self.score()
    #     if not self._player_one and not Game.idx_player_2(idx):
    #         return self.score()
    #     else:
    #         return self.move(idx)

    def move(self, idx):
        # idx = player move
        

        # Illegal move if empty hole
        if self._board[idx] == 0:
            return self.score()
        if idx == 7 or idx == 15:
            return self.score()

        if self.over():
            return self.score()

        # add move to history
        self._moves.append(idx)
        self._history.append(self._board[:])

        # count stones in hole
        count = self._board[idx]

        # makes hole empty
        self._board[idx] = 0
        # input pemain = looping index player move
        current_idx = idx


        # count = stones hold
        while count > 0:
            # move to next hole with modulo
            current_idx = (current_idx + 1) % len(self._board)
            # skipping opponent's score hole for player 1
            if self._player_one and current_idx == 15:
                continue
            # skipping opponent's score hole for player 2
            if (not self._player_one) and current_idx == 7:
                continue
            # add stone to current hole
            self._board[current_idx] += 1
            # decrement stone count
            count -= 1
            # print("Current Moves: "+str(current_idx))

        # return to current player if last stone is in own score hole
        if current_idx == 7 or current_idx == 15:
            return self.score

        stone_hold = self._board[current_idx]
        while stone_hold > 1:
            idx = current_idx
            self.move(idx)
            stone_hold = 0
        

        # if last stone is landed in own hole with no stone, pick all stones in opponent's score hole that parallels with current hole
        if(self._board[current_idx] == 1 and self._board[14 - current_idx] >= 1 and
           Game.own_zone(current_idx, self._player_one)):
            if((self._board[14 - current_idx] != sum(self._board[0:7]) and not self._player_one) or ((self._board[14 - current_idx] != sum(self._board[8:15]) and self._player_one))):
                extra_stones = self._board[14 - current_idx]
                self._board[14 - current_idx] = 0

                if self._player_one:
                    self._board[7] += extra_stones
                else:
                    self._board[15] += extra_stones

        if self.side_empty():
            self._board[7] += sum(self._board[0:7])
            self._board[15] += sum(self._board[8:15])
            self._board[0:7] = [0, 0, 0, 0, 0, 0, 0]
            self._board[8:15] = [0, 0, 0, 0, 0, 0, 0]
            return self.score()

        # 
        self._player_one = self._player_one if idx == current_idx else not self._player_one

        # back to current player
        return self.score()
