
import random
import argparse
import sys
import tictactoe
from player import HumanPlayer, RandomPlayer

if __name__ == "__main__":
  ttt = tictactoe.TicTacToe()
  p1 = HumanPlayer()
  p2 = RandomPlayer()

  p1.set_symbol(ttt.x)
  p2.set_symbol(ttt.o)

  active_player = p1

  while not ttt.game_over():
    ttt.draw_board()
    active_player.make_move(ttt)
    active_player.update(ttt)

    if active_player == p1:
      active_player = p2
    else:
      active_player = p1

# parser = argparse.ArgumentParser()
# parser.add_argument('-t', '--train', help='Trains the ai', action="store_true")
# parser.add_argument('-p', '--play', help='Play against the ai', action="store_true")
# parser.add_argument('-e', '--greediness', help='Greediness', default='.7')

# args = parser.parse_args()

# if args.train and args.play:
#     print("You cannot do both at the same time")
#     sys.exit(1)

# if args.play:
#     for i in range(100):
#         play()

# if args.train:
#     train()


# result = { game.State.DRAW : 0, game.State.WIN_O: 0, game.State.WIN_X: 0 }
# for i in range(100):
#     result[run_game()] += 1

# print(result)



