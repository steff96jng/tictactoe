
import random
import argparse
import sys
import tictactoe
from player import HumanPlayer, RandomPlayer, AgentPlayer

if __name__ == "__main__":
  debug = False
  ttt = tictactoe.TicTacToe()
  p1 = RandomPlayer() # change this player to the player you like
  p2 = AgentPlayer()

  p1.set_symbol(ttt.x)
  p2.set_symbol(ttt.o)

  active_player = p1

  stats = {'x': 0, 'o': 0, 'draw': 0}
  stat_history = []
  print("Start Training")
  x = 1000
  y = 10

  while True:
    for i in range(x):
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

      if (i % 200) == 0 or i == (x - 1):
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

    if y > 0:
      p2.train(ttt)
      y -= 1

    p2.reset_history()

    stat_history.append(stats)
    stats = {'x': 0, 'o': 0, 'draw': 0}
    overall_stats = { 'x': 0, 'o': 0, 'draw': 0}

    for stat in stat_history:
      overall_stats['x'] += stat['x']
      overall_stats['o'] += stat['o']
      overall_stats['draw'] += stat['draw']
      # print(stat)

    overall_stats['x'] = overall_stats['x'] / (len(stat_history) * x)
    overall_stats['o'] = overall_stats['o'] / (len(stat_history) * x)
    overall_stats['draw'] = overall_stats['draw'] / (len(stat_history) * x)
    print(overall_stats)