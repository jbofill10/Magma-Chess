import parse_games
import os
import pandas as pd


def main():

    if not os.path.isfile('Data/pickles/game_data'):
        parse_games.run()
        games = pd.read_pickle('Data/pickles/game_data')

    else:
        games = pd.read_pickle('Data/pickles/game_data')

    print(games)


if __name__ == '__main__':
    main()