import matplotlib.pyplot as plt
import jsonpickle
from stats_proc import EpochData, StatsProcessor

filename = "data_export/stats_current_iivduiphpxavylccjsgz.json"

def read_json_file(path) -> str:
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def median(list: list) -> float:
    m = 0

    for n in list:
        m += n
    
    return m / len(list)
    



def plot_wins(data):
    x_player_win = []
    o_player_win = []
    players_draw = []
    epoch_data = data.epoch_data

    for ed in epoch_data:
        x_player_win.append(ed.data["x"])
        o_player_win.append(ed.data["o"])
        players_draw.append(ed.data["draw"])

    plt.plot(x_player_win, label='x_player_win')
    plt.plot(o_player_win, label='o_player_win')
    plt.plot(players_draw, label='players_draw')
    plt.ylabel('Gewinnverteilung')
    plt.legend()
    plt.show()


def plot_invalid_moves(data):
    tried_moves = []
    illegal_x = []
    illegal_o = []
    illegal_x_o = []
    median_data = []
    epoch_data = data.epoch_data


    for ed in epoch_data:
        tried_moves.append(ed.data["tried_moves"])
        illegal_o.append(ed.data["x_illegal"])
        illegal_x.append(ed.data["y_illegal"])
        illegal_x_o.append(ed.data["x_illegal"] + ed.data["y_illegal"])
        median_data.append(median(illegal_o + illegal_x))
    

    plt.plot(tried_moves, label='tried_moves')
    plt.plot(illegal_o, label='illegal_o')
    plt.plot(illegal_x, label='illegal_x')
    plt.plot(illegal_x_o, label='illegal_x_o')
    plt.plot(median_data, label='median')
    plt.ylabel('Illegale Spielzüge')
    plt.plot()
    plt.legend()
    plt.show()


def plot_invalid_moves_relative(data): 
    epoch_data = data.epoch_data
    x_invalid_rel = []
    o_invalid_rel = []
    x_o_invalid_rel = []

    for ed in epoch_data:
        x_invalid_rel.append(ed.data["x_illegal_rel"])
        o_invalid_rel.append(ed.data["y_illegal_rel"])
        x_o_invalid_rel.append(ed.data["x_illegal_rel"] + ed.data["y_illegal_rel"])

    plt.plot(x_invalid_rel, label="x_invalid_%")
    plt.plot(o_invalid_rel, label="o_invalid_%")
    plt.plot(x_o_invalid_rel, label="x_o_invalid_%")
    plt.legend()
    plt.ylabel('Illegale Spielzüge in %')
    plt.show()
    

content = read_json_file(filename)
data = jsonpickle.decode(content)

plot_invalid_moves(data)




