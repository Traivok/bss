import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mfn.bootstrap import lbb
from mfn.entropy import MFN
import seaborn as sns
from scipy.stats import kurtosis, skew


def calculate_statistics(data):
    """
    Calculate and display the mean, median, standard deviation,
    kurtosis, and skewness for a given ndarray.

    Args:
    data (np.ndarray): The input array for which to calculate statistics.

    Returns:
    pd.DataFrame: A DataFrame containing the statistical measures.
    """
    # Calculate the statistics
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)
    curtose = kurtosis(data)
    assimetria = skew(data)

    # Create a DataFrame to display the results as a table
    df = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Standard Deviation', 'Kurtosis', 'Skewness'],
        'Value': [mean, median, std_dev, curtose, assimetria]
    })

    return df


class Plotter:
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def plot_series(self):
        lbb_samples = lbb(
            self.data,
            b=10,
            B=.1,
            size=100
        )
        lbb_df = pd.DataFrame(lbb_samples).reset_index()
        lbb_df = lbb_df.melt(id_vars='index', value_vars=lbb_df.columns[1:])

        # Plotting the mean of the LBB samples
        lbb_df.groupby("variable").agg("mean")["value"].plot(color="red")
        plt.plot(self.data)
        plt.title(f"LBB mean in red and original time series in blue for {self.name}")
        plt.show()

        # Plotting the mean of the LBB samples with confidence interval
        sns.lineplot(
            lbb_df,
            x='variable', y='value',
            err_style="band", errorbar=("ci", 95), estimator="mean",
        )
        plt.title(f"LBB mean with Confidence Interval of 95% for {self.name}")
        plt.show()

    def plot_mfn(self):
        value_dict = MFN(
            self.data,
            b=10,
            B=.1,
            size=100,
            dx=3
        )

        f, ax = plt.subplots(figsize=(6, 6))
        value_df = pd.DataFrame(value_dict).reset_index()
        value_df = value_df.melt(id_vars='index', value_vars=value_df.columns[1:])
        sns.barplot(value_df, x='variable', y='value', errorbar="sd")
        plt.title(f"MFN method results for {self.name}")
        f.tight_layout()

    def plot_table(self):
        # Set the theme for the plot
        sns.set_theme(style="whitegrid")

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 2))  # Set figure size as needed

        # Hide the axes
        ax.axis('off')
        ax.axis('tight')

        df = calculate_statistics(self.data)

        # Create the table
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

        # Adjust table appearance
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))

        # Display the table
        plt.show()
#%%

#%%