import random
import argparse
import sys
import tictactoe
from player import HumanPlayer, RandomPlayer, AgentPlayer

if __name__ == "__main__":
    debug = False
    ttt = tictactoe.TicTacToe()
    p1 = AgentPlayer()  # change this player to the player you like
    p2 = AgentPlayer()

    p1.set_symbol(ttt.x)
    p2.set_symbol(ttt.o)

    active_player = p1

    stat_history = []
    print("Start Training")
    x = 1000
    y = 1000

    while True:
        stats = {
            "x": 0,
            "o": 0,
            "draw": 0,
            "x_illegal": 0,
            "y_illegal": 0,
            "tried_moves": 0,
        }
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
                stats["draw"] = stats["draw"] + 1
            elif ttt.winner == ttt.x:
                stats["x"] = stats["x"] + 1
            elif ttt.winner == ttt.o:
                stats["o"] = stats["o"] + 1

            stats["tried_moves"] += ttt.tried_moves
            ttt.reset()
            active_player = p1

        stats["x_illegal"] = p1.illegal_moves
        stats["y_illegal"] = p2.illegal_moves

        p1.train(ttt)
        p1.reset_history()

        p2.train(ttt)
        p2.reset_history()

        stat_history.append(stats.copy())
        overall_stats = {
            "x": 0,
            "o": 0,
            "draw": 0,
            "x_illegal": 0,
            "y_illegal": 0,
            "tried_moves": 0,
        }

        for stat in stat_history:
            overall_stats["x"] += stat["x"]
            overall_stats["o"] += stat["o"]
            overall_stats["draw"] += stat["draw"]
            overall_stats["x_illegal"] += stat["x_illegal"]
            overall_stats["y_illegal"] += stat["y_illegal"]
            overall_stats["tried_moves"] += stat["tried_moves"]

        overall_stats["x"] = overall_stats["x"] / (len(stat_history) * x)
        overall_stats["o"] = overall_stats["o"] / (len(stat_history) * x)
        overall_stats["draw"] = overall_stats["draw"] / (len(stat_history) * x)

        stats["x"] = stats["x"] / x
        stats["o"] = stats["o"] / x
        stats["draw"] = stats["draw"] / x
        stats["x_illegal_rel"] = stats["x_illegal"] / stats["tried_moves"]
        stats["y_illegal_rel"] = stats["y_illegal"] / stats["tried_moves"]

        print("overall", overall_stats)
        print("current", stats)

