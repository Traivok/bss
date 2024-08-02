import pandas as pd
from numpy import ndarray


class CryptoCsvReader:
    def __init__(self, path):
        self.path = path
        self.column_name = 'Close'

    def read(self) -> ndarray:
        df = pd.read_csv(self.path, sep=',')
        df_filtered = df[[self.column_name]]
        return df_filtered[self.column_name].to_numpy()
