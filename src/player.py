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
    pass

  def update(self, ttt: TicTacToe):
    pass

  def update_history(self, ttt: TicTacToe):
    pass


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
  def __init__(self, epsilon = 0.7, alpha = 0.5, debug = False):
    """
    parameters:

    epsilon: greediness, probability of taking a random action instead of a greedy action

    alpha: learning rate
    """
    self.debug = debug
    self.history = []
    self.epsilon = epsilon
    self.alpha = alpha
    self.model = self.__build_model()

  def update_history(self, ttt: TicTacToe):
    result = 0
    if ttt.game_over() and ttt.is_draw():
      result = 0
    elif ttt.game_over() and ttt.winner == self.symbol:
      result = 1
    else:
      result = -1

    self.history.append((ttt.get_state(), result))

  def make_move(self, ttt: TicTacToe):
    def rnd_move():
      while True:
        coord = np.random.randint(3, size=2)
        x = coord[0]
        y = coord[1]

        if ttt.make_move(x,y, self.symbol) or ttt.game_over():
          return

    if np.random.rand() < self.epsilon:
      rnd_move()

    state = ttt.get_state()
    one_hot = self.one_hot_encoded(state, ttt)

    values = self.model.predict(np.asarray([one_hot]))
    max = np.argmax(values)
    x = max % 3
    y = max // 3
    if  ttt.make_move(x, y, self.symbol):
      return
    else:
      rnd_move()


  def train(self, ttt: TicTacToe):
    states = []
    q_values = []

    for game_state in self.history:
      state, result = game_state
      states.append(self.one_hot_encoded(state, ttt))
      q_values.append(result)

    self.model.fit(np.asarray(states), np.asarray(q_values), epochs=10, batch_size=len(states))


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
    model.add(Dense(units=128, activation='relu', input_dim=19)) # input layer
    model.add(Dense(units=64, activation='relu')) #
    model.add(Dense(units=64, activation='relu')) #
    model.add(Dense(units=32, activation='relu')) # output layer
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    return model