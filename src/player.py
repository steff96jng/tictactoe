import numpy as np
from tictactoe import TicTacToe


class BasePlayer:
  def set_symbol(self, symbol: int):
    self.symbol = symbol

  def make_move(self, ttt: TicTacToe):
    raise NotImplementedError

  def update(self, state):
    raise NotImplementedError

class HumanPlayer(BasePlayer):
  def __init__(self):
    pass

  def make_move(self, ttt: TicTacToe):
    while True:
      coord = input('Enter coordinates x,y: ')
      x,y = coord.split(',')
      x = int(x)
      y = int(y)
      if ttt.make_move(x, y, self.symbol):
        return

  def update(self, state):
    pass

class RandomPlayer(BasePlayer):
  def __init__(self):
    pass

  def make_move(self, ttt: TicTacToe):
    while True:
      coord = np.random.randint(3, size=2)
      x = coord[0]
      y = coord[1]

      if ttt.make_move(x,y, self.symbol):
        return
