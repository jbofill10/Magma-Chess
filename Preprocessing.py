from tqdm import tqdm
from db import PSQL

import numpy as np
import pandas as pd
import chess.pgn
import io
import pprint
import sys


def run(df):

    sql = PSQL()
    df.drop(['White', 'Black'], inplace=True, axis=1)

    df['Result'] = df['Result'].replace({'1-0': 1, '1/2-1/2': 0, '0-1': -1})

    # Tracks game result
    count = 0
    # Count of each position
    index = 0

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
        white_kcastle = False
        black_kcastle = False

        white_qcastle = False
        black_qcastle = False

        for move in game.mainline_moves():
            if move_counter == length - 1:
                board.reset()
                break

            try:
                if board.is_kingside_castling(move):
                    if board.turn:
                        white_kcastle = True
                    else:
                        black_kcastle = True

                if board.is_queenside_castling(move):
                    if board.turn:
                        white_qcastle = True
                    else:
                        black_qcastle = True

                board.push(move)

            except Exception as e:

                print(e)

                sys.exit(0)
            b = convert_to_int(board, white_kcastle, black_kcastle, white_qcastle, black_qcastle)

            sql.add_position(index, str(b.tolist()).replace("[", "{").replace("]", "}").replace(".0", ""), result)

            index += 1

            move_counter += 1
        count += 1


def convert_to_int(board, white_kcastle, black_kcastle, white_qcastle, black_qcastle):
    l = [None] * 64
    for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):  # Check if white
        l[sq] = board.piece_type_at(sq)
    for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):  # Check if black
        l[sq] = -board.piece_type_at(sq)
    board_map = [0 if v is None else v for v in l]

    matrix = np.zeros((2, 8, 8))

    counter = 0
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0][0])):
            matrix[0][i][j] = board_map[counter]

            counter += 1

    # Turn
    matrix[1][0][0] = 12 if board.turn else -12

    # Check for castling rights
    matrix[1][6][0] = 1 if white_kcastle else 0
    matrix[1][6][0] = 1 if black_kcastle else 0
    matrix[1][7][7] = 1 if white_qcastle else 0
    matrix[1][7][7] = 1 if black_qcastle else 0

    return matrix
