import pandas as pd
from numpy import ndarray
from mfn.entropy import MFN  # Make sure to import MFN correctly

class CryptoCsvReader:
    def __init__(self, path):
        self.path = path
        self.column_name = 'Close'

    def read(self) -> ndarray:
        # Load the data from the CSV file
        df = pd.read_csv(self.path, sep=',')

        # Convert 'Date' column to datetime format and set it as the index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # Filter the data to the specified date range
        start_date = pd.to_datetime('2020-04-10')
        end_date = pd.to_datetime('2024-07-25')
        df = df.loc[start_date:end_date]

        # Create a complete date range from the start to end dates
        date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='B')

        # Reindex the DataFrame to include all business days
        df = df.reindex(date_range)

        # Forward fill the missing data
        df.fillna(method='ffill', inplace=True)

        # Reset the index to have 'Date' as a column again
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Date'}, inplace=True)

        # Extract the specified column as a numpy array
        df_filtered = df[[self.column_name]]
        return df_filtered[self.column_name].to_numpy()


def process_csv_files(csv_files, output_file):
    results = []
    for f, name in csv_files:
        reader = CryptoCsvReader(f'data/{f}')
        time_series = reader.read()
        value_dict = MFN(
            time_series,
            b=10,
            B=.1,
            size=100,
            dx=3
        )
        pe = value_dict['permutation entropy']  # array of values
        fim = value_dict['fisher information']  # another array

        # Ensure pe and fim are of the same length
        if len(pe) != len(fim):
            raise ValueError("Permutation entropy and Fisher Information arrays have different lengths.")

        # Create a DataFrame to store results
        df_results = pd.DataFrame({
            'pe': pe,
            'fim': fim,
            'stock': name
        })

        results.append(df_results)

    # Concatenate all results into a single DataFrame
    final_df = pd.concat(results, ignore_index=True)

    # Save the final DataFrame to a CSV file
    final_df.to_csv(output_file, index=False)

csv_files = [
    ('BTC-USD.csv', 'BTC'),
    ('BNB-USD.csv', 'BNB'),
    ('ETH-USD.csv', 'ETH'),
    ('SOL-USD.csv', 'SOL'),
    ('XRP-USD.csv', 'XRP'),
    ('EURUSD=X.csv', 'EUR'),
    ('NYA.csv', 'NYA'),
    ('CMX.csv', 'Gold'),
    ('SNP.csv', 'S&P 500'),
]

process_csv_files(csv_files, 'combined_results.csv')

#%%
