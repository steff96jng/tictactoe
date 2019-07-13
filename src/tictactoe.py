import numpy as np

LENGTH = 3


class TicTacToe:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x = 1
        self.o = -1
        self.empty = 0
        self.winner = None
        self.ended = False
        self.turns = 0

    def is_empty(self, x: int, y: int) -> bool:
        return self.board[y, x] == self.empty

    def get_state(self):
        state = []
        for y in range(LENGTH):
            for x in range(LENGTH):
                state.append(self.board[y, x])

        return state.copy()  # return board as 9x1 vector

    def game_over(self):
        if self.turns <= 5:  # we need at least 5 turns
            return False

        for y in range(LENGTH):  # check rows
            for player in (self.x, self.o):
                if self.board[y].sum() == (player * LENGTH):
                    self.winner = player
                    self.ended = True
                    return True

        for x in range(LENGTH):  # check columns
            for player in (self.x, self.o):
                if self.board[:, x].sum() == (player * LENGTH):
                    self.winner = player
                    self.ended = True
                    return True

        # check diagonals - top left to bottom right
        for player in (self.x, self.o):
            if self.board.trace() == (player * LENGTH):
                self.winner = player
                self.ended = True
                return True
            # check diagonals - top right to bottom left
            if np.fliplr(self.board).trace() == (player * LENGTH):
                self.winner = player
                self.ended = True
                return True

        if (
            self.turns >= 9
        ):  # check for draw, it's automatically a draw whenever we reach turn #9 and none of the conditions above apply
            self.winner = None
            self.ended = True
            return True

        return False

    def is_draw(self):
        return self.ended and self.winner == None

    def make_move(self, x: int, y: int, player: int):
        if x < 0 or x >= LENGTH or y < 0 or y >= LENGTH or not self.is_empty(x, y):
            return False

        self.board[y, x] = player
        self.turns += 1
        return True

    def reset(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.winner = None
        self.ended = False
        self.turns = 0

    def draw_board(self):
        for y in range(LENGTH):
            for x in range(LENGTH):
                print(" ", end="")
                if self.board[y, x] == self.x:
                    print("x", end="")
                elif self.board[y, x] == self.o:
                    print("o", end="")
                else:
                    print("-", end="")
            print("")
        print("")
        print("------")
        print("")

