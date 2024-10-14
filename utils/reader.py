import pandas as pd
from numpy import ndarray

class CryptoCsvReader:
    def __init__(self, path):
        self.path = path
        self.column_name = 'value'

    def read(self) -> ndarray:
        # Load the data from the CSV file
        df = pd.read_csv(self.path, sep=',')

        # Convert 'Date' column to datetime format and set it as the index
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Filter the data to the specified date range
        start_date = pd.to_datetime('2014-06-09')
        end_date = pd.to_datetime('2024-06-05')
        df = df.loc[start_date:end_date]

        # Create a complete date range from the start to end dates
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        # Reindex the DataFrame to include all business days
        df = df.reindex(date_range)

        # Forward fill the missing data
        # df.fillna(method='ffill', inplace=True)
        df.ffill(inplace=True)
        # Reset the index to have 'Date' as a column again
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date'}, inplace=True)

        # Extract the specified column as a numpy array
        df_filtered = df[[self.column_name]]
        return df_filtered[self.column_name].to_numpy()


