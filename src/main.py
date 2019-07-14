import random
import argparse
import sys
import tictactoe
import stats_proc
from player import HumanPlayer, RandomPlayer, AgentPlayer

if __name__ == "__main__":
    current_stats_proc = stats_proc.StatsProcessor("current_")
    overall_stats_proc = stats_proc.StatsProcessor("overall_")
    debug = False
    # environment setup
    ttt = tictactoe.TicTacToe()
    p1 = AgentPlayer(name="p1", epsilon=0.7)
    p2 = AgentPlayer(name="p2", epsilon=0.1)

    p1.set_symbol(ttt.x)
    p2.set_symbol(ttt.o)

    active_player = p1

    stat_history = []
    print("Start Training")
    episodes = 1000
    iteration = 0
    stat_id = 0

    try:
        while True:
            iteration += 1
            stats = {"x": 0, "o": 0, "draw": 0}
            for i in range(episodes):
                while not ttt.game_over():
                    if debug:
                        ttt.draw_board()

                    active_player.make_move(ttt)

                    if active_player == p1:
                        active_player = p2
                    else:
                        active_player = p1

                # append game state
                p1.update_history(ttt)
                p2.update_history(ttt)

                if debug:
                    ttt.draw_board()

                if (i % 200) == 0 or i == (episodes - 1):
                    print(i)

                if ttt.winner == None:
                    stats["draw"] = stats["draw"] + 1
                elif ttt.winner == ttt.x:
                    stats["x"] = stats["x"] + 1
                elif ttt.winner == ttt.o:
                    stats["o"] = stats["o"] + 1

                ttt.reset()
                active_player = p1

            # training
            p1.train(ttt)
            p1.reset_history()

            p2.train(ttt)
            p2.reset_history()

            # statistics
            stat_history.append(stats.copy())
            overall_stats = {"x": 0, "o": 0, "draw": 0}

            for stat in stat_history:
                overall_stats["x"] += stat["x"]
                overall_stats["o"] += stat["o"]
                overall_stats["draw"] += stat["draw"]

            overall_stats["x"] = overall_stats["x"] / (len(stat_history) * episodes)
            overall_stats["o"] = overall_stats["o"] / (len(stat_history) * episodes)
            overall_stats["draw"] = overall_stats["draw"] / (
                len(stat_history) * episodes
            )

            stats["x"] = stats["x"] / episodes
            stats["o"] = stats["o"] / episodes
            stats["draw"] = stats["draw"] / episodes

            current_stats_proc.append_epoch_data(stats)
            stat_id += 1
            print("overall", overall_stats)
            print("current", stats)
            print("finished iteration", iteration)

    except KeyboardInterrupt:
        print("Recognized [Ctrl + C]. Terminating.")
        current_stats_proc.export_json()
        p1.model_stats.export_json()
        p2.model_stats.export_json()

    except:
        print("Another error occured. Terminating.")
        current_stats_proc.export_json()
        p1.model_stats.export_json()
        p2.model_stats.export_json()

