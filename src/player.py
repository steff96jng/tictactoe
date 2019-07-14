import random

import tensorflow as tf
import jsonpickle
import stats_proc
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.models import Sequential, load_model, print_function
from tensorflow.python.keras import optimizers
from tensorflow.keras.models import load_model

import numpy as np

from tictactoe import TicTacToe, LENGTH


class BasePlayer:
    def set_symbol(self, symbol: int):
        self.symbol = symbol

    def make_move(self, ttt: TicTacToe):
        pass

    def train(self, ttt: TicTacToe):
        pass

    def update_history(self, ttt: TicTacToe):
        pass

    def reset_history(self):
        pass


class HumanPlayer(BasePlayer):
    def __init__(self):
        pass

    def make_move(self, ttt: TicTacToe):
        while True:
            coord = input("Enter coordinates x,y: ")
            x, y = coord.split(",")
            x = int(x)
            y = int(y)
            if ttt.make_move(x, y, self.symbol):
                return


class RandomPlayer(BasePlayer):
    def __init__(self):
        pass

    def make_move(self, ttt: TicTacToe):
        while True:
            coord = np.random.randint(3, size=2)
            x = coord[0]
            y = coord[1]

            if ttt.make_move(x, y, self.symbol):
                return


class AgentPlayer(BasePlayer):
    model_stats = None

    def __init__(self, epsilon=0.7, name="player"):
        """
        parameters:

        epsilon: greediness, probability of taking a random action instead of a greedy action

        name: name of the player, used for generating stats
        """
        self.history = []
        self.epsilon = epsilon
        self.model = self.__build_model()
        self.name = name
        self.model_stats = stats_proc.StatsProcessor("model_" + name + "_")

    def update_history(self, ttt: TicTacToe):
        reward = 0
        if ttt.game_over() and ttt.is_draw():
            reward = 0
        elif ttt.game_over() and ttt.winner == self.symbol:
            reward = 1
        else:
            reward = -1

        self.history.append((ttt.get_state(), reward))

    def make_move(self, ttt: TicTacToe):
        # explore - make a random move
        if np.random.rand() < self.epsilon:
            while True:
                coord = np.random.randint(3, size=2)
                x = coord[0]
                y = coord[1]

                if ttt.make_move(x, y, self.symbol) or ttt.game_over():
                    return

        # let the network predict the next move
        state = ttt.get_state()
        one_hot = self.one_hot_encoded(state, ttt)
        values = self.model.predict(np.asarray([one_hot]))[0]

        high = -1000  # value of field
        field = -1  # index of field

        for i in range(len(state)):  # select best move
            if state[i] == 0:
                if values[i] > high:
                    high = values[i].copy()
                    field = i

        x = field % 3
        y = field // 3
        if ttt.make_move(x, y, self.symbol):
            return
        else:
            raise Exception("dafuq?")

    def train(self, ttt: TicTacToe):
        states = []
        q_values = []

        for game_state in self.history:
            state, result = game_state
            states.append(self.one_hot_encoded(state, ttt))
            q_values.append(result)

        self.model.fit(
            np.asarray(states), np.asarray(q_values), epochs=5, batch_size=len(states)
        )

    def one_hot_encoded(self, state, ttt: TicTacToe):
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
                raise Exception("How?")

        if self.symbol == ttt.x:
            one_hot_state.append(1)
        elif self.symbol == ttt.o:
            one_hot_state.append(0)
        else:
            raise Exception("How?")

        return one_hot_state

    def reset_history(self):
        self.history = []

    def __build_model(self):
        model = Sequential()
        # fmt: off
        model.add(Dense(units=128, activation="relu", input_dim=19))  # input layer
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=140, activation="relu"))
        model.add(Dense(units=60, activation='relu'))
        model.add(Dense(units=9))  # output layer: Use 9 units, because we have 9 game-fields
        model.compile(optimizer='adam', loss="mean_squared_error", metrics=["accuracy"])
        # fmt: on
        return model

    def stop_training(self):
        self.epsilon = 0

    def save_model(self, file: str):
        self.model.save(file)

    def load_model(self, file: str):
        try:
            self.model = tf.keras.models.load_model(file)
        except Exception as e:
            print("Failed to load model from file", e)
            raise

