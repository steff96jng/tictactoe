import random

import tensorflow as tf
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras import optimizers
from tensorflow.keras.models import load_model
import numpy as np

from tictactoe import TicTacToe, LENGTH


class BasePlayer:
  def set_symbol(self, symbol: int):
    self.symbol = symbol

  def make_move(self, ttt: TicTacToe):
    raise NotImplementedError

  def update(self, ttt: TicTacToe):
    raise NotImplementedError

  def update_history(self, ttt: TicTacToe):
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

  def update(self, ttt: TicTacToe):
    pass

  def update_history(self, ttt: TicTacToe):
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

  def update(self, ttt: TicTacToe):
    pass

  def update_history(self, ttt: TicTacToe):
    pass


class AgentPlayer(BasePlayer):
  def __init__(self, epsilon = 0.5, alpha = 0.5):
    """
    parameters:

    epsilon: greediness, probability of taking a random action instead of a greedy action

    alpha: learning rate
    """
    self.history = []
    self.epsilon = epsilon
    self.alpha = alpha
    self.model = self.__build_model()

  def update_history(self, ttt: TicTacToe):
    self.history.append(ttt.get_state())

  def make_move(self, ttt: TicTacToe):
    if np.random.rand() < self.epsilon:
      return random.randrange(LENGTH * LENGTH)

    state = ttt.get_state()
    one_hot = self.one_hot_encoded(state, ttt)
    values = self.model.predict(one_hot)
    return np.argmax(values)

  def update(self, ttt: TicTacToe):
    pass # todo - training here

  def one_hot_encoded(self, state: [int], ttt: TicTacToe):
    """
    one_hot_encoded returns the game state as one hot encoded
    """
    one_hot_state = []

    for field in state:
      if field == ttt.x:
        one_hot_state.append(1)
        one_hot_state.append(0)
      elif field == ttt.o:
        one_hot_state.append(0)
        one_hot_state.append(1)
      elif field == ttt.empty:
        one_hot_state.append(0)
        one_hot_state.append(0)
      else:
        raise Exception('How?')

    if self.symbol == ttt.x:
      one_hot_state.append(1)
    elif self.symbol == ttt.o:
      one_hot_state.append(0)
    else:
      raise Exception('How?')

    return one_hot_state

  def reset_history(self):
    self.history = []

  def __build_model(self):
    model = Sequential()
    model.add(Dense(units=9, activation='relu', input_dim=19)) # input layer
    model.add(Dense(units=9, activation='relu')) #
    model.add(Dense(units=9, activation='sigmoid')) #
    model.add(Dense(uints=9, activation='linear')) # output layer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model