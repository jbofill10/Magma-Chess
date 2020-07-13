from tqdm import tqdm
from db import SQL

import numpy as np
import pandas as pd
import chess.pgn
import io
import pprint
import sys


def run(df):
    sql = SQL()
    pp = pprint.PrettyPrinter(indent=4)
    df.drop(['White', 'Black'], inplace=True, axis=1)

    df['Result'] = df['Result'].replace({'1-0': 1, '1/2-1/2': 0, '0-1': -1})

    # Tracks game result
    count = 0
    # Count of each position
    index = 0
    preprocessed_data = []
    board = chess.Board()
    for i in tqdm(df['gamePGN']):
        result = df['Result'].iloc[count]
        try:
            game = chess.pgn.read_game(io.StringIO(i))
        except Exception as e:
            print(e)
            print("Failed Here")
            continue

        length = len(list(game.mainline_moves()))
        move_counter = 0
        for move in game.mainline_moves():
            if move_counter == length - 1:
                board.reset()
                break

            try:
                board.push(move)

            except Exception as e:

                print(e)

                sys.exit(0)
            b = convert_to_int(board)
            sql.add_position(index, str(b), result)

            index += 1

            move_counter += 1
    count += 1

    preproc_df = pd.DataFrame(preprocessed_data, columns=['position', 'result'])

    pd.to_pickle(preproc_df, 'Data/pickles/preprocessed_data')


def convert_to_int(board):
    l = [None] * 64
    for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):  # Check if white
        l[sq] = board.piece_type_at(sq)
    for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):  # Check if black
        l[sq] = -board.piece_type_at(sq)
    board_map = [0 if v is None else v for v in l]

    matrix = np.zeros((8, 9))
    counter = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            matrix[i][j] = board_map[counter]

            counter += 1

    matrix[0][8] = 12 if board.turn else -12

    return matrix
