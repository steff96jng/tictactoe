import matplotlib.pyplot as plt
import jsonpickle
import os.path
from sys import argv
from math import sqrt
from stats_proc import EpochData, StatsProcessor

if len(argv) < 3:
    print('Invalid argument count. The command should be executed as follows:')
    print('\npython visualize.py <Path to data-file> <Visualization> [Additional argument]')
    print('\nPossible visualizations:\n  - wins    | Visualizes the win-ratio')
    print('\nAdditional arguments:\n  - show    | Shows the diagram immidately')
    exit()

filename = argv[1]

if not os.path.exists(filename):
    print('[ERR] File', filename, 'does not exist. Terminating now.')
    exit()


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


def get_filename(path):
    file = os.path.basename(path)
    file, _ = os.path.splitext(file)
    return file


def plot_wins(data, datafile):
    x_player_win = []
    o_player_win = []
    players_draw = []
    rms_x_win = []
    rms_o_win = []
    rms_draw = []
    epoch_data = data.epoch_data

    for ed in epoch_data:
        x_player_win.append(ed.data["x"] * 100)
        o_player_win.append(ed.data["o"] * 100)
        players_draw.append(ed.data["draw"] * 100)
        rms_x_win.append(root_mean_square_median(x_player_win))
        rms_o_win.append(root_mean_square_median(o_player_win))
        rms_draw.append(root_mean_square_median(players_draw))

    plt.plot(x_player_win, label='X-Spieler')
    plt.plot(o_player_win, label='O-Spieler')
    plt.plot(players_draw, label='Unentschieden')
    plt.plot(rms_x_win, label="Quadr. Mittel X-Gewonnen")
    plt.plot(rms_o_win, label="Quadr. Mittel O-Gewonnen")
    plt.plot(rms_draw, label="Quadr. Mittel Unentschieden")

    plt.ylabel("Gewonnen in %")
    plt.xlabel("Epochen x 1000")
    plt.title("Gewinnverteilung")
    
    
    ax = plt.subplot(111)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([0.1, 0.3, box.width, box.height * .7])

    # Put a legend to the right of the current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.52, -0.3), fancybox=True, ncol=3)
    plt.savefig(get_filename(datafile))

    if "show" in argv and hasattr(plt, "show"):
        plt.show()


content = read_json_file(filename)
data = jsonpickle.decode(content)


if argv[2] == 'wins':
    plot_wins(data, filename)

