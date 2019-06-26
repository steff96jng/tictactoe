import game
import random
import argparse
import sys

import tensorflow as tf
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras import optimizers
import numpy as np
import math

class TTTAgent():
    """
    Steps to do:
        1. build the model
        2. run the model
            2.1 get an action, or make a random one
            2.2 advance to next state
            2.3 remember previous state
            2.4 check end
        3. train the agent with data gained in the episode
            3.1  reward!?

    Resources:
        https://keon.io/deep-q-learning/
        https://en.wikipedia.org/wiki/Stochastic_gradient_descent
        https://github.com/AxiomaticUncertainty/Deep-Q-Learning-for-Tic-Tac-Toe/blob/master/tic_tac_toe.py
        https://www.youtube.com/watch?v=Qa2RxBXH4sU&t
    """

    def __init__(self, state_size : int, action_size : int):
        """
        state size is going to contain the current board & color the agent has, so it's ~10
        """
        self.__gamma = 0.95   # discount rate
        self.__epsilon = 0.7  # exploration rate, usually it's lower - e.g. .1-.3
        self.__action_size = action_size
        self.__state_size = state_size

        self.__model = self.__build_model(state_size, action_size)


    def __build_model(self, state_size, action_size):
        # create a deep q model
        model = Sequential()
        model.add(Dense(units=24, activation='relu', input_dim=state_size))
        model.add(Dense(units=72, activation='relu'))
        model.add(Dense(units=72, activation='relu'))
        model.add(Dense(units=action_size, activation='linear'))
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        # adam => https://en.wikipedia.org/wiki/Stochastic_gradient_descent

        return model

    def make_move(self, state):
        """
        what to do when the agent das an unallowed move?
        e.g. trying to place on an occupied field
        ==> punish the agent!
        """
        if np.random.rand() <= self.__epsilon:          # make our own move?
            return random.randrange(self.__state_size)  # make rnd move

        act_values = self.__model.predict(state)        # return the move the would ai make
        return np.argmax(act_values)

    def __one_hot(self, state):
        one_hot_state = []
        for field in state:
            if field == 0: # append state for empty field
                one_hot_state.append(1)
                one_hot_state.append(0)
                one_hot_state.append(0)
            elif field == 1: # append state for field player 1 (x)
                one_hot_state.append(0)
                one_hot_state.append(1)
                one_hot_state.append(0)
            else: # append state for field player 2 (x)
                one_hot_state.append(0)
                one_hot_state.append(0)
                one_hot_state.append(1)

        return one_hot_state

    def remember_state(self, state):
        pass

    def train(self, batch_size):
        pass