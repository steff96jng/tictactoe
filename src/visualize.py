import matplotlib.pyplot as plt
import jsonpickle
from math import sqrt
from stats_proc import EpochData, StatsProcessor

filename = "G:\\stats_current_jhvslxxhwkclmxryjpey.json"

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
    
def root_mean_square_median(list: list) -> float:
    m = 0

    for n in list:
        m += n ** 2

    return sqrt(m / len(list))


def plot_wins(data):
    x_player_win = []
    o_player_win = []
    players_draw = []
    rms_x_win = []
    rms_o_win = []
    rms_draw = []
    epoch_data = data.epoch_data

    for ed in epoch_data:
        x_player_win.append(ed.data["x"])
        o_player_win.append(ed.data["o"])
        players_draw.append(ed.data["draw"])
        rms_x_win.append(root_mean_square_median(x_player_win))
        rms_o_win.append(root_mean_square_median(o_player_win))
        rms_draw.append(root_mean_square_median(players_draw))
        

    #plt.plot(x_player_win, label='x_player_win')
    #plt.plot(o_player_win, label='o_player_win')
    #plt.plot(players_draw, label='players_draw')
    plt.plot(rms_x_win, label = 'rms_x_win')
    plt.plot(rms_o_win, label = 'rms_o_win')
    plt.plot(rms_draw, label = 'rms_draw')

    plt.ylabel('Gewinnverteilung')
    plt.legend()
    plt.show()

content = read_json_file(filename)
data = jsonpickle.decode(content)

plot_wins(data)




