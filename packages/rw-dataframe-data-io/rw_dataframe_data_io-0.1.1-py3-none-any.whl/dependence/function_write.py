import pickle
import pandas as pd


def write_pickle(file_path, data):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def write_csv(file_path, data, sep=',', column_names=None):
    data.to_csv(file_path, index=False, sep=sep, header=column_names is not None, columns=column_names)


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        pd.json.dump(data.to_dict(), file)


def test_write():
    print("je sais ecrire")