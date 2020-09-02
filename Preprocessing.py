from tqdm import tqdm
from db import PSQL

import numpy as np
import pandas as pd
import chess.pgn
import io
import pprint
import sys
import threading


def run(df):

    df.drop(['White', 'Black'], inplace=True, axis=1)

    df['Result'] = df['Result'].replace({'1-0': 1, '1/2-1/2': 0, '0-1': -1})
    df = df[df['Result'].isin([1,0,-1])]

    split = len(df)//4

    df1 = df[0:split]
    df2 = df[split:(2*split)]
    df3 = df[2*split:(3*split)]
    df4 = df[3*split::]

    t1 = threading.Thread(target=parse_games, kwargs=dict(df=df1))
    t2 = threading.Thread(target=parse_games, kwargs=dict(df=df2))
    t3 = threading.Thread(target=parse_games, kwargs=dict(df=df3))
    t4 = threading.Thread(target=parse_games, kwargs=dict(df=df4))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    # parse_games(df)


def parse_games(df):
    sql = PSQL(list_size=len(df))
    # Tracks game result
    count = 0
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

            b = convert_to_int(board, white_kcastle, black_kcastle, white_qcastle, black_qcastle)

            sql.add_position(str(b.tolist()).replace("[", "{").replace("]", "}").replace(".0", ""), result)

            move_counter += 1
        count += 1


def convert_to_int(board, white_kcastle, black_kcastle, white_qcastle, black_qcastle):
    white_pos = [None] * 64
    black_pos = [None] * 64
    for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):  # Check if white
        white_pos[sq] = board.piece_type_at(sq)
    for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):  # Check if black
        black_pos[sq] = board.piece_type_at(sq)
    white_map = [0 if v is None else v for v in white_pos]
    black_map = [0 if v is None else v for v in black_pos]

    matrix = np.zeros((7, 8, 8))

    counter = 0
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0][0])):
            matrix[0][i][j] = white_map[counter]
            matrix[3][i][j] = black_map[counter]

            counter += 1

    # Turn
    if board.turn:
        matrix[6].fill(0)
    else:
        matrix[6].fill(1)

    # Check for castling rights
    if white_kcastle:
        matrix[1].fill(1)
    if white_qcastle:
        matrix[2].fill(1)
    if black_kcastle:
        matrix[4].fill(1)
    if black_qcastle:
        matrix[5].fill(1)

    return matrix
