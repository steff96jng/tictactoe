import game
import random
import argparse
import sys


def run_game():
    board = game.Board()

    while not board.is_game_over():
        turn_state = False
        while not turn_state: # brute force for now
            x = random.randrange(3)
            y = random.randrange(3)
            player = board.active_player()
            turn_state = board.make_turn(player, x,y)

    # board.printBoard()
    # print(board.state())
    # print(board.getBoard())
    return board.state()


def train():
    pass


def play():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', help='Trains the ai', action="store_true")
    parser.add_argument('-p', '--play', help='Play against the ai', action="store_true")
    parser.add_argument('-e', '--greediness', help='Greediness', default='.7')

    args = parser.parse_args()

    if args.train and args.play:
        print("You cannot do both at the same time")
        sys.exit(1)

    if args.play:
        play()

    if args.train:
        train()


    result = { game.State.DRAW : 0, game.State.WIN_O: 0, game.State.WIN_X: 0 }
    for i in range(10):
        result[run_game()] += 1

    print(result)



