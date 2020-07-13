from tqdm import tqdm

import pandas as pd
import os


def run():

    paths = []

    for root, dirs, files in os.walk('Data/games'):
        paths = [root + "/" + file for file in files]
    paths = sorted(paths)
    game_info = []

    for path in tqdm(paths):
        if 'lichess' in path:
            read_format = 'r'
        else:
            read_format = 'rb'

        with open(path, read_format) as file:
            lines = file.read()

            if isinstance(lines, bytes):
                lines = bytes(lines).decode('utf-8', errors='ignore')

            cols = ['White', 'Black', 'Result', 'gamePGN']

            lines = lines.split("\r\n\r\n")

            for i in range(0, len(lines) - 1, 2):
                current_game_info = []

                if '\r\n' in lines[i]:
                    game_specs = lines[i].split('\r\n')

                else:
                    game_specs = lines[i].split('\n')

                game_moves = lines[i + 1]

                for spec in game_specs:
                    spec = spec.replace('[', '').replace(']', '').replace('"', '').strip()
                    data = spec.split(' ', 1)

                    if data[0] in cols:
                        if len(data) == 2:
                            current_game_info.append(data[1])
                        else:
                            current_game_info.append('')

                current_game_info.append(game_moves)

                game_info.append(current_game_info)

    df = pd.DataFrame(game_info, columns=cols)
    df.to_pickle('Data/pickles/game_data')