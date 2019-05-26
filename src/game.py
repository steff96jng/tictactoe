from enum import Enum, auto

class Color(Enum):
    EMPTY = '-'
    X = 'x'
    O = 'o'

class State(Enum):
    TURN_X = auto()
    TURN_O = auto()
    WIN_X = auto()
    WIN_O = auto()
    DRAW = auto()

class Board:

    def __init__(self):
        self.__turns = 0
        self.__activePlayer = Color.X
        self.__lastAcvitePlayer = Color.EMPTY
        self.__state = State.TURN_X
        self.__board =  [['-','-','-']  # 0
                        ,['-','-','-']  # 1
                        ,['-','-','-']] # 2


    def active_player(self):
        return self.__activePlayer


    def state(self):
        return self.__state


    def is_game_over(self):
        return (self.__state == State.WIN_X
                    or self.__state == State.WIN_O
                    or self.__state == State.DRAW)


    def make_move(self, color: Color, n: int):
        y = int(n / 3)
        x = n % 3
        self.make_turn(color, x, y)


    def make_turn(self, color: Color, x: int, y: int):
        """
        Let the player make a turn
        """
        if (color != self.__activePlayer
            or y < 0 or y >= len(self.__board)
            or x < 0 or x >= len(self.__board[y])
            or self.__board[y][x] != Color.EMPTY.value):
            return False

        self.__board[y][x] = color.value
        self.__turns += 1

        self.__lastAcvitePlayer = self.__activePlayer

        if self.__activePlayer == Color.X:
            self.__activePlayer = Color.O
        else:
            self.__activePlayer = Color.X
        
        self.__update_state()
        return True


    def print_board(self):
        """
        Print the game board
        """
        for row in range(len(self.__board)):
            print(*self.__board[row])            


    def get_board(self):
        """
        Returns a copy of the game board as a 1x9 vector
        0 => Empty field
        1 => Occupied by x
        2 => Occupied by o
        """
        tmpBoard = []
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                v = 0
                if self.__board[row][col] == Color.X.value:
                    v = 1
                elif self.__board[row][col] == Color.O.value:
                    v = 2

                tmpBoard.append(v)

        return tmpBoard


    def __update_state(self):
        tmpState = State.DRAW

        # update current player
        if self.__activePlayer == Color.X:
            tmpState = State.TURN_O
        else:
            tmpState = State.TURN_X

        # check if anyone has won/draw
        # which can only be the case, after at least 3 turns
        if self.__turns < 3:
            self.__state = tmpState
            return

        if self.__check_rows() or self.__check_columns() or self.__check_diagonal():
            # the last active playerr was the one, who made the winning move
            if self.__lastAcvitePlayer == Color.X:
                tmpState = State.WIN_X
            else:
                tmpState = State.WIN_O
        elif self.__turns >= 9: # 9 truns, no win => draw
            tmpState = State.DRAW

        self.__state = tmpState


    def __check_rows(self):
        return ((self.__board[0][0] == self.__board[0][1] and self.__board[0][1] == self.__board[0][2] and self.__board[0][1] != Color.EMPTY.value)
            or (self.__board[1][0] == self.__board[1][1] and self.__board[1][1] == self.__board[1][2] and self.__board[1][1] != Color.EMPTY.value)
            or (self.__board[2][0] == self.__board[2][1] and self.__board[2][1] == self.__board[2][2] and self.__board[2][1] != Color.EMPTY.value))


    def __check_columns(self):
        return ((self.__board[0][0] == self.__board[1][0] and self.__board[1][0] == self.__board[2][0] and self.__board[1][0] != Color.EMPTY.value)
            or (self.__board[0][1] == self.__board[1][1] and self.__board[1][1] == self.__board[2][1] and self.__board[1][1] != Color.EMPTY.value)
            or (self.__board[0][2] == self.__board[1][2] and self.__board[1][2] == self.__board[2][2] and self.__board[1][2] != Color.EMPTY.value))


    def __check_diagonal(self):
        return (self.__board[1][1] != Color.EMPTY.value and
            (self.__board[0][0] == self.__board[1][1] and self.__board[1][1] == self.__board[2][2]
            or self.__board[0][2] == self.__board[1][1] and self.__board[1][1] == self.__board[2][0]))
