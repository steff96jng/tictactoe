
import random
import argparse
import sys
import tictactoe
from player import HumanPlayer, RandomPlayer, AgentPlayer

if __name__ == "__main__":
  debug = False
  ttt = tictactoe.TicTacToe()
  p1 = HumanPlayer() # change this player to the player you like
  p2 = AgentPlayer()

  p1.set_symbol(ttt.x)
  p2.set_symbol(ttt.o)

  active_player = p1

  stats = {'x': 0, 'o': 0, 'draw': 0}
  stat_history = []
  print("Start Training")
  while True:
    for i in range(1):
      while not ttt.game_over():
        if debug:
          ttt.draw_board()

        active_player.make_move(ttt)

        if active_player == p1:
          active_player = p2
        else:
          active_player = p1

      p1.update_history(ttt)
      p2.update_history(ttt)

      if debug:
        ttt.draw_board()

      if (i % 200) == 0:
        print("Round", i, "finished")

      if ttt.winner == None:
        stats['draw'] = stats['draw'] + 1
      elif ttt.winner == ttt.x:
        stats['x'] = stats['x'] + 1
      elif ttt.winner == ttt.o:
        stats['o'] = stats['o'] + 1

      ttt.reset()
      active_player = p1

    # p1.train(ttt)
    # p1.reset_history()

    p2.train(ttt)
    p2.reset_history()

    stat_history.append(stats)
    stats = {'x': 0, 'o': 0, 'draw': 0}

    for stat in stat_history:
      print(stat)
