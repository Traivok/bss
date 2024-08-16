import json
import csv
from datetime import datetime


# Function to convert JSON to CSV
def json_to_csv(json_file):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract relevant information
    result = data['chart']['result'][0]
    exchange_name = result['meta']['exchangeName']
    timestamps = result['timestamp']
    quotes = result['indicators']['quote'][0]
    adjclose = result['indicators']['adjclose'][0]['adjclose']

    # Open CSV file for writing
    csv_file = f'{exchange_name}.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write data rows
        for i in range(len(timestamps)):
            # Convert timestamp to date
            date = datetime.utcfromtimestamp(timestamps[i]).strftime('%Y-%m-%d')

            # Prepare data row
            row = {
                'Date': date,
                'Open': quotes['open'][i],
                'High': quotes['high'][i],
                'Low': quotes['low'][i],
                'Close': quotes['close'][i],
                'Adj Close': adjclose[i],
                'Volume': quotes['volume'][i]
            }

            # Write row to CSV
            writer.writerow(row)

    print(f"Data has been written to {csv_file}")


# Function to read from a CSV file
def read_csv(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)  # Print each row as a dictionary


# File paths
json_file = 'json/cmx.json'

# Convert JSON to CSV
json_to_csv(json_file)