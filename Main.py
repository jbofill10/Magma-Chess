import parse_games, Preprocessing
import os
import pandas as pd
from db import PSQL
from cnn import CovNet

def main():

    # if not os.path.isfile('Data/pickles/game_data'):
    #     parse_games.run()
    #     games = pd.read_pickle('Data/pickles/game_data')
    #
    # else:
    #     games = pd.read_pickle('Data/pickles/game_data')
    #
    # # print(games)
    # games = games[games.Result != '*']
    #
    # Preprocessing.run(games)

    model = CovNet()

    model.train()

if __name__ == '__main__':
    main()